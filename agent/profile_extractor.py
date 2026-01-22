from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool,OpenAIChatCompletionsModel
from openai.types.responses import ResponseTextDeltaEvent
from typing import Dict
from openai import OpenAI,AsyncOpenAI
import os,json
import asyncio

load_dotenv(override=True)

async def create_profile_agent():
    ollama_client =AsyncOpenAI(base_url=os.getenv("OLLAMA_BASE_URL"), api_key=os.getenv("OLLAMA_API_KEY"))
    model_name = os.getenv("MODEL_NAME")
    qwen_model = OpenAIChatCompletionsModel(model=model_name, openai_client=ollama_client)

    instruction = """
            You are a Profile Extraction Agent.

            Analyze the resume and return ONLY valid JSON with:
            - primary_role
            - secondary_roles
            - skills
            - experience_years
            - seniority (junior/mid/senior)
            - preferred_locations
            - job_type
            - confidence_score (0-1)
    """

    agent = Agent(name="Profile Extractor", instructions=instruction, model=qwen_model) 


    with open("resume_text.txt", "r") as f:
        content = f.read()
    with trace("profile_extractor_trace.json"):
        result = await Runner.run(agent, content)
    
    print("✅ Extracted Profile:")
    print(result.final_output)
    
asyncio.run(create_profile_agent())
