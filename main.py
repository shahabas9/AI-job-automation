import asyncio
import json
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import  Runner,OpenAIChatCompletionsModel
from agent.job_search import create_job_search_agent
from agent.profile_extractor import create_profile_agent
from utils.file_processing import extract_text_from_file
from services.job_fetcher import fetch_jobs_all_sources
import json
import uuid
from pipeline.match_pipeline import match_jobs
from pipeline.rank_pipeline import rank_jobs
from services.job_fetcher import fetch_jobs_all_sources
from services.embedding_service import EmbeddingService
from services.qdrant_service import QdrantService
from utils.text_builders import profile_to_text, job_to_text
from agent.job_explanation import run_explanation_agent
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from agent.resume_tailoring import generate_tailored_resume
from agent.cover_letter import generate_cover_letter

load_dotenv(override=True)

app = FastAPI(title="AI Job Hunter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ============================
# GLOBAL SERVICES (INIT ONCE)
# ============================
ollama_client = AsyncOpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    api_key=os.getenv("OLLAMA_API_KEY")
)

CHAT_MODEL = os.getenv("MODEL_NAME")
EMBED_MODEL = os.getenv("EMBED_MODEL_NAME")

chat_model = OpenAIChatCompletionsModel(
    model=CHAT_MODEL,
    openai_client=ollama_client
)

embedder = EmbeddingService(
    client=ollama_client,
    model=EMBED_MODEL
)

qdrant_jobs = QdrantService("jobs", vector_size=768)

# ============================
# REQUEST / RESPONSE MODELS
# ============================
class JobResponse(BaseModel):
    final_score: float
    semantic_score: float
    job: dict
    explanation: str | None = None


class JobsAllResponse(BaseModel):
    page: int
    size: int
    total: int
    jobs: List[JobResponse]


class ApplicationPackage(BaseModel):
    resume_text: str
    cover_letter_text: str


class PrepareApplicationRequest(BaseModel):
    profile: dict
    job: dict


# ============================
# 1️⃣ PROFILE EXTRACTION
# ============================
@app.post("/profile/extract")
async def extract_profile(file: UploadFile = File(...)):
    # Read file bytes
    content = await file.read()
    
    # Extract text using utility (handles PDF, DOCX, TXT)
    resume_text = extract_text_from_file(content, file.filename)

    agent = create_profile_agent(chat_model)

    result = await Runner.run(agent, resume_text)
    profile = result.final_output

    if isinstance(profile, str):
        profile = json.loads(profile)

    return profile


# ============================
# 2️⃣ JOB SEARCH
# ============================
@app.post("/jobs/search")
async def search_jobs(profile: dict):
    agent = create_job_search_agent(chat_model)

    result = await Runner.run(
        agent,
        json.dumps(profile)
    )

    search_plan = result.final_output
    if isinstance(search_plan, str):
        search_plan = json.loads(search_plan)

    all_jobs = []
    for item in search_plan["search_queries"]:
        jobs = fetch_jobs_all_sources(
            query=item["query"],
            location=item["location"]
        )
        all_jobs.extend(jobs)

    return {
        "count": len(all_jobs),
        "jobs": all_jobs
    }


# ============================
# 2.5️⃣ AUTO FIND MATCH
# ============================
@app.post("/jobs/find_and_match", response_model=List[JobResponse])
async def find_and_match_jobs(profile: dict):
    # 1. Search Jobs
    agent = create_job_search_agent(chat_model)
    result = await Runner.run(agent, json.dumps(profile))
    search_plan = result.final_output
    if isinstance(search_plan, str):
        search_plan = json.loads(search_plan)
    
    all_jobs = []
    # Limit queries to avoid timeout?
    for item in search_plan.get("search_queries", [])[:3]: 
        try:
            jobs = fetch_jobs_all_sources(query=item["query"], location=item["location"])
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"Error fetching jobs for {item}: {e}")

    # 2. Embed and Upsert
    # Processing in batches might be better, but sequential for now is safe
    for job in all_jobs:
        try:
            text = job_to_text(job)
            vector = await embedder.embed(text)
            job_id = str(uuid.uuid4())
            qdrant_jobs.upsert(point_id=job_id, vector=vector, payload=job)
        except Exception as e:
            print(f"Error indexing job: {e}")

    # 3. Match
    matched = await match_jobs(
        profile=profile,
        embedder=embedder,
        qdrant_jobs=qdrant_jobs,
        top_k=25
    )

    # 4. Rank
    ranked = rank_jobs(profile, matched)

    # 5. Explain (Top 5)
    explained = []
    for item in ranked[:5]:
        explanation = await run_explanation_agent(
            profile=profile,
            ranked_job=item
        )
        item["explanation"] = explanation
        explained.append(item)
    
    return explained


