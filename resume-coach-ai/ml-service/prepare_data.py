"""
Download and prepare datasets from Kaggle for resume-job matching
Combines resume dataset with job postings to create training data
"""

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import re

def setup_kaggle():
    """Instructions for Kaggle API setup"""
    print("="*70)
    print("Kaggle API Setup Required")
    print("="*70)
    print("\n📋 Steps to set up Kaggle API:")
    print("\n1. Go to: https://www.kaggle.com/settings/account")
    print("2. Scroll to 'API' section")
    print("3. Click 'Create New Token'")
    print("4. Download kaggle.json file")
    print("5. Place kaggle.json in: C:\\Users\\<YourUsername>\\.kaggle\\")
    print("   (Create .kaggle folder if it doesn't exist)")
    print("\n6. Run: pip install kaggle")
    print("="*70)
    
    kaggle_dir = os.path.expanduser("~/.kaggle")
    kaggle_json = os.path.join(kaggle_dir, "kaggle.json")
    
    if os.path.exists(kaggle_json):
        print("✅ Kaggle API credentials found!")
        return True
    else:
        print("❌ Kaggle API credentials not found!")
        print(f"Please place kaggle.json at: {kaggle_json}")
        return False

def download_datasets():
    """Download datasets from Kaggle"""
    print("\n📥 Downloading datasets from Kaggle...")
    
    datasets_to_download = [
        {
            "name": "Resume Dataset",
            "slug": "snehaanbhawal/resume-dataset",
            "path": "./data/resume-dataset"
        },
        {
            "name": "LinkedIn Job Postings",
            "slug": "arshkon/linkedin-job-postings",
            "path": "./data/linkedin-jobs"
        }
    ]
    
    os.makedirs("./data", exist_ok=True)
    
    for dataset in datasets_to_download:
        print(f"\nDownloading: {dataset['name']}...")
        try:
            os.system(f'kaggle datasets download -d {dataset["slug"]} -p {dataset["path"]} --unzip')
            print(f"✅ Downloaded: {dataset['name']}")
        except Exception as e:
            print(f"❌ Error downloading {dataset['name']}: {e}")
            print("You may need to accept dataset terms on Kaggle website first")
    
    print("\n✅ Dataset download complete!")

def clean_text(text):
    """Clean and normalize text"""
    if pd.isna(text):
        return ""
    text = str(text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()

def extract_skills(text):
    """Extract common tech skills from text"""
    skills_list = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php', 'swift', 'kotlin',
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'laravel',
        'sql', 'postgresql', 'mongodb', 'redis', 'mysql', 'oracle', 'cassandra', 'elasticsearch',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible',
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'nlp', 'computer vision',
        'git', 'agile', 'scrum', 'rest api', 'graphql', 'microservices', 'ci/cd', 'devops',
        'html', 'css', 'tailwind', 'bootstrap', 'sass', 'webpack', 'vite',
        'testing', 'junit', 'pytest', 'jest', 'cypress', 'selenium',
        'linux', 'unix', 'bash', 'powershell', 'networking', 'security'
    ]
    
    text_lower = text.lower()
    found_skills = [skill for skill in skills_list if skill in text_lower]
    return found_skills

def extract_experience_years(text):
    """Extract years of experience from text"""
    patterns = [
        r'(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?',
        r'(\d+)\s*years?\s*of\s*experience',
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            return max([int(m) for m in matches])
    return 0

def calculate_match_score(resume_text, job_text):
    """Enhanced match score calculation with multiple factors"""
    
    # 1. TF-IDF similarity (30% weight) - boosted from raw score
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english', ngram_range=(1, 2))
    try:
        vectors = vectorizer.fit_transform([resume_text, job_text])
        tfidf_score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        # Boost TF-IDF score (multiply by 1.5, cap at 1.0)
        tfidf_score = min(tfidf_score * 1.5, 1.0)
    except:
        tfidf_score = 0.0
    
    # 2. Skill overlap (35% weight)
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))
    
    if len(job_skills) > 0:
        skill_overlap = len(resume_skills.intersection(job_skills)) / len(job_skills)
    else:
        skill_overlap = 0.0
    
    # 3. Keyword matching (25% weight)
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())
    
    # Filter out common words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    resume_words = resume_words - stop_words
    job_words = job_words - stop_words
    
    if len(job_words) > 0:
        keyword_match = len(resume_words.intersection(job_words)) / len(job_words)
        keyword_match = min(keyword_match * 2, 1.0)  # Boost keyword matching
    else:
        keyword_match = 0.0
    
    # 4. Experience match (10% weight)
    resume_years = extract_experience_years(resume_text)
    job_years = extract_experience_years(job_text)
    
    if job_years > 0:
        if resume_years >= job_years:
            experience_score = 1.0
        elif resume_years >= job_years * 0.7:  # Within 70% is good
            experience_score = 0.8
        else:
            experience_score = 0.5
    else:
        experience_score = 0.7  # Neutral if no experience mentioned
    
    # Combined weighted score
    match_score = (
        tfidf_score * 30 + 
        skill_overlap * 35 + 
        keyword_match * 25 + 
        experience_score * 10
    )
    
    # Add small controlled randomness for diversity (±3 points)
    noise = np.random.uniform(-3, 3)
    match_score = np.clip(match_score + noise, 0, 100)
    
    return round(match_score, 2)

