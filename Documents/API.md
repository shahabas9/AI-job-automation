# API Documentation

## Base URL
```
http://localhost:8000
```

For production, replace with your deployed URL.

---

## Authentication

Currently, the API is open. For production deployment, consider adding:
- API Key authentication
- OAuth2
- Rate limiting

---

## Endpoints

### 1. Health Check

Check if the API is running.

#### Request
```http
GET /health
```

#### Response
```json
{
  "status": "healthy",
  "service": "AI Job Hunter API"
}
```

---

### 2. API Information

Get information about available endpoints.

#### Request
```http
GET /
```

#### Response
```json
{
  "service": "AI Job Hunter API",
  "version": "1.0.0",
  "endpoints": {
    "profile": "/profile/extract",
    "jobs": {
      "search": "/jobs/search",
      "all": "/jobs/all",
      "match": "/jobs/match",
      "explain": "/jobs/explain",
      "find_and_match": "/jobs/find_and_match"
    },
    "apply": {
      "prepare": "/apply/prepare",
      "assist": "/apply/assist"
    }
  },
  "docs": "/docs"
}
```

---

### 3. Extract Profile

Extract structured profile from a resume file.

#### Request
```http
POST /profile/extract
Content-Type: multipart/form-data

file: <resume.pdf|.docx|.txt>
```

#### cURL Example
```bash
curl -X POST http://localhost:8000/profile/extract \
  -F "file=@/path/to/resume.pdf"
```

#### Response
```json
{
  "primary_role": "Software Engineer",
  "secondary_roles": ["Backend Developer", "Full Stack Developer"],
  "skills": [
    "Python",
    "FastAPI",
    "React",
    "PostgreSQL",
    "Docker",
    "AWS"
  ],
  "experience_years": 3,
  "seniority": "mid",
  "preferred_locations": ["San Francisco", "Remote"],
  "job_type": "full-time",
  "confidence_score": 0.95
}
```

#### Error Responses
- `422 Unprocessable Entity`: No file provided or invalid file format

---

### 4. Get All Jobs (Paginated)

Fetch and rank all relevant jobs with pagination support.

#### Request
```http
POST /jobs/all?page=1&size=20
Content-Type: application/json

{
  "primary_role": "Software Engineer",
  "skills": ["Python", "FastAPI"],
  "experience_years": 3,
  "seniority": "mid",
  "preferred_locations": ["Remote"],
  "job_type": "full-time"
}
```

#### Query Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number (minimum: 1) |
| size | integer | 20 | Items per page (minimum: 1, maximum: 100) |

#### cURL Example
```bash
curl -X POST "http://localhost:8000/jobs/all?page=1&size=10" \
  -H "Content-Type: application/json" \
  -d '{
    "primary_role": "Software Engineer",
    "skills": ["Python", "FastAPI"],
    "experience_years": 3,
    "seniority": "mid"
  }'
```

#### Response
```json
{
  "page": 1,
  "size": 20,
  "total": 214,
  "jobs": [
    {
      "final_score": 0.89,
      "semantic_score": 0.85,
      "job": {
        "job_title": "Backend Engineer",
        "company_name": "Tech Corp",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "job_description": "We are looking for an experienced Backend Engineer...",
        "job_requirements": "3+ years Python, FastAPI experience...",
        "salary_min": 120000,
        "salary_max": 180000,
        "posted_date": "2024-01-15",
        "redirect_url": "https://techcorp.com/jobs/backend-engineer"
      },
      "explanation": null
    }
  ]
}
```

#### Error Responses
- `422 Unprocessable Entity`: Invalid query parameters (page < 1, size > 100)
- `400 Bad Request`: Invalid profile data

---

### 5. Prepare Application

Generate job-specific resume and cover letter.

#### Request
```http
POST /apply/prepare
Content-Type: application/json

{
  "profile": {
    "primary_role": "Software Engineer",
    "skills": ["Python", "FastAPI", "PostgreSQL"],
    "experience_years": 3,
    "seniority": "mid"
  },
  "job": {
    "job_title": "Backend Developer",
    "company_name": "Tech Corp",
    "job_description": "We're looking for an experienced Backend Developer...",
    "job_requirements": "3+ years Python, FastAPI, PostgreSQL experience",
    "location": "Remote",
    "job_type": "Full-time"
  }
}
```

#### cURL Example
```bash
curl -X POST http://localhost:8000/apply/prepare \
  -H "Content-Type: application/json" \
  -d @examples/test_prepare_application.json
```

#### Response
```json
{
  "resume_text": "PROFESSIONAL SUMMARY\n\nExperienced Software Engineer with 3 years of expertise in backend development using Python and FastAPI. Proven track record of building scalable APIs and working with PostgreSQL databases.\n\nSKILLS\n• Python\n• FastAPI\n• PostgreSQL\n• REST API Development\n\nEXPERIENCE\n\nSoftware Engineer\nPrevious Company | 2021 - 2024\n• Developed and maintained RESTful APIs using FastAPI\n• Optimized PostgreSQL database queries for improved performance\n• Collaborated with frontend teams to integrate backend services\n\n...",
  
  "cover_letter_text": "Dear Hiring Manager,\n\nI am excited to apply for the Backend Developer position at Tech Corp. With 3 years of experience building scalable backend systems using Python and FastAPI, I am confident I can contribute effectively to your team.\n\nIn my current role, I have developed RESTful APIs that serve millions of requests daily, working extensively with PostgreSQL for data persistence. My experience aligns perfectly with your requirements for FastAPI expertise and database management skills.\n\nI am particularly drawn to this opportunity because of Tech Corp's reputation for technical excellence and innovation. I am eager to bring my skills in Python and FastAPI to help build robust backend solutions.\n\nThank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your team.\n\nBest regards,\n[Your Name]"
}
```

