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

## 🤝 Contributing

This is a student project for Gen AI course at FAST University.


