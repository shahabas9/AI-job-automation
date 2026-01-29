# AI Job Hunter - System Architecture

## Overview

This document provides a detailed technical architecture of the AI Job Hunter backend system.

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                              │
│  (Web App, Mobile App, CLI, or Direct API consumers)             │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ HTTP/JSON
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                      FASTAPI APPLICATION                          │
│                         (main.py)                                 │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │   Profile      │  │    Jobs        │  │    Apply       │    │
│  │   Endpoints    │  │   Endpoints    │  │   Endpoints    │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└────────────┬──────────────────┬───────────────────┬─────────────┘
             │                  │                   │
             ▼                  ▼                   ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   AI AGENTS      │  │   PIPELINES      │  │    SERVICES      │
│                  │  │                  │  │                  │
│ • Profile        │  │ • Match          │  │ • Embedding      │
│   Extractor      │  │ • Rank           │  │ • Qdrant         │
│ • Job Search     │  │ • Embed          │  │ • Job Fetcher    │
│ • Explanation    │  │                  │  │                  │
│ • Resume         │  │                  │  │                  │
│ • Cover Letter   │  │                  │  │                  │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                      │
         ▼                     ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│    LLM LAYER     │  │   VECTOR DB      │  │   JOB APIs       │
│                  │  │                  │  │                  │
│ • Ollama         │  │ • Qdrant         │  │ • Adzuna         │
│ • OpenAI         │  │   (localhost or  │  │ • JSearch        │
│                  │  │    cloud)        │  │   (RapidAPI)     │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## Detailed Component Architecture

### 1. API Layer (FastAPI)

```python
FastAPI Application
├── Middleware
│   ├── CORS
│   └── Error Handling
│
├── Endpoints
│   ├── /profile/extract
│   ├── /jobs/all (paginated)
│   ├── /jobs/search
│   ├── /jobs/match
│   ├── /jobs/explain
│   ├── /apply/prepare
│   └── /apply/assist
│
└── Models (Pydantic)
    ├── JobResponse
    ├── JobsAllResponse
    ├── ApplicationPackage
    └── PrepareApplicationRequest
```

### 2. AI Agents Layer

```
AI Agents Architecture
│
├── Base: OpenAI Agents SDK
│   └── model: Ollama or OpenAI
│
├── Profile Extractor
│   ├── Input: Resume text
│   ├── Output: Structured JSON
│   └── Fields: role, skills, experience, etc.
│
├── Job Search Planner
│   ├── Input: Profile JSON
│   ├── Output: Search queries
│   └── Logic: Primary + secondary roles
│
├── Explanation Generator
│   ├── Input: Profile + Job
│   ├── Output: Match explanation
│   └── Style: Factual, concise, clear
│
├── Resume Tailor
│   ├── Input: Profile + Job description
│   ├── Output: Job-specific resume
│   └── Features: ATS-friendly, keyword-optimized
│
└── Cover Letter Writer
    ├── Input: Profile + Job description
    ├── Output: Personalized letter
    └── Features: Professional, compelling, concise
```

### 3. Pipeline Layer

```
Processing Pipelines
│
├── Profile Pipeline
│   └── resume → text extraction → AI agent → profile JSON
│
├── Match Pipeline
│   └── profile → embedding → vector search → matched jobs
│
├── Rank Pipeline
│   └── matched jobs → semantic + rule scores → ranked list
│
└── Embed Pipeline
    └── job data → text format → embedding → vector storage
```

### 4. Services Layer

```
External Services
│
├── Embedding Service
│   ├── Model: nomic-embed-text
│   ├── Dimension: 768
│   └── Client: AsyncOpenAI (Ollama)
│
├── Qdrant Service
│   ├── Collection: "jobs"
│   ├── Vector size: 768
│   └── Operations: upsert, search
│
├── Job Fetcher Service
│   ├── Adzuna API
│   │   ├── App ID + API Key
│   │   └── Multiple locations
│   │
│   └── JSearch (RapidAPI)
│       ├── RapidAPI Key
│       └── Global search
│
└── File Processing
    └── Formats: PDF, DOCX, TXT
```

