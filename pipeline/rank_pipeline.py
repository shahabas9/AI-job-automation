def skill_overlap_score(profile: dict, job: dict) -> float:
    profile_skills = set(s.lower() for s in profile.get("skills", []))
    description = (job.get("description") or "").lower()

    if not profile_skills:
        return 0.0

    matches = sum(1 for s in profile_skills if s in description)
    return min(matches / len(profile_skills), 1.0)


def location_score(profile: dict, job: dict) -> float:
    prefs = [l.lower() for l in profile.get("preferred_locations", [])]
    job_loc = (job.get("location") or "").lower()

    if "remote" in prefs and "remote" in job_loc:
        return 1.0

    if any(p in job_loc for p in prefs):
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
def rank_jobs(profile: dict, matched_jobs: list) -> list:
    ranked = []

    for item in matched_jobs:
        semantic = item["score"]
        job = item["job"]

        skill = skill_overlap_score(profile, job)
        location = location_score(profile, job)
        seniority = seniority_score(profile, job)

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
