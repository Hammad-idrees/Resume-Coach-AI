-- Additional tables for ATS Optimization and Interview Simulation
-- Add these to your existing schema.sql

-- ATS Scores Table (separate from general match scores)
CREATE TABLE IF NOT EXISTS ats_scores (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL,
  resume_text TEXT NOT NULL,
  job_description TEXT NOT NULL,
  ats_score FLOAT NOT NULL CHECK (ats_score >= 0 AND ats_score <= 100),
  keyword_match_percentage FLOAT NOT NULL CHECK (keyword_match_percentage >= 0 AND keyword_match_percentage <= 100),
  missing_keywords JSONB DEFAULT '[]'::jsonb,
  matched_keywords JSONB DEFAULT '[]'::jsonb,
  suggestions JSONB DEFAULT '[]'::jsonb,
  tfidf_similarity FLOAT,
  resume_keyword_count INTEGER,
  job_keyword_count INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Interview Sessions Table
CREATE TABLE IF NOT EXISTS interviews (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL,
  job_description TEXT NOT NULL,
  job_role TEXT,
  questions JSONB NOT NULL DEFAULT '[]'::jsonb,
  answers JSONB NOT NULL DEFAULT '[]'::jsonb,
  evaluations JSONB NOT NULL DEFAULT '[]'::jsonb,
  overall_score FLOAT CHECK (overall_score >= 0 AND overall_score <= 100),
  average_score FLOAT CHECK (average_score >= 0 AND average_score <= 10),
  grade TEXT,
  total_questions INTEGER,
  questions_answered INTEGER,
  summary TEXT,
  category_breakdown JSONB DEFAULT '{}'::jsonb,
  started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  completed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for ATS scores
CREATE INDEX IF NOT EXISTS idx_ats_scores_user_id ON ats_scores(user_id);
CREATE INDEX IF NOT EXISTS idx_ats_scores_created_at ON ats_scores(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ats_scores_ats_score ON ats_scores(ats_score DESC);

-- Create indexes for interviews
CREATE INDEX IF NOT EXISTS idx_interviews_user_id ON interviews(user_id);
CREATE INDEX IF NOT EXISTS idx_interviews_created_at ON interviews(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_interviews_overall_score ON interviews(overall_score DESC);
CREATE INDEX IF NOT EXISTS idx_interviews_completed_at ON interviews(completed_at DESC);

-- Enable Row Level Security
ALTER TABLE ats_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE interviews ENABLE ROW LEVEL SECURITY;

-- RLS Policies for ATS Scores
CREATE POLICY "Users can view their own ATS scores"
  ON ats_scores FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own ATS scores"
  ON ats_scores FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own ATS scores"
  ON ats_scores FOR DELETE
  USING (auth.uid() = user_id);

-- RLS Policies for Interviews
CREATE POLICY "Users can view their own interviews"
  ON interviews FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own interviews"
  ON interviews FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own interviews"
  ON interviews FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own interviews"
  ON interviews FOR DELETE
  USING (auth.uid() = user_id);

-- Add comments
COMMENT ON TABLE ats_scores IS 'Stores ATS optimization analysis results with keyword matching and suggestions';
COMMENT ON TABLE interviews IS 'Stores interview simulation sessions with questions, answers, and AI evaluations';

-- Sample queries for testing
-- SELECT * FROM ats_scores WHERE user_id = 'your-user-id' ORDER BY created_at DESC LIMIT 10;
-- SELECT * FROM interviews WHERE user_id = 'your-user-id' AND completed_at IS NOT NULL ORDER BY overall_score DESC;

DO $$
BEGIN
  RAISE NOTICE 'ATS Scores and Interviews tables created successfully!';
  RAISE NOTICE 'RLS policies enabled for data security';
END $$;
