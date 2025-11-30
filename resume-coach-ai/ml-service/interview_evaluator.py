"""
Interview Simulation Module
Generates interview questions and evaluates user responses using LLM.
"""

from typing import List, Dict, Any, Optional
import re
from transformers import pipeline
import torch

# Initialize sentiment analysis for tone detection
try:
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=0 if torch.cuda.is_available() else -1
    )
except Exception as e:
    print(f"Warning: Could not load sentiment analyzer: {e}")
    sentiment_analyzer = None


def generate_interview_questions(job_description: str, job_role: str = "", num_questions: int = 5) -> List[Dict[str, str]]:
    """
    Generate interview questions based on job description and role.
    
    Args:
        job_description: The job posting text
        job_role: Job title/role (e.g., "Software Engineer")
        num_questions: Number of questions to generate
        
    Returns:
        List of question dictionaries with id, question, category, and difficulty
    """
    
    # Extract key requirements from job description
    job_lower = job_description.lower()
    
    # Detect technical skills mentioned
    technical_skills = []
    common_skills = ['python', 'javascript', 'react', 'node', 'aws', 'docker', 
                    'kubernetes', 'sql', 'mongodb', 'machine learning', 'ai',
                    'django', 'flask', 'fastapi', 'java', 'c++', 'golang']
    
    for skill in common_skills:
        if skill in job_lower:
            technical_skills.append(skill)
    
    # Detect experience level
    experience_level = "entry"
    if any(word in job_lower for word in ['senior', '5+ years', '7+ years', 'lead']):
        experience_level = "senior"
    elif any(word in job_lower for word in ['mid-level', '3+ years', '4+ years']):
        experience_level = "mid"
    
    # Expanded question bank with 60+ questions customized by job context
    questions_bank = {
        "introduction": [
            {
                "question": "Tell me about yourself and your background in the context of this role.",
                "category": "Introduction",
                "difficulty": "easy"
            },
            {
                "question": "Walk me through your resume and highlight your most relevant experience for this position.",
                "category": "Introduction",
                "difficulty": "easy"
            },
            {
                "question": f"What interests you about working in {job_role if job_role else 'this field'}?",
                "category": "Introduction",
                "difficulty": "easy"
            },
            {
                "question": "How did you get started in your current career path?",
                "category": "Introduction",
                "difficulty": "easy"
            },
            {
                "question": "What are your key strengths that make you suitable for this role?",
                "category": "Introduction",
                "difficulty": "easy"
            }
        ],
        "technical": [
            {
                "question": f"Describe your hands-on experience with {technical_skills[0] if technical_skills else 'the technologies'} mentioned in the job description.",
                "category": "Technical",
                "difficulty": "medium"
            },
            {
                "question": "Explain a challenging technical problem you solved recently and walk me through your approach.",
                "category": "Technical",
                "difficulty": "medium"
            },
            {
                "question": "How do you stay updated with the latest technologies and industry trends in your field?",
                "category": "Technical",
                "difficulty": "easy"
            },
            {
                "question": f"Can you explain how you would architect a system using {', '.join(technical_skills[:2]) if len(technical_skills) >= 2 else 'modern technologies'}?",
                "category": "Technical",
                "difficulty": "hard"
            },
            {
                "question": "Describe a time when you had to debug a complex issue. What was your methodology?",
                "category": "Technical",
                "difficulty": "medium"
            },
            {
                "question": "How do you ensure code quality and maintainability in your projects?",
                "category": "Technical",
                "difficulty": "medium"
            },
            {
                "question": "Tell me about a technical decision you made that you later regretted. What did you learn?",
                "category": "Technical",
                "difficulty": "hard"
            },
            {
                "question": "How do you approach performance optimization in your applications?",
                "category": "Technical",
                "difficulty": "medium"
            },
            {
                "question": "Describe your experience with version control and collaborative development workflows.",
                "category": "Technical",
                "difficulty": "easy"
            },
            {
                "question": "How do you handle technical debt in a codebase?",
                "category": "Technical",
                "difficulty": "medium"
            },
            {
                "question": "What testing strategies do you implement to ensure software reliability?",
                "category": "Technical",
                "difficulty": "medium"
            },
            {
                "question": "Explain a recent technology you learned and how you applied it in a project.",
                "category": "Technical",
                "difficulty": "medium"
            },
            {
                "question": "How would you explain a complex technical concept to a non-technical stakeholder?",
                "category": "Technical",
                "difficulty": "medium"
            },
            {
                "question": "Describe your experience with database design and optimization.",
                "category": "Technical",
                "difficulty": "medium"
            },
            {
                "question": "How do you approach security considerations in your development work?",
                "category": "Technical",
                "difficulty": "medium"
            }
        ],
        "behavioral": [
            {
                "question": "Describe a time when you had to work under tight deadlines. How did you manage your time and priorities?",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Tell me about a time when you disagreed with a team member or manager. How did you handle the situation?",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Give an example of a project where you demonstrated leadership, even if you weren't the formal leader.",
                "category": "Behavioral",
                "difficulty": "hard"
            },
            {
                "question": "Describe a situation where you had to learn something completely new quickly. How did you approach it?",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Tell me about a time when you made a mistake at work. How did you handle it?",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Describe a situation where you had to give difficult feedback to a colleague. How did you approach it?",
                "category": "Behavioral",
                "difficulty": "hard"
            },
            {
                "question": "Give me an example of when you went above and beyond your job responsibilities.",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Tell me about a time when you had to deal with a difficult client or stakeholder.",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Describe a project that failed or didn't go as planned. What did you learn from it?",
                "category": "Behavioral",
                "difficulty": "hard"
            },
            {
                "question": "Tell me about a time when you had to persuade others to adopt your idea or approach.",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Describe a situation where you had to balance multiple competing priorities.",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Give an example of when you helped a team member who was struggling.",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Tell me about a time when you received constructive criticism. How did you respond?",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Describe a situation where you had to adapt to significant changes at work.",
                "category": "Behavioral",
                "difficulty": "medium"
            },
            {
                "question": "Give an example of when you took initiative without being asked.",
                "category": "Behavioral",
                "difficulty": "medium"
            }
        ],
        "situational": [
            {
                "question": "How would you prioritize multiple urgent tasks with conflicting deadlines from different stakeholders?",
                "category": "Situational",
                "difficulty": "medium"
            },
            {
                "question": "If you inherited a poorly documented and legacy codebase, what would be your step-by-step approach?",
                "category": "Situational",
                "difficulty": "medium"
            },
            {
                "question": "How would you handle a situation where you discovered a critical bug in production?",
                "category": "Situational",
                "difficulty": "medium"
            },
            {
                "question": "If a project deadline is at risk, what steps would you take to get back on track?",
                "category": "Situational",
                "difficulty": "medium"
            },
            {
                "question": "How would you approach a situation where a team member is consistently missing deadlines?",
                "category": "Situational",
                "difficulty": "hard"
            },
            {
                "question": "If you had to choose between delivering a feature quickly or ensuring perfect code quality, how would you decide?",
                "category": "Situational",
                "difficulty": "hard"
            },
            {
                "question": "How would you handle a disagreement about technical architecture with senior team members?",
                "category": "Situational",
                "difficulty": "hard"
            },
            {
                "question": "If you were asked to work on a project with unfamiliar technology, how would you approach it?",
                "category": "Situational",
                "difficulty": "medium"
            },
            {
                "question": "How would you respond if a stakeholder kept changing project requirements?",
                "category": "Situational",
                "difficulty": "medium"
            },
            {
                "question": "What would you do if you discovered that your team's approach was inefficient, but they were resistant to change?",
                "category": "Situational",
                "difficulty": "hard"
            },
            {
                "question": "How would you handle a situation where you need to say no to a manager's request?",
                "category": "Situational",
                "difficulty": "hard"
            },
            {
                "question": "If you noticed a team member struggling but not asking for help, what would you do?",
                "category": "Situational",
                "difficulty": "medium"
            }
        ],
        "motivation": [
            {
                "question": f"Why are you interested in this {job_role if job_role else 'particular position'}?",
                "category": "Motivation",
                "difficulty": "easy"
            },
            {
                "question": "Where do you see yourself in 5 years, and how does this role fit into your career goals?",
                "category": "Motivation",
                "difficulty": "easy"
            },
            {
                "question": "What motivates you in your work, and what are you most passionate about professionally?",
                "category": "Motivation",
                "difficulty": "easy"
            },
            {
                "question": "What attracts you to our company specifically?",
                "category": "Motivation",
                "difficulty": "easy"
            },
            {
                "question": "What kind of work environment do you thrive in?",
                "category": "Motivation",
                "difficulty": "easy"
            },
            {
                "question": "What are your salary expectations and what factors are important to you beyond compensation?",
                "category": "Motivation",
                "difficulty": "medium"
            },
            {
                "question": "Why are you looking to leave your current role?",
                "category": "Motivation",
                "difficulty": "medium"
            },
            {
                "question": "What would make you choose our company over other opportunities?",
                "category": "Motivation",
                "difficulty": "medium"
            },
            {
                "question": "What are your long-term career aspirations?",
                "category": "Motivation",
                "difficulty": "easy"
            },
            {
                "question": "What type of projects or challenges are you most excited to work on?",
                "category": "Motivation",
                "difficulty": "easy"
            },
            {
                "question": "How do you define success in your career?",
                "category": "Motivation",
                "difficulty": "easy"
            },
            {
                "question": "What professional achievement are you most proud of and why?",
                "category": "Motivation",
                "difficulty": "easy"
            }
        ]
    }
    
    # Add skill-specific technical questions dynamically
    if technical_skills:
        for skill in technical_skills[:3]:  # Add up to 3 skill-specific questions
            questions_bank["technical"].append({
                "question": f"Can you discuss a specific project where you used {skill.title()}? What challenges did you face and how did you overcome them?",
                "category": "Technical",
                "difficulty": "medium"
            })
            questions_bank["technical"].append({
                "question": f"How would you explain {skill.title()} to someone who is just learning it?",
                "category": "Technical",
                "difficulty": "easy"
            })
    
    # Import random for better question selection
    import random
    
    # Select questions based on experience level and balance
    selected_questions = []
    
    # Randomly select introduction question for variety
    selected_questions.append(random.choice(questions_bank["introduction"][:3]))
    
    # Distribution based on num_questions with randomization
    if num_questions >= 5:
        # Balanced approach with random selection from each category
        selected_questions.append(random.choice(questions_bank["technical"][:5]))
        selected_questions.append(random.choice(questions_bank["behavioral"][:5]))
        selected_questions.append(random.choice(questions_bank["situational"][:4]))
        selected_questions.append(random.choice(questions_bank["motivation"][:4]))
        
        # Add more if needed with variety
        if num_questions > 5:
            remaining = num_questions - 5
            extra_pool = (
                random.sample(questions_bank["technical"][5:10], min(3, len(questions_bank["technical"][5:10]))) +
                random.sample(questions_bank["behavioral"][5:10], min(2, len(questions_bank["behavioral"][5:10]))) +
                random.sample(questions_bank["situational"][4:8], min(2, len(questions_bank["situational"][4:8])))
            )
            selected_questions.extend(random.sample(extra_pool, min(remaining, len(extra_pool))))
    else:
        # For fewer questions, prioritize based on job level with randomization
        if experience_level == "senior":
            pool = [
                random.choice(questions_bank["technical"][:5]),
                random.choice(questions_bank["behavioral"][2:5]),
                random.choice(questions_bank["motivation"][:3])
            ]
            selected_questions.extend(pool[:num_questions - 1])
        else:
            pool = [
                random.choice(questions_bank["technical"][:3]),
                random.choice(questions_bank["motivation"][:3]),
                random.choice(questions_bank["behavioral"][:3])
            ]
            selected_questions.extend(pool[:num_questions - 1])
    
    # Add IDs to questions
    for idx, q in enumerate(selected_questions[:num_questions], 1):
        q["id"] = idx
    
    return selected_questions[:num_questions]


