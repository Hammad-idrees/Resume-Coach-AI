"""
Job Description Parser Module
Uses spaCy NLP and regex to extract structured information from job descriptions.
Extracts: skills, experience requirements, qualifications, salary, location, entities.
"""

import spacy
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Load skills database
SKILLS_DB_PATH = Path(__file__).parent / "skills_database.json"
with open(SKILLS_DB_PATH, "r") as f:
    skills_data = json.load(f)

# Flatten all skills into a single list for matching
SKILLS_DB = []
for category, skills_list in skills_data.items():
    SKILLS_DB.extend(skills_list)

# Remove duplicates and sort for efficient matching
SKILLS_DB = sorted(set(SKILLS_DB), key=lambda x: len(x), reverse=True)


def parse_job_description(text: str) -> Dict[str, Any]:
    """
    Parse a job description and extract structured information.
    
    Args:
        text: Raw job description text
        
    Returns:
        Dictionary containing:
        - skills: List of technical skills found
        - experience_years: Years of experience required (if found)
        - qualifications: Education/certification requirements
        - salary: Salary range (if mentioned)
        - location: Job location (if mentioned)
        - entities: Named entities extracted by spaCy
        - job_title: Detected job title (if found)
        - company: Company name (if found)
    """
    
    # Process text with spaCy
    doc = nlp(text)
    
    # Extract skills by matching against database
    skills = extract_skills(text)
    
    # Extract experience requirements
    experience = extract_experience(text)
    
    # Extract qualifications/education
    qualifications = extract_qualifications(text)
    
    # Extract salary information
    salary = extract_salary(text)
    
    # Extract location
    location = extract_location(doc)
    
    # Extract entities using spaCy NER
    entities = extract_entities(doc)
    
    # Try to detect job title
    job_title = extract_job_title(doc, text)
    
    # Try to detect company name
    company = extract_company(doc)
    
    return {
        "skills": skills,
        "experience_years": experience,
        "qualifications": qualifications,
        "salary": salary,
        "location": location,
        "entities": entities,
        "job_title": job_title,
        "company": company
    }


def extract_skills(text: str) -> List[str]:
    """
    Extract technical skills from text by matching against skills database.
    Uses case-insensitive matching and handles word boundaries.
    """
    text_lower = text.lower()
    found_skills = []
    
    for skill in SKILLS_DB:
        skill_lower = skill.lower()
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, text_lower):
            # Add original casing from database
            if skill not in found_skills:
                found_skills.append(skill)
    
    return found_skills


def extract_experience(text: str) -> Optional[str]:
    """
    Extract years of experience required using regex patterns.
    Matches patterns like: "3+ years", "5-7 years", "minimum 2 years", etc.
    """
    patterns = [
        r'(\d+)\+?\s*(?:to|\-)\s*(\d+)\s*years?',  # 3-5 years, 3 to 5 years
        r'(\d+)\+\s*years?',  # 3+ years
        r'minimum\s+(\d+)\s*years?',  # minimum 3 years
        r'at least\s+(\d+)\s*years?',  # at least 3 years
        r'(\d+)\s*years?.*experience',  # 3 years of experience
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            if len(match.groups()) == 2:
                # Range found (e.g., 3-5 years)
                return f"{match.group(1)}-{match.group(2)} years"
            else:
                # Single value found
                return f"{match.group(1)}+ years"
    
    return None


def extract_qualifications(text: str) -> List[str]:
    """
    Extract education and qualification requirements.
    Looks for degree levels, certifications, and specific qualifications.
    """
    qualifications = []
    
    # Common degree patterns
    degree_patterns = [
        r"bachelor'?s?\s+(?:degree)?(?:\s+in\s+[\w\s]+)?",
        r"master'?s?\s+(?:degree)?(?:\s+in\s+[\w\s]+)?",
        r"phd|doctorate|doctoral\s+(?:degree)?",
        r"associate'?s?\s+(?:degree)?",
        r"b\.?s\.?|m\.?s\.?|m\.?b\.?a\.?|ph\.?d\.?",
        r"(?:bachelor|master|doctoral)\s+(?:of\s+)?(?:science|arts|engineering|business)",
    ]
    
    text_lower = text.lower()
    for pattern in degree_patterns:
        matches = re.finditer(pattern, text_lower)
        for match in matches:
            qual = match.group(0).strip()
            if qual and qual not in [q.lower() for q in qualifications]:
                # Capitalize properly
                qualifications.append(qual.title())
    
    # Look for certification mentions
    if re.search(r'certification|certified', text_lower):
        cert_match = re.search(r'([A-Z]{2,}(?:\s+[A-Z]{2,})*)\s+certified', text, re.IGNORECASE)
        if cert_match:
            qualifications.append(f"{cert_match.group(1)} Certified")
    
    return qualifications


def extract_salary(text: str) -> Optional[str]:
    """
    Extract salary information from text.
    Matches patterns like: $80,000 - $100,000, $80k-$100k, etc.
    """
    # Salary range patterns
    patterns = [
        r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:to|\-)\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:per\s+year|annually|/year)?',
        r'\$\s*(\d+)k?\s*(?:to|\-)\s*\$?\s*(\d+)k?\s*(?:per\s+year|annually|/year)?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    
    # Single salary value
    single_pattern = r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:per\s+year|annually|/year)'
    match = re.search(single_pattern, text, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    
    return None


def extract_location(doc) -> Optional[str]:
    """
    Extract location from spaCy NER entities.
    Looks for GPE (geopolitical entity) and LOC (location) entities.
    """
    locations = []
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            if ent.text not in locations:
                locations.append(ent.text)
    
    if locations:
        # Return the first location or combine multiple
        return ", ".join(locations[:2])  # Limit to 2 locations
    
    return None


def extract_entities(doc) -> List[Dict[str, str]]:
    """
    Extract all named entities using spaCy NER.
    Returns list of entities with their text and label.
    """
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })
    
    return entities


def extract_job_title(doc, text: str) -> Optional[str]:
    """
    Try to detect the job title from the text.
    Uses heuristics like looking at the beginning or for WORK_OF_ART entities.
    """
    # Check first few lines for job title
    lines = text.strip().split('\n')
    if lines:
        first_line = lines[0].strip()
        # If first line is short and doesn't contain common words, likely a title
        if len(first_line.split()) <= 8 and not any(word in first_line.lower() for word in ['the', 'we', 'are', 'is', 'company']):
            return first_line
    
    # Look for pattern like "Position: Senior Software Engineer"
    title_pattern = r'(?:position|title|role):\s*(.+?)(?:\n|$)'
    match = re.search(title_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    return None


def extract_company(doc) -> Optional[str]:
    """
    Try to detect company name from ORG entities.
    """
    for ent in doc.ents:
        if ent.label_ == "ORG":
            return ent.text
    
    return None


if __name__ == "__main__":
    # Test with sample job description
    sample_job = """
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
    """
    
    result = parse_job_description(sample_job)
    print("Parsed Job Description:")
    print(json.dumps(result, indent=2))
