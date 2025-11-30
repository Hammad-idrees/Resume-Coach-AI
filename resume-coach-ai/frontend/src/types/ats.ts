export interface ATSOptimizationRequest {
  resume_text: string;
  job_description: string;
}

export interface ATSOptimizationResponse {
  ats_score: number;
  keyword_match_percentage: number;
  missing_keywords: string[];
  matched_keywords: string[];
  suggestions: string[];
  tfidf_similarity: number;
  resume_keyword_count: number;
  job_keyword_count: number;
}

export interface ATSAnalysis extends ATSOptimizationResponse {
  analyzed_at?: string;
}
