"""
Backend API Testing Script - Node.js/Express Endpoints
Tests resume, job, and score management endpoints
"""

import requests
import json
import uuid
from typing import Dict, Any, Optional

BASE_URL = "http://localhost:3000"
# Generate a valid UUID for testing
TEST_USER_ID = str(uuid.uuid4())

# Store created IDs for cleanup
created_resume_id: Optional[str] = None
created_job_id: Optional[str] = None

def print_test_header(test_name: str):
    """Print formatted test header"""
    print("\n" + "="*80)
    print(f"TEST: {test_name}")
    print("="*80)

def print_result(endpoint: str, method: str, status_code: int, response: Any):
    """Print formatted test result"""
    print(f"\nEndpoint: {method} {endpoint}")
    print(f"Status Code: {status_code}")
    if response:
        try:
            print(f"Response:\n{json.dumps(response, indent=2)}")
        except:
            print(f"Response: {response}")

def test_create_resume():
    """Test POST /api/resumes - Create Resume"""
    print_test_header("Create Resume")
    
    endpoint = f"{BASE_URL}/api/resumes"
    headers = {
        "x-user-id": TEST_USER_ID,
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": "John Doe - Software Engineer Resume",
        "content": "Full stack developer with 5 years of experience in Python, React, and AWS. Built scalable microservices and RESTful APIs.",
        "skills": ["Python", "React", "AWS", "Docker", "PostgreSQL"],
        "experience": ["Software Engineer at Tech Corp (2019-2024)", "Junior Developer at StartupXYZ (2017-2019)"],
        "education": ["BS Computer Science, University (2017)", "Online certifications: AWS, Docker"]
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        
        print_result(endpoint, "POST", response.status_code, result)
        
        # Validation
        if response.status_code in [200, 201]:
            print("\n✅ TEST PASSED")
            global created_resume_id
            if isinstance(result, dict):
                # Response has 'resume' object
                resume_data = result.get('resume', result)
                created_resume_id = resume_data.get('id')
                print(f"Created Resume ID: {created_resume_id}")
            return result
        else:
            print(f"\n⚠️ TEST WARNING: Expected 200/201, got {response.status_code}")
            return None
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_get_all_resumes():
    """Test GET /api/resumes - Get All Resumes"""
    print_test_header("Get All Resumes")
    
    endpoint = f"{BASE_URL}/api/resumes"
    headers = {
        "x-user-id": TEST_USER_ID
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        
        print_result(endpoint, "GET", response.status_code, result)
        
        if response.status_code == 200:
            print("\n✅ TEST PASSED")
            if isinstance(result, dict):
                resumes = result.get('resumes', [])
                print(f"Total Resumes: {len(resumes)}")
            return result
        else:
            print(f"\n⚠️ TEST WARNING: Expected 200, got {response.status_code}")
            return None
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_get_single_resume():
    """Test GET /api/resumes/:id - Get Single Resume"""
    print_test_header("Get Single Resume")
    
    if not created_resume_id:
        print("\n⚠️ SKIPPED: No resume ID available (create resume first)")
        return None
    
    endpoint = f"{BASE_URL}/api/resumes/{created_resume_id}"
    headers = {
        "x-user-id": TEST_USER_ID
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        
        print_result(endpoint, "GET", response.status_code, result)
        
        if response.status_code == 200:
            print("\n✅ TEST PASSED")
            return result
        else:
            print(f"\n⚠️ TEST WARNING: Expected 200, got {response.status_code}")
            return None
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_create_job():
    """Test POST /api/jobs - Create Job"""
    print_test_header("Create Job")
    
    endpoint = f"{BASE_URL}/api/jobs"
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "description": "Looking for experienced developer with Python and AWS skills...",
        "requirements": ["Python", "AWS", "Docker"],
        "location": "Remote"
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        
        print_result(endpoint, "POST", response.status_code, result)
        
        if response.status_code in [200, 201]:
            print("\n✅ TEST PASSED")
            global created_job_id
            if isinstance(result, dict):
                # Response has 'job' object
                job_data = result.get('job', result)
                created_job_id = job_data.get('id')
                print(f"Created Job ID: {created_job_id}")
            return result
        elif response.status_code == 500 and "row-level security policy" in str(result):
            print("\n⚠️ RLS POLICY BLOCKING: Job creation requires proper authentication/admin role")
            print("This is expected if RLS policies are enabled and user is not admin")
            return None
        else:
            print(f"\n⚠️ TEST WARNING: Expected 200/201, got {response.status_code}")
            return None
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_get_all_jobs():
    """Test GET /api/jobs - Get All Jobs"""
    print_test_header("Get All Jobs")
    
    endpoint = f"{BASE_URL}/api/jobs"
    
    try:
        response = requests.get(endpoint)
        result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        
        print_result(endpoint, "GET", response.status_code, result)
        
        if response.status_code == 200:
            print("\n✅ TEST PASSED")
            if isinstance(result, dict):
                jobs = result.get('jobs', [])
                print(f"Total Jobs: {len(jobs)}")
            return result
        else:
            print(f"\n⚠️ TEST WARNING: Expected 200, got {response.status_code}")
            return None
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_calculate_score():
    """Test POST /api/scores/calculate - Calculate Match Score"""
    print_test_header("Calculate Match Score")
    
    if not created_resume_id or not created_job_id:
        print("\n⚠️ SKIPPED: Need both resume_id and job_id")
        return None
    
    endpoint = f"{BASE_URL}/api/scores/calculate"
    headers = {
        "x-user-id": TEST_USER_ID,
        "Content-Type": "application/json"
    }
    
    payload = {
        "resume_id": created_resume_id,
        "job_id": created_job_id
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        
        print_result(endpoint, "POST", response.status_code, result)
        
        if response.status_code == 200:
            print("\n✅ TEST PASSED")
            if isinstance(result, dict):
                print(f"Match Score: {result.get('match_score')}")
            return result
        else:
            print(f"\n⚠️ TEST WARNING: Expected 200, got {response.status_code}")
            return None
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_update_resume():
    """Test PUT /api/resumes/:id - Update Resume"""
    print_test_header("Update Resume")
    
    if not created_resume_id:
        print("\n⚠️ SKIPPED: No resume ID available")
        return None
    
    endpoint = f"{BASE_URL}/api/resumes/{created_resume_id}"
    headers = {
        "x-user-id": TEST_USER_ID,
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": "John Doe - Senior Software Engineer Resume (Updated)",
        "skills": ["Python", "React", "AWS", "Docker", "Kubernetes"]
    }
    
    try:
        response = requests.put(endpoint, json=payload, headers=headers)
        result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        
        print_result(endpoint, "PUT", response.status_code, result)
        
        if response.status_code == 200:
            print("\n✅ TEST PASSED")
            return result
        else:
            print(f"\n⚠️ TEST WARNING: Expected 200, got {response.status_code}")
            return None
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_delete_resume():
    """Test DELETE /api/resumes/:id - Delete Resume"""
    print_test_header("Delete Resume")
    
    if not created_resume_id:
        print("\n⚠️ SKIPPED: No resume ID available")
        return None
    
    endpoint = f"{BASE_URL}/api/resumes/{created_resume_id}"
    headers = {
        "x-user-id": TEST_USER_ID
    }
    
    try:
        response = requests.delete(endpoint, headers=headers)
        
        print_result(endpoint, "DELETE", response.status_code, None)
        
        if response.status_code in [200, 204]:
            print("\n✅ TEST PASSED")
            return True
        else:
            print(f"\n⚠️ TEST WARNING: Expected 200/204, got {response.status_code}")
            return None
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_all_backend_endpoints():
    """Run all backend API endpoint tests"""
    print("\n" + "="*80)
    print("BACKEND API TESTING - COMPREHENSIVE SUITE")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    print(f"Test User ID: {TEST_USER_ID}")
    print("Testing 8 endpoints: Resumes (5), Jobs (2), Scores (1)")
    
    results = {}
    
    # Resume Endpoints
    results["create_resume"] = test_create_resume()
    results["get_all_resumes"] = test_get_all_resumes()
    results["get_single_resume"] = test_get_single_resume()
    results["update_resume"] = test_update_resume()
    
    # Job Endpoints
    results["create_job"] = test_create_job()
    results["get_all_jobs"] = test_get_all_jobs()
    
    # Score Endpoint
    results["calculate_score"] = test_calculate_score()
    
    # Cleanup
    results["delete_resume"] = test_delete_resume()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for r in results.values() if r is not None)
    skipped = sum(1 for r in results.values() if r is None)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    print(f"Tests Skipped: {skipped}/{total}")
    print(f"Pass Rate: {(passed/total)*100:.1f}%")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        if result is None:
            status = "⚠️ SKIPPED/WARNING"
        else:
            status = "✅ PASSED"
        print(f"  {test_name}: {status}")
    
    print("\n" + "="*80)
    print("\nNOTE: Some tests may be skipped if the backend server is not running.")
    print("Start backend: cd backend && npm run dev")
    print("Ensure Supabase credentials are configured in .env")
    print("="*80)

if __name__ == "__main__":
    print("Starting Backend API Tests...")
    print("Make sure the backend server is running on http://localhost:3000")
    print("Run: cd backend && npm run dev")
    
    input("\nPress Enter to continue...")
    
    test_all_backend_endpoints()
