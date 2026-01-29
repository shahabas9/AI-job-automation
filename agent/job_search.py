from agents import Agent
from openai import OpenAI,AsyncOpenAI
from agents import OpenAIChatCompletionsModel
import os

def create_job_search_agent(model):
    
    instruction = """
    You are a Job Search Planning Agent.

    Input: Candidate profile JSON
    Task:
    - Generate job search queries based on the candidate's profile
    - IMPORTANT: Prioritize the candidate's preferred_locations
    - If preferred_locations includes specific cities (e.g., "Wayanad"), 
      ALSO include a query for the broader Country or major nearby tech hubs (e.g., "India", "Bangalore")
    - If preferred_locations is simple (e.g. "India"), use that.
    - Always ensure at least one query uses the broadest relevant location (Country level).
    - Cover primary role and top 2-3 secondary roles
    - Generate 3-5 search queries maximum

    Return ONLY valid JSON (no markdown, no code blocks):
    {
      "search_queries": [
        {"query": "role", "location": "City, Country"},
        {"query": "role", "location": "Country"} 
      ]
    }
    
    Example:
    If preferred_locations = ["Wayanad, Kerala, India"], generate queries for "Wayanad" AND "India" AND "Kerala".
    If preferred_locations = ["Remote"], you can use "Remote" or major markets
    """
    agent = Agent(name="Job Search Agent", instructions=instruction, model=model) 

    return agent
