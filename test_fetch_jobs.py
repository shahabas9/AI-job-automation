import asyncio
import json
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import  Runner,OpenAIChatCompletionsModel
from agent.job_search import create_job_search_agent
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

load_dotenv(override=True)










async def test_full_pipeline():

    # ============================
    # 1. OLLAMA / MODEL SETUP
    # ============================
    ollama_client = AsyncOpenAI(
        base_url=os.getenv("OLLAMA_BASE_URL"),
        api_key=os.getenv("OLLAMA_API_KEY")
    )

    chat_model_name = os.getenv("MODEL_NAME")          # qwen / llama
    embed_model_name = os.getenv("EMBED_MODEL_NAME")   # nomic-embed-text

    chat_model = OpenAIChatCompletionsModel(
        model=chat_model_name,
        openai_client=ollama_client
    )

    embedder = EmbeddingService(
        client=ollama_client,
        model=embed_model_name
    )

    # ============================
    # 2. QDRANT SETUP
    # ============================
    qdrant_jobs = QdrantService(
        collection_name="jobs",
        vector_size=768
    )

    qdrant_profile = QdrantService(
        collection_name="profile",
        vector_size=768
    )

    # ============================
    # 3. PROFILE (MOCK FOR NOW)
    # ============================
    profile_json = {
        "primary_role": "AI Engineer",
        "secondary_roles": ["Machine Learning Engineer"],
        "skills": ["Python", "PyTorch", "LLMs", "RAG"],
        "experience_years": 2,
        "seniority": "junior",
        "preferred_locations": ["INDIA", "UAE"],
        "job_type": ["Full-time"]
    }

    print("\n👤 PROFILE")
    print(json.dumps(profile_json, indent=2))

    # ============================
    # 4. JOB SEARCH AGENT
    # ============================
    job_search_agent = create_job_search_agent()

    result = await Runner.run(
        job_search_agent,
        json.dumps(profile_json)
    )

    search_plan = result.final_output
    if isinstance(search_plan, str):
        search_plan = json.loads(search_plan)

    print("\n🔍 SEARCH PLAN")
    print(json.dumps(search_plan, indent=2))

    # ============================
    # 5. FETCH JOBS
    # ============================
    all_jobs = []

    for item in search_plan["search_queries"]:
        jobs = fetch_jobs_all_sources(
            query=item["query"],
            location=item["location"]
        )
        all_jobs.extend(jobs)

    print(f"\n✅ TOTAL JOBS FETCHED: {len(all_jobs)}")

    for job in all_jobs[:3]:
        print(json.dumps(job, indent=2))
        print("-" * 50)

    # ============================
    # 6. EMBED PROFILE
    # ============================
    profile_text = profile_to_text(profile_json)
    profile_vector = await embedder.embed(profile_text)
    profile_id = str(uuid.uuid4())
    qdrant_profile.upsert(
        point_id=profile_id,
        vector=profile_vector,
        payload=profile_json
    )

    print("✅ Profile embedded & stored")

    # ============================
    # 7. EMBED JOBS
    # ============================
    for job in all_jobs:
        text = job_to_text(job)
        vector = await embedder.embed(text)

        job_point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                f"{job['title']}-{job['company']}-{job.get('location')}"
            )
        )

        qdrant_jobs.upsert(
            point_id=job_point_id,
            vector=vector,
            payload=job
        )

    print(f"✅ {len(all_jobs)} job embeddings stored in Qdrant")

    # ============================
    # 8. MATCH JOBS
    # ============================
    ranked_jobs = await match_jobs(
        profile=profile_json,
        embedder=embedder,
        qdrant_jobs=qdrant_jobs,
        top_k=5
    )

    print("\n🏆 TOP MATCHED JOBS\n")

    for idx, item in enumerate(ranked_jobs, start=1):
        job = item["job"]
        print(f"{idx}. {job['title']} at {job['company']}")
        print(f"   Score: {item['score']}")
        print(f"   Location: {job['location']}")
        print(f"   Apply: {job['apply_url']}")
        print("-" * 60)

    ranked_jobs = rank_jobs(profile_json, ranked_jobs)

    print("\n🏆 TOP RANKED JOBS\n")

    for i, item in enumerate(ranked_jobs[:5], start=1):
        job = item["job"]
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   Final Score: {item['final_score']}")
        print(f"   Semantic: {item['semantic_score']}")
        print(f"   Location: {job['location']}")
        print(f"   Apply: {job['apply_url']}")
        print("-" * 60)

    print("\n🧠 JOB EXPLANATIONS\n")

    for item in ranked_jobs[:3]:
        explanation = await run_explanation_agent(
            profile=profile_json,
            ranked_job=item
        )

        job = item["job"]
        print(f"📌 {job['title']} at {job['company']}")
        print(explanation)
        print("-" * 70)



    print("\n🎉 FULL PIPELINE TEST COMPLETED SUCCESSFULLY")




if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
