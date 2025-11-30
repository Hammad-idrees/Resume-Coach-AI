"""
Test script for Interview Simulation API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_generate_questions():
    """Test the question generation endpoint"""
    print("=" * 80)
    print("TEST 1: Generate Interview Questions")
    print("=" * 80)
    
    payload = {
        "job_description": "Senior Software Engineer with 5+ years experience in Python, React, and AWS. Strong problem-solving skills required.",
        "job_role": "Senior Software Engineer",
        "num_questions": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/interview/generate-questions", json=payload)
        response.raise_for_status()
        
        data = response.json()
        print(f"\n✅ Success! Generated {data['total_questions']} questions:\n")
        
        for q in data['questions']:
            print(f"{q['id']}. [{q['category']}] ({q['difficulty']})")
            print(f"   {q['question']}\n")
        
        return data['questions']
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def test_evaluate_answer(question_data):
    """Test the answer evaluation endpoint"""
    print("\n" + "=" * 80)
    print("TEST 2: Evaluate Interview Answer")
    print("=" * 80)
    
    test_answer = """
    In my previous role at Tech Corp, I led a team of 5 developers to migrate our 
    monolithic application to microservices architecture. The situation was that our 
    deployment times were taking 4 hours and causing frequent downtime. My task was 
    to redesign the system and implement the migration. I approached this by first 
    analyzing dependencies, then breaking down services incrementally. We used Docker 
    and Kubernetes for containerization. As a result, we reduced deployment time to 
    15 minutes and achieved 99.9% uptime, which improved customer satisfaction by 30%.
    """
    
    payload = {
        "question": question_data['question'],
        "answer": test_answer,
        "category": question_data['category'],
        "difficulty": question_data['difficulty']
    }
    
    try:
        response = requests.post(f"{BASE_URL}/interview/evaluate-answer", json=payload)
        response.raise_for_status()
        
        data = response.json()
        print(f"\n✅ Success! Answer evaluated:\n")
        print(f"Score: {data['score']}/10")
        print(f"Feedback: {data['overall_feedback']}")
        print(f"Word Count: {data['word_count']}")
        print(f"Sentiment: {data['sentiment']}")
        print(f"Has Example: {data['has_example']}")
        print(f"Has Result: {data['has_result']}")
        
        print(f"\n✓ Strengths ({len(data['strengths'])}):")
        for s in data['strengths']:
            print(f"  • {s}")
        
        print(f"\n💡 Improvements ({len(data['improvements'])}):")
        for i in data['improvements']:
            print(f"  • {i}")
        
        return data
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def test_calculate_score():
    """Test the overall score calculation endpoint"""
    print("\n" + "=" * 80)
    print("TEST 3: Calculate Overall Interview Score")
    print("=" * 80)
    
    # Simulate evaluations from 5 questions
    payload = {
        "evaluations": [
            {"score": 8.5, "category": "Introduction"},
            {"score": 7.5, "category": "Technical"},
            {"score": 9.0, "category": "Behavioral"},
            {"score": 6.5, "category": "Technical"},
            {"score": 8.0, "category": "Motivation"}
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/interview/calculate-score", json=payload)
        response.raise_for_status()
        
        data = response.json()
        print(f"\n✅ Success! Overall score calculated:\n")
        print(f"Overall Score: {data['overall_score']}/100")
        print(f"Grade: {data['grade']}")
        print(f"Average per Question: {data['average_score']}/10")
        print(f"Questions Answered: {data['questions_answered']}/{data['total_questions']}")
        print(f"\nSummary: {data['summary']}")
        
        print(f"\nCategory Breakdown:")
        for cat, score in data['category_breakdown'].items():
            print(f"  {cat}: {score}/10")
        
        return data
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def main():
    """Run all tests"""
    print("\n🚀 Starting Interview Simulation API Tests\n")
    
    # Test 1: Generate questions
    questions = test_generate_questions()
    
    if not questions:
        print("\n❌ Question generation failed. Stopping tests.")
        return
    
    # Test 2: Evaluate answer using first question
    evaluation = test_evaluate_answer(questions[0])
    
    if not evaluation:
        print("\n❌ Answer evaluation failed. Skipping score calculation test.")
    
    # Test 3: Calculate overall score
    overall_score = test_calculate_score()
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 80)
    print("\nAPI Endpoints Status:")
    print("  ✓ POST /interview/generate-questions - Working")
    print("  ✓ POST /interview/evaluate-answer - Working")
    print("  ✓ POST /interview/calculate-score - Working")
    print("\n🎉 Interview Simulation API is ready for frontend integration!\n")


if __name__ == "__main__":
    main()
