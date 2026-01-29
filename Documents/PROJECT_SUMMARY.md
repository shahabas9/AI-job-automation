# AI Job Hunter - Project Summary

## 🎯 Project Overview

**AI Job Hunter** is a production-ready backend system that helps job seekers find relevant opportunities and prepare tailored application materials using AI.

### Key Differentiator
✅ **Assisted, NOT Automated** - Maintains user control and compliance with job platforms' terms of service.

---

## ✨ Features

### 1. Smart Profile Extraction
- Upload resume (PDF/DOCX/TXT)
- AI extracts structured profile
- Identifies skills, experience, seniority

### 2. Intelligent Job Matching
- Vector-based semantic search
- Rule-based ranking
- Fetches from multiple sources (Adzuna, JSearch)
- Pagination support for large result sets

### 3. AI Explainability
- Clear explanations for each match
- Factual, non-exaggerated reasoning
- Transparency in recommendations

### 4. Application Preparation
- Job-specific resume generation
- Personalized cover letters
- Editable, ATS-friendly format

### 5. Assisted Apply
- Safe, compliant workflow
- No auto-submission
- No credential storage
- User maintains full control

---

## 🏗️ Architecture

```
┌─────────────┐
│   Resume    │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Profile Extraction  │ ◄── AI Agent #1
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Job Fetching      │ ◄── Multiple APIs
│ (Adzuna, JSearch)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Embedding + Store  │ ◄── Vector DB (Qdrant)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Vector Search      │ ◄── Semantic Matching
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Ranking Engine     │ ◄── AI + Rules
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Explainability     │ ◄── AI Agent #2
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Document Generation │ ◄── AI Agents #3, #4
│ (Resume + Cover)    │
└─────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI |
| **Language** | Python 3.10+ (Async) |
| **AI/LLM** | OpenAI SDK / Ollama |
| **Vector DB** | Qdrant |
| **Job Sources** | Adzuna, JSearch APIs |
| **Validation** | Pydantic |
| **Testing** | Pytest |

---

## 📡 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/profile/extract` | Extract profile from resume |
| `POST` | `/jobs/all` | Get all jobs (paginated) |
| `POST` | `/apply/prepare` | Generate resume + cover letter |
| `POST` | `/apply/assist` | Get application instructions |

### Additional Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/` | API information |
| `POST` | `/jobs/search` | Search and fetch jobs |
| `POST` | `/jobs/match` | Match and rank jobs |
| `POST` | `/jobs/explain` | Get explanations |

---

## 🤖 AI Agents

### 1. Profile Extraction Agent
**Purpose:** Extract structured data from resumes  
**Input:** Raw resume text  
**Output:** JSON with role, skills, experience, etc.

### 2. Job Search Planning Agent
**Purpose:** Generate optimal search queries  
**Input:** User profile  
**Output:** Search queries for job APIs

### 3. Explanation Agent
**Purpose:** Explain why jobs match  
**Input:** Profile + job  
**Output:** Clear, factual explanation

### 4. Resume Tailoring Agent
**Purpose:** Generate job-specific resumes  
**Input:** Profile + job description  
**Output:** Tailored resume text

### 5. Cover Letter Agent
**Purpose:** Write personalized cover letters  
**Input:** Profile + job description  
**Output:** Compelling cover letter

---

## 📊 Data Flow

```
User Resume
    ↓
Profile JSON
    ↓
Search Queries → Job APIs → Raw Jobs
    ↓
Embeddings → Qdrant (Vector Storage)
    ↓
Query Vector → Similar Jobs (top_k=500)
    ↓
Ranking Algorithm → Sorted Jobs
    ↓
Pagination → User gets page 1,2,3...
    ↓
Selected Job + Profile → AI Agents
    ↓
Resume + Cover Letter → User Reviews
    ↓
Apply URL → User Submits Manually
```

---

## 🔒 Security & Compliance

### What We DO
✅ Extract and analyze resumes  
✅ Match jobs using AI  
✅ Generate application documents  
✅ Provide application URLs  

