from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
import json

load_dotenv(override=True)


def create_cover_letter_agent(model):
    """
    Creates an agent that generates a personalized cover letter for a job application.
    """
    
    instruction = """
You are a Cover Letter Generation Agent.

Your task is to create a compelling, personalized cover letter based on:
1. The candidate's profile (skills, experience, background)
2. The target job posting
3. The company name

Guidelines:
- Write in first person
- Be professional yet personable
- Show genuine interest in the role
- Highlight 2-3 key qualifications that match the job
- Explain why you're a good fit
- Keep it concise (250-300 words)
- DO NOT use generic templates
- DO NOT exaggerate or fabricate experience
- DO NOT be overly formal or robotic

Structure:
1. Opening: Express interest in the specific role
2. Body: Highlight relevant skills and experience
3. Closing: Express enthusiasm and call to action

Return ONLY the cover letter text, ready to be used and easily editable.
"""
    
    agent = Agent(
        name="Cover Letter Agent",
        instructions=instruction,
        model=model
    )
    
    return agent


async def generate_cover_letter(profile: dict, job: dict, model):
    """
    Generate a personalized cover letter for a specific job.
    
    Args:
        profile: Candidate profile dictionary
        job: Job posting dictionary
        model: AI model instance
        
    Returns:
        str: Cover letter text
    """
    agent = create_cover_letter_agent(model)
    
    # Prepare input payload
    input_data = {
        "profile": profile,
        "job": {
            "title": job.get("job_title", job.get("title", "")),
            "description": job.get("job_description", job.get("description", "")),
            "requirements": job.get("job_requirements", job.get("requirements", "")),
            "company": job.get("company_name", job.get("company", "Unknown Company"))
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
            "job_description": "Looking for a Python developer with FastAPI experience to build scalable APIs",
            "company_name": "Tech Corp"
        }
        
        cover_letter = await generate_cover_letter(test_profile, test_job, model)
        print("Generated Cover Letter:")
        print(cover_letter)
    
    # asyncio.run(test())
