import json
import asyncio
from services.embedding_service import EmbeddingService
from services.qdrant_service import QdrantService
from utils.text_builders import profile_to_text, job_to_text


async def embed_jobs(jobs, embedder, qdrant):
    for job in jobs:
        text = job_to_text(job)
        vector = await embedder.embed(text)
        qdrant.upsert(
            point_id=job["job_id"],
            vector=vector,
            payload=job
        )

async def embed_profile(profile, embedder, qdrant):
    text = profile_to_text(profile)
    vector = await embedder.embed(text)
    qdrant.upsert(
        point_id="PROFILE",
        vector=vector,
        payload=profile
    )
