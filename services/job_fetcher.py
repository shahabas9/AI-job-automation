from services.job_fetcher_jsearch import fetch_jobs as fetch_jsearch
from services.job_fetcher_adzuna import fetch_jobs_adzuna,map_location_to_adzuna


from services.job_fetcher_scraper import fetch_with_scraper

def fetch_jobs_all_sources(query: str, location: str):
    print(f"🌍 Fetching jobs for query='{query}' in location='{location}'...", flush=True)
    jobs = []

    # 1. JSearch (Primary API)
    jsearch_jobs = fetch_jsearch(query, location, pages=1)
    print(f"  -> JSearch found {len(jsearch_jobs)} jobs", flush=True)
    jobs.extend(jsearch_jobs)

    # 2. JobSpy Scraper (Fallback/Augmentation)
    # Use scraper if JSearch failed (0 jobs) OR if query explicitly mentions LinkedIn/Indeed
    # Or always use it if we want maximum coverage (but it's slower)
    if len(jsearch_jobs) == 0 or "linkedin" in query.lower() or "indeed" in query.lower():
        print(f"  -> Triggering Scraper (JobSpy)...", flush=True)
        # Clean query for scraper (remove 'LinkedIn' keyword if present to avoid double filtering)
        clean_query = query.replace("LinkedIn", "").replace("Indeed", "").strip()
        scraped_jobs = fetch_with_scraper(clean_query, location, limit=10)
        print(f"  -> JobSpy found {len(scraped_jobs)} jobs", flush=True)
        jobs.extend(scraped_jobs)

    # 3. Adzuna (Secondary API)
    adzuna_country = map_location_to_adzuna(location)
    adzuna_jobs = fetch_jobs_adzuna(query, adzuna_country)
    print(f"  -> Adzuna (country={adzuna_country}) found {len(adzuna_jobs)} jobs", flush=True)
    jobs.extend(adzuna_jobs)

    print(f"  => Total fetched: {len(jobs)} jobs", flush=True)
    return jobs