def evaluate_answer(
    question: str,
    answer: str,
    category: str = "General",
    difficulty: str = "medium"
) -> Dict[str, Any]:
    """
    Evaluate an interview answer and provide scoring and feedback.
    
    Args:
        question: The interview question asked
        answer: User's answer to the question
        category: Question category (Technical, Behavioral, etc.)
        difficulty: Question difficulty level
        
    Returns:
        Dictionary containing score, feedback, strengths, and improvements
    """
    
    # Input validation
    if not answer or len(answer.strip()) < 10:
        return {
            "score": 2,
            "overall_feedback": "Answer is too short. Please provide a more detailed response.",
            "strengths": [],
            "improvements": [
                "Provide more detail and elaboration",
                "Use specific examples to support your points",
                "Aim for at least 50-100 words"
            ],
            "sentiment": "neutral",
            "word_count": len(answer.split())
        }
    
    # Calculate basic metrics
    word_count = len(answer.split())
    sentence_count = len(re.split(r'[.!?]+', answer.strip()))
    
    # Analyze answer structure
    has_example = any(word in answer.lower() for word in [
        'example', 'instance', 'time when', 'project', 'situation', 
        'experience', 'worked on', 'developed', 'implemented'
    ])
    
    has_result = any(word in answer.lower() for word in [
        'result', 'outcome', 'achieved', 'improved', 'increased',
        'reduced', 'successful', 'delivered', 'completed'
    ])
    
    has_numbers = bool(re.search(r'\d+', answer))
    
    # Sentiment analysis
    sentiment = "neutral"
    if sentiment_analyzer:
        try:
            sentiment_result = sentiment_analyzer(answer[:512])[0]  # Limit to 512 tokens
            sentiment = sentiment_result['label'].lower()
        except:
            pass
    
    # Scoring algorithm
    base_score = 5.0
    
    # Length scoring
    if word_count >= 150:
        base_score += 2.0
    elif word_count >= 100:
        base_score += 1.5
    elif word_count >= 50:
        base_score += 1.0
    elif word_count < 30:
        base_score -= 1.0
    
    # Structure scoring
    if has_example:
        base_score += 1.5
    if has_result:
        base_score += 1.0
    if has_numbers:
        base_score += 0.5
    
    # Category-specific scoring
    if category.lower() == "technical":
        technical_terms = ['algorithm', 'database', 'api', 'framework', 
                          'architecture', 'design', 'code', 'testing',
                          'deployment', 'optimization', 'performance']
        tech_mentions = sum(1 for term in technical_terms if term in answer.lower())
        base_score += min(tech_mentions * 0.3, 1.5)
    
    elif category.lower() == "behavioral":
        star_elements = {
            'situation': any(w in answer.lower() for w in ['situation', 'time when', 'faced', 'encountered']),
            'task': any(w in answer.lower() for w in ['task', 'goal', 'objective', 'needed to']),
            'action': any(w in answer.lower() for w in ['action', 'did', 'approach', 'implemented', 'decided']),
            'result': has_result
        }
        star_score = sum(star_elements.values())
        base_score += star_score * 0.5
    
    # Cap score at 10
    final_score = min(round(base_score, 1), 10.0)
    
    # Generate feedback
    strengths = []
    improvements = []
    
    # Identify strengths
    if word_count >= 100:
        strengths.append("Well-detailed response with good length")
    if has_example:
        strengths.append("Provided concrete examples from experience")
    if has_result:
        strengths.append("Mentioned outcomes and results")
    if has_numbers:
        strengths.append("Used quantifiable metrics")
    if sentiment == "positive":
        strengths.append("Positive and confident tone")
    
    # Identify improvements
    if word_count < 50:
        improvements.append("Expand your answer with more details")
    if not has_example:
        improvements.append("Include specific examples from your experience")
    if not has_result:
        improvements.append("Discuss the outcomes and impact of your actions")
    if not has_numbers:
        improvements.append("Add quantifiable metrics where possible (e.g., '30% improvement')")
    
    if category.lower() == "behavioral" and final_score < 8:
        improvements.append("Use the STAR method: Situation, Task, Action, Result")
    
    if category.lower() == "technical" and final_score < 8:
        improvements.append("Include more technical details and terminology")
    
    # Overall feedback
    if final_score >= 8:
        overall_feedback = "Excellent answer! You provided a detailed, well-structured response with relevant examples."
    elif final_score >= 6:
        overall_feedback = "Good answer with room for improvement. Consider adding more specific examples and details."
    elif final_score >= 4:
        overall_feedback = "Acceptable answer, but needs more depth. Focus on providing concrete examples and outcomes."
    else:
        overall_feedback = "Needs significant improvement. Provide more detailed responses with specific examples."
    
    return {
        "score": final_score,
        "overall_feedback": overall_feedback,
        "strengths": strengths if strengths else ["Answer provided"],
        "improvements": improvements if improvements else ["Continue practicing interview responses"],
        "sentiment": sentiment,
        "word_count": word_count,
        "has_example": has_example,
        "has_result": has_result
    }


