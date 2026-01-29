#!/bin/bash

# Start the Frontend
echo "🚀 Starting AI Job Hunter Frontend..."
echo ""

# Navigate to frontend directory
cd frontend

# Check node modules
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start dev server
echo "✅ Starting Vite server..."
npm run dev
