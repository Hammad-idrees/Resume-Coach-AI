# 📋 ResumeCoach AI - Traceability Matrix

Quick reference guide mapping features to implementation locations (file paths and line numbers).

---

## 🔐 Authentication & Security

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| User Registration | `frontend/src/pages/Signup.tsx` | 1-252 | Complete signup form with validation |
| User Login | `frontend/src/pages/Login.tsx` | 1-145 | Email/password authentication |
| Auth Context Provider | `frontend/src/contexts/AuthContext.tsx` | 1-130 | Global auth state management |
| Protected Routes | `frontend/src/components/ProtectedRoute.tsx` | 1-25 | Route guard component |
| JWT Token Injection | `frontend/src/lib/api.ts` | 15-37 | Axios interceptor for auth headers |
| Supabase Config | `frontend/src/lib/supabase.ts` | 1-10 | Supabase client initialization |
| Logout Functionality | `frontend/src/components/Sidebar.tsx` | 75-85 | Logout button with confirmation |
| User Profile Display | `frontend/src/components/Header.tsx` | 12-35 | Dynamic user name and email |
| Row-Level Security | `backend/database/schema.sql` | 120-160 | RLS policies for data isolation |

---

## 📄 Resume Management

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Resume List View | `frontend/src/pages/Resumes.tsx` | 90-150 | Display all user resumes |
| Upload Resume Form | `frontend/src/pages/Resumes.tsx` | 45-75 | Create new resume with title/content |
| Resume View Modal | `frontend/src/pages/Resumes.tsx` | 178-222 | Full resume details display |
| Resume Edit Modal | `frontend/src/pages/Resumes.tsx` | 224-326 | Edit form with save functionality |
| Delete Resume | `frontend/src/pages/Resumes.tsx` | 30-40 | Delete with confirmation |
| Resume API Client | `frontend/src/lib/api.ts` | 42-48 | CRUD API functions |
| Backend Resume Routes | `backend/src/routes/resume.ts` | 1-150 | Express endpoints for resumes |
| Database Schema | `backend/database/schema.sql` | 12-21 | Resumes table definition |
| Resume Skills Display | `frontend/src/pages/Resumes.tsx` | 115-130 | Chip-based skills visualization |

---

## 💼 Job Management & Matching

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Job Listings Display | `frontend/src/pages/Jobs.tsx` | 90-150 | Grid view of all jobs |
| Job Search Filter | `frontend/src/pages/Jobs.tsx` | 52-70 | Search by title/company/location |
| Job Details Modal | `frontend/src/pages/Jobs.tsx` | 140-210 | Full job description view |
| Match with Resume Button | `frontend/src/pages/Jobs.tsx` | 196-200 | Trigger resume matching |
| Resume Selector Modal | `frontend/src/pages/Jobs.tsx` | 220-320 | Choose resume for matching |
| Match Calculation | `frontend/src/pages/Jobs.tsx` | 50-75 | API call to ML service |
| Job API Client | `frontend/src/lib/api.ts` | 50-53 | GET endpoints for jobs |
| Backend Job Routes | `backend/src/routes/job.ts` | 1-100 | Express endpoints for jobs |
| Jobs Database Table | `backend/database/schema.sql` | 25-35 | Jobs table with JSONB fields |
| Job Data Population | `backend/database/populate_jobs.sql` | 1-90 | 10 realistic job entries |

---

## 🤖 ML Model - Resume-Job Matching

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| DistilBERT Model Loading | `ml-service/app.py` | 65-85 | Model initialization on startup |
| Prediction Endpoint | `ml-service/app.py` | 150-210 | `/predict-match` POST endpoint |
| Model Architecture Config | `ml-service/train_model.py` | 45-75 | DistilBERT regression setup |
| Training Script | `ml-service/train_model.py` | 1-350 | Complete model training pipeline |
| Tokenization | `ml-service/app.py` | 175-182 | Input text preprocessing |
| Score Calculation | `ml-service/app.py` | 185-191 | Inference and scaling to 0-100 |
| Keyword Extraction | `ml-service/app.py` | 95-103 | Common skills identification |
| Confidence Calculation | `ml-service/app.py` | 118-122 | Confidence score logic |
| Recommendation Logic | `ml-service/app.py` | 105-116 | Score-based recommendations |
| Model Weights | `ml-service/models/resume_scorer/` | - | Saved DistilBERT weights |
| Training Dataset | `ml-service/data/training_dataset.csv` | - | 2000 synthetic samples |

