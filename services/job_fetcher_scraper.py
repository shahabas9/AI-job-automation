from jobspy import scrape_jobs
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_with_scraper(query: str, location: str, limit: int = 15):
    """
    Fetch jobs using JobSpy (Scraping LinkedIn, Indeed, Glassdoor, ZipRecruiter).
    
    Args:
        query (str): Job title or keywords
        location (str): Job location
        limit (int): Max jobs to fetch
        
    Returns:
        list: List of job dictionaries in standard format
    """
    print(f"🕵️‍♂️ Scraping jobs for '{query}' in '{location}'...", flush=True)
    
    # Define sites to scrape
    # Note: Indeed is often strictly blocked, so we prioritize others or handle failures gracefully
    site_names = ["linkedin", "indeed", "zip_recruiter"]
    
    try:
        jobs_df = scrape_jobs(
            site_name=site_names,
            search_term=query,
            location=location,
            results_wanted=limit,
            hours_old=72,  # Fetch jobs posted in last 3 days
            country_urlpatterns={
                "Global": "https://www.linkedin.com" 
                # JobSpy handles country codes automatically usually, 
                # but explicit mapping can be added if needed.
                # For India, it detects via location usually.
            }
        )
        
        if jobs_df.empty:
            print(f"⚠️ Scraper found 0 jobs for {query}", flush=True)
            return []
            
        print(f"✅ Scraper found {len(jobs_df)} jobs", flush=True)
        
        # Convert DataFrame to list of dicts with standarized keys
        # Convert DataFrame to list of dicts with standarized keys
        
        def safe_str(val):
            if pd.isna(val) or val is None:
                return ""
            return str(val).strip()

        standardized_jobs = []
        for _, row in jobs_df.iterrows():
            try:
                # Map JobSpy columns to our schema
                job = {
                    "title": safe_str(row.get("title")),
                    "company": safe_str(row.get("company")),
                    "location": safe_str(row.get("location")),
                    "description": safe_str(row.get("description")) or "No description available",
                    "apply_url": safe_str(row.get("job_url")),
                    "source": safe_str(row.get("site")), # e.g., "linkedin"
                    "job_type": safe_str(row.get("job_type")),
                    "posted_at": safe_str(row.get("date_posted")),
                    "salary": safe_str(row.get("median_salary")),
                    "currency": safe_str(row.get("currency"))
                }
                standardized_jobs.append(job)
            except Exception as e:
                print(f"❌ Error parsing job row: {e}")
                continue
                
        return standardized_jobs

    except Exception as e:
        print(f"❌ Scraping failed: {e}", flush=True)
        return []

if __name__ == "__main__":
    # Test run
    jobs = fetch_with_scraper("DevOps Engineer", "India", limit=5)
    for j in jobs:
        print(f"- {j['title']} at {j['company']} ({j['source']})")
