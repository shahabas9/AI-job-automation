import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
BASE_URL = "https://jsearch.p.rapidapi.com/search"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}


def fetch_jobs(query: str, location: str, pages: int = 1):
    all_jobs = []

    for page in range(1, pages + 1):
        params = {
            "query": query,
            "page": page,
            "num_pages": 1
        }
        if location.lower() != "remote":
            params["location"] = location

        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print("❌ JSearch failed")
            print("Status:", response.status_code)
            print("Response:", response.text)
            return []

        data = response.json()
        jobs = data.get("data", [])

        for job in jobs:
            all_jobs.append({
                "job_id": job.get("job_id"),
                "title": job.get("job_title"),
                "company": job.get("employer_name"),
                "location": job.get("job_location"),
                "description": job.get("job_description"),
                "apply_url": job.get("job_apply_link"),
                "job_type": job.get("job_employment_type"),
                "posted_at": job.get("job_posted_at_datetime_utc"),
                "source": job.get("job_publisher")
            })
    
    return all_jobs


if __name__ == "__main__":
    fetch_jobs("developer", "chicago")