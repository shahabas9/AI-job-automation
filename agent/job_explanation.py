from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool,OpenAIChatCompletionsModel
from typing import Dict
from openai import OpenAI,AsyncOpenAI
import os,json
import asyncio

load_dotenv(override=True)


async def run_explanation_agent(profile: dict, ranked_job: dict):

    # ----------------------------
    # 1. Model setup
    # ----------------------------
    ollama_client = AsyncOpenAI(
        base_url=os.getenv("OLLAMA_BASE_URL"),
        api_key=os.getenv("OLLAMA_API_KEY")
    )

    model_name = os.getenv("MODEL_NAME")

    model = OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=ollama_client
    )

    # ----------------------------
    # 2. Instructions (VERY IMPORTANT)
    # ----------------------------
    instruction = """
You are a Job Match Explanation Agent.

Explain WHY this job matches the candidate.
Be factual and specific.
Use 3–4 short sentences.
DO NOT exaggerate.
DO NOT invent skills or requirements.
DO NOT mention scores explicitly.

Focus on:
- skill alignment
- role fit
- experience level
- location or work type if relevant
"""

    agent = Agent(
        name="Job Match Explainer",
        instructions=instruction,
        model=model
    )

    # ----------------------------
    # 3. Build input
    # ----------------------------
    input_payload = {
        "candidate_profile": profile,
        "job": ranked_job["job"],
        "semantic_score": ranked_job["semantic_score"],
        "final_score": ranked_job["final_score"]
    }

    # ----------------------------
    # 4. Run agent
    # ----------------------------
    with trace("explanation_trace.json"):
        result = await Runner.run(
            agent,
            json.dumps(input_payload)
        )

    return result.final_output