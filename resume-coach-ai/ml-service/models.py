"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class PredictRequest(BaseModel):
    """Request model for match prediction"""
    resume_text: str = Field(..., min_length=10, description="Resume text content")
    job_description: str = Field(..., min_length=10, description="Job description text")
    
    class Config:
        json_schema_extra = {
            "example": {
                "resume_text": "Senior Python Developer with 5 years of experience in Django, FastAPI, and machine learning. Built scalable APIs and ML models.",
                "job_description": "Looking for Python Developer with experience in FastAPI and ML. 3+ years required. Django is a plus."
            }
        }


class PredictResponse(BaseModel):
    """Response model for match prediction"""
    match_score: float = Field(..., ge=0, le=100, description="Match score between 0-100")
    confidence: float = Field(..., ge=0, le=1, description="Model confidence (0-1)")
    keywords_matched: List[str] = Field(default_factory=list, description="Common keywords found")
    recommendation: str = Field(..., description="Match recommendation category")
    
    class Config:
        json_schema_extra = {
            "example": {
                "match_score": 78.45,
                "confidence": 0.92,
                "keywords_matched": ["python", "django", "fastapi", "ml"],
                "recommendation": "Strong Match"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    version: str
    
    class Config:
        protected_namespaces = ()  # Allow model_* field names


class JobParseRequest(BaseModel):
    """Request model for job description parsing"""
    job_description: str = Field(..., min_length=10, description="Job description text to parse")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_description": "Senior Software Engineer with 5+ years in Python and React. Bachelor's degree required. Salary: $120k-$150k. Location: San Francisco."
            }
        }


class JobParseResponse(BaseModel):
    """Response model for parsed job description"""
    skills: List[str] = Field(default_factory=list, description="Extracted technical skills")
    experience_years: Optional[str] = Field(None, description="Required years of experience")
    qualifications: List[str] = Field(default_factory=list, description="Education/certification requirements")
    salary: Optional[str] = Field(None, description="Salary information if found")
    location: Optional[str] = Field(None, description="Job location if found")
    entities: List[Dict[str, str]] = Field(default_factory=list, description="Named entities extracted")
    job_title: Optional[str] = Field(None, description="Detected job title")
    company: Optional[str] = Field(None, description="Company name if found")
    
    class Config:
        json_schema_extra = {
            "example": {
                "skills": ["Python", "React", "AWS", "Docker"],
                "experience_years": "5+ years",
                "qualifications": ["Bachelor'S Degree In Computer Science"],
                "salary": "$120,000 - $150,000 per year",
                "location": "San Francisco, CA",
                "entities": [{"text": "ABC Tech Company", "label": "ORG"}],
                "job_title": "Senior Software Engineer",
                "company": "ABC Tech Company"
            }
        }


class ATSOptimizeRequest(BaseModel):
    """Request model for ATS optimization"""
    resume_text: str = Field(..., min_length=10, description="Resume text content")
    job_description: str = Field(..., min_length=10, description="Job description text")
    
    class Config:
        json_schema_extra = {
            "example": {
                "resume_text": "Senior Software Engineer with 5 years in Python development. Built scalable web applications using Django and Flask.",
                "job_description": "Seeking Senior Software Engineer with 5+ years experience in Python, JavaScript, React, and AWS cloud technologies."
            }
        }


class ATSOptimizeResponse(BaseModel):
    """Response model for ATS optimization analysis"""
    ats_score: float = Field(..., ge=0, le=100, description="Overall ATS compatibility score (0-100)")
    keyword_match_percentage: float = Field(..., ge=0, le=100, description="Percentage of job keywords in resume")
    missing_keywords: List[str] = Field(default_factory=list, description="Important keywords missing from resume")
    matched_keywords: List[str] = Field(default_factory=list, description="Keywords found in both resume and job")
    suggestions: List[str] = Field(default_factory=list, description="Actionable optimization suggestions")
    tfidf_similarity: float = Field(..., ge=0, le=1, description="TF-IDF cosine similarity score")
    resume_keyword_count: int = Field(..., description="Number of keywords extracted from resume")
    job_keyword_count: int = Field(..., description="Number of keywords extracted from job description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ats_score": 65.5,
                "keyword_match_percentage": 58.3,
                "missing_keywords": ["react", "aws", "kubernetes", "docker"],
                "matched_keywords": ["python", "django", "flask", "software", "engineer"],
                "suggestions": [
                    "✓ Good: Resume is reasonably matched. Minor improvements can boost ATS score.",
                    "Improve keyword density: 58.3% match is decent but could be better.",
                    "Consider adding these keywords: react, aws, kubernetes"
                ],
                "tfidf_similarity": 0.6543,
                "resume_keyword_count": 45,
                "job_keyword_count": 38
            }
        }


