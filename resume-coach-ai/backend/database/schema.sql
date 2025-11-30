-- ResumeCoach AI - Supabase Database Schema
-- Run this script in your Supabase SQL editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table (if not using Supabase Auth built-in)
-- Note: If using Supabase Auth, you can reference auth.users instead

-- Create resumes table
CREATE TABLE IF NOT EXISTS resumes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  skills JSONB DEFAULT '[]'::jsonb,
  experience JSONB DEFAULT '[]'::jsonb,
  education JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create jobs table
CREATE TABLE IF NOT EXISTS jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  company TEXT NOT NULL,
  location TEXT DEFAULT 'Remote',
  salary TEXT DEFAULT 'Competitive',
  requirements JSONB DEFAULT '[]'::jsonb,
  skills JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create scores table
CREATE TABLE IF NOT EXISTS scores (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL,
  resume_id UUID REFERENCES resumes(id) ON DELETE CASCADE,
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  match_score FLOAT NOT NULL CHECK (match_score >= 0 AND match_score <= 100),
  confidence FLOAT NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  keywords_matched JSONB DEFAULT '[]'::jsonb,
  recommendation TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_resumes_created_at ON resumes(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);

CREATE INDEX IF NOT EXISTS idx_scores_user_id ON scores(user_id);
CREATE INDEX IF NOT EXISTS idx_scores_resume_id ON scores(resume_id);
CREATE INDEX IF NOT EXISTS idx_scores_job_id ON scores(job_id);
CREATE INDEX IF NOT EXISTS idx_scores_created_at ON scores(created_at DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add trigger to resumes table
DROP TRIGGER IF EXISTS update_resumes_updated_at ON resumes;
CREATE TRIGGER update_resumes_updated_at
  BEFORE UPDATE ON resumes
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Add trigger to jobs table
DROP TRIGGER IF EXISTS update_jobs_updated_at ON jobs;
CREATE TRIGGER update_jobs_updated_at
  BEFORE UPDATE ON jobs
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Insert sample job postings for testing
INSERT INTO jobs (title, description, company, location, salary, requirements, skills) VALUES
(
  'Senior Python Developer',
  'We are looking for an experienced Python developer to join our team. You will be working on building scalable backend services using Django and FastAPI. Experience with machine learning is a plus.',
  'Tech Innovators Inc',
  'Remote',
  '$120,000 - $150,000',
  '["5+ years Python experience", "Strong knowledge of Django or FastAPI", "Experience with PostgreSQL", "RESTful API design", "Git version control"]'::jsonb,
  '["Python", "Django", "FastAPI", "PostgreSQL", "Docker", "AWS"]'::jsonb
),
(
  'Full Stack Developer (MERN)',
  'Join our startup as a Full Stack Developer. Build modern web applications using MongoDB, Express, React, and Node.js. Work on exciting projects in a fast-paced environment.',
  'Startup Labs',
  'San Francisco, CA',
  '$100,000 - $130,000',
  '["3+ years JavaScript development", "Experience with React and Node.js", "MongoDB expertise", "RESTful API development", "Agile methodology"]'::jsonb,
  '["JavaScript", "React", "Node.js", "Express", "MongoDB", "TypeScript"]'::jsonb
),
(
  'Machine Learning Engineer',
  'We need a talented ML Engineer to develop and deploy machine learning models. Experience with PyTorch, TensorFlow, and cloud platforms required.',
  'AI Solutions Corp',
  'Remote',
  '$140,000 - $180,000',
  '["Master''s degree in CS or related field", "3+ years ML experience", "Strong Python and ML frameworks", "Experience with model deployment", "Cloud platform experience (AWS/GCP)"]'::jsonb,
  '["Python", "PyTorch", "TensorFlow", "Scikit-learn", "AWS", "Docker", "Kubernetes"]'::jsonb
),
(
  'DevOps Engineer',
  'Looking for a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines. Kubernetes and AWS experience essential.',
  'Cloud Systems Ltd',
  'New York, NY',
  '$110,000 - $140,000',
  '["4+ years DevOps experience", "Strong AWS knowledge", "Kubernetes expertise", "CI/CD pipeline management", "Infrastructure as Code (Terraform)"]'::jsonb,
  '["AWS", "Kubernetes", "Docker", "Terraform", "Jenkins", "Python", "Bash"]'::jsonb
),
(
  'Frontend Developer (React)',
  'We are seeking a creative Frontend Developer with strong React skills. Build beautiful, responsive user interfaces for our SaaS platform.',
  'WebTech Solutions',
  'Remote',
  '$90,000 - $120,000',
  '["3+ years frontend development", "Expert React knowledge", "CSS/Tailwind CSS", "State management (Redux/Context)", "REST API integration"]'::jsonb,
  '["React", "JavaScript", "TypeScript", "Tailwind CSS", "Redux", "HTML", "CSS"]'::jsonb
);

-- Verify data insertion
SELECT COUNT(*) as total_jobs FROM jobs;

-- Display sample data
SELECT id, title, company, location FROM jobs;

-- Grant necessary permissions (adjust as needed)
-- ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE scores ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (example - adjust based on your auth setup)
-- CREATE POLICY "Users can view their own resumes" ON resumes
--   FOR SELECT USING (auth.uid() = user_id);

-- CREATE POLICY "Users can insert their own resumes" ON resumes
--   FOR INSERT WITH CHECK (auth.uid() = user_id);

-- CREATE POLICY "Users can update their own resumes" ON resumes
--   FOR UPDATE USING (auth.uid() = user_id);

-- CREATE POLICY "Users can delete their own resumes" ON resumes
--   FOR DELETE USING (auth.uid() = user_id);

-- CREATE POLICY "Jobs are viewable by everyone" ON jobs
--   FOR SELECT USING (true);

-- CREATE POLICY "Users can view their own scores" ON scores
--   FOR SELECT USING (auth.uid() = user_id);

COMMENT ON TABLE resumes IS 'Stores user resume information including skills, experience, and education';
COMMENT ON TABLE jobs IS 'Contains job postings with requirements and desired skills';
COMMENT ON TABLE scores IS 'Stores ML-generated match scores between resumes and jobs';

-- Success message
DO $$
BEGIN
  RAISE NOTICE 'Database schema created successfully!';
  RAISE NOTICE 'Tables: resumes, jobs, scores';
  RAISE NOTICE 'Sample jobs inserted: 5';
END $$;