def prepare_training_data():
    """Prepare training dataset by combining resumes and jobs"""
    print("\n🔧 Preparing training data...")
    
    # Load resume dataset
    resume_files = [
        "./data/resume-dataset/Resume.csv",
        "./data/resume-dataset/UpdatedResumeDataSet.csv",
        "./data/resume-dataset/Resume/Resume.csv"
    ]
    
    resumes_df = None
    for file_path in resume_files:
        if os.path.exists(file_path):
            print(f"Loading resumes from: {file_path}")
            resumes_df = pd.read_csv(file_path)
            break
    
    if resumes_df is None:
        print("❌ Resume dataset not found! Using sample data...")
        return create_sample_dataset()
    
    # Load job postings
    job_files = [
        "./data/linkedin-jobs/job_postings.csv",
        "./data/linkedin-jobs/postings.csv"
    ]
    
    jobs_df = None
    for file_path in job_files:
        if os.path.exists(file_path):
            print(f"Loading jobs from: {file_path}")
            jobs_df = pd.read_csv(file_path, nrows=5000)  # Limit to 5000 jobs
            break
    
    if jobs_df is None:
        print("❌ Job postings dataset not found! Using sample data...")
        return create_sample_dataset()
    
    print(f"✅ Loaded {len(resumes_df)} resumes")
    print(f"✅ Loaded {len(jobs_df)} job postings")
    
    # Identify columns
    resume_text_col = 'Resume_str' if 'Resume_str' in resumes_df.columns else 'Resume'
    resume_category_col = 'Category' if 'Category' in resumes_df.columns else None
    
    job_desc_col = 'description' if 'description' in jobs_df.columns else 'job_description'
    job_title_col = 'title' if 'title' in jobs_df.columns else 'job_title'
    
    print(f"\nUsing resume column: {resume_text_col}")
    print(f"Using job description column: {job_desc_col}")
    
    # Clean data
    print("\n🧹 Cleaning text data...")
    resumes_df['resume_clean'] = resumes_df[resume_text_col].apply(clean_text)
    jobs_df['job_clean'] = jobs_df[job_desc_col].apply(clean_text)
    
    # Remove empty entries
    resumes_df = resumes_df[resumes_df['resume_clean'].str.len() > 50]
    jobs_df = jobs_df[jobs_df['job_clean'].str.len() > 50]
    
    print(f"After cleaning: {len(resumes_df)} resumes, {len(jobs_df)} jobs")
    
    # Create training pairs with strategic pairing for better score distribution
    print("\n🔗 Creating resume-job pairs and calculating match scores...")
    print("Strategy: Creating pairs with diverse match scores...")
    print("This may take a few minutes...")
    
    training_data = []
    np.random.seed(42)  # For reproducibility
    
    # First, categorize resumes and jobs by extracting their skills
    print("\n📊 Analyzing skills in resumes and jobs...")
    resumes_df['skills'] = resumes_df['resume_clean'].apply(lambda x: set(extract_skills(x)))
    jobs_df['skills'] = jobs_df['job_clean'].apply(lambda x: set(extract_skills(x)))
    
    num_samples = min(2000, len(resumes_df) * 2)
    
    # Create three types of pairs for balanced dataset:
    # 1. Good matches (40%): pair resumes and jobs with skill overlap
    # 2. Moderate matches (30%): some skill overlap
    # 3. Poor matches (30%): minimal or no skill overlap
    
    good_match_count = int(num_samples * 0.4)
    moderate_match_count = int(num_samples * 0.3)
    poor_match_count = num_samples - good_match_count - moderate_match_count
    
    processed = 0
    
    # 1. Create GOOD matches (skill overlap >= 40%)
    print(f"\n✅ Creating {good_match_count} good match pairs...")
    attempts = 0
    while len([d for d in training_data if d['match_score'] >= 60]) < good_match_count and attempts < good_match_count * 5:
        resume_idx = np.random.randint(0, len(resumes_df))
        job_idx = np.random.randint(0, len(jobs_df))
        
        resume = resumes_df.iloc[resume_idx]
        job = jobs_df.iloc[job_idx]
        
        # Check if there's skill overlap
        skill_overlap = len(resume['skills'].intersection(job['skills']))
        
        if skill_overlap >= 2:  # At least 2 common skills
            score = calculate_match_score(resume['resume_clean'], job['job_clean'])
            
            training_data.append({
                'resume_text': resume['resume_clean'][:2000],
                'job_description': job['job_clean'][:2000],
                'match_score': min(score + 15, 100)  # Boost good matches
            })
            
            processed += 1
            if processed % 100 == 0:
                print(f"  Processed {processed} pairs...")
        
        attempts += 1
    
    # 2. Create MODERATE matches
    print(f"\n⚠️  Creating {moderate_match_count} moderate match pairs...")
    attempts = 0
    while len([d for d in training_data if 40 <= d['match_score'] < 60]) < moderate_match_count and attempts < moderate_match_count * 5:
        resume_idx = np.random.randint(0, len(resumes_df))
        job_idx = np.random.randint(0, len(jobs_df))
        
        resume = resumes_df.iloc[resume_idx]
        job = jobs_df.iloc[job_idx]
        
        score = calculate_match_score(resume['resume_clean'], job['job_clean'])
        
        # Accept if in moderate range
        if 35 <= score <= 65:
            training_data.append({
                'resume_text': resume['resume_clean'][:2000],
                'job_description': job['job_clean'][:2000],
                'match_score': score
            })
            
            processed += 1
            if processed % 100 == 0:
                print(f"  Processed {processed} pairs...")
        
        attempts += 1
    
    # 3. Create POOR matches (completely random pairing)
    print(f"\n❌ Creating {poor_match_count} poor match pairs...")
    for i in range(poor_match_count):
        resume_idx = np.random.randint(0, len(resumes_df))
        job_idx = np.random.randint(0, len(jobs_df))
        
        resume = resumes_df.iloc[resume_idx]
        job = jobs_df.iloc[job_idx]
        
        score = calculate_match_score(resume['resume_clean'], job['job_clean'])
        
        training_data.append({
            'resume_text': resume['resume_clean'][:2000],
            'job_description': job['job_clean'][:2000],
            'match_score': score
        })
        
        processed += 1
        if processed % 100 == 0:
            print(f"  Processed {processed} pairs...")
    
    # Create DataFrame
    training_df = pd.DataFrame(training_data)
    
    # Save to CSV
    output_path = './data/training_dataset.csv'
    training_df.to_csv(output_path, index=False)
    
    print(f"\n✅ Training dataset created: {output_path}")
    print(f"✅ Total samples: {len(training_df)}")
    print(f"✅ Match score range: {training_df['match_score'].min():.2f} - {training_df['match_score'].max():.2f}")
    print(f"✅ Mean match score: {training_df['match_score'].mean():.2f}")
    
    return training_df

