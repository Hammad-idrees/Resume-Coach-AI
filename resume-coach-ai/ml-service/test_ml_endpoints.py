"""
Comprehensive API Testing Script for ML Service
Tests all remaining endpoints: /predict-match, /parse-job, /optimize-ats
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_test_header(test_name: str):
    """Print formatted test header"""
    print("\n" + "="*80)
    print(f"TEST: {test_name}")
    print("="*80)

def print_result(endpoint: str, status_code: int, response: Dict[Any, Any]):
    """Print formatted test result"""
    print(f"\nEndpoint: {endpoint}")
    print(f"Status Code: {status_code}")
    print(f"Response:\n{json.dumps(response, indent=2)}")

def test_predict_match():
    """Test Resume-Job Match Prediction endpoint"""
    print_test_header("Resume-Job Match Prediction")
    
    endpoint = f"{BASE_URL}/predict-match"
    
    payload = {
        "resume_text": "Software Engineer with 5 years of experience in Python, React, and AWS. Built scalable microservices and RESTful APIs. Strong problem-solving skills.",
        "job_description": "Looking for a Senior Software Engineer with Python and cloud experience. Must have REST API development experience."
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        result = response.json()
        
        print_result(endpoint, response.status_code, result)
        
        # Validation
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert "match_score" in result, "Missing match_score in response"
        assert "confidence" in result, "Missing confidence in response"
        # API uses 'keywords_matched' not 'matching_keywords'
        assert "keywords_matched" in result or "matching_keywords" in result, "Missing keywords field in response"
        
        print("\n✅ TEST PASSED")
        print(f"Match Score: {result.get('match_score')}")
        print(f"Confidence: {result.get('confidence')}")
        print(f"Keywords Matched: {result.get('keywords_matched', result.get('matching_keywords'))}")
        print(f"Recommendation: {result.get('recommendation')}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_parse_job():
    """Test Job Description Parsing endpoint"""
    print_test_header("Job Description Parsing")
    
    endpoint = f"{BASE_URL}/parse-job"
    
    payload = {
        "job_description": "We are seeking a Machine Learning Engineer with 3+ years of experience in TensorFlow, PyTorch, and NLP. Must have strong Python skills and experience with model deployment."
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        result = response.json()
        
        print_result(endpoint, response.status_code, result)
        
        # Validation
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert "entities" in result, "Missing entities in response"
        
        print("\n✅ TEST PASSED")
        
        # API returns different structure - skills as array, entities as list of objects
        print(f"Skills Found: {result.get('skills', [])}")
        print(f"Experience: {result.get('experience_years')}")
        print(f"Job Title: {result.get('job_title')}")
        print(f"Company: {result.get('company')}")
        print(f"Entities Count: {len(result.get('entities', []))}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_optimize_ats():
    """Test ATS Optimization Analysis endpoint"""
    print_test_header("ATS Optimization Analysis")
    
    endpoint = f"{BASE_URL}/optimize-ats"
    
    payload = {
        "resume_text": "Data Analyst with expertise in SQL, Excel, and Tableau. Created dashboards and reports for business intelligence.",
        "job_description": "Looking for a Data Analyst with SQL, Python, Tableau, and Power BI skills. Experience with data visualization and ETL pipelines required."
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        result = response.json()
        
        print_result(endpoint, response.status_code, result)
        
        # Validation
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert "ats_score" in result, "Missing ats_score in response"
        assert "keyword_match_percentage" in result, "Missing keyword_match_percentage"
        assert "missing_keywords" in result, "Missing missing_keywords"
        assert "matched_keywords" in result, "Missing matched_keywords"
        assert "suggestions" in result, "Missing suggestions"
        
        print("\n✅ TEST PASSED")
        print(f"ATS Score: {result.get('ats_score')}/100")
        print(f"Keyword Match: {result.get('keyword_match_percentage')}%")
        print(f"Missing Keywords ({len(result.get('missing_keywords', []))}): {result.get('missing_keywords')}")
        print(f"Matched Keywords ({len(result.get('matched_keywords', []))}): {result.get('matched_keywords')}")
        print(f"Suggestions ({len(result.get('suggestions', []))}): {result.get('suggestions')}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return None

def test_all_endpoints():
    """Run all ML service endpoint tests"""
    print("\n" + "="*80)
    print("ML SERVICE API TESTING - COMPREHENSIVE SUITE")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    print("Testing 3 endpoints: /predict-match, /parse-job, /optimize-ats")
    
    results = {
        "predict_match": None,
        "parse_job": None,
        "optimize_ats": None
    }
    
    # Test 1: Predict Match
    results["predict_match"] = test_predict_match()
    
    # Test 2: Parse Job
    results["parse_job"] = test_parse_job()
    
    # Test 3: Optimize ATS
    results["optimize_ats"] = test_optimize_ats()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for r in results.values() if r is not None)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    print(f"Pass Rate: {(passed/total)*100:.1f}%")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = "✅ PASSED" if result is not None else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    print("Starting ML Service API Tests...")
    print("Make sure the ML service is running on http://localhost:8000")
    print("Run: uvicorn app:app --reload")
    
    input("\nPress Enter to continue...")
    
    test_all_endpoints()