---

## 🎯 ATS Optimization

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| ATS Optimization Page | `frontend/src/pages/ATSOptimization.tsx` | 1-250 | Full ATS checker interface |
| Resume Input Textarea | `frontend/src/pages/ATSOptimization.tsx` | 80-95 | Paste resume text |
| Job Description Input | `frontend/src/pages/ATSOptimization.tsx` | 100-115 | Paste job description |
| Analyze Button | `frontend/src/pages/ATSOptimization.tsx` | 120-130 | Trigger analysis |
| Score Display | `frontend/src/pages/ATSOptimization.tsx` | 160-180 | Visual score with color coding |
| Missing Keywords | `frontend/src/pages/ATSOptimization.tsx` | 185-200 | Display missing terms |
| Suggestions List | `frontend/src/pages/ATSOptimization.tsx` | 205-225 | Improvement recommendations |
| ATS API Client | `frontend/src/lib/api.ts` | 65-67 | Direct ML service call |
| TF-IDF Vectorization | `ml-service/ats_optimizer.py` | 25-40 | Text to vector conversion |
| Cosine Similarity | `ml-service/ats_optimizer.py` | 45-55 | Calculate compatibility |
| Keyword Analysis | `ml-service/ats_optimizer.py` | 80-120 | Find missing keywords |
| Recommendation Engine | `ml-service/ats_optimizer.py` | 161-185 | Generate suggestions |
| ATS Endpoint | `ml-service/app.py` | 275-310 | `/optimize-ats` POST route |
| Score Threshold Logic | `ml-service/ats_optimizer.py` | 161-168 | Critical/Poor/Fair/Good levels |

---

## 🗣️ Interview Simulation

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Interview Simulator Page | `frontend/src/pages/InterviewSimulation.tsx` | 1-400 | Complete interview interface |
| Job Description Input | `frontend/src/pages/InterviewSimulation.tsx` | 65-80 | Enter job details |
| Generate Questions Button | `frontend/src/pages/InterviewSimulation.tsx` | 85-95 | Trigger question generation |
| Questions Display | `frontend/src/pages/InterviewSimulation.tsx` | 150-200 | Show generated questions |
| Answer Input Textarea | `frontend/src/pages/InterviewSimulation.tsx` | 210-230 | Type interview answers |
| Submit Answer Button | `frontend/src/pages/InterviewSimulation.tsx` | 235-245 | Evaluate single answer |
| Feedback Display | `frontend/src/pages/InterviewSimulation.tsx` | 260-290 | Show scores and suggestions |
| Overall Score Calculation | `frontend/src/pages/InterviewSimulation.tsx` | 300-320 | Average all answers |
| Interview API Client | `frontend/src/lib/api.ts` | 70-80 | Three interview endpoints |
| Question Templates | `ml-service/interview_evaluator.py` | 15-130 | 60+ questions across 5 categories |
| Question Generation Logic | `ml-service/interview_evaluator.py` | 140-180 | Random selection with filtering |
| Sentiment Analysis | `ml-service/interview_evaluator.py` | 200-215 | DistilBERT for answer quality |
| Answer Evaluation | `ml-service/interview_evaluator.py` | 220-270 | Multi-factor scoring (0-10) |
| Generate Questions Endpoint | `ml-service/app.py` | 315-345 | `/interview/generate-questions` |
| Evaluate Answer Endpoint | `ml-service/app.py` | 350-380 | `/interview/evaluate-answer` |
| Calculate Score Endpoint | `ml-service/app.py` | 385-405 | `/interview/calculate-score` |

---

## 📊 NLP Job Parser

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| spaCy Model Loading | `ml-service/job_parser.py` | 10-15 | Load en_core_web_sm |
| Named Entity Recognition | `ml-service/job_parser.py` | 50-80 | Extract entities from text |
| Skills Extraction | `ml-service/job_parser.py` | 85-120 | Identify technical skills |
| Experience Parsing | `ml-service/job_parser.py` | 125-145 | Years and level detection |
| Salary Extraction | `ml-service/job_parser.py` | 150-170 | Parse salary ranges |
| Location Detection | `ml-service/job_parser.py` | 175-190 | Extract location info |
| Qualifications Parser | `ml-service/job_parser.py` | 195-220 | Education requirements |
| Employment Type | `ml-service/job_parser.py` | 225-240 | Full-time/Part-time/Contract |
| Parse Job Endpoint | `ml-service/app.py` | 215-245 | `/parse-job` POST route |
| Technical Skills DB | `ml-service/app.py` | 50-55 | List of 50+ skills |

