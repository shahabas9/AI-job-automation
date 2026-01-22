import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs"

def fetch_jobs_adzuna(query: str, location: str, page: int = 1, results_per_page: int = 20):
    """
    location examples:
    - 'us'
    - 'gb'
    - 'ae'
    - 'in'
    """
    url = f"{BASE_URL}/{location}/search/{page}"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "what": query,
        "results_per_page": results_per_page,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("❌ Adzuna failed")
        print("Status:", response.status_code)
        print("Response:", response.text)
        return []

    data = response.json()
    jobs = []

    for job in data.get("results", []):
        jobs.append({
            "job_id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "description": job.get("description"),
            "apply_url": job.get("redirect_url"),
            "job_type": None,
            "posted_at": job.get("created"),
            "source": "Adzuna"
        })

    return jobs


ADZUNA_SUPPORTED = {
    "at","au","be","br","ca","ch","de","es","fr","gb",
    "in","it","mx","nl","nz","pl","sg","us","za"
}

def map_location_to_adzuna(location: str) -> str:
    location = location.lower()

    if location in ADZUNA_SUPPORTED:
        return location

    if "india" in location:
        return "in"

    # UAE, Remote, Middle East → fallback
    return "us"
