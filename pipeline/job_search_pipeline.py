from openai import Runner
from agents.job_search_agent import create_job_search_agent

async def run_job_search(profile_json):
    agent = create_job_search_agent()
    result = await Runner.run(agent, profile_json)
    return result.final_output
