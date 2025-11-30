import { useState, useEffect } from 'react';
import { FileText, Upload, Trash2, Edit, Eye } from 'lucide-react';
import { resumeApi } from '../lib/api';
import ResumeUploadForm from '../components/ResumeUploadForm';

const Resumes = () => {
  const [resumes, setResumes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showUploadForm, setShowUploadForm] = useState(false);
  const [viewingResume, setViewingResume] = useState<any>(null);
  const [editingResume, setEditingResume] = useState<any>(null);
  // Removed unused formData state

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      const response = await resumeApi.getAll();
      setResumes(response.data.resumes || []);
    } catch (error) {
      console.error('Error fetching resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this resume?')) {
      try {
        await resumeApi.delete(id);
        fetchResumes();
      } catch (error) {
        console.error('Error deleting resume:', error);
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Resumes</h1>
          <p className="text-gray-500 mt-1">
            {resumes.length > 0 
              ? `You have ${resumes.length} resume${resumes.length > 1 ? 's' : ''} uploaded` 
              : 'Upload your first resume to get started'}
          </p>
        </div>
        <button
          onClick={() => setShowUploadForm(!showUploadForm)}
          className="btn-primary flex items-center gap-2"
        >
          <Upload size={20} />
          Upload Resume
        </button>
      </div>

      {/* Upload Form Modal */}
      {showUploadForm && (
        <ResumeUploadForm
          onUploadSuccess={() => {
            fetchResumes();
            setShowUploadForm(false);
          }}
          onClose={() => setShowUploadForm(false)}
        />
      )}

      {/* Resumes List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {resumes.length === 0 ? (
          <div className="col-span-full card text-center py-12">
            <FileText size={48} className="mx-auto mb-3 text-gray-400" />
            <p className="text-gray-500 font-medium">No resumes yet</p>
            <p className="text-sm text-gray-400 mt-1">Click "Upload Resume" to add your first resume</p>
          </div>
        ) : (
          resumes.map((resume) => (
            <div key={resume.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="bg-primary-100 p-2 rounded-lg">
                    <FileText size={24} className="text-primary-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">{resume.title}</h3>
                    <p className="text-xs text-gray-500">
                      {new Date(resume.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>

              <p className="text-sm text-gray-600 mb-4 line-clamp-3">{resume.content}</p>

              {resume.skills && resume.skills.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {resume.skills.slice(0, 3).map((skill: string, index: number) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                    >
                      {skill}
                    </span>
                  ))}
                  {resume.skills.length > 3 && (
                    <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                      +{resume.skills.length - 3} more
                    </span>
                  )}
                </div>
              )}

              <div className="flex gap-2 pt-4 border-t">
                <button 
                  onClick={() => setViewingResume(resume)}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm bg-primary-50 text-primary-600 rounded-lg hover:bg-primary-100 transition-colors"
                >
                  <Eye size={16} />
                  View
                </button>
                <button 
                  onClick={() => setEditingResume(resume)}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  <Edit size={16} />
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(resume.id)}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 text-sm bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors"
                >
                  <Trash2 size={16} />
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* View Resume Modal */}
      {viewingResume && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">{viewingResume.title}</h2>
                  <p className="text-sm text-gray-500 mt-1">
                    Created: {new Date(viewingResume.created_at).toLocaleDateString()}
                  </p>
                </div>
                <button
                  onClick={() => setViewingResume(null)}
                  className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
                >
                  ×
                </button>
              </div>

              {viewingResume.skills && viewingResume.skills.length > 0 && (
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-900 mb-3">Skills</h3>
                  <div className="flex flex-wrap gap-2">
                    {viewingResume.skills.map((skill: string, index: number) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-primary-50 text-primary-700 text-sm rounded-full font-medium"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-3">Resume Content</h3>
                <div className="prose max-w-none">
                  <p className="text-gray-700 whitespace-pre-wrap">{viewingResume.content}</p>
                </div>
              </div>

              <div className="flex gap-3 pt-4 border-t">
                <button
                  onClick={() => {
                    setViewingResume(null);
                    setEditingResume(viewingResume);
                  }}
                  className="btn-secondary flex items-center gap-2"
                >
                  <Edit size={16} />
                  Edit Resume
                </button>
                <button
                  onClick={() => setViewingResume(null)}
                  className="btn-primary"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Edit Resume Modal */}
      {editingResume && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-start justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Edit Resume</h2>
                <button
                  onClick={() => setEditingResume(null)}
                  className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
                >
                  ×
                </button>
              </div>

              <form
                onSubmit={async (e) => {
                  e.preventDefault();
                  try {
                    await resumeApi.update(editingResume.id, editingResume);
                    setEditingResume(null);
                    fetchResumes();
                  } catch (error) {
                    console.error('Error updating resume:', error);
                    alert('Failed to update resume');
                  }
                }}
                className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Resume Title *
                  </label>
                  <input
                    type="text"
                    value={editingResume.title}
                    onChange={(e) => setEditingResume({ ...editingResume, title: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Skills (comma-separated)
                  </label>
                  <input
                    type="text"
                    value={editingResume.skills?.join(', ') || ''}
                    onChange={(e) => setEditingResume({
                      ...editingResume,
                      skills: e.target.value.split(',').map((s: string) => s.trim()).filter(Boolean)
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="e.g., JavaScript, React, Node.js"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Resume Content *
                  </label>
                  <textarea
                    value={editingResume.content}
                    onChange={(e) => setEditingResume({ ...editingResume, content: e.target.value })}
                    rows={12}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent font-mono text-sm"
                    required
                  />
                </div>

                <div className="flex gap-3 pt-4 border-t">
                  <button type="submit" className="btn-primary">
                    Save Changes
                  </button>
                  <button
                    type="button"
                    onClick={() => setEditingResume(null)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Resumes;