### What We DON'T DO
❌ Auto-submit applications  
❌ Store credentials  
❌ Bypass CAPTCHAs  
❌ Scrape protected sites  

### Compliance
- GDPR-ready (user data control)
- Respects job boards' ToS
- No automated form submission
- Transparent AI explanations

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start Qdrant
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 4. Start Server
```bash
./start.sh
# Or: uvicorn main:app --reload
```

### 5. Test API
```bash
./test_api.sh
# Or: curl http://localhost:8000/health
```

---

## 📈 Performance

### Benchmarks (Expected)
- Profile extraction: ~2-5 seconds
- Job search + match: ~3-10 seconds
- Resume generation: ~5-10 seconds
- Cover letter: ~5-8 seconds

### Scalability
- **Vector DB**: Handles millions of jobs
- **Stateless**: Easy horizontal scaling
- **Async**: High concurrent request handling
- **Pagination**: Efficient large result sets

---

## 🧪 Testing

### Run Tests
```bash
pytest tests/test_main.py -v
```

### Test Coverage
- Health checks
- Profile extraction
- Pagination logic
- Application preparation
- Error handling
- Security (basic)

---

## 📦 Project Structure

```
job_hunting/
├── agent/                    # AI Agents
│   ├── profile_extractor.py
│   ├── job_search.py
│   ├── job_explanation.py
│   ├── resume_tailoring.py
│   └── cover_letter.py
├── services/                 # External services
│   ├── embedding_service.py
│   ├── qdrant_service.py
│   ├── job_fetcher.py
│   └── ...
├── pipeline/                 # Processing pipelines
│   ├── match_pipeline.py
│   ├── rank_pipeline.py
│   └── ...
├── utils/                    # Utilities
├── tests/                    # Test suite
├── examples/                 # Example payloads
├── main.py                   # FastAPI app
├── requirements.txt
├── .env
├── README.md
├── API.md
├── DEPLOYMENT.md
└── start.sh
```

---

## 🛣️ Roadmap

### Phase 1: ✅ Core Features (DONE)
- [x] Profile extraction
- [x] Job matching with pagination
- [x] Resume & cover letter generation
- [x] Assisted apply workflow

### Phase 2: 🚧 Enhancements (Next)
- [ ] LinkedIn job integration
- [ ] Multiple resume versions
- [ ] Application tracking (user-managed)
- [ ] Email notifications

### Phase 3: 🔮 Future
- [ ] Browser extension
- [ ] Mobile app integration
- [ ] Analytics dashboard
- [ ] A/B testing for documents

---

## 📚 Documentation

- **README.md** - Getting started guide
- **API.md** - Detailed API documentation
- **DEPLOYMENT.md** - Production deployment guide
- **This file** - Project summary

---

## 🤝 Contributing

Contributions welcome! Please:
1. Maintain the assisted workflow principle
2. Add tests for new features
3. Update documentation
4. Follow existing code style

---

## 📝 License

MIT License - See LICENSE file

---

## 📧 Support

- **Docs**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **API Docs**: See API.md

---

## 🎓 Use Cases

### For Job Seekers
- Upload resume once
- Get personalized job matches
- Generate tailored application materials
- Apply to multiple jobs efficiently

### For Career Coaches
- Help clients find suitable roles
- Generate multiple resume versions
- Track application progress
- Provide data-driven advice

### For Technical Recruiters
- Match candidates to roles
- Generate position descriptions
- Identify skill gaps
- Streamline candidate screening

---

## 💡 Key Insights

### Why Vector Search?
- Semantic understanding beyond keyword matching
- Finds relevant jobs even with different terminology
- Handles synonyms and related concepts

### Why Assisted (Not Automated)?
- Legal compliance with job platforms
- Better user control and customization
- Higher quality applications
- Ethical AI practices

### Why Multiple Agents?
- Specialized AI for each task
- Better prompt engineering
- Easier to test and improve
- Modular architecture

---

**Built with ❤️ for job seekers everywhere**

Last Updated: 2026-01-28
