"""
Create a high-quality synthetic dataset with accurate match scores
Uses rule-based logic to generate reliable training labels
"""

import pandas as pd
import numpy as np
import os

# Define job categories with their key skills
JOB_CATEGORIES = {
    'Software Engineer': {
        'skills': ['python', 'java', 'javascript', 'react', 'node.js', 'django', 'spring', 'sql', 'git', 'api'],
        'years_range': (2, 8),
        'common_titles': ['software engineer', 'developer', 'programmer', 'software developer']
    },
    'Data Scientist': {
        'skills': ['python', 'machine learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'sql', 'statistics', 'nlp', 'deep learning'],
        'years_range': (2, 6),
        'common_titles': ['data scientist', 'ml engineer', 'ai engineer']
    },
    'Full Stack Developer': {
        'skills': ['javascript', 'react', 'node.js', 'mongodb', 'express', 'html', 'css', 'typescript', 'rest api'],
        'years_range': (2, 7),
        'common_titles': ['full stack', 'fullstack', 'mern', 'mean stack']
    },
    'DevOps Engineer': {
        'skills': ['aws', 'docker', 'kubernetes', 'jenkins', 'terraform', 'linux', 'ci/cd', 'ansible', 'git'],
        'years_range': (3, 8),
        'common_titles': ['devops', 'cloud engineer', 'infrastructure']
    },
    'Frontend Developer': {
        'skills': ['react', 'javascript', 'html', 'css', 'typescript', 'vue', 'angular', 'webpack', 'sass'],
        'years_range': (1, 6),
        'common_titles': ['frontend', 'ui developer', 'web developer']
    },
    'Backend Developer': {
        'skills': ['python', 'java', 'node.js', 'sql', 'postgresql', 'mongodb', 'rest api', 'microservices', 'redis'],
        'years_range': (2, 7),
        'common_titles': ['backend', 'api developer', 'server developer']
    },
    'Mobile Developer': {
        'skills': ['react native', 'flutter', 'kotlin', 'swift', 'android', 'ios', 'mobile', 'firebase'],
        'years_range': (2, 6),
        'common_titles': ['mobile developer', 'android developer', 'ios developer']
    },
    'QA Engineer': {
        'skills': ['testing', 'selenium', 'pytest', 'junit', 'cypress', 'automation', 'api testing', 'quality assurance'],
        'years_range': (2, 6),
        'common_titles': ['qa engineer', 'test engineer', 'quality analyst']
    }
}

def generate_resume(category, match_level='high'):
    """Generate a synthetic resume"""
    cat_info = JOB_CATEGORIES[category]
    
    if match_level == 'high':
        # Include 70-100% of required skills
        num_skills = np.random.randint(int(len(cat_info['skills']) * 0.7), len(cat_info['skills']) + 1)
        skills = np.random.choice(cat_info['skills'], size=num_skills, replace=False).tolist()
        years = np.random.randint(cat_info['years_range'][0], cat_info['years_range'][1] + 2)
    elif match_level == 'medium':
        # Include 40-70% of required skills
        num_skills = np.random.randint(int(len(cat_info['skills']) * 0.4), int(len(cat_info['skills']) * 0.7) + 1)
        skills = np.random.choice(cat_info['skills'], size=num_skills, replace=False).tolist()
        # Add some irrelevant skills
        other_cats = [c for c in JOB_CATEGORIES if c != category]
        other_cat = np.random.choice(other_cats)
        skills += np.random.choice(JOB_CATEGORIES[other_cat]['skills'], size=2, replace=False).tolist()
        years = np.random.randint(1, cat_info['years_range'][1])
    else:  # low match
        # Include 0-40% of required skills
        num_skills = np.random.randint(0, int(len(cat_info['skills']) * 0.4) + 1)
        if num_skills > 0:
            skills = np.random.choice(cat_info['skills'], size=num_skills, replace=False).tolist()
        else:
            skills = []
        # Mostly irrelevant skills
        other_cats = [c for c in JOB_CATEGORIES if c != category]
        other_cat = np.random.choice(other_cats)
        skills += np.random.choice(JOB_CATEGORIES[other_cat]['skills'], size=5, replace=False).tolist()
        years = np.random.randint(0, 3)
    
    title = cat_info['common_titles'][0].title()
    
    resume = f"{title} with {years} years of experience. "
    resume += f"Proficient in {', '.join(skills[:5])}. "
    if len(skills) > 5:
        resume += f"Also skilled in {', '.join(skills[5:])}. "
    resume += f"Built multiple projects and worked in {np.random.choice(['agile', 'startup', 'enterprise'])} environment. "
    resume += f"Strong {np.random.choice(['problem-solving', 'communication', 'teamwork'])} skills."
    
    return resume, years

def generate_job(category):
    """Generate a job description"""
    cat_info = JOB_CATEGORIES[category]
    required_years = np.random.randint(cat_info['years_range'][0], cat_info['years_range'][1] + 1)
    
    # Require 60-80% of category skills
    num_required = np.random.randint(int(len(cat_info['skills']) * 0.6), int(len(cat_info['skills']) * 0.8) + 1)
    required_skills = np.random.choice(cat_info['skills'], size=num_required, replace=False).tolist()
    
    title = category
    job = f"{title} position. "
    job += f"Looking for {required_years}+ years of experience. "
    job += f"Required skills: {', '.join(required_skills)}. "
    job += f"Must have strong {np.random.choice(['analytical', 'technical', 'leadership'])} abilities. "
    job += f"{np.random.choice(['Remote', 'Hybrid', 'On-site'])} work. Competitive salary and benefits."
    
    return job, required_years, set(required_skills)

def calculate_accurate_score(resume, job, resume_years, job_years, job_required_skills):
    """Calculate accurate match score based on clear rules"""
    resume_lower = resume.lower()
    
    # 1. Skill match (50% weight)
    resume_skills = set()
    for skill in job_required_skills:
        if skill in resume_lower:
            resume_skills.add(skill)
    
    skill_match_ratio = len(resume_skills) / len(job_required_skills) if job_required_skills else 0
    skill_score = skill_match_ratio * 50
    
    # 2. Experience match (30% weight)
    if resume_years >= job_years:
        exp_score = 30
    elif resume_years >= job_years * 0.75:
        exp_score = 25
    elif resume_years >= job_years * 0.5:
        exp_score = 15
    else:
        exp_score = 5
    
    # 3. Content relevance (20% weight)
    job_words = set(job.lower().split())
    resume_words = set(resume_lower.split())
    common_words = job_words.intersection(resume_words)
    relevance_ratio = len(common_words) / len(job_words) if job_words else 0
    relevance_score = min(relevance_ratio * 30, 20)
    
    total_score = skill_score + exp_score + relevance_score
    
    # Add small random noise (±2 points)
    total_score += np.random.uniform(-2, 2)
    
    return round(np.clip(total_score, 0, 100), 2)

def create_synthetic_dataset(num_samples=2000):
    """Create synthetic dataset with accurate labels"""
    print("🔧 Creating synthetic dataset with accurate match scores...")
    
    data = []
    np.random.seed(42)
    
    categories = list(JOB_CATEGORIES.keys())
    
    # Distribution: 88% high match, 10% medium match, 2% low match (to get mean ~80)
    high_count = int(num_samples * 0.88)
    medium_count = int(num_samples * 0.10)
    low_count = num_samples - high_count - medium_count
    
    # Generate high match pairs
    print(f"Generating {high_count} high-match pairs...")
    for i in range(high_count):
        category = np.random.choice(categories)
        resume, resume_years = generate_resume(category, 'high')
        job, job_years, job_skills = generate_job(category)
        score = calculate_accurate_score(resume, job, resume_years, job_years, job_skills)
        
        data.append({
            'resume_text': resume,
            'job_description': job,
            'match_score': score,
            'category': category,
            'match_level': 'high'
        })
        
        if (i + 1) % 100 == 0:
            print(f"  Generated {i + 1}/{high_count} high-match pairs...")
    
    # Generate medium match pairs
    print(f"Generating {medium_count} medium-match pairs...")
    for i in range(medium_count):
        category = np.random.choice(categories)
        resume, resume_years = generate_resume(category, 'medium')
        job, job_years, job_skills = generate_job(category)
        score = calculate_accurate_score(resume, job, resume_years, job_years, job_skills)
        
        data.append({
            'resume_text': resume,
            'job_description': job,
            'match_score': score,
            'category': category,
            'match_level': 'medium'
        })
        
        if (i + 1) % 100 == 0:
            print(f"  Generated {i + 1}/{medium_count} medium-match pairs...")
    
    # Generate low match pairs (cross-category)
    print(f"Generating {low_count} low-match pairs...")
    for i in range(low_count):
        resume_category = np.random.choice(categories)
        job_category = np.random.choice([c for c in categories if c != resume_category])
        
        resume, resume_years = generate_resume(resume_category, 'low')
        job, job_years, job_skills = generate_job(job_category)
        score = calculate_accurate_score(resume, job, resume_years, job_years, job_skills)
        
        data.append({
            'resume_text': resume,
            'job_description': job,
            'match_score': score,
            'category': f'{resume_category} -> {job_category}',
            'match_level': 'low'
        })
        
        if (i + 1) % 100 == 0:
            print(f"  Generated {i + 1}/{low_count} low-match pairs...")
    
    df = pd.DataFrame(data)
    
    # Save dataset
    os.makedirs('./data', exist_ok=True)
    output_path = './data/training_dataset.csv'
    df[['resume_text', 'job_description', 'match_score']].to_csv(output_path, index=False)
    
    print(f"\n✅ Synthetic dataset created: {output_path}")
    print(f"✅ Total samples: {len(df)}")
    print(f"✅ Match score range: {df['match_score'].min():.2f} - {df['match_score'].max():.2f}")
    print(f"✅ Mean match score: {df['match_score'].mean():.2f}")
    print(f"✅ Median match score: {df['match_score'].median():.2f}")
    
    # Score distribution
    print(f"\n📊 Score Distribution:")
    print(f"  High (70-100): {len(df[df['match_score'] >= 70])} ({len(df[df['match_score'] >= 70])/len(df)*100:.1f}%)")
    print(f"  Medium (40-70): {len(df[(df['match_score'] >= 40) & (df['match_score'] < 70)])} ({len(df[(df['match_score'] >= 40) & (df['match_score'] < 70)])/len(df)*100:.1f}%)")
    print(f"  Low (0-40): {len(df[df['match_score'] < 40])} ({len(df[df['match_score'] < 40])/len(df)*100:.1f}%)")
    
    return df

if __name__ == "__main__":
    print("="*70)
    print("Synthetic Resume-Job Dataset Generator")
    print("="*70)
    
    df = create_synthetic_dataset(num_samples=2000)
    
    print("\n" + "="*70)
    print("✅ Dataset generation complete!")
    print("Next step: Run 'python train_model.py' to train the model")
    print("="*70)
