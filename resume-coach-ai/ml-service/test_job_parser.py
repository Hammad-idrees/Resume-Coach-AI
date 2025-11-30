import requests
import json

# Test job description
job_desc = '''
Senior Software Engineer

ABC Tech Company is seeking a talented Senior Software Engineer with 5+ years of experience
in Python, JavaScript, and cloud technologies. 

Requirements:
- Bachelor's degree in Computer Science or related field
- 5+ years of software development experience
- Strong proficiency in Python, JavaScript, React, Node.js
- Experience with AWS, Docker, and Kubernetes
- Knowledge of SQL and NoSQL databases (PostgreSQL, MongoDB)

Salary: $120,000 - $150,000 per year
Location: San Francisco, CA

We offer competitive compensation, health benefits, and remote work options.
'''

try:
    # Make request to parse-job endpoint
    response = requests.post(
        'http://127.0.0.1:8000/parse-job',
        json={'job_description': job_desc},
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print(' Job parsing successful!')
        print(json.dumps(result, indent=2))
    else:
        print(f' Error: {response.status_code}')
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print(' Could not connect to server. Make sure FastAPI is running on port 8000.')
except Exception as e:
    print(f' Error: {str(e)}')
