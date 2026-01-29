#!/bin/bash

# AI Job Hunter - Startup Script
# This script starts the FastAPI backend server

echo "🚀 Starting AI Job Hunter Backend..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with required environment variables."
    echo "See README.md for details."
    exit 1
fi

# Check if Qdrant is running (optional check)
echo "📊 Checking Qdrant connection..."
if ! curl -s http://localhost:6333/health > /dev/null 2>&1; then
    echo "⚠️  Warning: Qdrant not responding on localhost:6333"
    echo "Make sure Qdrant is running: docker run -p 6333:6333 qdrant/qdrant"
    echo ""
fi

# Check if Ollama is running (optional check)
echo "🤖 Checking Ollama connection..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Warning: Ollama not responding on localhost:11434"
    echo "Make sure Ollama is running with the required models"
    echo ""
fi

# Start the server
echo "✅ Starting FastAPI server..."
echo "📡 API will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
