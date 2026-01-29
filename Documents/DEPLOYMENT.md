# Production Deployment Guide

## Overview
This guide covers deploying the AI Job Hunter backend to production.

## Pre-Deployment Checklist

### 1. Environment Configuration
- [ ] All API keys are set in environment variables (not hardcoded)
- [ ] Database credentials are secure
- [ ] CORS origins are restricted (not `*` in production)
- [ ] Rate limiting is configured
- [ ] Logging is properly configured

### 2. Infrastructure Requirements

#### Compute
- **Minimum**: 2 vCPUs, 4GB RAM
- **Recommended**: 4 vCPUs, 8GB RAM (for handling concurrent requests)

#### Vector Database (Qdrant)
- **Option A**: Qdrant Cloud (recommended for production)
- **Option B**: Self-hosted on separate instance
  - Minimum: 2GB RAM, SSD storage
  - Recommended: 4GB RAM, 50GB SSD

#### LLM Provider
- **Option A**: Ollama (requires GPU for better performance)
  - GPU: NVIDIA with 8GB+ VRAM
  - CPU fallback: Slower but functional
- **Option B**: OpenAI API (recommended for simplicity)
  - No infrastructure required
  - Pay per use

## Deployment Options

### Option 1: Docker Deployment

#### 1.1 Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 1.2 Create docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_NAME=${MODEL_NAME}
      - OLLAMA_BASE_URL=${OLLAMA_BASE_URL}
      - OLLAMA_API_KEY=${OLLAMA_API_KEY}
      - EMBED_MODEL_NAME=${EMBED_MODEL_NAME}
      - RAPIDAPI_KEY=${RAPIDAPI_KEY}
      - ADZUNA_APP_ID=${ADZUNA_APP_ID}
      - ADZUNA_API_KEY=${ADZUNA_API_KEY}
    depends_on:
      - qdrant
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

volumes:
  qdrant_data:
```

#### 1.3 Deploy

```bash
docker-compose up -d
```

### Option 2: Cloud Deployment (AWS/GCP/Azure)

#### AWS (EC2 + ECS)

1. **Create ECR Repository**
```bash
aws ecr create-repository --repository-name ai-job-hunter
```

2. **Build and Push Image**
```bash
docker build -t ai-job-hunter .
docker tag ai-job-hunter:latest <ECR_URL>/ai-job-hunter:latest
docker push <ECR_URL>/ai-job-hunter:latest
```

3. **Create ECS Task Definition**
- Container: Your ECR image
- CPU: 2048 (2 vCPU)
- Memory: 4096 (4GB)
- Port mappings: 8000

4. **Create ECS Service**
- Load Balancer: Application Load Balancer
- Health Check: `/health`
- Auto Scaling: min 2, max 10 instances

#### GCP (Cloud Run)

```bash
gcloud run deploy ai-job-hunter \
  --image gcr.io/YOUR_PROJECT/ai-job-hunter \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --max-instances 10
```

### Option 3: Platform-as-a-Service

#### Railway

1. Connect GitHub repository
2. Add environment variables
3. Deploy automatically on push

#### Render

1. Create new Web Service
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Production Optimizations

### 1. Add Caching Layer

Install Redis:
```bash
pip install redis
```

Add to main.py:
```python
import redis
from functools import lru_cache

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@lru_cache(maxsize=1000)
def get_cached_profile(profile_hash: str):
    # Cache profile lookups
    pass
```

### 2. Add Rate Limiting

Install:
```bash
pip install slowapi
```

Add to main.py:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/jobs/all")
@limiter.limit("10/minute")
async def get_all_jobs(...):
    ...
```

### 3. Add Request Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

### 4. Add Monitoring

#### Using Prometheus + Grafana

```bash
pip install prometheus-fastapi-instrumentator
```

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### 5. Add Error Tracking (Sentry)

```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    traces_sample_rate=1.0,
)
```

## Security Best Practices

### 1. CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://app.yourdomain.com"
    ],  # NOT "*" in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 2. API Key Authentication

```python
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key
```

### 3. HTTPS Only

- Use reverse proxy (nginx) with SSL/TLS
- Force HTTPS redirects
- Use certificates from Let's Encrypt

## Monitoring & Alerts

### Key Metrics to Monitor

1. **Request Rate**: Requests per second
2. **Response Time**: p50, p95, p99 latencies
3. **Error Rate**: 4xx and 5xx responses
4. **Database Performance**: Qdrant query time
5. **LLM Performance**: AI agent response time
6. **Resource Usage**: CPU, Memory, Disk

### Alert Rules

- Response time > 5s for 5 minutes
- Error rate > 5% for 5 minutes
- Memory usage > 90% for 10 minutes
- Qdrant connection failures

## Backup Strategy

### Vector Database (Qdrant)

```bash
# Snapshot Qdrant data
docker exec qdrant qdrant-cli snapshot create

# Backup to S3
aws s3 sync /qdrant/storage s3://your-backup-bucket/qdrant/
```

### Schedule with Cron

```bash
0 2 * * * /usr/local/bin/backup-qdrant.sh
```

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**: Distribute traffic across instances
2. **Stateless Design**: No session storage in app (already implemented)
3. **Shared Vector DB**: All instances connect to same Qdrant
4. **Auto-scaling**: Based on CPU/Memory/Request Count

### Vertical Scaling

- Increase CPU/Memory for single instance
- Better LLM performance with more resources
- Recommended for initial deployment

## Post-Deployment

### 1. Smoke Tests

```bash
# Test health
curl https://api.yourdomain.com/health

# Test profile extraction
curl -X POST https://api.yourdomain.com/profile/extract \
  -F "file=@test_resume.pdf"
```

### 2. Load Testing

```bash
# Install Apache Bench
brew install apache-bench

# Test endpoint
ab -n 100 -c 10 https://api.yourdomain.com/health
```

### 3. Monitor Logs

```bash
# Docker
docker logs -f ai-job-hunter

# Cloud platforms
# Use platform-specific logging tools
```

## Troubleshooting

### Common Issues

1. **Qdrant Connection Failed**
   - Check QDRANT_URL environment variable
   - Verify Qdrant is running and accessible
   - Check firewall rules

2. **LLM Timeout**
   - Increase timeout settings
   - Check Ollama/OpenAI connectivity
   - Monitor API quotas

3. **High Memory Usage**
   - Check for memory leaks
   - Reduce top_k in vector searches
   - Implement pagination properly

4. **Slow Response Times**
   - Add caching layer
   - Optimize database queries
   - Scale horizontally

## Cost Optimization

### LLM Costs

- **Ollama (Self-hosted)**: Infrastructure only (~$50-200/month)
- **OpenAI API**: Pay per token (~$0.01-0.10 per request)

### Recommendations

1. Use Ollama for profile extraction and search (frequent operations)
2. Use OpenAI for resume/cover letter generation (less frequent, quality matters)
3. Cache common queries
4. Batch operations where possible

## Compliance

### Data Privacy

- Don't store user resumes permanently
- Log only anonymized data
- Implement data retention policies
- Add GDPR-compliant data deletion

### Terms of Service

- Respect job board ToS
- Don't auto-submit applications
- Rate limit API calls to third-party services
- Get user consent for data processing

---

**Last Updated**: 2026-01-28
