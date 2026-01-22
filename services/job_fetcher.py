from services.job_fetcher_jsearch import fetch_jobs as fetch_jsearch
from services.job_fetcher_adzuna import fetch_jobs_adzuna,map_location_to_adzuna


def fetch_jobs_all_sources(query: str, location: str):
    jobs = []

    # JSearch
    jobs.extend(fetch_jsearch(query, location, pages=1))

    # Adzuna
    adzuna_country = map_location_to_adzuna(location)
    jobs.extend(fetch_jobs_adzuna(query, adzuna_country))

    return jobs