def create_sample_dataset():
    """Create sample dataset as fallback"""
    print("\n⚠️  Using sample dataset (fallback)...")
    sample_data = pd.DataFrame({
        'resume_text': [
            "Software Engineer with 5 years of Python and JavaScript experience. Skilled in React, Node.js, and Django.",
            "Data Scientist with ML expertise. Python, TensorFlow, PyTorch. PhD in Computer Science.",
            "Full Stack Developer. JavaScript, React, Node.js, MongoDB. 4 years experience."
        ],
        'job_description': [
            "Looking for Full Stack Developer with Python and React. 3+ years required.",
            "Data Scientist position. Machine learning, Python, deep learning frameworks required.",
            "Full Stack Developer position. MERN stack required. 3+ years."
        ],
        'match_score': [85, 95, 90]
    })
    
    output_path = './data/training_dataset.csv'
    sample_data.to_csv(output_path, index=False)
    return sample_data

def main():
    print("\n" + "="*70)
    print("Resume-Job Matching Dataset Preparation")
    print("="*70)
    
    # Check Kaggle API
    if not setup_kaggle():
        response = input("\nContinue with sample dataset? (yes/no): ")
        if response.lower() != 'yes':
            print("Please set up Kaggle API and try again.")
            return
        create_sample_dataset()
        return
    
    # Download datasets
    download_choice = input("\nDownload datasets from Kaggle? (yes/no): ")
    if download_choice.lower() == 'yes':
        download_datasets()
    
    # Prepare training data
    prepare_training_data()
    
    print("\n" + "="*70)
    print("✅ Data preparation complete!")
    print("Next step: Run 'python train_model.py' to train the model")
    print("="*70)

if __name__ == "__main__":
    main()