---

## Data Flow Diagrams

### Flow 1: Profile Extraction

```
┌─────────┐     ┌─────────────┐     ┌──────────────┐     ┌─────────┐
│ Upload  │────▶│   Extract   │────▶│  AI Agent    │────▶│ Profile │
│ Resume  │     │    Text     │     │  (LLM call)  │     │  JSON   │
└─────────┘     └─────────────┘     └──────────────┘     └─────────┘
   (PDF)          (pdfplumber)       (Profile Agent)      (validated)
```

### Flow 2: Job Matching (with Pagination)

```
┌─────────┐     ┌─────────────┐     ┌──────────────┐
│ Profile │────▶│  Generate   │────▶│  Fetch Jobs  │
│  JSON   │     │   Queries   │     │  from APIs   │
└─────────┘     └─────────────┘     └──────┬───────┘
                  (Search Agent)            │
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │    Embed     │
                                    │   & Store    │
                                    └──────┬───────┘
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │   Vector     │
                                    │   Search     │
                                    └──────┬───────┘
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │    Rank      │
                                    │    Jobs      │
                                    └──────┬───────┘
                                           │
                                           ▼
                                    ┌──────────────┐
┌──────────┐                        │   Paginate   │     ┌──────────┐
│  Client  │◀───────────────────────│   Results    │────▶│  Return  │
│ (page=1) │   Jobs 1-20            └──────────────┘     │  JSON    │
└──────────┘                                              └──────────┘
```

### Flow 3: Application Preparation

```
┌─────────┐     ┌─────────────────┐     ┌──────────────┐     ┌─────────┐
│ Profile │────▶│  Resume Tailor  │────▶│   Resume     │────▶│   API   │
│   +     │     │     Agent       │     │    Text      │     │Response │
│  Job    │     └─────────────────┘     └──────────────┘     │         │
└────┬────┘                                                   │         │
     │         ┌─────────────────┐     ┌──────────────┐     │         │
     └────────▶│ Cover Letter    │────▶│ Cover Letter │────▶│         │
               │     Agent       │     │    Text      │     └─────────┘
               └─────────────────┘     └──────────────┘
```

---

## Technology Stack Details

### Backend Framework
```yaml
FastAPI:
  version: 0.115.6
  features:
    - Async support
    - Auto OpenAPI docs
    - Pydantic validation
    - Type hints
```

### AI/LLM
```yaml
OpenAI SDK:
  version: 1.85.0
  compatible_with:
    - OpenAI API
    - Ollama (local)
  
OpenAI Agents:
  version: 0.0.17
  features:
    - Agent framework
    - Tool calling
    - Context management
```

### Vector Database
```yaml
Qdrant:
  client_version: 1.16.2
  features:
    - Fast vector search
    - Filtering support
    - Payload storage
  deployment:
    - Docker (local)
    - Qdrant Cloud
```

### Job APIs
```yaml
Adzuna:
  type: Job search API
  authentication: App ID + Key
  rate_limit: Variable

JSearch (RapidAPI):
  type: Job aggregator
  authentication: RapidAPI Key
  coverage: Global
```

---

## Security Architecture

### Authentication (Future)
```
┌─────────┐     ┌─────────────┐     ┌──────────────┐
│ Client  │────▶│  API Key    │────▶│   Validate   │
│ Request │     │   Header    │     │     Key      │
└─────────┘     └─────────────┘     └──────┬───────┘
                                            │
                                     ┌──────▼───────┐
                                     │   Process    │
                                     │   Request    │
                                     └──────────────┘
```

### Data Privacy
```
User Resume ──┬──▶ Extract Profile ──▶ Store Profile (temporary)
              │
              └──▶ Discard Original ──▶ No long-term storage
```

