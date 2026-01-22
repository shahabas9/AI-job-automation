from services.job_fetcher import fetch_jobs_all_sources

def run_job_fetch(search_plan):
    all_jobs = []

    for item in search_plan["search_queries"]:
        jobs = fetch_jobs_all_sources(
            query=item["query"],
            location=item["location"]
        )
        all_jobs.extend(jobs)

    # Deduplicate
    unique = {(j["title"], j["company"]): j for j in all_jobs}
    return list(unique.values())
