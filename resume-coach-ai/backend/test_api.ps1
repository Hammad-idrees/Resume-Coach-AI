# Test Node.js Backend API

Write-Host "=== Testing ResumeCoach AI Backend API ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Root endpoint
Write-Host ""
Write-Host "[Test 1] Root endpoint (GET /)" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:3000/" -Method Get
    Write-Host "✓ Success!" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

# Test 2: Health check
Write-Host ""
Write-Host "[Test 2] Health check (GET /api/health)" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:3000/api/health" -Method Get
    Write-Host "✓ Success!" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

# Test 3: Get all jobs
Write-Host ""
Write-Host "[Test 3] Get all jobs (GET /api/jobs)" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:3000/api/jobs" -Method Get
    Write-Host "✓ Success!" -ForegroundColor Green
    Write-Host "Jobs count: $($response.count)"
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

# Test 4: ML service health check
Write-Host ""
Write-Host "[Test 4] ML service health (GET /api/score/ml/health)" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:3000/api/score/ml/health" -Method Get
    Write-Host "✓ Success!" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
    Write-Host "Note: ML service must be running on port 8000" -ForegroundColor Yellow
}

# Test 5: Get match score (requires ML service)
Write-Host ""
Write-Host "[Test 5] Get match score (POST /api/score)" -ForegroundColor Yellow
try {
    $body = @{
        resume_text = "Senior Python Developer with 5 years of experience in Django, FastAPI, and machine learning. Strong skills in AWS, Docker, and PostgreSQL."
        job_description = "Looking for experienced Python Developer with FastAPI and ML experience. Must have cloud deployment experience."
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:3000/api/score" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body

    Write-Host "✓ Success!" -ForegroundColor Green
    Write-Host "Match Score: $($response.score.match_score)"
    Write-Host "Confidence: $($response.score.confidence)"
    Write-Host "Keywords: $($response.score.keywords_matched -join ', ')"
    Write-Host "Recommendation: $($response.score.recommendation)"
} catch {
    Write-Host "Failed: $_" -ForegroundColor Red
    Write-Host "Note: ML service must be running on port 8000" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Testing Complete ===" -ForegroundColor Cyan
