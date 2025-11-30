# Test script for Resume Scorer API

Write-Host "Testing Resume Scorer API..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
$health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
$health | ConvertTo-Json
Write-Host ""

# Test 2: Strong Match (Python Developer)
Write-Host "Test 2: Strong Match - Python Developer" -ForegroundColor Yellow
$body1 = @{
    resume_text = "Senior Python Developer with 5 years of experience in Django, FastAPI, and machine learning. Built scalable APIs and ML models. Proficient in Docker, Kubernetes, AWS."
    job_description = "Looking for Python Developer with experience in FastAPI and ML. 3+ years required. Django is a plus. Cloud experience (AWS) preferred."
} | ConvertTo-Json

$result1 = Invoke-RestMethod -Uri "http://localhost:8000/predict-match" -Method Post -Body $body1 -ContentType "application/json"
$result1 | ConvertTo-Json -Depth 10
Write-Host ""

# Test 3: Weak Match (Mismatched Skills)
Write-Host "Test 3: Weak Match - Mismatched Skills" -ForegroundColor Yellow
$body2 = @{
    resume_text = "Marketing Manager with 8 years in social media, content creation, and brand strategy. Skilled in Adobe Creative Suite and analytics."
    job_description = "Software Engineer needed with Python, React, and backend development experience. 3+ years required."
} | ConvertTo-Json

$result2 = Invoke-RestMethod -Uri "http://localhost:8000/predict-match" -Method Post -Body $body2 -ContentType "application/json"
$result2 | ConvertTo-Json -Depth 10
Write-Host ""

# Test 4: Good Match (Full Stack Developer)
Write-Host "Test 4: Good Match - Full Stack Developer" -ForegroundColor Yellow
$body3 = @{
    resume_text = "Full Stack Developer with React, Node.js, MongoDB experience. Built 10+ web applications. JavaScript, TypeScript, Express, REST APIs."
    job_description = "Full Stack Developer position. MERN stack (MongoDB, Express, React, Node.js). 2+ years experience. TypeScript is a plus."
} | ConvertTo-Json

$result3 = Invoke-RestMethod -Uri "http://localhost:8000/predict-match" -Method Post -Body $body3 -ContentType "application/json"
$result3 | ConvertTo-Json -Depth 10
Write-Host ""

Write-Host "All tests completed!" -ForegroundColor Green
