"""
ATS (Applicant Tracking System) Optimization Module
Analyzes resume-job match for ATS compatibility and provides optimization suggestions.
"""

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from typing import Dict, List, Set, Any
from collections import Counter
import string

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Get English stopwords
STOP_WORDS = set(stopwords.words('english'))


def preprocess_text(text: str) -> str:
    """
    Preprocess text for analysis.
    - Convert to lowercase
    - Remove punctuation
    - Remove extra whitespace
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def extract_keywords(text: str, top_n: int = 50) -> List[str]:
    """
    Extract important keywords from text using TF-IDF.
    Filters out stopwords and short words.
    """
    # Preprocess
    text = preprocess_text(text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Filter: remove stopwords, punctuation, short words
    filtered_tokens = [
        token for token in tokens
        if token not in STOP_WORDS
        and token not in string.punctuation
        and len(token) > 2
        and token.isalpha()
    ]
    
    # Get most common keywords
    counter = Counter(filtered_tokens)
    keywords = [word for word, count in counter.most_common(top_n)]
    
    return keywords


def calculate_tfidf_similarity(resume_text: str, job_description: str) -> float:
    """
    Calculate TF-IDF cosine similarity between resume and job description.
    Returns a score between 0 and 1.
    """
    # Preprocess texts
    resume_clean = preprocess_text(resume_text)
    job_clean = preprocess_text(job_description)
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=500,
        stop_words='english',
        ngram_range=(1, 2)  # Include bigrams
    )
    
    try:
        # Fit and transform
        vectors = vectorizer.fit_transform([resume_clean, job_clean])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        
        return float(similarity)
    except Exception:
        # Return 0 if vectorization fails
        return 0.0


def calculate_keyword_match(resume_keywords: List[str], job_keywords: List[str]) -> float:
    """
    Calculate keyword match percentage.
    Returns percentage of job keywords found in resume.
    """
    if not job_keywords:
        return 0.0
    
    resume_set = set(word.lower() for word in resume_keywords)
    job_set = set(word.lower() for word in job_keywords)
    
    # Find intersection
    matched = resume_set.intersection(job_set)
    
    # Calculate percentage
    match_percentage = (len(matched) / len(job_set)) * 100
    
    return round(match_percentage, 2)


def identify_missing_keywords(resume_keywords: List[str], job_keywords: List[str], top_n: int = 15) -> List[str]:
    """
    Identify important keywords from job description that are missing in resume.
    """
    resume_set = set(word.lower() for word in resume_keywords)
    job_set = set(word.lower() for word in job_keywords)
    
    # Find missing keywords
    missing = job_set - resume_set
    
    # Return top N missing keywords
    return list(missing)[:top_n]


def generate_suggestions(
    ats_score: float,
    keyword_match: float,
    missing_keywords: List[str],
    resume_text: str,
    job_description: str
) -> List[str]:
    """
    Generate actionable optimization suggestions based on analysis.
    """
    suggestions = []
    
    # Score-based suggestions (ats_score is 0-100, not 0-1)
    if ats_score < 30:
        suggestions.append("❌ Critical: Your resume has very low relevance to this job (Score: {:.1f}/100). Consider rewriting to highlight relevant experience.".format(ats_score))
    elif ats_score < 50:
        suggestions.append("⚠️ Warning: Resume relevance is below average (Score: {:.1f}/100). Add more job-specific keywords and skills.".format(ats_score))
    elif ats_score < 70:
        suggestions.append("✓ Good: Resume is reasonably matched (Score: {:.1f}/100). Minor improvements can boost ATS score.".format(ats_score))
    else:
        suggestions.append("✅ Excellent: Resume is well-optimized for this job description (Score: {:.1f}/100).".format(ats_score))
    
    # Keyword match suggestions
    if keyword_match < 40:
        suggestions.append(f"Add missing keywords: Your resume matches only {keyword_match}% of job keywords. Incorporate more relevant terms.")
    elif keyword_match < 60:
        suggestions.append(f"Improve keyword density: {keyword_match}% match is decent but could be better. Add more technical skills and qualifications.")
    else:
        suggestions.append(f"Strong keyword alignment: {keyword_match}% of job keywords are present in your resume.")
    
    # Missing keywords suggestions
    if len(missing_keywords) > 10:
        top_missing = missing_keywords[:5]
        suggestions.append(f"High-priority keywords to add: {', '.join(top_missing)}")
    elif len(missing_keywords) > 5:
        suggestions.append(f"Consider adding these keywords: {', '.join(missing_keywords[:3])}")
    
    # Content-specific suggestions
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    # Check for experience mentions
    if 'experience' in job_lower and 'experience' not in resume_lower:
        suggestions.append("Add an 'Experience' section if you have relevant work history.")
    
    # Check for education mentions
    if any(word in job_lower for word in ['degree', 'bachelor', 'master', 'education']) and \
       'education' not in resume_lower:
        suggestions.append("Include your education qualifications prominently.")
    
    # Check for skills section
    if 'skills' in job_lower and 'skills' not in resume_lower:
        suggestions.append("Create a dedicated 'Skills' section listing technical and soft skills.")
    
    # Check for certifications
    if 'certification' in job_lower or 'certified' in job_lower:
        if 'certification' not in resume_lower and 'certified' not in resume_lower:
            suggestions.append("Add any relevant certifications if you have them.")
    
    # Format suggestions
    if len(resume_text) < 500:
        suggestions.append("Resume seems too short. Expand descriptions to 1-2 pages for better ATS parsing.")
    
    # Action items
    suggestions.append("💡 Pro tip: Mirror the job description's language and terminology where truthful.")
    suggestions.append("💡 Use standard section headings: Experience, Education, Skills, Certifications.")
    suggestions.append("💡 Quantify achievements with metrics (e.g., 'Improved performance by 30%').")
    
    return suggestions


def optimize_ats(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Main function to analyze ATS compatibility and provide optimization recommendations.
    
    Args:
        resume_text: Full text content of resume
        job_description: Full text of job posting
        
    Returns:
        Dictionary containing:
        - ats_score: Overall ATS compatibility score (0-100)
        - keyword_match_percentage: Percentage of job keywords in resume
        - missing_keywords: List of important missing keywords
        - matched_keywords: List of keywords found in both
        - suggestions: List of actionable recommendations
        - tfidf_similarity: Raw TF-IDF similarity score (0-1)
    """
    
    # Extract keywords from both texts
    resume_keywords = extract_keywords(resume_text, top_n=100)
    job_keywords = extract_keywords(job_description, top_n=100)
    
    # Calculate TF-IDF similarity
    tfidf_sim = calculate_tfidf_similarity(resume_text, job_description)
    
    # Calculate keyword match
    keyword_match = calculate_keyword_match(resume_keywords, job_keywords)
    
    # Identify missing keywords
    missing_keywords = identify_missing_keywords(resume_keywords, job_keywords, top_n=15)
    
    # Find matched keywords
    resume_set = set(word.lower() for word in resume_keywords)
    job_set = set(word.lower() for word in job_keywords)
    matched_keywords = list(resume_set.intersection(job_set))[:20]
    
    # Calculate overall ATS score (weighted combination)
    # 60% TF-IDF similarity + 40% keyword match
    ats_score = round((tfidf_sim * 60) + (keyword_match * 0.4), 2)
    
    # Generate suggestions
    suggestions = generate_suggestions(
        ats_score=ats_score,
        keyword_match=keyword_match,
        missing_keywords=missing_keywords,
        resume_text=resume_text,
        job_description=job_description
    )
    
    return {
        "ats_score": ats_score,
        "keyword_match_percentage": keyword_match,
        "missing_keywords": missing_keywords,
        "matched_keywords": matched_keywords,
        "suggestions": suggestions,
        "tfidf_similarity": round(tfidf_sim, 4),
        "resume_keyword_count": len(resume_keywords),
        "job_keyword_count": len(job_keywords)
    }


if __name__ == "__main__":
    # Test with sample data
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
    """
    
    result = optimize_ats(sample_resume, sample_job)
    
    print("=" * 60)
    print("ATS OPTIMIZATION ANALYSIS")
    print("=" * 60)
    print(f"\n📊 ATS Score: {result['ats_score']}/100")
    print(f"🎯 Keyword Match: {result['keyword_match_percentage']}%")
    print(f"📈 TF-IDF Similarity: {result['tfidf_similarity']}")
    print(f"\n✅ Matched Keywords ({len(result['matched_keywords'])}):")
    print(", ".join(result['matched_keywords'][:10]))
    print(f"\n❌ Missing Keywords ({len(result['missing_keywords'])}):")
    print(", ".join(result['missing_keywords']))
    print(f"\n💡 Suggestions ({len(result['suggestions'])}):")
    for i, suggestion in enumerate(result['suggestions'], 1):
        print(f"{i}. {suggestion}")
    print("\n" + "=" * 60)