class InterviewQuestion(BaseModel):
    """Model for an interview question"""
    id: int = Field(..., description="Question ID")
    question: str = Field(..., min_length=10, description="Interview question text")
    category: str = Field(..., description="Question category (Introduction, Technical, Behavioral, etc.)")
    difficulty: str = Field(..., description="Difficulty level (easy, medium, hard)")


class GenerateQuestionsRequest(BaseModel):
    """Request model for generating interview questions"""
    job_description: str = Field(..., min_length=20, description="Job description text")
    job_role: Optional[str] = Field("", description="Job title/role")
    num_questions: int = Field(5, ge=3, le=10, description="Number of questions to generate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_description": "Senior Software Engineer with 5+ years experience in Python and React. Strong problem-solving skills required.",
                "job_role": "Senior Software Engineer",
                "num_questions": 5
            }
        }


class GenerateQuestionsResponse(BaseModel):
    """Response model for generated interview questions"""
    questions: List[InterviewQuestion] = Field(..., description="List of generated questions")
    total_questions: int = Field(..., description="Total number of questions generated")
    
    class Config:
        json_schema_extra = {
            "example": {
                "questions": [
                    {
                        "id": 1,
                        "question": "Tell me about yourself and your background.",
                        "category": "Introduction",
                        "difficulty": "easy"
                    },
                    {
                        "id": 2,
                        "question": "Describe your experience with Python and how you've used it in past projects.",
                        "category": "Technical",
                        "difficulty": "medium"
                    }
                ],
                "total_questions": 5
            }
        }


class EvaluateAnswerRequest(BaseModel):
    """Request model for evaluating an interview answer"""
    question: str = Field(..., min_length=10, description="Interview question")
    answer: str = Field(..., min_length=1, description="User's answer")
    category: str = Field("General", description="Question category")
    difficulty: str = Field("medium", description="Question difficulty")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Tell me about a challenging project you worked on.",
                "answer": "In my previous role, I led a team to migrate our monolithic application to microservices. We faced challenges with data consistency but successfully completed the migration in 6 months, reducing deployment time by 60%.",
                "category": "Behavioral",
                "difficulty": "medium"
            }
        }


class EvaluateAnswerResponse(BaseModel):
    """Response model for answer evaluation"""
    score: float = Field(..., ge=0, le=10, description="Answer score out of 10")
    overall_feedback: str = Field(..., description="Overall feedback on the answer")
    strengths: List[str] = Field(default_factory=list, description="Identified strengths in the answer")
    improvements: List[str] = Field(default_factory=list, description="Suggested improvements")
    sentiment: str = Field(..., description="Detected sentiment (positive, negative, neutral)")
    word_count: int = Field(..., description="Number of words in answer")
    has_example: bool = Field(..., description="Whether answer includes examples")
    has_result: bool = Field(..., description="Whether answer mentions results/outcomes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "score": 8.5,
                "overall_feedback": "Excellent answer! You provided a detailed, well-structured response with relevant examples.",
                "strengths": [
                    "Well-detailed response with good length",
                    "Provided concrete examples from experience",
                    "Mentioned outcomes and results",
                    "Used quantifiable metrics"
                ],
                "improvements": [
                    "Consider adding more technical details about the migration process"
                ],
                "sentiment": "positive",
                "word_count": 87,
                "has_example": True,
                "has_result": True
            }
        }


class InterviewScoreRequest(BaseModel):
    """Request model for calculating overall interview score"""
    evaluations: List[Dict[str, Any]] = Field(..., description="List of evaluation results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "evaluations": [
                    {"score": 8.5, "category": "Introduction"},
                    {"score": 7.5, "category": "Technical"},
                    {"score": 9.0, "category": "Behavioral"}
                ]
            }
        }


class InterviewScoreResponse(BaseModel):
    """Response model for overall interview score"""
    overall_score: float = Field(..., ge=0, le=100, description="Overall interview score (0-100)")
    average_score: float = Field(..., ge=0, le=10, description="Average score per question (0-10)")
    grade: str = Field(..., description="Letter grade (A+, A, B+, etc.)")
    total_questions: int = Field(..., description="Total number of questions")
    questions_answered: int = Field(..., description="Number of questions answered")
    summary: str = Field(..., description="Overall performance summary")
    category_breakdown: Dict[str, float] = Field(default_factory=dict, description="Average scores by category")
    
    class Config:
        json_schema_extra = {
            "example": {
                "overall_score": 83.3,
                "average_score": 8.33,
                "grade": "B+",
                "total_questions": 5,
                "questions_answered": 5,
                "summary": "Outstanding performance! You demonstrated strong communication skills and provided excellent, detailed responses.",
                "category_breakdown": {
                    "Introduction": 8.5,
                    "Technical": 7.0,
                    "Behavioral": 9.0,
                    "Motivation": 8.0
                }
            }
        }