---

## 📈 Match History & Scores

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Scores Page | `frontend/src/pages/Scores.tsx` | 1-193 | Match history display |
| Score Statistics Cards | `frontend/src/pages/Scores.tsx` | 60-100 | Total/Average/Monthly stats |
| Match History List | `frontend/src/pages/Scores.tsx` | 115-180 | All matches with details |
| Score Color Coding | `frontend/src/pages/Scores.tsx` | 26-30 | Visual score indicators |
| Keywords Display | `frontend/src/pages/Scores.tsx` | 150-165 | Matched keywords chips |
| Fetch Score History | `frontend/src/pages/Scores.tsx` | 14-22 | API call for user scores |
| Score API Client | `frontend/src/lib/api.ts` | 55-60 | Score endpoints |
| Backend Score Routes | `backend/src/routes/score.ts` | 1-180 | Express score endpoints |
| Score Calculation Endpoint | `backend/src/routes/score.ts` | 10-60 | POST /api/score |
| Score History Endpoint | `backend/src/routes/score.ts` | 86-115 | GET /api/score/history |
| ML Service Integration | `backend/src/routes/score.ts` | 23-30 | Call to ML predict-match |
| Save Score to Database | `backend/src/routes/score.ts` | 35-50 | Insert score record |
| Scores Database Table | `backend/database/schema.sql` | 38-48 | Scores table schema |

---

## 🎨 Dashboard & Navigation

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Dashboard Page | `frontend/src/pages/Dashboard.tsx` | 1-150 | Main overview page |
| Welcome Message | `frontend/src/pages/Dashboard.tsx` | 45-55 | Personalized greeting |
| Stats Cards | `frontend/src/pages/Dashboard.tsx` | 60-100 | Resume/Job/Match counts |
| Recent Activity | `frontend/src/pages/Dashboard.tsx` | 110-140 | Latest matches |
| Header Component | `frontend/src/components/Header.tsx` | 1-80 | Top navigation bar |
| User Profile Icon | `frontend/src/components/Header.tsx` | 35-50 | Avatar with dropdown |
| Sidebar Component | `frontend/src/components/Sidebar.tsx` | 1-200 | Left navigation menu |
| Mobile Hamburger Menu | `frontend/src/components/Sidebar.tsx` | 25-45 | Responsive toggle |
| Navigation Links | `frontend/src/components/Sidebar.tsx` | 90-140 | Route navigation |
| User Profile Section | `frontend/src/components/Sidebar.tsx` | 58-74 | Avatar, name, email |
| Layout Component | `frontend/src/components/Layout.tsx` | 1-50 | Main app structure |
| App Router | `frontend/src/App.tsx` | 1-100 | Route configuration |

---

## 🗄️ Database Schema

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| UUID Extension | `backend/database/schema.sql` | 6 | Enable uuid_generate_v4() |
| Resumes Table | `backend/database/schema.sql` | 12-21 | Resume storage schema |
| Jobs Table | `backend/database/schema.sql` | 25-35 | Job postings schema |
| Scores Table | `backend/database/schema.sql` | 38-48 | Match scores schema |
| ATS Scores Table | `backend/database/schema_additional.sql` | 10-20 | ATS analysis results |
| Interviews Table | `backend/database/schema_additional.sql` | 25-35 | Interview sessions |
| Indexes | `backend/database/schema.sql` | 50-65 | Performance optimization |
| Foreign Keys | `backend/database/schema.sql` | 68-78 | Referential integrity |
| JSONB Fields | `backend/database/schema.sql` | 16-32 | Skills, requirements arrays |
| RLS Policies | `backend/database/schema.sql` | 120-160 | Row-level security |
| Enable RLS Script | `backend/database/enable_rls.sql` | 1-50 | Apply RLS to tables |
| Disable RLS Script | `backend/database/populate_jobs.sql` | 1-15 | Remove RLS for demo |
| Sample Data | `backend/database/schema.sql` | 86-110 | Seed jobs |