#### Error Responses
```json
// Missing profile
{
  "detail": "Profile is required"
}

// Missing job
{
  "detail": "Job is required"
}

// Generation failure
{
  "detail": "Failed to generate application materials: <error message>"
}
```

**Response Codes:**
- `200 OK`: Successfully generated materials
- `400 Bad Request`: Missing profile or job
- `500 Internal Server Error`: Generation failed

---

### 6. Assist Apply

Get application URL and step-by-step instructions for manual submission.

#### Request
```http
POST /apply/assist
Content-Type: application/json

{
  "job_title": "Backend Developer",
  "company_name": "Tech Corp",
  "redirect_url": "https://techcorp.com/jobs/apply/backend-developer"
}
```

> **Note:** The endpoint also accepts `job_apply_link` or `url` as the application URL field.

#### cURL Example
```bash
curl -X POST http://localhost:8000/apply/assist \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Backend Developer",
    "company_name": "Tech Corp",
    "redirect_url": "https://techcorp.com/jobs/apply/123"
  }'
```

#### Response
```json
{
  "message": "Ready to assist with application",
  "instructions": [
    "1. Review and edit your generated resume and cover letter",
    "2. Click the link below to open the job application page",
    "3. Fill in the application form manually",
    "4. Upload your tailored resume and cover letter",
    "5. Submit the application when ready"
  ],
  "apply_url": "https://techcorp.com/jobs/apply/backend-developer",
  "job_title": "Backend Developer",
  "company": "Tech Corp",
  "warning": "⚠️ You must complete and submit the application manually. No credentials are stored or auto-filled."
}
```

#### Error Response
```json
{
  "detail": "Job does not have a valid application URL"
}
```

**Response Codes:**
- `200 OK`: Successfully retrieved assist information
- `400 Bad Request`: Missing or invalid application URL

---

## Complete Workflow Example

### Step 1: Extract Profile
```bash
curl -X POST http://localhost:8000/profile/extract \
  -F "file=@my_resume.pdf" \
  > profile.json
```

### Step 2: Find Jobs
```bash
curl -X POST "http://localhost:8000/jobs/all?page=1&size=10" \
  -H "Content-Type: application/json" \
  -d @profile.json \
  > jobs.json
```

### Step 3: Select a Job and Prepare Application
```bash
# Create payload with profile and selected job
cat > prepare_request.json << EOF
{
  "profile": $(cat profile.json),
  "job": {
    "job_title": "Backend Engineer",
    "company_name": "Tech Corp",
    "job_description": "...",
    "job_requirements": "..."
  }
}
EOF

curl -X POST http://localhost:8000/apply/prepare \
  -H "Content-Type: application/json" \
  -d @prepare_request.json \
  > application_materials.json
```

### Step 4: Get Application Instructions
```bash
curl -X POST http://localhost:8000/apply/assist \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Backend Engineer",
    "company_name": "Tech Corp",
    "redirect_url": "https://techcorp.com/apply"
  }' \
  > assist_info.json
```

---

## Additional Endpoints

### Search Jobs
```http
POST /jobs/search
```
Generates search queries and fetches jobs from multiple sources.

### Match Jobs
```http
POST /jobs/match
```
Performs vector-based matching and ranking without pagination.

### Explain Jobs
```http
POST /jobs/explain
```
Returns top matches with AI-generated explanations.

### Find and Match (All-in-One)
```http
POST /jobs/find_and_match
```
Combines search, match, rank, and explain in one request.

For detailed documentation of these endpoints, visit:
```
http://localhost:8000/docs
```

---

## Rate Limits

Currently no rate limits. For production:
- Recommended: 100 requests/minute per IP
- Burst: 20 requests/second

---

## Best Practices

### 1. Profile Extraction
- Support PDF, DOCX, and TXT formats
- Maximum file size: 10MB
- Ensure resume has clear structure

### 2. Pagination
- Use reasonable page sizes (10-50)
- Cache results when possible
- Don't fetch all jobs at once

### 3. Application Preparation
- Always review generated materials before use
- Edit to add personal touches
- Verify all information is accurate

### 4. Error Handling
```javascript
try {
  const response = await fetch('/jobs/all', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile)
  });
  
  if (!response.ok) {
    const error = await response.json();
    console.error('API Error:', error.detail);
  }
  
  const data = await response.json();
  // Process data
} catch (error) {
  console.error('Network Error:', error);
}
```

---

## WebSocket Support

Not yet implemented. Future feature for real-time job updates.

---

## Webhooks

Not yet implemented. Future feature for:
- New job matches
- Application status updates
- Profile change notifications

---

## API Versions

Current version: `v1.0.0`

Future versions will be available at:
```
/v2/jobs/all
```

---

## Support

- **Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Issues**: GitHub Issues
- **Email**: support@example.com

---

Last Updated: 2026-01-28
