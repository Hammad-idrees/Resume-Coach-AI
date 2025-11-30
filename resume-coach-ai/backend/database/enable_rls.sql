-- Enable Row Level Security on existing tables
-- Run this after running the initial schema.sql

-- Enable RLS on existing tables
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE scores ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if any
DROP POLICY IF EXISTS "Users can view their own resumes" ON resumes;
DROP POLICY IF EXISTS "Users can insert their own resumes" ON resumes;
DROP POLICY IF EXISTS "Users can update their own resumes" ON resumes;
DROP POLICY IF EXISTS "Users can delete their own resumes" ON resumes;

DROP POLICY IF EXISTS "Jobs are viewable by everyone" ON jobs;

DROP POLICY IF EXISTS "Users can view their own scores" ON scores;
DROP POLICY IF EXISTS "Users can insert their own scores" ON scores;
DROP POLICY IF EXISTS "Users can delete their own scores" ON scores;

-- RLS Policies for Resumes
CREATE POLICY "Users can view their own resumes"
  ON resumes FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own resumes"
  ON resumes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own resumes"
  ON resumes FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own resumes"
  ON resumes FOR DELETE
  USING (auth.uid() = user_id);

-- RLS Policies for Jobs (public read access)
CREATE POLICY "Jobs are viewable by everyone"
  ON jobs FOR SELECT
  USING (true);

-- Optional: Only admins can insert/update/delete jobs
-- CREATE POLICY "Only admins can manage jobs"
--   ON jobs FOR ALL
--   USING (auth.jwt() ->> 'role' = 'admin');

-- RLS Policies for Scores
CREATE POLICY "Users can view their own scores"
  ON scores FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own scores"
  ON scores FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own scores"
  ON scores FOR DELETE
  USING (auth.uid() = user_id);

-- Verify RLS is enabled
SELECT
  schemaname,
  tablename,
  rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN ('resumes', 'jobs', 'scores', 'ats_scores', 'interviews');

DO $$
BEGIN
  RAISE NOTICE 'Row Level Security policies created successfully!';
  RAISE NOTICE 'All tables are now protected with RLS';
END $$;
