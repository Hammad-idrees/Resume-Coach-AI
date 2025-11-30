import requests
import json

# Test ATS optimization endpoint

sample_resume = """
Senior Software Engineer

Experienced software engineer with 5 years in Python development.
Built scalable web applications using Django and Flask frameworks.
Strong background in database design with PostgreSQL and MongoDB.
Implemented RESTful APIs and microservices architecture.
Proficient in Git, Docker, and CI/CD pipelines.

Experience:
- Developed e-commerce platform serving 100K+ users
- Optimized database queries improving performance by 40%
- Led team of 3 junior developers

Education:
Bachelor's degree in Computer Science

Skills:
Python, Django, Flask, PostgreSQL, MongoDB, Docker, Git, REST APIs, Microservices
"""

sample_job = """
Senior Software Engineer Position

We are seeking a talented Senior Software Engineer with 5+ years of experience
in Python, JavaScript, and cloud technologies.

Requirements:
- 5+ years of software development experience
- Strong proficiency in Python, JavaScript, React, Node.js
- Experience with AWS, Docker, and Kubernetes
- Knowledge of PostgreSQL and MongoDB databases
- Familiarity with microservices architecture
- Experience with CI/CD pipelines and DevOps practices

Nice to have:
- Machine learning experience
- React Native for mobile development
- TypeScript knowledge
"""

try:
    response = requests.post(
        'http://127.0.0.1:8000/optimize-ats',
        json={
            'resume_text': sample_resume,
            'job_description': sample_job
        },
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print("=" * 70)
        print("ATS OPTIMIZATION ANALYSIS - API TEST")
        print("=" * 70)
        print(f"\n📊 ATS Score: {result['ats_score']}/100")
        print(f"🎯 Keyword Match: {result['keyword_match_percentage']}%")
        print(f"📈 TF-IDF Similarity: {result['tfidf_similarity']}")
        print(f"📝 Resume Keywords: {result['resume_keyword_count']}")
        print(f"📋 Job Keywords: {result['job_keyword_count']}")
        
        print(f"\n✅ Matched Keywords ({len(result['matched_keywords'])}):")
        print(", ".join(result['matched_keywords'][:15]))
        
        print(f"\n❌ Missing Keywords ({len(result['missing_keywords'])}):")
        print(", ".join(result['missing_keywords']))
        
        print(f"\n💡 Optimization Suggestions ({len(result['suggestions'])}):")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"{i}. {suggestion}")
        
        print("\n" + "=" * 70)
        print("✅ Test PASSED - API endpoint working correctly!")
        print("=" * 70)
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print('❌ Could not connect to server. Make sure FastAPI is running on port 8000.')
    print('Run: python -m uvicorn app:app --port 8000')
except Exception as e:
    print(f'❌ Error: {str(e)}')
