from services.job_fetcher_jsearch import fetch_jobs
import json

print("Searching for 'DevOps India site:linkedin.com'...")
jobs_linkedin = fetch_jobs("DevOps India site:linkedin.com", "India", pages=1)
print(f"Found {len(jobs_linkedin)} jobs from LinkedIn query trick")

if jobs_linkedin:
    print("First job source:", jobs_linkedin[0].get('source'))

print("\nSearching for 'DevOps India site:indeed.com'...")
jobs_indeed = fetch_jobs("DevOps India site:indeed.com", "India", pages=1)
print(f"Found {len(jobs_indeed)} jobs from Indeed query trick")

if jobs_indeed:
    print("First job source:", jobs_indeed[0].get('source'))
