import { useState } from 'react';
import { resumeApi } from '../lib/api';
import { parseResume, extractSkills } from '../utils/parseResume';
import type { UploadStatus, ResumeUploadData, ParsedResume } from '../types/resume';

interface UseResumeUploadReturn {
  uploadStatus: UploadStatus;
  parsedResume: ParsedResume | null;
  uploadResume: (file: File, title?: string) => Promise<void>;
  resetUpload: () => void;
}

export const useResumeUpload = (): UseResumeUploadReturn => {
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>({
    isUploading: false,
    progress: 0,
    error: null,
    success: false,
  });
  
  const [parsedResume, setParsedResume] = useState<ParsedResume | null>(null);
  
  const uploadResume = async (file: File, title?: string) => {
    try {
      // Reset state
      setUploadStatus({
        isUploading: true,
        progress: 0,
        error: null,
        success: false,
      });
      setParsedResume(null);
      
      // Step 1: Parse the file (30% progress)
      setUploadStatus(prev => ({ ...prev, progress: 10 }));
      const parsed = await parseResume(file);
      setParsedResume(parsed);
      setUploadStatus(prev => ({ ...prev, progress: 30 }));
      
      // Step 2: Extract skills (50% progress)
      const extractedSkills = extractSkills(parsed.content);
      setUploadStatus(prev => ({ ...prev, progress: 50 }));
      
      // Step 3: Prepare upload data
      const uploadData: ResumeUploadData = {
        title: title || file.name.replace(/\.(pdf|docx)$/i, ''),
        content: parsed.content,
        skills: extractedSkills,
        filename: parsed.filename,
      };
      
      setUploadStatus(prev => ({ ...prev, progress: 70 }));
      
      // Step 4: Upload to backend
      await resumeApi.create(uploadData);
      
      setUploadStatus({
        isUploading: false,
        progress: 100,
        error: null,
        success: true,
      });
    } catch (error: any) {
      console.error('Resume upload error:', error);
      
      setUploadStatus({
        isUploading: false,
        progress: 0,
        error: error.message || 'Failed to upload resume. Please try again.',
        success: false,
      });
    }
  };
  
  const resetUpload = () => {
    setUploadStatus({
      isUploading: false,
      progress: 0,
      error: null,
      success: false,
    });
    setParsedResume(null);
  };
  
  return {
    uploadStatus,
    parsedResume,
    uploadResume,
    resetUpload,
  };
};
