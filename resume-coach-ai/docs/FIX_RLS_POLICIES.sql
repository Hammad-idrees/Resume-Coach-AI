-- SOLUTION 1: Disable RLS temporarily for testing (NOT RECOMMENDED FOR PRODUCTION)
-- Run this in Supabase SQL Editor if you want to disable RLS for demo purposes

ALTER TABLE resumes DISABLE ROW LEVEL SECURITY;
ALTER TABLE jobs DISABLE ROW LEVEL SECURITY;
ALTER TABLE scores DISABLE ROW LEVEL SECURITY;
ALTER TABLE ats_scores DISABLE ROW LEVEL SECURITY;
ALTER TABLE interviews DISABLE ROW LEVEL SECURITY;


-- SOLUTION 2: Update RLS policies to work with authenticated users (RECOMMENDED)
-- First, drop existing policies
DROP POLICY IF EXISTS "Users can view their own resumes" ON resumes;
DROP POLICY IF EXISTS "Users can insert their own resumes" ON resumes;
DROP POLICY IF EXISTS "Users can update their own resumes" ON resumes;
DROP POLICY IF EXISTS "Users can delete their own resumes" ON resumes;

-- Create new policies that work with Supabase Auth
CREATE POLICY "Enable read access for authenticated users" 
ON resumes FOR SELECT 
TO authenticated
USING (auth.uid() = user_id);

CREATE POLICY "Enable insert for authenticated users" 
ON resumes FOR INSERT 
TO authenticated
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Enable update for authenticated users" 
ON resumes FOR UPDATE 
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Enable delete for authenticated users" 
ON resumes FOR DELETE 
TO authenticated
USING (auth.uid() = user_id);

-- Apply same pattern to other tables
-- For jobs table
DROP POLICY IF EXISTS "Users can view all jobs" ON jobs;
CREATE POLICY "Enable read access for all authenticated users" 
ON jobs FOR SELECT 
TO authenticated
USING (true);

-- For scores table
DROP POLICY IF EXISTS "Users can view their own scores" ON scores;
DROP POLICY IF EXISTS "Users can insert their own scores" ON scores;

CREATE POLICY "Enable read access for authenticated users" 
ON scores FOR SELECT 
TO authenticated
USING (auth.uid() = user_id);

CREATE POLICY "Enable insert for authenticated users" 
ON scores FOR INSERT 
TO authenticated
WITH CHECK (auth.uid() = user_id);

-- For ats_scores table
DROP POLICY IF EXISTS "Users can view their own ats scores" ON ats_scores;
DROP POLICY IF EXISTS "Users can insert their own ats scores" ON ats_scores;

CREATE POLICY "Enable read access for authenticated users" 
ON ats_scores FOR SELECT 
TO authenticated
USING (auth.uid() = user_id);

CREATE POLICY "Enable insert for authenticated users" 
ON ats_scores FOR INSERT 
TO authenticated
WITH CHECK (auth.uid() = user_id);

-- For interviews table
DROP POLICY IF EXISTS "Users can view their own interviews" ON interviews;
DROP POLICY IF EXISTS "Users can insert their own interviews" ON interviews;

CREATE POLICY "Enable read access for authenticated users" 
ON interviews FOR SELECT 
TO authenticated
USING (auth.uid() = user_id);

CREATE POLICY "Enable insert for authenticated users" 
ON interviews FOR INSERT 
TO authenticated
WITH CHECK (auth.uid() = user_id);


-- SOLUTION 3: Quick fix - Disable RLS just for resumes table
ALTER TABLE resumes DISABLE ROW LEVEL SECURITY;
