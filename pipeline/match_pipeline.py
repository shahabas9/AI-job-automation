from utils.text_builders import profile_to_text

async def match_jobs(
    profile: dict,
    embedder,
    qdrant_jobs,
    top_k: int = 10
):
    # 1. Convert profile → text
    profile_text = profile_to_text(profile)

    # 2. Embed profile
    profile_vector = await embedder.embed(profile_text)

    # 3. Search Qdrant
    results = qdrant_jobs.search(
        query_vector=profile_vector,
        limit=top_k
    )

    # 4. Build ranked output
    ranked_jobs = []

    for hit in results:
        ranked_jobs.append({
            "score": round(hit.score, 4),
            "job": hit.payload
        })

    return ranked_jobs
