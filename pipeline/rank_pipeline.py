def skill_overlap_score(profile: dict, job: dict) -> float:
    profile_skills = set(s.lower() for s in profile.get("skills", []))
    description = (job.get("description") or "").lower()

    if not profile_skills:
        return 0.0

    matches = sum(1 for s in profile_skills if s in description)
    return min(matches / len(profile_skills), 1.0)


def normalize_locations(locations: list) -> list:
    """Flatten and normalize location strings"""
    normalized = []
    for loc in locations:
        # Split by comma and strip
        parts = [p.strip().lower() for p in loc.split(',')]
        normalized.extend(parts)
    return list(set(normalized)) # Remove duplicates

def location_score(profile: dict, job: dict) -> float:
    prefs = profile.get("preferred_locations", [])
    prefs_normalized = normalize_locations(prefs)
    job_loc = (job.get("location") or "").lower()

    if "remote" in prefs_normalized and "remote" in job_loc:
        return 1.0

    # Check if any normalized preference is inside job location
    # e.g. if pref="india", it matches job_loc="delhi, india"
    # e.g. if pref="bangalore", it matches job_loc="bangalore urban"
    if any(p in job_loc for p in prefs_normalized if len(p) > 2): # Avoid matching short abbreviations unless specific coverage
        return 1.0

    return 0.0


def seniority_score(profile: dict, job: dict) -> float:
    seniority = profile.get("seniority", "").lower()
    title = (job.get("title") or "").lower()

    if seniority == "junior" and "senior" in title:
        return 0.0

    if seniority == "senior" and "junior" in title:
        return 0.2

    return 1.0
def rank_jobs(profile: dict, matched_jobs: list, filter_by_location: bool = True, min_jobs: int = 15) -> list:
    """
    Rank jobs based on multiple factors with smart location filtering.
    
    Args:
        profile: User profile with preferences
        matched_jobs: List of jobs from vector search
        filter_by_location: If True, attempt to filter by location
        min_jobs: Minimum number of jobs to return (relaxes filter if needed)
    
    Returns:
        Ranked list of jobs
    """
    # Step 1: Try strict location filtering first
    filtered_jobs = matched_jobs
    location_filtered = False
    
    if filter_by_location:
        prefs = profile.get("preferred_locations", [])
        if prefs and prefs != []:
            # Only filter if there are actual location preferences
            prefs_normalized = normalize_locations(prefs)
            strict_filtered = []
            
            print(f"📍 Filtering by normalized locations: {prefs_normalized}", flush=True)

            for item in matched_jobs:
                job = item["job"]
                job_loc = (job.get("location") or "").lower()
                
                # Check if job location matches any preferred location
                # Also allow "Remote" jobs if that's in preferences
                if any(pref in job_loc for pref in prefs_normalized if len(pref) > 2):
                    strict_filtered.append(item)
                elif "remote" in prefs_normalized and "remote" in job_loc:
                    strict_filtered.append(item)
            
            # Smart filtering: If strict filter gives too few results, relax it
            if len(strict_filtered) >= min_jobs:
                filtered_jobs = strict_filtered
                location_filtered = True
                print(f"✅ Location filter applied: {len(strict_filtered)} jobs match preferred locations", flush=True)
            else:
                print(f"⚠️ Only {len(strict_filtered)} jobs match location filter. Showing all {len(matched_jobs)} jobs for better selection.", flush=True)
                filtered_jobs = matched_jobs
                location_filtered = False
    
    # Step 2: Rank the filtered jobs
    ranked = []
    for item in filtered_jobs:
        semantic = item["score"]
        job = item["job"]

        skill = skill_overlap_score(profile, job)
        location = location_score(profile, job)
        seniority = seniority_score(profile, job)

        # If location filtering was relaxed, increase location score weight
        if not location_filtered and filter_by_location:
            # Give higher weight to location when we couldn't filter strictly
            final_score = (
                0.50 * semantic +
                0.10 * skill +
                0.35 * location +  # Increased from 0.10
                0.05 * seniority
            )
        else:
            final_score = (
                0.75 * semantic +
                0.10 * skill +
                0.10 * location +
                0.05 * seniority
            )

        ranked.append({
            "final_score": round(final_score, 4),
            "semantic_score": round(semantic, 4),
            "job": job
        })

    ranked.sort(key=lambda x: x["final_score"], reverse=True)
    return ranked
