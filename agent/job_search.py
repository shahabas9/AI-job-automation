from agents import Agent
from openai import OpenAI,AsyncOpenAI
from agents import OpenAIChatCompletionsModel
import os

def create_job_search_agent():
    ollama_client =AsyncOpenAI(base_url=os.getenv("OLLAMA_BASE_URL"), api_key=os.getenv("OLLAMA_API_KEY"))
    model_name = os.getenv("MODEL_NAME")
    qwen_model = OpenAIChatCompletionsModel(model=model_name, openai_client=ollama_client)
    
    instruction = """
    You are a Job Search Planning Agent.

    Input: Candidate profile JSON
    Task:
    - Generate job search queries
    - Cover primary and secondary roles
    - Respect location preferences and nearby locations

    Return ONLY valid JSON:
    {
      "search_queries": [
        {"query": "...", "location": "..."}
      ]
    }
    """
    agent = Agent(name="Profile Extractor", instructions=instruction, model=qwen_model) 

    return agent