---

## 🧪 Testing & Validation

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| ML Endpoints Test | `ml-service/test_ml_endpoints.py` | 1-200 | Test all 6 ML endpoints |
| Predict Match Test | `ml-service/test_ml_endpoints.py` | 24-50 | Test resume-job matching |
| Parse Job Test | `ml-service/test_ml_endpoints.py` | 55-75 | Test job parser |
| ATS Optimize Test | `ml-service/test_ml_endpoints.py` | 80-100 | Test ATS scoring |
| Interview Tests | `ml-service/test_ml_endpoints.py` | 105-150 | Test question generation |
| Model Evaluation | `ml-service/test_model.py` | 1-150 | Model accuracy testing |
| Health Check | `ml-service/app.py` | 135-142 | `/health` endpoint |

---

## 🔧 Configuration & Setup

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Frontend Package Config | `frontend/package.json` | 1-50 | Dependencies and scripts |
| Vite Configuration | `frontend/vite.config.ts` | 1-15 | Build settings |
| Tailwind Config | `frontend/tailwind.config.js` | 1-20 | CSS framework setup |
| TypeScript Config | `frontend/tsconfig.json` | 1-30 | TypeScript compiler options |
| Backend Package Config | `backend/package.json` | 1-50 | Node dependencies |
| Backend TypeScript Config | `backend/tsconfig.json` | 1-30 | Server-side TS settings |
| Supabase Backend Config | `backend/src/config/supabase.ts` | 1-15 | Database connection |
| ML Requirements | `ml-service/requirements.txt` | 1-30 | Python dependencies |
| ML Models Directory | `ml-service/models/resume_scorer/` | - | Trained model weights |
| Environment Variables | `.env` | 1-10 | API keys and secrets |
| Git Ignore | `.gitignore` | 1-50 | Excluded files |

---

## 📦 API Integration Layer

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Axios Instance | `frontend/src/lib/api.ts` | 5-10 | Base API client |
| Request Interceptor | `frontend/src/lib/api.ts` | 15-37 | Add auth headers |
| Resume API | `frontend/src/lib/api.ts` | 42-48 | Resume CRUD functions |
| Job API | `frontend/src/lib/api.ts` | 50-53 | Job endpoints |
| Score API | `frontend/src/lib/api.ts` | 55-61 | Match scoring |
| ATS API | `frontend/src/lib/api.ts` | 63-65 | ATS optimization |
| Interview API | `frontend/src/lib/api.ts` | 67-77 | Interview simulation |
| Backend Index | `backend/src/index.ts` | 1-100 | Express app setup |
| CORS Middleware | `backend/src/index.ts` | 20-28 | Enable cross-origin |
| Route Registration | `backend/src/index.ts` | 45-50 | Mount route handlers |
| ML Service App | `ml-service/app.py` | 1-50 | FastAPI app initialization |
| CORS Config | `ml-service/app.py` | 38-45 | Allow all origins |

---

## 🎯 Model Training Pipeline

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Data Generation | `ml-service/generate_dataset.py` | 1-200 | Synthetic data creation |
| Training Script | `ml-service/train_model.py` | 1-350 | Complete training flow |
| Model Initialization | `ml-service/train_model.py` | 45-75 | DistilBERT setup |
| Training Loop | `ml-service/train_model.py` | 150-250 | Epoch iteration |
| Validation | `ml-service/train_model.py` | 260-300 | Eval metrics |
| Model Saving | `ml-service/train_model.py` | 320-335 | Save weights |
| Hyperparameters | `ml-service/train_model.py` | 30-40 | Learning rate, epochs, etc. |
| Dataset Class | `ml-service/train_model.py` | 80-120 | PyTorch dataset |
| Data Loader | `ml-service/train_model.py` | 125-135 | Batch loading |

---

