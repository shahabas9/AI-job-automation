from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool,OpenAIChatCompletionsModel
from openai.types.responses import ResponseTextDeltaEvent
from typing import Dict
from openai import OpenAI,AsyncOpenAI
import os,json
import asyncio

load_dotenv(override=True)

def create_profile_agent(model):
    instruction = """
            You are a Profile Extraction Agent.

            Analyze the resume and return ONLY valid JSON with:
            - full_name (Extract the candidate's name)
            - email
            - phone
            - linkedin_url
            - primary_role (e.g., "DevOps Engineer", "Software Engineer")
            - secondary_roles (list of related roles)
            - work_experience (List of objects: {company, role, start_date, end_date, description})
            - education (List of objects: {institution, degree, graduation_year})
            - skills (list of technical skills)
            - experience_years (integer)
            - seniority (junior/mid/senior)
            - preferred_locations (IMPORTANT: extract from resume - city, country, or "Remote")
            - job_type (full-time/part-time/contract)
            - confidence_score (0-1)
            
            For preferred_locations:
            - Look for: current location, desired location, willing to relocate to
            - Extract specific cities/countries mentioned (e.g., ["India", "Bangalore"])
            - If mentions "Remote" or "Work from home", include "Remote"
            - If no location mentioned, return empty list []
    """

    agent = Agent(name="Profile Extractor", instructions=instruction, model=model) 
    return agent

if __name__ == "__main__":
    async def main():
        ollama_client = AsyncOpenAI(base_url=os.getenv("OLLAMA_BASE_URL"), api_key=os.getenv("OLLAMA_API_KEY"))
        model_name = os.getenv("MODEL_NAME")
        qwen_model = OpenAIChatCompletionsModel(model=model_name, openai_client=ollama_client)
        
        agent = create_profile_agent(qwen_model)
        
        # Example usage
        # result = await Runner.run(agent, "some resume text")
        # print(result.final_output)

    # asyncio.run(main())