# ============================
# 3️⃣ MATCH + RANK
# ============================
@app.post("/jobs/match", response_model=List[JobResponse])
async def match_and_rank(profile: dict):

    # Match (vector search)
    matched = await match_jobs(
        profile=profile,
        embedder=embedder,
        qdrant_jobs=qdrant_jobs,
        top_k=25
    )

    # Rank
    ranked = rank_jobs(profile, matched)

    return ranked[:20]


# ============================
# 4️⃣ EXPLAIN
# ============================
@app.post("/jobs/explain", response_model=List[JobResponse])
async def explain_jobs(profile: dict):

    matched = await match_jobs(
        profile=profile,
        embedder=embedder,
        qdrant_jobs=qdrant_jobs,
        top_k=10
    )

    ranked = rank_jobs(profile, matched)

    explained = []
    for item in ranked[:5]:
        explanation = await run_explanation_agent(
            profile=profile,
            ranked_job=item
        )

        item["explanation"] = explanation
        explained.append(item)

    return explained


# ============================
# 5️⃣ GET ALL JOBS (PAGINATED)
# ============================
@app.post("/jobs/all", response_model=JobsAllResponse)
async def get_all_jobs(
    profile: dict,
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    size: int = Query(20, ge=1, le=100, description="Number of jobs per page")
):
    """
    Get all relevant jobs with pagination.
    
    Behavior:
    1. Generates search queries based on profile
    2. Fetches fresh jobs from APIs
    3. Indexes them in vector DB
    4. Matches and ranks jobs
    5. Returns paginated results
    
    Args:
        profile: User profile JSON
        page: Page number (1-indexed)
        size: Items per page (max 100)
    
    Returns:
        Paginated job results with total count
    """
    
    # Step 0: Clear old jobs from database to ensure fresh, relevant results
    print("🧹 Clearing old jobs from database...")
    qdrant_jobs.clear()
    
    # Step 1: Generate search queries
    agent = create_job_search_agent(chat_model)
    result = await Runner.run(agent, json.dumps(profile))
    search_plan = result.final_output
    
    # Parse JSON with error handling
    if isinstance(search_plan, str):
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in search_plan:
                search_plan = search_plan.split("```json")[1].split("```")[0].strip()
            elif "```" in search_plan:
                search_plan = search_plan.split("```")[1].split("```")[0].strip()
            
            search_plan = json.loads(search_plan)
            print(f"🔍 Generated Search Plan: {json.dumps(search_plan, indent=2)}", flush=True)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Raw output: {search_plan}")
            # Fallback: create basic search from profile
            primary_role = profile.get("primary_role", "Software Engineer")
            locations = profile.get("preferred_locations", ["Remote"])
            search_plan = {
                "search_queries": [
                    {"query": primary_role, "location": loc} 
                    for loc in locations[:2]
                ]
            }
    
    # Step 1.5: Expand queries to target LinkedIn and Indeed
    base_queries = search_plan.get("search_queries", [])
    expanded_queries = []
    
    # Add original queries
    expanded_queries.extend(base_queries)
    
    # Add platform-specific queries for the top query
    if base_queries:
        top_query = base_queries[0]
        q_text = top_query["query"]
        q_loc = top_query["location"]
        
        # Add LinkedIn specific query
        expanded_queries.append({
            "query": f"{q_text} LinkedIn",
            "location": q_loc
        })
        
        # Add Indeed specific query
        expanded_queries.append({
            "query": f"{q_text} Indeed",
            "location": q_loc
        })
    
    # Update search plan to use expanded list
    search_plan["search_queries"] = expanded_queries
    print(f"🚀 Expanded Search Plan with {len(expanded_queries)} queries (inc. LinkedIn/Indeed)", flush=True)
    
    # Step 2: Fetch fresh jobs
    all_jobs = []
    for item in search_plan.get("search_queries", [])[:8]:  # Increased to 8 to cover expanded queries
        try:
            jobs = fetch_jobs_all_sources(query=item["query"], location=item["location"])
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"Error fetching jobs for {item}: {e}")
    
    # Deduplicate jobs based on Title and Company
    unique_jobs_map = {}
    for job in all_jobs:
        t = str(job.get("title", "")).lower().strip()
        c = str(job.get("company", "")).lower().strip()
        # Key: title + company
        key = f"{t}|{c}"
        if key not in unique_jobs_map and t and c:
            unique_jobs_map[key] = job
    
    deduplicated_jobs = list(unique_jobs_map.values())
    print(f"🧹 Deduplication: Reduced {len(all_jobs)} jobs to {len(deduplicated_jobs)} unique jobs", flush=True)

    # Step 3: Index jobs in Qdrant
    for job in deduplicated_jobs:
        try:
            text = job_to_text(job)
            vector = await embedder.embed(text)
            job_id = str(uuid.uuid4())
            qdrant_jobs.upsert(point_id=job_id, vector=vector, payload=job)
        except Exception as e:
            print(f"Error indexing job: {e}")
    
    # Step 4: Match jobs (large candidate set from DB)
    matched = await match_jobs(
        profile=profile,
        embedder=embedder,
        qdrant_jobs=qdrant_jobs,
        top_k=500  # Large candidate pool
    )
    
    # Step 5: Rank all jobs
    ranked = rank_jobs(profile, matched)
    
    # Step 6: Pagination
    total = len(ranked)
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    
    # Get paginated results
    paginated_jobs = ranked[start_idx:end_idx]
    
    return JobsAllResponse(
        page=page,
        size=size,
        total=total,
        jobs=paginated_jobs
    )


