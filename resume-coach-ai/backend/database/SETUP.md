# Supabase Database Setup Guide

## Prerequisites
- Supabase account (free tier works)
- Project created at https://supabase.com

## Step 1: Get Your Credentials

1. Go to your Supabase project dashboard
2. Navigate to **Settings** → **API**
3. Copy the following:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (starts with `eyJ...`)

## Step 2: Configure Environment

Update your `backend/.env` file:

```bash
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_anon_key_here
ML_SERVICE_URL=http://localhost:8000
PORT=3000
NODE_ENV=development
```

## Step 3: Create Database Schema

1. Go to your Supabase dashboard
2. Navigate to **SQL Editor**
3. Click **New Query**
4. Copy and paste the contents of `backend/database/schema.sql`
5. Click **Run** or press `Ctrl+Enter`

This will create:
- ✅ 3 tables: `resumes`, `jobs`, `scores`
- ✅ Indexes for performance
- ✅ Updated_at triggers
- ✅ 5 sample job postings

## Step 4: Verify Schema

Run the test queries in `backend/database/test_queries.sql`:

```sql
-- Check tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('resumes', 'jobs', 'scores');

-- Should return 3 rows: resumes, jobs, scores
```

## Step 5: Test Database Connection

From the `backend` directory:

```bash
# Install ts-node if not already installed
npm install -D ts-node

# Run database test
npx ts-node test_database.ts
```

Expected output:
```
🔍 Testing Supabase Database Connection...

[Test 1] Testing basic connection...
✅ Connection successful!

[Test 2] Counting records in tables...
   Resumes: 0
   Jobs: 5
   Scores: 0

[Test 3] Fetching sample jobs...
✅ Found 5 jobs:
   1. Senior Python Developer at Tech Innovators Inc (Remote)
   2. Full Stack Developer (MERN) at Startup Labs (San Francisco, CA)
   ...

[Test 4] Testing insert operation...
✅ Resume created with ID: ...

[Test 5] Testing update operation...
✅ Resume updated: Test Resume - Updated

[Test 6] Testing query with filter...
✅ Found 3 remote jobs

[Test 7] Testing delete operation...
✅ Test resume deleted

[Test 8] Testing JSONB queries...
✅ Found 4 jobs requiring Python

═══════════════════════════════════════
✅ All Database Tests Passed!
═══════════════════════════════════════
```

## Step 6: Test with API Server

Start your backend server:

```bash
npm run dev
```

Test the jobs endpoint:

```powershell
# Get all jobs
Invoke-RestMethod -Uri "http://localhost:3000/api/jobs"

# Get specific job
Invoke-RestMethod -Uri "http://localhost:3000/api/jobs/<job-id>"
```

## Database Schema Overview

### Resumes Table
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to auth.users)
- title: TEXT
- content: TEXT
- skills: JSONB (array of strings)
- experience: JSONB (array of objects)
- education: JSONB (array of objects)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### Jobs Table
```sql
- id: UUID (Primary Key)
- title: TEXT
- description: TEXT
- company: TEXT
- location: TEXT
- salary: TEXT
- requirements: JSONB (array of strings)
- skills: JSONB (array of strings)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### Scores Table
```sql
- id: UUID (Primary Key)
- user_id: UUID
- resume_id: UUID (Foreign Key)
- job_id: UUID (Foreign Key)
- match_score: FLOAT (0-100)
- confidence: FLOAT (0-1)
- keywords_matched: JSONB (array of strings)
- recommendation: TEXT
- created_at: TIMESTAMP
```

## Sample Data

5 job postings are automatically inserted:
1. Senior Python Developer (Tech Innovators Inc) - Remote
2. Full Stack Developer MERN (Startup Labs) - San Francisco
3. Machine Learning Engineer (AI Solutions Corp) - Remote
4. DevOps Engineer (Cloud Systems Ltd) - New York
5. Frontend Developer React (WebTech Solutions) - Remote

## Troubleshooting

### Error: "Missing Supabase environment variables"
- Check `.env` file exists in `backend/` directory
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are set correctly

### Error: "relation 'jobs' does not exist"
- Run `schema.sql` in Supabase SQL Editor
- Verify tables created: Go to **Database** → **Tables**

### Error: "Invalid API key"
- Use the **anon/public** key, not the service_role key
- Regenerate keys if compromised: Settings → API → Reset

### Connection Timeout
- Check internet connection
- Verify Supabase project is not paused (free tier pauses after inactivity)
- Check firewall settings

## Row Level Security (RLS)

Currently disabled for development. To enable for production:

1. Enable RLS in Supabase dashboard
2. Uncomment RLS policy examples in `schema.sql`
3. Implement proper authentication in API routes

## Next Steps

After database is set up:
1. ✅ Test all CRUD endpoints with Supabase
2. ✅ Implement user authentication
3. ✅ Add data validation
4. ✅ Set up RLS policies
5. ✅ Deploy to production

## Useful Commands

```bash
# Test database connection
npx ts-node test_database.ts

# Test API endpoints
npm run dev

# Build for production
npm run build
```

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase JS Client](https://supabase.com/docs/reference/javascript/introduction)
- [PostgreSQL JSONB](https://www.postgresql.org/docs/current/datatype-json.html)
