#!/bin/bash

# AI Job Hunter - API Test Script
# This script demonstrates how to test various API endpoints

API_BASE="http://localhost:8000"

echo "🧪 AI Job Hunter API Testing"
echo "=============================="
echo ""

# Test 1: Health Check
echo "1️⃣ Testing Health Check..."
curl -s "$API_BASE/health" | jq '.'
echo ""

# Test 2: Root endpoint
echo "2️⃣ Testing Root Endpoint..."
curl -s "$API_BASE/" | jq '.'
echo ""

# Test 3: Get All Jobs (Paginated)
echo "3️⃣ Testing Get All Jobs (Paginated)..."
echo "Note: This requires existing jobs in Qdrant vector DB"
curl -s -X POST "$API_BASE/jobs/all?page=1&size=5" \
  -H "Content-Type: application/json" \
  -d @examples/test_profile.json | jq '.'
echo ""

# Test 4: Prepare Application
echo "4️⃣ Testing Application Preparation (Resume + Cover Letter)..."
curl -s -X POST "$API_BASE/apply/prepare" \
  -H "Content-Type: application/json" \
  -d @examples/test_prepare_application.json | jq '.'
echo ""

# Test 5: Assist Apply
echo "5️⃣ Testing Assist Apply..."
curl -s -X POST "$API_BASE/apply/assist" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Backend Engineer",
    "company_name": "Tech Corp",
    "redirect_url": "https://example.com/jobs/apply/123"
  }' | jq '.'
echo ""

echo "✅ All tests completed!"
echo ""
echo "📚 For more details, visit: http://localhost:8000/docs"
