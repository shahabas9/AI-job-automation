from parser.parse_resume import extract_text
from agents.profile_extractor_agent import create_profile_agent
from openai import Runner

async def run_profile_pipeline(resume_path, model):
    resume_text = extract_text(resume_path)

    agent = create_profile_agent(model)
    result = await Runner.run(agent, resume_text)

    return result.final_output
