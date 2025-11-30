"""
Test the trained resume scorer model
"""

import torch
import pandas as pd
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import numpy as np

def load_model():
    """Load the trained model and tokenizer"""
    print("Loading trained model...")
    model = DistilBertForSequenceClassification.from_pretrained('./models/resume_scorer')
    tokenizer = DistilBertTokenizer.from_pretrained('./models/resume_scorer')
    
    if torch.cuda.is_available():
        model = model.cuda()
        print(f"Model loaded on GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("Model loaded on CPU")
    
    return model, tokenizer

def predict_match_score(model, tokenizer, resume_text, job_description):
    """Predict match score for a resume-job pair"""
    combined = f"Resume: {resume_text} [SEP] Job: {job_description}"
    
    inputs = tokenizer(
        combined,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )
    
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        score = outputs.logits.item()
        # Clip to 0-1 range and scale to 0-100
        score = np.clip(score, 0, 1) * 100
    
    return score

def test_samples():
    """Test with multiple samples"""
    model, tokenizer = load_model()
    
    test_cases = [
        {
            "resume": "Senior Python Developer with 8 years experience. Expert in Django, FastAPI, PostgreSQL, and AWS. Led teams of 5+ developers.",
            "job": "Senior Python Developer needed. Django, FastAPI, cloud experience required. Team leadership preferred. 5+ years.",
            "expected": "High match (85-95)"
        },
        {
            "resume": "Marketing Manager with social media and content creation experience. Skilled in SEO and campaign management.",
            "job": "Software Engineer with Python, React, and backend development. 3+ years required.",
            "expected": "Low match (10-30)"
        },
        {
            "resume": "Full Stack Developer. JavaScript, React, Node.js, MongoDB. Built 10+ web applications. 4 years experience.",
            "job": "Full Stack Developer position. MERN stack (MongoDB, Express, React, Node.js). 3+ years.",
            "expected": "High match (85-95)"
        },
        {
            "resume": "Data Scientist with ML expertise. Python, TensorFlow, PyTorch, pandas. PhD in Statistics.",
            "job": "Data Scientist role. Machine learning, Python, deep learning frameworks. Advanced degree required.",
            "expected": "Very high match (90-98)"
        },
        {
            "resume": "Entry-level Java developer. Fresh graduate with internship experience. Basic Spring Boot knowledge.",
            "job": "Senior Java Architect. 10+ years experience with microservices, Spring Cloud, Kubernetes required.",
            "expected": "Very low match (5-20)"
        }
    ]
    
    print("\n" + "="*80)
    print("Testing Resume-Job Match Predictions")
    print("="*80 + "\n")
    
    for i, test in enumerate(test_cases, 1):
        score = predict_match_score(model, tokenizer, test["resume"], test["job"])
        
        print(f"Test Case {i}:")
        print(f"Resume: {test['resume'][:70]}...")
        print(f"Job: {test['job'][:70]}...")
        print(f"Expected: {test['expected']}")
        print(f"Predicted Score: {score:.2f}/100")
        print("-" * 80 + "\n")

def interactive_test():
    """Interactive testing mode"""
    model, tokenizer = load_model()
    
    print("\n" + "="*80)
    print("Interactive Testing Mode")
    print("="*80 + "\n")
    
    while True:
        print("\nEnter resume text (or 'quit' to exit):")
        resume = input("> ")
        
        if resume.lower() == 'quit':
            break
        
        print("\nEnter job description:")
        job = input("> ")
        
        score = predict_match_score(model, tokenizer, resume, job)
        
        print(f"\n{'='*60}")
        print(f"Match Score: {score:.2f}/100")
        
        if score >= 85:
            print("Assessment: Excellent Match! ✅")
        elif score >= 70:
            print("Assessment: Good Match 👍")
        elif score >= 50:
            print("Assessment: Moderate Match ⚠️")
        else:
            print("Assessment: Poor Match ❌")
        
        print(f"{'='*60}\n")

if __name__ == "__main__":
    import sys
    
    print("\n🧪 Resume Scorer Model Testing\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_test()
    else:
        test_samples()
        print("\nTip: Run 'python test_model.py --interactive' for interactive testing")
