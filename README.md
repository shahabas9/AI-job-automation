# AI Job Hunter - Backend API

A production-ready backend system for intelligent job matching and assisted application submission.

## 🎯 Features

- **Smart Profile Extraction**: AI-powered resume parsing to extract structured candidate profiles
- **Intelligent Job Matching**: Vector-based semantic search with Qdrant for finding relevant jobs
- **Advanced Ranking**: Combines semantic similarity with rule-based scoring
- **AI Explainability**: Clear explanations for why each job matches your profile
- **Tailored Documents**: Generate job-specific resumes and cover letters
- **Safe Application Workflow**: Assisted (not automated) application process - fully compliant

## 🏗️ Architecture

```
Resume → Profile Extraction → Job Fetching → Embedding + Vector Search 
    → Ranking → Explainability → Application Preparation
```

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **AI/LLM**: OpenAI SDK / Ollama
- **Vector DB**: Qdrant
- **Async**: Python AsyncIO
- **Job Sources**: Adzuna, JSearch APIs

## 📋 Prerequisites

- Python 3.10+
- Ollama running locally (or OpenAI API key)
- Qdrant instance (local or cloud)
- API keys for job sources (Adzuna, RapidAPI)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create or update `.env` file:

```env
MODEL_NAME=qwen3-coder:480b-cloud
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama
EMBED_MODEL_NAME=nomic-embed-text

# Job API Keys
RAPIDAPI_KEY=your_rapidapi_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_API_KEY=your_adzuna_api_key

# Optional: OpenAI (if not using Ollama)
OPENAI_API_KEY=your_openai_key
```

### 3. Start Qdrant (if running locally)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 4. Run the API

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### 1️⃣ **Profile Extraction**

Extract structured profile from resume.

```http
POST /profile/extract
Content-Type: multipart/form-data

file: <resume.pdf|.docx|.txt>
```

**Response:**
```json
{
  "primary_role": "Software Engineer",
  "skills": ["Python", "FastAPI", "React"],
  "experience_years": 3,
  "seniority": "mid",
  "preferred_locations": ["San Francisco", "Remote"],
  "job_type": "full-time",
  "confidence_score": 0.95
}
```

---

### 2️⃣ **Get All Jobs (Paginated)**

Fetch and rank all relevant jobs with pagination.

```http
POST /jobs/all?page=1&size=20
Content-Type: application/json

{
  "primary_role": "Software Engineer",
  "skills": ["Python", "FastAPI"],
  "experience_years": 3,
  "seniority": "mid"
}
```

**Query Parameters:**
- `page` (default: 1) - Page number (1-indexed)
- `size` (default: 20, max: 100) - Items per page

**Response:**
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
        "location": "San Francisco",
        "job_description": "...",
        "salary_min": 120000,
        "salary_max": 180000
      },
      "explanation": null
    }
  ]
}
```

---

### 3️⃣ **Prepare Application**

Generate job-specific resume and cover letter.

```http
POST /apply/prepare
Content-Type: application/json

{
  "profile": {
    "primary_role": "Software Engineer",
    "skills": ["Python", "FastAPI"],
    "experience_years": 3
  },
  "job": {
    "job_title": "Backend Developer",
    "company_name": "Tech Corp",
    "job_description": "We're looking for...",
    "job_requirements": "3+ years Python..."
  }
}
```

**Response:**
```json
{
  "resume_text": "PROFESSIONAL SUMMARY\nExperienced Software Engineer...",
  "cover_letter_text": "Dear Hiring Manager,\nI am excited to apply..."
}
```

---

### 4️⃣ **Assist Apply**

Get application URL and instructions (NO auto-submission).

```http
POST /apply/assist
Content-Type: application/json

{
  "job_title": "Backend Developer",
  "company_name": "Tech Corp",
  "redirect_url": "https://example.com/jobs/apply/123"
}
```

**Response:**
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
  "apply_url": "https://example.com/jobs/apply/123",
  "job_title": "Backend Developer",
  "company": "Tech Corp",
  "warning": "⚠️ You must complete and submit the application manually."
}
```

---

### Other Endpoints

- **POST /jobs/search** - Generate job search queries and fetch jobs
- **POST /jobs/match** - Match jobs using vector search
- **POST /jobs/explain** - Get explanations for top matches
- **POST /jobs/find_and_match** - Combined search, match, and explain
- **GET /health** - Health check
- **GET /** - API info and documentation

## 🤖 AI Agents

### 1. Profile Extraction Agent
Analyzes resumes and extracts structured profiles.

### 2. Job Search Planning Agent
Generates optimized search queries based on candidate profile.

### 3. Explanation Agent
Provides clear, factual explanations for job matches.

### 4. Resume Tailoring Agent
Generates job-specific resumes highlighting relevant skills.

### 5. Cover Letter Agent
Creates personalized, compelling cover letters.

## 🔒 Security & Compliance

### IMPORTANT CONSTRAINTS

✅ **We DO:**
- Assist users with job applications
- Generate personalized documents
- Provide application URLs and instructions

❌ **We DON'T:**
- Auto-submit applications
- Store user credentials
- Bypass CAPTCHAs
- Scrape protected job sites
- Fill forms automatically

This is an **assisted workflow**, not automation. Users maintain full control.

## 📊 System Design Principles

- **Stateless**: No session management required
- **Scalable**: Async operations throughout
- **Production-ready**: Error handling, validation, logging
- **Explainable**: Every match has a clear reason
- **Compliant**: Respects ToS and privacy laws

## 🧪 Testing

### Test Profile Extraction
```bash
curl -X POST http://localhost:8000/profile/extract \
  -F "file=@resume.pdf"
```

### Test Job Matching
```bash
curl -X POST http://localhost:8000/jobs/all?page=1&size=10 \
  -H "Content-Type: application/json" \
  -d '{"primary_role": "Software Engineer", "skills": ["Python"]}'
```

### Test Application Preparation
```bash
curl -X POST http://localhost:8000/apply/prepare \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

## 📈 Performance Considerations

- **Vector Search**: Top-k limited to 500 for pagination endpoint
- **Batch Processing**: Job embedding happens in batches
- **Async Operations**: All AI calls are async for better throughput
- **Caching**: Consider adding Redis for frequently accessed profiles

## 🛣️ Roadmap

- [ ] Add support for LinkedIn job search
- [ ] Implement job change tracking
- [ ] Add application status tracking (user-managed)
- [ ] Support for multiple resume versions
- [ ] A/B testing for cover letter variations
- [ ] Analytics dashboard

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please ensure all changes:
1. Maintain the assisted (not automated) workflow
2. Include proper error handling
3. Add tests for new features
4. Update documentation

## 📧 Support

For issues or questions, please open a GitHub issue.

---

**Built with ❤️ for job seekers everywhere**
