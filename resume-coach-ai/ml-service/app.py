"""
FastAPI application for Resume-Job Match Scoring
Exposes ML model predictions via REST API
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import torch
from models import (
    PredictRequest, PredictResponse, HealthResponse, 
    JobParseRequest, JobParseResponse, 
    ATSOptimizeRequest, ATSOptimizeResponse,
    GenerateQuestionsRequest, GenerateQuestionsResponse,
    EvaluateAnswerRequest, EvaluateAnswerResponse,
    InterviewScoreRequest, InterviewScoreResponse
)
import logging
from typing import List
import re
import job_parser
import ats_optimizer
import interview_evaluator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Resume Scorer API",
    description="ML-powered API for scoring resume-job matches",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model
model = None
tokenizer = None
device = None

# Technical skills database
TECHNICAL_SKILLS = [
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
    'swift', 'kotlin', 'scala', 'r', 'php', 'sql', 'nosql', 'mongodb', 'postgresql',
    'mysql', 'redis', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
    'flask', 'fastapi', 'spring', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
    'pandas', 'numpy', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins',
    'git', 'linux', 'html', 'css', 'rest', 'graphql', 'microservices', 'agile'
]


@app.on_event("startup")
async def load_model():
    """Load the trained model on startup"""
    global model, tokenizer, device
    
    try:
        logger.info("Loading trained model...")
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {device}")
        
        model = DistilBertForSequenceClassification.from_pretrained('./models/resume_scorer')
        tokenizer = DistilBertTokenizer.from_pretrained('./models/resume_scorer')
        
        model.to(device)
        model.eval()
        
        logger.info("✅ Model loaded successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error loading model: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down API...")


def extract_keywords(resume: str, job: str) -> List[str]:
    """Extract common technical keywords from resume and job description"""
    resume_lower = resume.lower()
    job_lower = job.lower()
    
    matched_keywords = []
    for skill in TECHNICAL_SKILLS:
        if skill in resume_lower and skill in job_lower:
            matched_keywords.append(skill)
    
    return matched_keywords[:10]  # Return top 10


def get_recommendation(score: float) -> str:
    """Get recommendation category based on score"""
    if score >= 80:
        return "Excellent Match"
    elif score >= 70:
        return "Strong Match"
    elif score >= 60:
        return "Good Match"
    elif score >= 50:
        return "Moderate Match"
    elif score >= 40:
        return "Fair Match"
    else:
        return "Weak Match"


def calculate_confidence(score: float) -> float:
    """Calculate confidence based on prediction score variance"""
    # Higher confidence for scores near the training mean (75)
    distance_from_mean = abs(score - 75.0)
    confidence = max(0.5, 1.0 - (distance_from_mean / 150))
    return round(confidence, 2)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Resume Scorer API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        version="1.0.0"
    )


@app.post("/predict-match", response_model=PredictResponse, tags=["Prediction"])
async def predict_match(request: PredictRequest):
    """
    Predict match score between resume and job description
    
    Args:
        request: PredictRequest with resume_text and job_description
        
    Returns:
        PredictResponse with match_score, confidence, keywords, and recommendation
    """
    if model is None or tokenizer is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please check server logs."
        )
    
    try:
        # Combine resume and job description
        text = f"Resume: {request.resume_text} [SEP] Job: {request.job_description}"
        
        # Tokenize input
        inputs = tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # Move to device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Get prediction
        with torch.no_grad():
            outputs = model(**inputs)
            # Model outputs logits in range 0-1, scale to 0-100
            score = outputs.logits.item() * 100
            score = max(0, min(100, score))  # Clamp to 0-100
        
        # Extract common keywords
        keywords = extract_keywords(request.resume_text, request.job_description)
        
        # Calculate confidence
        confidence = calculate_confidence(score)
        
        # Get recommendation
        recommendation = get_recommendation(score)
        
        logger.info(f"Prediction: {score:.2f}, Confidence: {confidence}, Keywords: {len(keywords)}")
        
        return PredictResponse(
            match_score=round(score, 2),
            confidence=confidence,
            keywords_matched=keywords,
            recommendation=recommendation
        )
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/parse-job", response_model=JobParseResponse, tags=["Job Parser"])
async def parse_job_description(request: JobParseRequest):
    """
    Parse job description and extract structured information
    
    Args:
        request: JobParseRequest with job_description text
        
    Returns:
        JobParseResponse with extracted skills, experience, qualifications, salary, location, etc.
    """
    try:
        # Parse job description using NLP
        result = job_parser.parse_job_description(request.job_description)
        
        logger.info(f"Job parsing successful: {len(result['skills'])} skills found")
        
        return JobParseResponse(
            skills=result['skills'],
            experience_years=result['experience_years'],
            qualifications=result['qualifications'],
            salary=result['salary'],
            location=result['location'],
            entities=result['entities'],
            job_title=result['job_title'],
            company=result['company']
        )
        
    except Exception as e:
        logger.error(f"Error parsing job description: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job parsing failed: {str(e)}"
        )


@app.post("/optimize-ats", response_model=ATSOptimizeResponse, tags=["ATS Optimization"])
async def optimize_ats(request: ATSOptimizeRequest):
    """
    Analyze ATS compatibility and provide optimization recommendations
    
    Args:
        request: ATSOptimizeRequest with resume_text and job_description
        
    Returns:
        ATSOptimizeResponse with ATS score, keyword analysis, and suggestions
    """
    try:
        # Run ATS optimization analysis
        result = ats_optimizer.optimize_ats(
            request.resume_text,
            request.job_description
        )
        
        logger.info(
            f"ATS optimization complete: Score={result['ats_score']}, "
            f"Keyword Match={result['keyword_match_percentage']}%, "
            f"Missing Keywords={len(result['missing_keywords'])}"
        )
        
        return ATSOptimizeResponse(
            ats_score=result['ats_score'],
            keyword_match_percentage=result['keyword_match_percentage'],
            missing_keywords=result['missing_keywords'],
            matched_keywords=result['matched_keywords'],
            suggestions=result['suggestions'],
            tfidf_similarity=result['tfidf_similarity'],
            resume_keyword_count=result['resume_keyword_count'],
            job_keyword_count=result['job_keyword_count']
        )
        
    except Exception as e:
        logger.error(f"Error during ATS optimization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ATS optimization failed: {str(e)}"
        )


@app.post("/interview/generate-questions", response_model=GenerateQuestionsResponse, tags=["Interview Simulation"])
async def generate_interview_questions(request: GenerateQuestionsRequest):
    """
    Generate interview questions based on job description and role
    
    Args:
        request: GenerateQuestionsRequest with job_description, job_role, and num_questions
        
    Returns:
        GenerateQuestionsResponse with list of generated questions
    """
    try:
        logger.info(f"Generating {request.num_questions} interview questions for role: {request.job_role}")
        
        # Generate questions using interview evaluator
        questions = interview_evaluator.generate_interview_questions(
            job_description=request.job_description,
            job_role=request.job_role,
            num_questions=request.num_questions
        )
        
        logger.info(f"Successfully generated {len(questions)} interview questions")
        
        return GenerateQuestionsResponse(
            questions=questions,
            total_questions=len(questions)
        )
        
    except Exception as e:
        logger.error(f"Error generating interview questions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Question generation failed: {str(e)}"
        )


@app.post("/interview/evaluate-answer", response_model=EvaluateAnswerResponse, tags=["Interview Simulation"])
async def evaluate_interview_answer(request: EvaluateAnswerRequest):
    """
    Evaluate an interview answer and provide scoring and feedback
    
    Args:
        request: EvaluateAnswerRequest with question, answer, category, and difficulty
        
    Returns:
        EvaluateAnswerResponse with score, feedback, strengths, and improvements
    """
    try:
        logger.info(f"Evaluating answer for question: {request.question[:50]}...")
        
        # Evaluate answer using interview evaluator
        evaluation = interview_evaluator.evaluate_answer(
            question=request.question,
            answer=request.answer,
            category=request.category,
            difficulty=request.difficulty
        )
        
        logger.info(f"Answer evaluated: Score={evaluation['score']}/10, Word count={evaluation['word_count']}")
        
        return EvaluateAnswerResponse(**evaluation)
        
    except Exception as e:
        logger.error(f"Error evaluating interview answer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Answer evaluation failed: {str(e)}"
        )


@app.post("/interview/calculate-score", response_model=InterviewScoreResponse, tags=["Interview Simulation"])
async def calculate_interview_score(request: InterviewScoreRequest):
    """
    Calculate overall interview performance score from individual evaluations
    
    Args:
        request: InterviewScoreRequest with list of evaluation results
        
    Returns:
        InterviewScoreResponse with overall score, grade, and summary
    """
    try:
        logger.info(f"Calculating overall interview score for {len(request.evaluations)} questions")
        
        # Calculate overall score
        result = interview_evaluator.calculate_interview_score(request.evaluations)
        
        logger.info(
            f"Interview score calculated: {result['overall_score']}/100, "
            f"Grade={result['grade']}, Questions={result['total_questions']}"
        )
        
        return InterviewScoreResponse(**result)
        
    except Exception as e:
        logger.error(f"Error calculating interview score: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Score calculation failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error occurred"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)