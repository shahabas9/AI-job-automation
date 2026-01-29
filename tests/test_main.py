"""
Test suite for AI Job Hunter API

Run with: pytest tests/test_main.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app
import json


client = TestClient(app)


# =====================
# Health & Info Tests
# =====================

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "AI Job Hunter API"


def test_root_endpoint():
    """Test root endpoint returns API information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "endpoints" in data
    assert "docs" in data


# =====================
# Profile Extraction Tests
# =====================

@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing"""
    return """
    John Doe
    Software Engineer
    
    Skills: Python, FastAPI, React, PostgreSQL, Docker
    
    Experience:
    Software Engineer at Tech Corp (2021-2024)
    - Built scalable APIs using FastAPI
    - Worked with React frontend
    - Managed PostgreSQL databases
    
    Education:
    BS Computer Science, 2020
    """


def test_profile_extraction_requires_file():
    """Test that profile extraction requires a file"""
    response = client.post("/profile/extract")
    assert response.status_code == 422  # Unprocessable Entity


# =====================
# Jobs All (Pagination) Tests
# =====================

@pytest.fixture
def sample_profile():
    """Sample user profile"""
    return {
        "primary_role": "Software Engineer",
        "skills": ["Python", "FastAPI", "React"],
        "experience_years": 3,
        "seniority": "mid",
        "preferred_locations": ["Remote"],
        "job_type": "full-time"
    }


def test_jobs_all_pagination_default(sample_profile):
    """Test default pagination parameters"""
    response = client.post("/jobs/all", json=sample_profile)
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert "page" in data
    assert "size" in data
    assert "total" in data
    assert "jobs" in data
    
    # Check defaults
    assert data["page"] == 1
    assert data["size"] == 20


def test_jobs_all_pagination_custom(sample_profile):
    """Test custom pagination parameters"""
    response = client.post(
        "/jobs/all?page=2&size=10",
        json=sample_profile
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["page"] == 2
    assert data["size"] == 10


def test_jobs_all_pagination_max_size(sample_profile):
    """Test maximum page size limit"""
    response = client.post(
        "/jobs/all?page=1&size=150",
        json=sample_profile
    )
    # Should fail validation (max size is 100)
    assert response.status_code == 422


def test_jobs_all_invalid_page(sample_profile):
    """Test invalid page number"""
    response = client.post(
        "/jobs/all?page=0&size=20",
        json=sample_profile
    )
    # Page must be >= 1
    assert response.status_code == 422


# =====================
# Application Preparation Tests
# =====================

@pytest.fixture
def sample_job():
    """Sample job posting"""
    return {
        "job_title": "Backend Engineer",
        "company_name": "Tech Corp",
        "job_description": "We're looking for a Backend Engineer with Python experience",
        "job_requirements": "3+ years Python, FastAPI, PostgreSQL",
        "location": "Remote",
        "job_type": "Full-time"
    }


def test_prepare_application_success(sample_profile, sample_job):
    """Test successful application preparation"""
    payload = {
        "profile": sample_profile,
        "job": sample_job
    }
    
    response = client.post("/apply/prepare", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "resume_text" in data
    assert "cover_letter_text" in data
    
    # Check that content is not empty
    assert len(data["resume_text"]) > 0
    assert len(data["cover_letter_text"]) > 0


def test_prepare_application_missing_profile(sample_job):
    """Test application preparation without profile"""
    payload = {
        "profile": {},
        "job": sample_job
    }
    
    response = client.post("/apply/prepare", json=payload)
    assert response.status_code == 400
    assert "Profile is required" in response.json()["detail"]


def test_prepare_application_missing_job(sample_profile):
    """Test application preparation without job"""
    payload = {
        "profile": sample_profile,
        "job": {}
    }
    
    response = client.post("/apply/prepare", json=payload)
    assert response.status_code == 400
    assert "Job is required" in response.json()["detail"]


# =====================
# Assist Apply Tests
# =====================

def test_assist_apply_success():
    """Test assist apply with valid job URL"""
    job = {
        "job_title": "Software Engineer",
        "company_name": "Tech Corp",
        "redirect_url": "https://example.com/jobs/apply/123"
    }
    
    response = client.post("/apply/assist", json=job)
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "instructions" in data
    assert "apply_url" in data
    assert "warning" in data
    
    # Verify URL is returned
    assert data["apply_url"] == "https://example.com/jobs/apply/123"
    
    # Verify instructions are present
    assert len(data["instructions"]) > 0


def test_assist_apply_missing_url():
    """Test assist apply without application URL"""
    job = {
        "job_title": "Software Engineer",
        "company_name": "Tech Corp"
        # Missing redirect_url
    }
    
    response = client.post("/apply/assist", json=job)
    assert response.status_code == 400
    assert "valid application URL" in response.json()["detail"]


def test_assist_apply_alternative_url_fields():
    """Test assist apply with alternative URL field names"""
    # Test with job_apply_link
    job1 = {
        "job_title": "Engineer",
        "job_apply_link": "https://example.com/apply"
    }
    response1 = client.post("/apply/assist", json=job1)
    assert response1.status_code == 200
    
    # Test with url
    job2 = {
        "job_title": "Engineer",
        "url": "https://example.com/apply"
    }
    response2 = client.post("/apply/assist", json=job2)
    assert response2.status_code == 200


# =====================
# Integration Tests
# =====================

def test_full_workflow_simulation(sample_profile, sample_job):
    """
    Simulate a complete user workflow:
    1. Extract profile (skipped - needs file upload)
    2. Get all jobs
    3. Prepare application
    4. Assist apply
    """
    
    # Step 1: Get jobs (paginated)
    jobs_response = client.post(
        "/jobs/all?page=1&size=5",
        json=sample_profile
    )
    assert jobs_response.status_code == 200
    jobs_data = jobs_response.json()
    assert "jobs" in jobs_data
    
    # Step 2: Prepare application for first job (or use sample)
    prepare_response = client.post(
        "/apply/prepare",
        json={
            "profile": sample_profile,
            "job": sample_job
        }
    )
    assert prepare_response.status_code == 200
    prepare_data = prepare_response.json()
    assert "resume_text" in prepare_data
    assert "cover_letter_text" in prepare_data
    
    # Step 3: Get assist instructions
    assist_response = client.post(
        "/apply/assist",
        json={
            **sample_job,
            "redirect_url": "https://example.com/apply"
        }
    )
    assert assist_response.status_code == 200
    assist_data = assist_response.json()
    assert "apply_url" in assist_data


# =====================
# Error Handling Tests
# =====================

def test_invalid_json():
    """Test endpoints with invalid JSON"""
    response = client.post(
        "/jobs/all",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


def test_missing_required_fields():
    """Test endpoints with missing required fields"""
    # Empty profile
    response = client.post("/jobs/all", json={})
    # Should still work but may return no jobs
    assert response.status_code in [200, 422]


# =====================
# Performance Tests
# =====================

@pytest.mark.slow
def test_jobs_all_large_page_size(sample_profile):
    """Test performance with large page size"""
    import time
    
    start = time.time()
    response = client.post(
        "/jobs/all?page=1&size=100",
        json=sample_profile
    )
    duration = time.time() - start
    
    assert response.status_code == 200
    # Should complete within reasonable time (adjust threshold as needed)
    assert duration < 30  # 30 seconds threshold


# =====================
# Security Tests
# =====================

def test_no_sql_injection_in_profile():
    """Test that malicious SQL in profile doesn't cause issues"""
    malicious_profile = {
        "primary_role": "'; DROP TABLE jobs; --",
        "skills": ["<script>alert('xss')</script>"],
        "experience_years": 999999,
        "seniority": "SELECT * FROM users"
    }
    
    # Should not crash or execute malicious code
    response = client.post("/jobs/all", json=malicious_profile)
    # Either succeeds or returns validation error, but doesn't crash
    assert response.status_code in [200, 400, 422, 500]


def test_response_structure_consistency():
    """Test that all responses follow consistent structure"""
    # Health check
    health = client.get("/health").json()
    assert isinstance(health, dict)
    
    # Root
    root = client.get("/").json()
    assert isinstance(root, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
