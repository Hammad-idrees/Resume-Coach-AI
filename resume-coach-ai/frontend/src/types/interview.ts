// TypeScript interfaces for Interview Simulation module

export interface InterviewQuestion {
  id: number;
  question: string;
  category: string;
  difficulty: string;
}

export interface GenerateQuestionsRequest {
  job_description: string;
  job_role?: string;
  num_questions?: number;
}

export interface GenerateQuestionsResponse {
  questions: InterviewQuestion[];
  total_questions: number;
}

export interface EvaluateAnswerRequest {
  question: string;
  answer: string;
  category: string;
  difficulty: string;
}

export interface EvaluateAnswerResponse {
  score: number;
  overall_feedback: string;
  strengths: string[];
  improvements: string[];
  sentiment: string;
  word_count: number;
  has_example: boolean;
  has_result: boolean;
}

export interface InterviewMessage {
  id: number;
  role: 'assistant' | 'user';
  content: string;
  timestamp: Date;
  evaluation?: EvaluateAnswerResponse;
  question?: InterviewQuestion;
}

export interface InterviewScoreRequest {
  evaluations: Array<{
    score: number;
    category: string;
  }>;
}

export interface InterviewScoreResponse {
  overall_score: number;
  average_score: number;
  grade: string;
  total_questions: number;
  questions_answered: number;
  summary: string;
  category_breakdown: Record<string, number>;
}

export interface InterviewSession {
  id: string;
  job_description: string;
  job_role: string;
  questions: InterviewQuestion[];
  messages: InterviewMessage[];
  current_question_index: number;
  started_at: Date;
  completed_at?: Date;
  final_score?: InterviewScoreResponse;
}
