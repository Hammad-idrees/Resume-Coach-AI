import * as pdfjsLib from 'pdfjs-dist';
import mammoth from 'mammoth';
import type { ParsedResume } from '../types/resume';

// Configure PDF.js worker using jsdelivr CDN
if (typeof window !== 'undefined') {
  pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjsLib.version}/build/pdf.worker.min.mjs`;
}

/**
 * Parse PDF file to extract text content
 */
export const parsePDF = async (file: File): Promise<string> => {
  try {
    const arrayBuffer = await file.arrayBuffer();
    
    // Load the PDF document
    const loadingTask = pdfjsLib.getDocument({
      data: arrayBuffer,
      useWorkerFetch: false,
      isEvalSupported: false,
      useSystemFonts: true,
    });
    
    const pdf = await loadingTask.promise;
    
    let fullText = '';
    
    // Extract text from each page
    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
      const page = await pdf.getPage(pageNum);
      const textContent = await page.getTextContent();
      const pageText = textContent.items
        .map((item: any) => item.str)
        .join(' ');
      fullText += pageText + '\n';
    }
    
    return fullText.trim();
  } catch (error: any) {
    console.error('Error parsing PDF:', error);
    console.error('Error details:', error.message, error.name);
    throw new Error(`Failed to parse PDF file: ${error.message || 'Unknown error'}. Please ensure it's a valid PDF document.`);
  }
};

/**
 * Parse DOCX file to extract text content
 */
export const parseDOCX = async (file: File): Promise<string> => {
  try {
    const arrayBuffer = await file.arrayBuffer();
    const result = await mammoth.extractRawText({ arrayBuffer });
    
    if (result.messages.length > 0) {
      console.warn('DOCX parsing warnings:', result.messages);
    }
    
    return result.value.trim();
  } catch (error) {
    console.error('Error parsing DOCX:', error);
    throw new Error('Failed to parse DOCX file. Please ensure it\'s a valid Word document.');
  }
};

/**
 * Main resume parsing function that handles both PDF and DOCX
 */
export const parseResume = async (file: File): Promise<ParsedResume> => {
  const fileType = file.name.toLowerCase().endsWith('.pdf') ? 'pdf' : 'docx';
  
  let content: string;
  
  if (fileType === 'pdf') {
    content = await parsePDF(file);
  } else if (fileType === 'docx') {
    content = await parseDOCX(file);
  } else {
    throw new Error('Unsupported file type. Please upload a PDF or DOCX file.');
  }
  
  // Clean up the text
  content = content
    .replace(/\s+/g, ' ') // Replace multiple spaces with single space
    .replace(/\n+/g, '\n') // Replace multiple newlines with single newline
    .trim();
  
  const wordCount = content.split(/\s+/).filter(word => word.length > 0).length;
  
  return {
    content,
    filename: file.name,
    fileType,
    wordCount,
    extractedAt: new Date().toISOString(),
  };
};

/**
 * Validate resume file
 */
export const validateResumeFile = (file: File): { valid: boolean; error?: string } => {
  const maxSize = 10 * 1024 * 1024; // 10MB
  const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  
  if (file.size > maxSize) {
    return {
      valid: false,
      error: 'File size exceeds 10MB limit',
    };
  }
  
  if (!allowedTypes.includes(file.type)) {
    return {
      valid: false,
      error: 'Only PDF and DOCX files are allowed',
    };
  }
  
  return { valid: true };
};

/**
 * Extract potential skills from resume text
 */
export const extractSkills = (content: string): string[] => {
  // Common tech skills and keywords
  const skillKeywords = [
    'javascript', 'typescript', 'python', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
    'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'laravel',
    'html', 'css', 'sass', 'tailwind', 'bootstrap', 'material-ui',
    'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'firebase', 'supabase',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd',
    'git', 'github', 'gitlab', 'bitbucket',
    'agile', 'scrum', 'jira', 'trello',
    'machine learning', 'deep learning', 'ai', 'data science', 'nlp',
    'rest api', 'graphql', 'microservices', 'serverless',
    'testing', 'jest', 'mocha', 'pytest', 'junit',
  ];
  
  const contentLower = content.toLowerCase();
  const foundSkills = new Set<string>();
  
  skillKeywords.forEach(skill => {
    if (contentLower.includes(skill.toLowerCase())) {
      foundSkills.add(skill);
    }
  });
  
  return Array.from(foundSkills).slice(0, 15); // Return top 15 skills
};
