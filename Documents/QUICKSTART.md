# Quick Start Guide

Get your AI Job Hunter backend running in 5 minutes!

---

## Prerequisites

Before you begin, make sure you have:

- ✅ Python 3.10 or higher installed
- ✅ Docker installed (for Qdrant)
- ✅ Git installed
- ✅ Terminal/Command line access

---

## Step 1: Clone & Setup

If you haven't already:

```bash
# Navigate to project directory
cd /Users/shahabas/shahabas-personal-work/job_hunting

# Or clone from Git
git clone <your-repo-url>
cd job_hunting
```

---

## Step 2: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output:** All packages installed successfully

---

## Step 3: Start Qdrant Vector Database

```bash
# Start Qdrant in Docker
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# Verify it's running
curl http://localhost:6333/health
```

**Expected output:** `{"title":"qdrant - vector search engine","version":"..."}`

---

## Step 4: Configure Environment Variables

Your `.env` file should already exist. Verify it contains:

```env
MODEL_NAME=qwen3-coder:480b-cloud
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama
EMBED_MODEL_NAME=nomic-embed-text

RAPIDAPI_KEY=your_rapidapi_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_API_KEY=your_adzuna_api_key
```

**Note:** If using OpenAI instead of Ollama, update the URLs and keys accordingly.

---

## Step 5: Start Ollama (If using local LLM)

If using Ollama locally:

```bash
# Make sure Ollama is running
ollama list

# Pull required models if not already present
ollama pull qwen3-coder:480b-cloud
ollama pull nomic-embed-text
```

**Skip this step if using OpenAI API instead.**

---

## Step 6: Start the API Server

```bash
# Make start script executable
chmod +x start.sh

# Start the server
./start.sh
```

**Alternative (manual start):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Step 7: Verify Installation

Open a new terminal and run:

```bash
# Health check
curl http://localhost:8000/health

# API info
curl http://localhost:8000/
```

**Expected output:**
```json
{"status": "healthy", "service": "AI Job Hunter API"}
```

---

## Step 8: Test the API

```bash
# Make test script executable
chmod +x test_api.sh

# Run tests
./test_api.sh
```

**Or view interactive documentation:**

Open your browser and go to:
```
http://localhost:8000/docs
```

You'll see Swagger UI with all endpoints documented!

---

## Step 9: Try Your First Request

### Test Profile Extraction

Create a sample resume file (`sample_resume.txt`):

```txt
John Doe
Software Engineer

Skills: Python, FastAPI, React, PostgreSQL, Docker
Experience: 3 years

Software Engineer at Tech Corp (2021-2024)
- Built scalable APIs using FastAPI
- Worked with PostgreSQL databases
- Deployed applications using Docker

Education: BS Computer Science, 2020
```

Then:

```bash
curl -X POST http://localhost:8000/profile/extract \
  -F "file=@sample_resume.txt"
```

### Test Job Search

```bash
curl -X POST "http://localhost:8000/jobs/all?page=1&size=5" \
  -H "Content-Type: application/json" \
  -d @examples/test_profile.json | jq '.'
```

---

## Common Issues & Solutions

### Issue 1: Port 8000 already in use

```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use a different port
uvicorn main:app --reload --port 8001
```

### Issue 2: Qdrant connection failed

```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Restart Qdrant
docker restart qdrant

# Check logs
docker logs qdrant
```

### Issue 3: Ollama not responding

```bash
# Check Ollama status
ollama list

# Restart Ollama service
# On Mac: restart Ollama app
# On Linux: sudo systemctl restart ollama
```

### Issue 4: Module not found errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Make sure virtual environment is activated
source venv/bin/activate
```

### Issue 5: API keys not working

```bash
# Verify .env file exists
cat .env

# Reload environment
source .env  # or restart the server
```

---

## Next Steps

Now that your API is running:

1. **Read the Documentation**
   - `README.md` - Overview and features
   - `API.md` - Detailed API documentation
   - `ARCHITECTURE.md` - System architecture
   - `DEPLOYMENT.md` - Production deployment

2. **Explore the Endpoints**
   - Visit `http://localhost:8000/docs`
   - Try different API endpoints
   - Test with your own resume

3. **Build a Frontend**
   - The `frontend/` directory has a sample UI
   - Or build your own using the API

4. **Deploy to Production**
   - See `DEPLOYMENT.md` for deployment guides
   - Configure proper security
   - Set up monitoring

---

## Development Workflow

### Running in Development Mode

```bash
# Start with auto-reload
uvicorn main:app --reload

# Watch for changes
# Edit code, and server auto-restarts
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_main.py::test_health_check -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Debugging

```bash
# Add breakpoints in code
import pdb; pdb.set_trace()

# Run in debug mode
uvicorn main:app --reload --log-level debug
```

---

## API Endpoints Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/` | GET | API information |
| `/profile/extract` | POST | Extract profile from resume |
| `/jobs/all` | POST | Get all jobs (paginated) |
| `/jobs/search` | POST | Search jobs |
| `/jobs/match` | POST | Match jobs |
| `/jobs/explain` | POST | Get explanations |
| `/apply/prepare` | POST | Generate resume + cover letter |
| `/apply/assist` | POST | Get application assistance |

---

## Environment Variables Reference

```env
# LLM Configuration
MODEL_NAME=qwen3-coder:480b-cloud      # Chat model
EMBED_MODEL_NAME=nomic-embed-text       # Embedding model
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama

# Alternative: OpenAI
# MODEL_NAME=gpt-4-turbo
# OPENAI_API_KEY=sk-...
# Comment out OLLAMA vars if using OpenAI

# Job API Keys
RAPIDAPI_KEY=<your_key>                 # For JSearch
ADZUNA_APP_ID=<your_id>                 # For Adzuna
ADZUNA_API_KEY=<your_key>               # For Adzuna

# Optional: Qdrant Cloud
# QDRANT_URL=https://your-cluster.qdrant.io
# QDRANT_API_KEY=<your_key>
```

---

## Getting Help

- **Documentation**: Check the `docs/` folder
- **API Docs**: http://localhost:8000/docs
- **Issues**: Open a GitHub issue
- **Logs**: Check terminal output for errors

---

## Quick Commands Cheat Sheet

```bash
# Start everything
docker start qdrant && ./start.sh

# Stop everything
# Ctrl+C (stop FastAPI)
docker stop qdrant

# View logs
docker logs qdrant
tail -f api.log

# Test API
curl http://localhost:8000/health
./test_api.sh

# Run tests
pytest tests/ -v

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

## Success Checklist

After setup, you should be able to:

- [ ] Access http://localhost:8000/health
- [ ] View docs at http://localhost:8000/docs
- [ ] Extract profile from a resume file
- [ ] Search and match jobs
- [ ] Generate resume and cover letter
- [ ] See all tests passing with `pytest`

---

**Congratulations! 🎉**

Your AI Job Hunter backend is now running!

Visit `http://localhost:8000/docs` to explore the API.

---

Last Updated: 2026-01-28
