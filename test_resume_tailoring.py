import asyncio
import json
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel
from agent.resume_tailoring import generate_tailored_resume

load_dotenv(override=True)

async def test_resume_generation():
    # Use the extracted profile
    profile = {
        "full_name": "MOHAMED SHAHABAS",
        "email": "mohdshahabasm@gmail.com",
        "phone": "+91-8129917078",
        "linkedin_url": "https://www.linkedin.com/in/mohamed-shahabas-929b04151/",
        "primary_role": "Data Scientist",
        "work_experience": [
            {
                "company": "2Cloud",
                "role": "Data Scientist",
                "start_date": "Sep 2025",
                "end_date": "Present",
                "description": "Leading a data science team to drive AI innovation."
            }
        ],
        "skills": ["Python", "TensorFlow", "AWS", "FastAPI"]
    }
    
    # Sample job
    job = {
        "title": "Senior Data Scientist",
        "description": "Looking for a Data Scientist with Python, ML, and cloud experience",
        "company": "Tech Corp"
    }
    
    # Initialize model
    ollama_client = AsyncOpenAI(
        base_url=os.getenv("OLLAMA_BASE_URL"),
        api_key=os.getenv("OLLAMA_API_KEY")
    )
    
    model = OpenAIChatCompletionsModel(
        model=os.getenv("MODEL_NAME"),
        openai_client=ollama_client
    )
    
    print("Generating tailored resume...")
    resume = await generate_tailored_resume(profile, job, model)
    print("\n" + "="*80)
    print("GENERATED RESUME:")
    print("="*80)
    print(resume)
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_resume_generation())
