export interface Resume {
  id: number;
  user_id: number;
  title: string;
  content: string;
  skills: string[];
  created_at: string;
  updated_at: string;
}

export interface ParsedResume {
  content: string;
  filename: string;
  fileType: 'pdf' | 'docx';
  wordCount: number;
  extractedAt: string;
}

export interface UploadStatus {
  isUploading: boolean;
  progress: number;
  error: string | null;
  success: boolean;
}

export interface ResumeUploadData {
  title: string;
  content: string;
  skills: string[];
  filename?: string;
}

export interface ResumeFormData {
  title: string;
  content: string;
  skills: string;
}