## 📱 Responsive Design

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Tailwind Breakpoints | `frontend/src/pages/*.tsx` | - | md:, lg: classes throughout |
| Mobile Sidebar Toggle | `frontend/src/components/Sidebar.tsx` | 25-45 | Hamburger menu |
| Mobile Overlay | `frontend/src/components/Sidebar.tsx` | 145-155 | Dark overlay click |
| Responsive Grid | `frontend/src/pages/Dashboard.tsx` | 60-100 | grid-cols-1 md:grid-cols-3 |
| Mobile Cards | `frontend/src/pages/Resumes.tsx` | 90-150 | Stack on small screens |
| Responsive Textareas | `frontend/src/pages/ATSOptimization.tsx` | 80-115 | h-64 md:h-96 |

---

## 🔍 Search & Filter

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Job Search | `frontend/src/pages/Jobs.tsx` | 52-70 | Title/company/location filter |
| Search Input | `frontend/src/pages/Jobs.tsx` | 58-66 | Text input with icon |
| Filter Logic | `frontend/src/pages/Jobs.tsx` | 72-78 | Array filter method |
| No Results Message | `frontend/src/pages/Jobs.tsx` | 47-49 | Empty state handling |

---

## 🚨 Error Handling

| Feature | File Path | Lines | Description |
|---------|-----------|-------|-------------|
| Frontend Try-Catch | `frontend/src/pages/*.tsx` | - | All async operations |
| API Error Display | `frontend/src/pages/Jobs.tsx` | 70-73 | Alert on failure |
| Backend Error Responses | `backend/src/routes/*.ts` | - | Consistent error format |
| ML Service Exceptions | `ml-service/app.py` | - | HTTPException usage |
| 404 Handling | `backend/src/routes/*.ts` | - | Resource not found |
| 500 Handling | `backend/src/routes/*.ts` | - | Server errors |
| Validation Errors | `frontend/src/pages/Signup.tsx` | 30-60 | Form validation |

---

## 📚 Documentation Files

| Document | File Path | Description |
|----------|-----------|-------------|
| Final Report | `FINAL_REPORT.tex` | Complete project documentation |
| Presentation Slides | `docs/PRESENTATION_SLIDES.md` | 10 slides for gamma.app |
| Traceability Matrix | `TRACEABILITY_MATRIX.md` | This document |
| Root README | `README.md` | Quick start guide |
| License | `LICENSE` | Project license |

---

## 🔑 Key Implementation Patterns

### Authentication Flow
1. User enters credentials → `Login.tsx` (line 45)
2. Call `signIn()` → `AuthContext.tsx` (line 60)
3. Supabase validates → `supabase.ts` (line 5)
4. JWT token stored in session
5. Axios interceptor adds token → `api.ts` (line 18)
6. Backend validates → `score.ts` (line 12)

### Resume-Job Matching Flow
1. User clicks "Match with Resume" → `Jobs.tsx` (line 196)
2. Opens resume selector modal → `Jobs.tsx` (line 220)
3. User selects resume → `Jobs.tsx` (line 50)
4. Frontend calls backend → `api.ts` (line 56)
5. Backend calls ML service → `score.ts` (line 23)
6. DistilBERT predicts score → `app.py` (line 185)
7. Save to database → `score.ts` (line 35)
8. Navigate to scores page → `Jobs.tsx` (line 68)

### ATS Optimization Flow
1. User pastes text → `ATSOptimization.tsx` (line 80)
2. Click "Analyze" → `ATSOptimization.tsx` (line 120)
3. Direct ML service call → `api.ts` (line 64)
4. TF-IDF vectorization → `ats_optimizer.py` (line 25)
5. Calculate similarity → `ats_optimizer.py` (line 45)
6. Generate suggestions → `ats_optimizer.py` (line 161)
7. Display results → `ATSOptimization.tsx` (line 160)

---

## 📞 Quick Reference

**Need to find authentication?** → Look for `AuthContext.tsx` or `Login.tsx`  
**Need to find ML model?** → Check `ml-service/app.py` lines 65-210  
**Need to find database schema?** → See `backend/database/schema.sql`  
**Need to find resume matching?** → Go to `Jobs.tsx` line 50 or `app.py` line 150  
**Need to find ATS scoring?** → Check `ats_optimizer.py` line 161 or `ATSOptimization.tsx` line 120  
**Need to find interview questions?** → See `interview_evaluator.py` lines 15-130  

---

**Last Updated:** November 27, 2025  
**Project:** ResumeCoach AI - Generative AI Term Project  
**Author:** Muhammad Hamdan Rauf