### Compliance Controls
```
Application Flow:
┌─────────────────┐
│ Generate Docs   │ ✅ AI-generated
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ User Reviews    │ ✅ User control
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Provide URL     │ ✅ No auto-submit
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ User Applies    │ ✅ Manual submission
└─────────────────┘
```

---

## Scaling Strategy

### Horizontal Scaling
```
                    ┌──────────────┐
                    │ Load Balancer│
                    └───────┬──────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
    ┌────────┐         ┌────────┐         ┌────────┐
    │API     │         │API     │         │API     │
    │Instance│         │Instance│         │Instance│
    │   #1   │         │   #2   │         │   #3   │
    └────┬───┘         └────┬───┘         └────┬───┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   Shared    │
                     │   Qdrant    │
                     └─────────────┘
```

### Caching Layer (Future)
```
Request ──▶ Redis Cache ──┬──▶ Hit: Return cached
                          │
                          └──▶ Miss: Query DB ──▶ Cache result
```

---

## Monitoring Architecture

### Metrics Collection
```
Application
    │
    ├──▶ Prometheus Metrics
    │       └──▶ Grafana Dashboard
    │
    ├──▶ Application Logs
    │       └──▶ CloudWatch / Elasticsearch
    │
    └──▶ Error Tracking
            └──▶ Sentry
```

### Key Metrics
```yaml
Performance:
  - Request rate (req/s)
  - Response time (p50, p95, p99)
  - Error rate (%)
  
Resources:
  - CPU usage (%)
  - Memory usage (%)
  - Disk I/O
  
Business:
  - Profiles extracted
  - Jobs matched
  - Applications prepared
```

---

## Deployment Architecture

### Docker Deployment
```
┌─────────────────────────────────────────┐
│          Docker Host                     │
│                                          │
│  ┌────────────────┐  ┌────────────────┐│
│  │  API Container │  │ Qdrant Container││
│  │  (FastAPI)     │  │  (Vector DB)    ││
│  │  Port: 8000    │  │  Port: 6333     ││
│  └────────────────┘  └────────────────┘│
│                                          │
│  ┌────────────────┐                     │
│  │ Ollama (opt.)  │                     │
│  │ GPU-enabled    │                     │
│  └────────────────┘                     │
└─────────────────────────────────────────┘
```

### Cloud Deployment (AWS)
```
Internet
    │
    ▼
┌─────────────────┐
│  Route 53 (DNS) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CloudFront     │ (CDN - optional)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   ALB           │ (Load Balancer)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌──────┐  ┌──────┐
│ ECS  │  │ ECS  │  (Containers)
│Task 1│  │Task 2│
└──┬───┘  └──┬───┘
   │         │
   └────┬────┘
        │
        ▼
┌─────────────────┐
│  Qdrant Cloud   │
└─────────────────┘
```

---

## Error Handling Flow

```
Request ──▶ Validation ──┬──▶ Valid: Process
                         │
                         └──▶ Invalid: 400/422
                                    │
                                    ▼
                              Log Error
                                    │
                                    ▼
                              Return Error JSON
```

---

## Future Architecture Enhancements

### Phase 2: Enhancements
```
┌──────────────────┐
│  Current System  │
└────────┬─────────┘
         │
         ├──▶ Add Redis (Caching)
         ├──▶ Add Rate Limiting
         ├──▶ Add API Authentication
         ├──▶ Add WebSocket (Real-time)
         └──▶ Add Message Queue (Background jobs)
```

### Phase 3: Advanced Features
```
┌──────────────────┐
│  Enhanced System │
└────────┬─────────┘
         │
         ├──▶ Application Tracking DB
         ├──▶ Analytics Engine
         ├──▶ Email Service (Notifications)
         ├──▶ Browser Automation (Optional)
         └──▶ Mobile API Optimizations
```

---

**Last Updated**: 2026-01-28
