MAX_CHARS = 2000   # safe for all embedding models

def truncate(text: str, max_chars: int = MAX_CHARS) -> str:
    if not text:
        return ""
    return text[:max_chars]


def job_to_text(job: dict) -> str:
    description = truncate(job.get("description", ""))

    return f"""
    Job Title: {job.get("title")}
    Company: {job.get("company")}
    Location: {job.get("location")}
    Job Type: {job.get("job_type")}
    Description: {description}
    """

def profile_to_text(profile: dict) -> str:
    return f"""
    Role: {profile.get("primary_role")}
    Secondary Roles: {", ".join(profile.get("secondary_roles", []))}
    Skills: {", ".join(profile.get("skills", []))}
    Experience: {profile.get("experience_years")} years
    Seniority: {profile.get("seniority")}
    Job Type: {", ".join(profile.get("job_type", []))}
    Preferred Locations: {", ".join(profile.get("preferred_locations", []))}
    """[:2000]
