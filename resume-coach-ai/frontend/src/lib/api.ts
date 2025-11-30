import axios from 'axios';
import { supabase } from './supabase';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add authentication headers
api.interceptors.request.use(async (config) => {
  // Get current session from Supabase
  const { data: { session } } = await supabase.auth.getSession();
  
  if (session?.access_token) {
    // Add Supabase JWT token
    config.headers['Authorization'] = `Bearer ${session.access_token}`;
    
    // Add user ID from session
    if (session.user?.id) {
      config.headers['x-user-id'] = session.user.id;
    }
  } else {
    // Fallback for demo mode (no auth)
    let userId = localStorage.getItem('userId');
    if (!userId) {
      userId = '550e8400-e29b-41d4-a716-446655440000'; // Default test UUID
      localStorage.setItem('userId', userId);
    }
    config.headers['x-user-id'] = userId;
  }
  
  return config;
});

// API functions
export const resumeApi = {
  getAll: () => api.get('/api/resumes'),
  getById: (id: string) => api.get(`/api/resumes/${id}`),
  create: (data: any) => api.post('/api/resumes', data),
  update: (id: string, data: any) => api.put(`/api/resumes/${id}`, data),
  delete: (id: string) => api.delete(`/api/resumes/${id}`),
};

export const jobApi = {
  getAll: () => api.get('/api/jobs'),
  getById: (id: string) => api.get(`/api/jobs/${id}`),
};

export const scoreApi = {
  calculate: (data: { resume_text: string; job_description: string; resume_id?: string; job_id?: string; user_id?: string }) =>
    api.post('/api/score', data),
  getHistory: () => api.get('/api/score/history'),
  getById: (id: string) => api.get(`/api/score/${id}`),
  checkMLHealth: () => api.get('/api/score/ml/health'),
};

export const atsApi = {
  optimize: (data: { resume_text: string; job_description: string }) =>
    axios.post('http://localhost:8000/optimize-ats', data),
};

export const interviewApi = {
  generateQuestions: (data: { job_description: string; job_role?: string; num_questions?: number }) =>
    axios.post('http://localhost:8000/interview/generate-questions', data),
  evaluateAnswer: (data: { question: string; answer: string; category: string; difficulty: string }) =>
    axios.post('http://localhost:8000/interview/evaluate-answer', data),
  calculateScore: (data: { evaluations: Array<{ score: number; category: string }> }) =>
    axios.post('http://localhost:8000/interview/calculate-score', data),
};
