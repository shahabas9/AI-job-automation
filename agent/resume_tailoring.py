from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
import json

load_dotenv(override=True)


def create_resume_tailoring_agent(model):
    """
    Creates an agent that tailors a resume for a specific job posting.
    """
    
    instruction = """
You are an Expert Resume Editor.

Your task is to REWRITE the candidate's existing resume to better match the target job, WITHOUT inventing new facts.

INPUTs:
1. Candidate Profile: {profile}
2. Target Job: {job}

STRICT RULES:
1. ✅ USE ONLY the experience, companies, and dates provided in the Profile.
2. ❌ DO NOT invent new jobs, companies, or degrees.
3. ❌ DO NOT change the candidate's name or contact info.
4. ✅ YOU MUST rewrite the *bullet points* of existing jobs to highlight keywords from the target job.
5. ✅ If the candidate lacks a specific skill, DO NOT add it. Focus on transferrable skills you see in the profile.

GOAL:
- Tailor the "Summary" to mention the target role and key matching skills.
- Rephrase "Experience" bullet points to use the terminology from the Job Description (e.g., change "Managed servers" to "Orchestrated infrastructure" if the job asks for it).
- Reorder "Skills" to prioritize matches.

Output format:
- Header (Name, Email, Phone, Links from Profile)
- tailored Summary
- Experience (Date, Company, Role -> Tailored Bullets)
- Education
- Skills

Keep it authentic. If the candidate is a DevOps Engineer, do NOT make them a Data Scientist.
"""
    
    agent = Agent(
        name="Resume Tailoring Agent",
        instructions=instruction,
        model=model
    )
    
    return agent


async def generate_tailored_resume(profile: dict, job: dict, model):
    """
    Generate a tailored resume for a specific job.
    
    Args:
        profile: Candidate profile dictionary
        job: Job posting dictionary
        model: AI model instance
        
    Returns:
        str: Tailored resume text
    """
    agent = create_resume_tailoring_agent(model)
    
    # Prepare input payload
    input_data = {
        "profile": profile,
        "job": {
            "title": job.get("job_title", job.get("title", "")),
            "description": job.get("job_description", job.get("description", "")),
            "requirements": job.get("job_requirements", job.get("requirements", "")),
            "company": job.get("company_name", job.get("company", ""))
        }
    }
    
    result = await Runner.run(agent, json.dumps(input_data))
    
    return result.final_output


def create_cover_letter_agent(model):
    """
    Creates an agent that writes a cover letter for a specific job.
    """
    instruction = """
    You are a Cover Letter Specialist.
    
    Your task is to write a compelling cover letter based on:
    1. The candidate's profile (skills, experience_years, roles)
    2. The target job description
    
    Guidelines:
    - Address the hiring manager professionally
    - Hook the reader in the opening paragraph
    - Map candidate's key achievements to job requirements
    - Demonstrate enthusiasm for the company/role
    - Keep it concise (3-4 paragraphs max)
    - Professional sign-off
    
    Return ONLY the cover letter body text (no markdown, no extra meta-data).
    """
    
    agent = Agent(
        name="Cover Letter Agent",
        instructions=instruction,
        model=model
    )
    return agent


async def generate_cover_letter(profile: dict, job: dict, model):
    """
    Generate a personalized cover letter.
    """
    agent = create_cover_letter_agent(model)
    
    # Prepare input payload
    input_data = {
        "profile": profile,
        "job": {
            "title": job.get("job_title", job.get("title", "")),
            "description": job.get("job_description", job.get("description", "")),
            "company": job.get("company_name", job.get("company", ""))
        }
    }
    
    result = await Runner.run(agent, json.dumps(input_data))
    return result.final_output


if __name__ == "__main__":
    import asyncio
    
    async def test():
        ollama_client = AsyncOpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL"),
            api_key=os.getenv("OLLAMA_API_KEY")
        )
        
        model_name = os.getenv("MODEL_NAME")
        model = OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=ollama_client
        )
        
        # Test profile
        test_profile = {
            "primary_role": "Software Engineer",
            "skills": ["Python", "FastAPI", "React", "PostgreSQL"],
            "experience_years": 3,
            "seniority": "mid"
        }
        
        # Test job
        test_job = {
            "job_title": "Backend Developer",
            "job_description": "Looking for a Python developer with FastAPI experience",
            "company_name": "Tech Corp"
        }
        
        resume = await generate_tailored_resume(test_profile, test_job, model)
        print("Generated Resume:")
        print(resume)
    
    # asyncio.run(test())