# ============================
# 6️⃣ PREPARE APPLICATION
# ============================
@app.post("/apply/prepare", response_model=ApplicationPackage)
async def prepare_application(request: PrepareApplicationRequest):
    """
    Generate job-specific resume and cover letter.
    
    Behavior:
    1. Analyzes profile and job posting
    2. Generates tailored resume
    3. Generates personalized cover letter
    4. Returns both as editable text
    
    Args:
        request: Contains profile and job dictionaries
    
    Returns:
        Resume and cover letter text
    """
    
    profile = request.profile
    job = request.job
    
    # Validate inputs
    if not profile:
        raise HTTPException(status_code=400, detail="Profile is required")
    if not job:
        raise HTTPException(status_code=400, detail="Job is required")
    
    try:
        # Generate tailored resume
        resume_text = await generate_tailored_resume(
            profile=profile,
            job=job,
            model=chat_model
        )
        
        # Generate personalized cover letter
        cover_letter_text = await generate_cover_letter(
            profile=profile,
            job=job,
            model=chat_model
        )
        
        return ApplicationPackage(
            resume_text=resume_text,
            cover_letter_text=cover_letter_text
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate application materials: {str(e)}"
        )


# ============================
# 7️⃣ ASSIST APPLY (SAFE & COMPLIANT)
# ============================
@app.post("/apply/assist")
async def assist_apply(job: dict):
    """
    Assist with job application through browser redirection.
    
    IMPORTANT CONSTRAINTS:
    - NO auto-submission
    - NO credential storage
    - NO CAPTCHA bypass
    - User must manually complete and submit
    
    Behavior:
    1. Validates job has application URL
    2. Returns instructions and redirect URL
    3. User opens in browser and applies manually
    
    Args:
        job: Job posting with application URL
    
    Returns:
        Instructions and application URL
    """
    
    # Extract application URL
    apply_url = job.get("apply_url") or job.get("redirect_url") or job.get("job_apply_link") or job.get("url")
    
    if not apply_url:
        raise HTTPException(
            status_code=400,
            detail="Job does not have a valid application URL"
        )
    
    return JSONResponse(
        content={
            "message": "Ready to assist with application",
            "instructions": [
                "1. Review and edit your generated resume and cover letter",
                "2. Click the link below to open the job application page",
                "3. Fill in the application form manually",
                "4. Upload your tailored resume and cover letter",
                "5. Submit the application when ready"
            ],
            "apply_url": apply_url,
            "job_title": job.get("job_title", job.get("title", "Unknown")),
            "company": job.get("company_name", job.get("company", "Unknown")),
            "warning": "⚠️ You must complete and submit the application manually. No credentials are stored or auto-filled."
        }
    )


# ============================
# 8️⃣ HEALTH CHECK
# ============================
@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "AI Job Hunter API"}


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "AI Job Hunter API",
        "version": "1.0.0",
        "endpoints": {
            "profile": "/profile/extract",
            "jobs": {
                "search": "/jobs/search",
                "all": "/jobs/all",
                "match": "/jobs/match",
                "explain": "/jobs/explain",
                "find_and_match": "/jobs/find_and_match"
            },
            "apply": {
                "prepare": "/apply/prepare",
                "assist": "/apply/assist"
            }
        },
        "docs": "/docs"
    }