def calculate_interview_score(evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate overall interview performance score from individual question evaluations.
    
    Args:
        evaluations: List of evaluation dictionaries from evaluate_answer
        
    Returns:
        Dictionary with overall score, grade, and summary
    """
    
    if not evaluations:
        return {
            "overall_score": 0,
            "average_score": 0,
            "grade": "F",
            "total_questions": 0,
            "summary": "No questions answered"
        }
    
    scores = [eval_data["score"] for eval_data in evaluations]
    average_score = sum(scores) / len(scores)
    overall_score = round(average_score * 10, 1)  # Convert to 100-point scale
    
    # Determine grade
    if overall_score >= 90:
        grade = "A+"
    elif overall_score >= 85:
        grade = "A"
    elif overall_score >= 80:
        grade = "B+"
    elif overall_score >= 75:
        grade = "B"
    elif overall_score >= 70:
        grade = "C+"
    elif overall_score >= 60:
        grade = "C"
    else:
        grade = "D"
    
    # Generate summary
    if overall_score >= 80:
        summary = "Outstanding performance! You demonstrated strong communication skills and provided excellent, detailed responses."
    elif overall_score >= 70:
        summary = "Good performance overall. You showed solid understanding but could improve in providing more specific examples."
    elif overall_score >= 60:
        summary = "Decent performance with room for improvement. Focus on structuring answers better and adding more detail."
    else:
        summary = "Needs improvement. Practice providing more detailed, structured responses with concrete examples."
    
    return {
        "overall_score": overall_score,
        "average_score": round(average_score, 2),
        "grade": grade,
        "total_questions": len(evaluations),
        "questions_answered": len([e for e in evaluations if e["score"] > 0]),
        "summary": summary,
        "category_breakdown": _calculate_category_breakdown(evaluations)
    }


def _calculate_category_breakdown(evaluations: List[Dict[str, Any]]) -> Dict[str, float]:
    """Helper function to calculate average scores by category"""
    category_scores = {}
    category_counts = {}
    
    for eval_data in evaluations:
        category = eval_data.get("category", "General")
        score = eval_data["score"]
        
        if category not in category_scores:
            category_scores[category] = 0
            category_counts[category] = 0
        
        category_scores[category] += score
        category_counts[category] += 1
    
    return {
        category: round(category_scores[category] / category_counts[category], 2)
        for category in category_scores
    }


if __name__ == "__main__":
    # Test the interview evaluator
    
    # Test question generation
    sample_job = """
    Senior Software Engineer position requiring 5+ years of experience with Python, 
    React, and AWS. Looking for someone with strong problem-solving skills and 
    experience in leading teams.
    """
    
    questions = generate_interview_questions(sample_job, "Senior Software Engineer", 5)
    
    print("=" * 80)
    print("GENERATED INTERVIEW QUESTIONS")
    print("=" * 80)
    for q in questions:
        print(f"\n{q['id']}. [{q['category']}] {q['question']}")
    
    # Test answer evaluation
    print("\n" + "=" * 80)
    print("ANSWER EVALUATION TEST")
    print("=" * 80)
    
    test_answer = """
    In my previous role at Tech Company, I worked on a project to optimize our API performance. 
    The situation was that our response times were averaging 2 seconds, which was affecting user experience.
    My task was to identify bottlenecks and implement solutions. I analyzed the code, identified 
    N+1 query issues, and implemented database query optimization and caching. As a result, 
    we reduced response times by 70% to around 600ms, which improved user satisfaction significantly.
    """
    
    evaluation = evaluate_answer(
        question="Describe a challenging technical problem you solved.",
        answer=test_answer,
        category="Technical",
        difficulty="medium"
    )
    
    print(f"\nScore: {evaluation['score']}/10")
    print(f"Feedback: {evaluation['overall_feedback']}")
    print(f"\nStrengths:")
    for s in evaluation['strengths']:
        print(f"  ✓ {s}")
    print(f"\nImprovements:")
    for i in evaluation['improvements']:
        print(f"  • {i}")
    
    # Test overall score calculation
    print("\n" + "=" * 80)
    print("OVERALL INTERVIEW SCORE")
    print("=" * 80)
    
    mock_evaluations = [
        {"score": 8.5, "category": "Introduction"},
        {"score": 7.5, "category": "Technical"},
        {"score": 9.0, "category": "Behavioral"},
        {"score": 6.5, "category": "Technical"},
        {"score": 8.0, "category": "Motivation"}
    ]
    
    overall = calculate_interview_score(mock_evaluations)
    print(f"\nOverall Score: {overall['overall_score']}/100")
    print(f"Grade: {overall['grade']}")
    print(f"Average per Question: {overall['average_score']}/10")
    print(f"Summary: {overall['summary']}")
    print(f"\nCategory Breakdown:")
    for cat, score in overall['category_breakdown'].items():
        print(f"  {cat}: {score}/10")
