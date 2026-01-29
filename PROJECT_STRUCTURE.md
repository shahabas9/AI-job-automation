# Project Structure

## Directory Overview

```
job_hunting/
├── 📁 agent/                    # AI Agents
│   ├── __init__.py
│   ├── profile_extractor.py     # Profile extraction agent
│   ├── job_search.py            # Job search planning agent
│   ├── job_explanation.py       # Match explanation agent
│   ├── resume_tailoring.py      # ⭐ Resume generation agent (NEW)
│   └── cover_letter.py          # ⭐ Cover letter agent (NEW)
│
├── 📁 services/                 # External services
│   ├── embedding_service.py     # Text embedding service
│   ├── qdrant_service.py        # Vector database service
│   ├── job_fetcher.py           # Multi-source job fetcher
│   ├── job_fetcher_adzuna.py    # Adzuna API integration
│   └── job_fetcher_jsearch.py   # JSearch API integration
│
├── 📁 pipeline/                 # Processing pipelines
│   ├── profile_pipeline.py      # Profile extraction pipeline
│   ├── job_search_pipeline.py   # Job search pipeline
│   ├── job_fetch_pipeline.py    # Job fetching pipeline
│   ├── embed_pipeline.py        # Embedding pipeline
│   ├── match_pipeline.py        # Job matching pipeline
│   └── rank_pipeline.py         # Job ranking pipeline
│
├── 📁 utils/                    # Utility functions
│   ├── __init__.py
│   ├── file_processing.py       # File handling (PDF/DOCX/TXT)
│   └── text_builders.py         # Text formatting utilities
│
├── 📁 parser/                   # Data parsers
│   ├── __init__.py
│   └── parse_resume.py          # Resume parsing logic
│
├── 📁 tests/                    # ⭐ Test suite (NEW)
│   ├── __init__.py
│   └── test_main.py             # Comprehensive API tests
│
├── 📁 examples/                 # ⭐ Example payloads (NEW)
│   ├── test_profile.json        # Sample profile
│   └── test_prepare_application.json  # Sample application request
│
├── 📁 data/                     # Data storage
│   └── (generated files)
│
├── 📁 frontend/                 # Frontend application
│   └── (existing frontend code)
│
├── 📁 .agent/                   # Agent workflows
│   └── workflows/
│       └── implementation-plan.md
│
├── 📄 main.py                   # ⭐ FastAPI application (UPDATED)
├── 📄 requirements.txt          # ⭐ Python dependencies (UPDATED)
├── 📄 .env                      # Environment variables
├── 📄 .gitignore               # Git ignore rules
│
├── 📄 start.sh                  # ⭐ Startup script (NEW)
├── 📄 test_api.sh              # ⭐ API testing script (NEW)
├── 📄 test_fetch_jobs.py       # Job fetching test
│
└── 📚 Documentation             # ⭐ All documentation (NEW)
    ├── README.md                # Project overview
    ├── QUICKSTART.md            # Quick start guide
    ├── API.md                   # API documentation
    ├── ARCHITECTURE.md          # System architecture
    ├── DEPLOYMENT.md            # Deployment guide
    ├── PROJECT_SUMMARY.md       # Quick reference
    └── COMPLETION_SUMMARY.md    # Implementation summary
```

---

## Files by Category

### 🎯 Core Application

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `main.py` | FastAPI application with all endpoints | ~450 | ✅ Updated |
| `requirements.txt` | Python dependencies | ~15 | ✅ Updated |
| `.env` | Environment configuration | ~10 | ✅ Existing |

### 🤖 AI Agents (5 total)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `agent/profile_extractor.py` | Extract profile from resume | ~40 | ✅ Existing |
| `agent/job_search.py` | Generate job search queries | ~30 | ✅ Existing |
| `agent/job_explanation.py` | Explain job matches | ~70 | ✅ Existing |
| `agent/resume_tailoring.py` | Generate job-specific resume | ~110 | ⭐ NEW |
| `agent/cover_letter.py` | Generate personalized cover letter | ~110 | ⭐ NEW |

### 🔧 Services (5 total)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `services/embedding_service.py` | Text embedding | ~15 | ✅ Existing |
| `services/qdrant_service.py` | Vector database operations | ~50 | ✅ Existing |
| `services/job_fetcher.py` | Multi-source fetching | ~20 | ✅ Existing |
| `services/job_fetcher_adzuna.py` | Adzuna integration | ~60 | ✅ Existing |
| `services/job_fetcher_jsearch.py` | JSearch integration | ~55 | ✅ Existing |

### 🔄 Pipelines (6 total)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `pipeline/profile_pipeline.py` | Profile extraction flow | ~15 | ✅ Existing |
| `pipeline/job_search_pipeline.py` | Search planning flow | ~10 | ✅ Existing |
| `pipeline/job_fetch_pipeline.py` | Job fetching flow | ~15 | ✅ Existing |
| `pipeline/embed_pipeline.py` | Embedding flow | ~25 | ✅ Existing |
| `pipeline/match_pipeline.py` | Job matching flow | ~25 | ✅ Existing |
| `pipeline/rank_pipeline.py` | Job ranking flow | ~60 | ✅ Existing |

### 🛠️ Utilities (3 files)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `utils/file_processing.py` | File handling | ~50 | ✅ Existing |
| `utils/text_builders.py` | Text formatting | ~30 | ✅ Existing |
| `parser/parse_resume.py` | Resume parsing | ~40 | ✅ Existing |

