import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, CheckCircle, AlertCircle, X, FileText } from 'lucide-react';
import { useResumeUpload } from '../hooks/useResumeUpload';
import { validateResumeFile } from '../utils/parseResume';

interface ResumeUploadFormProps {
  onUploadSuccess: () => void;
  onClose: () => void;
}

const ResumeUploadForm: React.FC<ResumeUploadFormProps> = ({ onUploadSuccess, onClose }) => {
  const [title, setTitle] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { uploadStatus, parsedResume, uploadResume, resetUpload } = useResumeUpload();

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      const validation = validateResumeFile(file);
      
      if (!validation.valid) {
        alert(validation.error);
        return;
      }
      
      setSelectedFile(file);
      // Auto-fill title from filename
      if (!title) {
        setTitle(file.name.replace(/\.(pdf|docx)$/i, ''));
      }
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
    disabled: uploadStatus.isUploading,
  });

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file to upload');
      return;
    }
    
    if (!title.trim()) {
      alert('Please enter a resume title');
      return;
    }

    await uploadResume(selectedFile, title);
  };

  const handleClose = () => {
    resetUpload();
    setSelectedFile(null);
    setTitle('');
    onClose();
  };

  // Auto-close on success after 2 seconds
  if (uploadStatus.success) {
    setTimeout(() => {
      onUploadSuccess();
      handleClose();
    }, 2000);
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">Upload Resume</h2>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            disabled={uploadStatus.isUploading}
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Title Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Resume Title *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g., Software Engineer Resume 2024"
              className="input-field"
              disabled={uploadStatus.isUploading}
            />
          </div>

          {/* File Upload Area */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload File *
            </label>
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                isDragActive
                  ? 'border-primary-500 bg-primary-50'
                  : selectedFile
                  ? 'border-green-500 bg-green-50'
                  : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
              } ${uploadStatus.isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <input {...getInputProps()} />
              
              {selectedFile ? (
                <div className="flex items-center justify-center gap-3">
                  <FileText size={32} className="text-green-600" />
                  <div className="text-left">
                    <p className="font-medium text-gray-900">{selectedFile.name}</p>
                    <p className="text-sm text-gray-500">
                      {(selectedFile.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                </div>
              ) : (
                <>
                  <Upload size={48} className="mx-auto mb-3 text-gray-400" />
                  <p className="text-gray-700 font-medium mb-1">
                    {isDragActive
                      ? 'Drop the file here'
                      : 'Drag & drop your resume or click to browse'}
                  </p>
                  <p className="text-sm text-gray-500">
                    Supports PDF and DOCX files (max 10MB)
                  </p>
                </>
              )}
            </div>
          </div>

          {/* Progress Bar */}
          {uploadStatus.isUploading && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Uploading...</span>
                <span className="font-medium text-primary-600">{uploadStatus.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadStatus.progress}%` }}
                />
              </div>
            </div>
          )}

          {/* Parsed Resume Preview */}
          {parsedResume && !uploadStatus.error && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <File size={20} className="text-blue-600 mt-1" />
                <div className="flex-1">
                  <p className="font-medium text-blue-900 mb-1">File Parsed Successfully</p>
                  <p className="text-sm text-blue-700">
                    Extracted {parsedResume.wordCount} words from {parsedResume.filename}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Success Message */}
          {uploadStatus.success && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <CheckCircle size={20} className="text-green-600 mt-1" />
                <div className="flex-1">
                  <p className="font-medium text-green-900 mb-1">Upload Successful!</p>
                  <p className="text-sm text-green-700">
                    Your resume has been uploaded and processed successfully.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Error Message */}
          {uploadStatus.error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <AlertCircle size={20} className="text-red-600 mt-1" />
                <div className="flex-1">
                  <p className="font-medium text-red-900 mb-1">Upload Failed</p>
                  <p className="text-sm text-red-700">{uploadStatus.error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Instructions */}
          {!selectedFile && !uploadStatus.isUploading && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="font-medium text-gray-900 mb-2">Instructions:</h3>
              <ul className="text-sm text-gray-600 space-y-1 list-disc list-inside">
                <li>Upload your resume in PDF or DOCX format</li>
                <li>The system will automatically extract text and identify skills</li>
                <li>You can edit the extracted content after upload</li>
                <li>Maximum file size is 10MB</li>
              </ul>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={handleClose}
            className="btn-secondary"
            disabled={uploadStatus.isUploading}
          >
            Cancel
          </button>
          <button
            onClick={handleUpload}
            disabled={!selectedFile || !title.trim() || uploadStatus.isUploading || uploadStatus.success}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {uploadStatus.isUploading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                Processing...
              </>
            ) : (
              <>
                <Upload size={18} />
                Upload Resume
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResumeUploadForm;
