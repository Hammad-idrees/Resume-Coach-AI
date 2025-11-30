-- Test queries for ResumeCoach AI database

-- 1. Check all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('resumes', 'jobs', 'scores');

-- 2. Count records in each table
SELECT 'resumes' as table_name, COUNT(*) as count FROM resumes
UNION ALL
SELECT 'jobs' as table_name, COUNT(*) as count FROM jobs
UNION ALL
SELECT 'scores' as table_name, COUNT(*) as count FROM scores;

-- 3. View all jobs
SELECT id, title, company, location, salary 
FROM jobs 
ORDER BY created_at DESC;

-- 4. View job details with skills
SELECT 
  title,
  company,
  location,
  salary,
  jsonb_array_length(skills) as skills_count,
  jsonb_array_length(requirements) as requirements_count
FROM jobs;

-- 5. Search jobs by skill (example: Python)
SELECT title, company, location
FROM jobs
WHERE skills::text ILIKE '%Python%';

-- 6. Get recent resumes (will be empty until users create resumes)
SELECT id, title, created_at
FROM resumes
ORDER BY created_at DESC
LIMIT 10;

-- 7. Get score statistics (will be empty until scores are generated)
SELECT 
  COUNT(*) as total_scores,
  ROUND(AVG(match_score)::numeric, 2) as avg_score,
  ROUND(MIN(match_score)::numeric, 2) as min_score,
  ROUND(MAX(match_score)::numeric, 2) as max_score
FROM scores;

-- 8. View indexes
SELECT
  tablename,
  indexname,
  indexdef
FROM pg_indexes
WHERE tablename IN ('resumes', 'jobs', 'scores')
ORDER BY tablename, indexname;
