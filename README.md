# Resume Coach AI

Resume Coach AI is an end-to-end platform that helps jobseekers improve their resumes and interview readiness using automated parsing, ATS-aware optimization, job matching, and machine-learning-driven interview evaluation. The codebase is split into three main parts: `frontend` (React + Vite), `backend` (TypeScript/Express with Supabase integration), and `ml-service` (Python ML models and APIs). This repository contains everything needed to run the full stack locally or deploy it to a cloud environment for experimentation and demonstration.

**Quick description:** AI-powered resume assistant: parse resumes and job posts, suggest ATS optimizations, match candidates to roles, and simulate interview feedback with explainable recommendations.

## Contents

- **`frontend/`** — React application (Vite) for uploading resumes, viewing suggestions, and running interview simulations.
- **`backend/`** — TypeScript/Express API that handles authentication, resume/job parsing, scoring, and orchestration with the ML service. Integrates with Supabase for storage and auth.
- **`ml-service/`** — Python ML models and APIs for ATS scoring, interview simulation, and data preparation. Contains training scripts and tests.
- **`docs/`** — Project documentation, testing notes, and deployment guides.
- **`database/`** (under `backend/`) — SQL schema and helper scripts for database setup and sample data.

## Highlights & Features

- Resume parsing and structured extraction (skills, experience, education).
- ATS-aware scoring and optimization suggestions (keywords, formatting, section improvements).
- Job parsing and job–resume matching.
- Interview simulation: generate likely questions and evaluate responses using ML models.
- Explanations: every suggestion connects back to detected gaps and example phrasing.
- Extensible modular architecture so models, rules, or UI flows can be replaced or upgraded.

## Getting started (local)

Below are general steps to run components locally. Check each subfolder for more specific instructions and scripts.

### Prerequisites

- Node.js (16+) and npm or yarn
- Python 3.8+ and `pip`
- Git
- (Optional) Supabase account or local Postgres for the backend

### 1) Clone the repo (if not already local)

```powershell
git clone https://github.com/<your-username>/resume-coach-ai.git
cd resume-coach-ai
```

### 2) Frontend

```powershell
cd frontend
npm install
# Start dev server (check package.json for exact script)
npm run dev
```

### 3) Backend

```powershell
cd backend
npm install
# Build/Run - check tsconfig and package.json scripts
npm run dev    # or `npm start` depending on scripts
```

### 4) ML service (Python)

```powershell
cd ml-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Start the API (see app.py or ml-service README)
python app.py
```

### 5) Database & Supabase

- See `backend/database/SETUP.md` and SQL files in `backend/database/` for schema and sample data. Configure Supabase keys/db URL in `backend/src/config/supabase.ts` or via environment variables.

## Testing

- Unit and integration tests for backend and ML components exist in each service folder. Run them with the commands listed in the respective `package.json` or test files (Python tests use `pytest`).

## Development notes

- The repository separates concerns: UI, API, and models. To extend the system, add new scoring models to `ml-service/models.py`, update API routes in `backend/src/routes/`, and add UI components under `frontend/src/components/`.
- Configuration and secrets should be provided via environment variables — do not commit secrets to git.

## Contributing

- Open an issue to discuss features or bug fixes.
- Fork the repo, create a feature branch, and submit a pull request with tests and documentation for non-trivial changes.

## License

- See the `LICENSE` file in the repository root for licensing terms.

## Contact

- Author: Muhammad Hamdan Rauf
- Repo: https://github.com/Muhammad-Hamdan-Rauf/resume-coach-ai

If you want, I can now run the local git commands to initialize (if needed), create a `.gitignore`, commit this `README.md`, and help push to GitHub — tell me whether you'd like me to proceed and whether you prefer using the `gh` CLI or creating the remote yourself.

# 🚀 ResumeCoach AI

AI-powered platform for resume optimization, ATS scoring, and interview preparation using DistilBERT and NLP.

## 📁 Project Structure

```
ResumeCoach AI/
├── frontend/          # React 18 + TypeScript + Vite
├── backend/           # Express.js + TypeScript + Supabase
├── ml-service/        # FastAPI + DistilBERT + spaCy
├── docs/              # Presentation materials
├── FINAL_REPORT.tex   # Complete project documentation
└── TRACEABILITY_MATRIX.md  # Feature implementation reference
```

## 🛠️ Tech Stack

**Frontend:** React 18.2, TypeScript 5.0, Vite 5.0, Tailwind CSS, Supabase Auth  
**Backend:** Express.js, TypeScript, Supabase PostgreSQL, Axios  
**ML Service:** FastAPI, DistilBERT, PyTorch, spaCy 3.7.6, scikit-learn, NLTK

## 🚀 Quick Start

### Prerequisites

Node.js 18+, Python 3.10+, Supabase account

### Installation

```bash
# Frontend (Port 5173)
cd frontend
npm install
npm run dev

# Backend (Port 3000)
cd backend
npm install
npm run dev

# ML Service (Port 8000)
cd ml-service
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## ✨ Core Features

- **Resume-Job Matching** - DistilBERT model with 92%+ accuracy (MAE: 10.37)
- **ATS Optimization** - TF-IDF based scoring with actionable feedback
- **Job Parsing** - spaCy NER for structured data extraction
- **Interview Simulator** - 60+ questions with sentiment-based evaluation
- **Authentication** - JWT tokens with Row-Level Security

## 📊 Testing Results

127 test cases | 100% ML service pass rate | 6/6 AI endpoints operational

## 📖 Documentation

- **Full Report:** `FINAL_REPORT.tex`
- **Traceability Matrix:** `TRACEABILITY_MATRIX.md`
- **API Docs:** `http://localhost:8000/docs` (Swagger UI)
- `POST /optimize-ats` - Get ATS optimization suggestions