### 🧪 Testing (2 files)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `tests/test_main.py` | Comprehensive test suite | ~240 | ⭐ NEW |
| `test_fetch_jobs.py` | Job fetching tests | ~150 | ✅ Existing |

### 📚 Documentation (7 files)

| File | Purpose | Pages | Status |
|------|---------|-------|--------|
| `README.md` | Project overview | 7 | ⭐ NEW |
| `QUICKSTART.md` | Quick start guide | 8 | ⭐ NEW |
| `API.md` | API documentation | 11 | ⭐ NEW |
| `ARCHITECTURE.md` | System architecture | 19 | ⭐ NEW |
| `DEPLOYMENT.md` | Deployment guide | 9 | ⭐ NEW |
| `PROJECT_SUMMARY.md` | Quick reference | 10 | ⭐ NEW |
| `COMPLETION_SUMMARY.md` | Implementation summary | 8 | ⭐ NEW |

### 🚀 Scripts (3 files)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `start.sh` | Server startup script | ~40 | ⭐ NEW |
| `test_api.sh` | API testing script | ~50 | ⭐ NEW |
| `.gitignore` | Git ignore rules | ~140 | ✅ Existing |

### 📋 Examples (2 files)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `examples/test_profile.json` | Sample profile | ~12 | ⭐ NEW |
| `examples/test_prepare_application.json` | Sample request | ~20 | ⭐ NEW |

---

## API Endpoints (10 total)

### Profile Management
```
POST   /profile/extract          Extract profile from resume
```

### Job Operations
```
POST   /jobs/all                 Get all jobs (paginated) ⭐ NEW
POST   /jobs/search              Search and fetch jobs
POST   /jobs/match               Match and rank jobs
POST   /jobs/explain             Get AI explanations
POST   /jobs/find_and_match      Combined workflow
```

### Application Operations
```
POST   /apply/prepare            Generate resume + cover letter ⭐ NEW
POST   /apply/assist             Get application assistance ⭐ NEW
```

### Utility
```
GET    /health                   Health check
GET    /                         API information
```

---

## Code Statistics

### Total Implementation

```
Total Files:              50+
Total Lines of Code:      ~3,500
Python Files:             25
Documentation Pages:      7
Test Files:               2
Configuration Files:      4
Scripts:                  3
```

### By Component

```
AI Agents:                5 files   (~360 lines)
Services:                 5 files   (~200 lines)
Pipelines:                6 files   (~150 lines)
API Endpoints:            1 file    (~450 lines)
Tests:                    1 file    (~240 lines)
Documentation:            7 files   (~3,500 lines)
Utilities:                3 files   (~120 lines)
```

---

## What's New (This Implementation)

### Files Created
```
✨ agent/resume_tailoring.py
✨ agent/cover_letter.py
✨ tests/test_main.py
✨ tests/__init__.py
✨ examples/test_profile.json
✨ examples/test_prepare_application.json
✨ start.sh
✨ test_api.sh
✨ README.md
✨ QUICKSTART.md
✨ API.md
✨ ARCHITECTURE.md
✨ DEPLOYMENT.md
✨ PROJECT_SUMMARY.md
✨ COMPLETION_SUMMARY.md
```

### Files Updated
```
🔄 main.py                       (Added 3 new endpoints + models)
🔄 requirements.txt              (Added FastAPI, pytest, etc.)
🔄 .agent/workflows/implementation-plan.md
```

---

## Dependencies

### Core Dependencies
```
fastapi==0.115.6                 Web framework
uvicorn==0.34.0                  ASGI server
pydantic==2.10.6                 Data validation
python-multipart==0.0.20         File uploads
httpx==0.28.1                    Async HTTP client
```

### AI & ML
```
openai==1.85.0                   AI/LLM SDK
openai-agents==0.0.17            Agent framework
qdrant-client==1.16.2            Vector database
```

### Testing
```
pytest==8.3.4                    Testing framework
pytest-asyncio==0.24.0           Async test support
```

### Utilities
```
pdfplumber                       PDF parsing
python-dotenv==1.1.0            Environment variables
```

---

## Integration Points

### External Services
```
🔌 Ollama / OpenAI              → LLM inference
🔌 Qdrant                       → Vector storage
🔌 Adzuna API                   → Job data
🔌 JSearch (RapidAPI)           → Job data
```

### Internal Modules
```
📦 agent       ←→ services      (AI uses services)
📦 services    ←→ pipeline      (Services in pipelines)
📦 pipeline    ←→ main.py       (Pipelines in API)
📦 utils       ←→ everywhere    (Shared utilities)
```

---

## Key Directories

### `/agent` - AI Intelligence
The brain of the application. Contains all AI agents that use LLMs to process data.

### `/services` - External Integrations
Handles communication with external APIs and databases.

### `/pipeline` - Business Logic
Orchestrates workflows by combining agents and services.

### `/tests` - Quality Assurance
Ensures everything works as expected.

### `/examples` - Developer Tools
Sample data for testing and development.

---

## File Naming Conventions

```
Main modules:         snake_case.py
Test files:           test_*.py
Scripts:              *.sh
Documentation:        UPPERCASE.md
Examples:             test_*.json
Config:               .env, .gitignore
```

---

## Quick Navigation

**Want to:**
- Understand the system? → Read `ARCHITECTURE.md`
- Get started quickly? → Read `QUICKSTART.md`
- See API details? → Read `API.md`
- Deploy to production? → Read `DEPLOYMENT.md`
- Understand features? → Read `README.md`
- Check completion? → Read `COMPLETION_SUMMARY.md`

---

Last Updated: 2026-01-28
