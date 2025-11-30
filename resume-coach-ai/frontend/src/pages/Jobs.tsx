import { useState, useEffect } from 'react';
import { Briefcase, MapPin, DollarSign, Search, ExternalLink, FileText } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { jobApi, resumeApi, scoreApi } from '../lib/api';
import { useNavigate } from 'react-router-dom';

const Jobs = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedJob, setSelectedJob] = useState<any>(null);
  const [resumes, setResumes] = useState<any[]>([]);
  const [showResumeSelector, setShowResumeSelector] = useState(false);
  const [matchingResume, setMatchingResume] = useState<any>(null);
  const [matchingJob, setMatchingJob] = useState<any>(null);
  const [isCalculatingMatch, setIsCalculatingMatch] = useState(false);

  useEffect(() => {
    fetchJobs();
    fetchResumes();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await jobApi.getAll();
      setJobs(response.data.jobs || []);
    } catch (error) {
      console.error('Error fetching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchResumes = async () => {
    try {
      const response = await resumeApi.getAll();
      setResumes(response.data.resumes || []);
    } catch (error) {
      console.error('Error fetching resumes:', error);
    }
  };

  const handleMatchWithResume = (job: any) => {
    setMatchingJob(job);
    setShowResumeSelector(true);
    setSelectedJob(null);
  };

  const handleResumeSelection = async (resume: any) => {
    setMatchingResume(resume);
    setIsCalculatingMatch(true);

    try {
      const jobDescription = `${matchingJob.title}\n${matchingJob.description}\nRequirements: ${matchingJob.requirements?.join(', ') || ''}\nSkills: ${matchingJob.skills?.join(', ') || ''}`;
      
      await scoreApi.calculate({
        resume_text: resume.content,
        job_description: jobDescription,
        resume_id: resume.id,
        job_id: matchingJob.id,
        user_id: user?.id
      });

      // Navigate to scores page with the new match
      setShowResumeSelector(false);
      setMatchingResume(null);
      setMatchingJob(null);
      navigate('/scores');
    } catch (error: any) {
      console.error('Error calculating match:', error);
      alert(error.response?.data?.error || 'Failed to calculate match score. Please try again.');
    } finally {
      setIsCalculatingMatch(false);
    }
  };

  const filteredJobs = jobs.filter((job) =>
    job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Job Listings</h1>
        <p className="text-gray-500 mt-1">
          {filteredJobs.length > 0 
            ? `Showing ${filteredJobs.length} job${filteredJobs.length > 1 ? 's' : ''} - Find your perfect match` 
            : 'No jobs found. Try adjusting your search.'}
        </p>
      </div>

      {/* Search */}
      <div className="card">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search by title, company, or location..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
          />
        </div>
      </div>

      {/* Jobs Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredJobs.length === 0 ? (
          <div className="col-span-full card text-center py-12">
            <Briefcase size={48} className="mx-auto mb-3 text-gray-400" />
            <p className="text-gray-500 font-medium">No jobs found</p>
            <p className="text-sm text-gray-400 mt-1">Try adjusting your search</p>
          </div>
        ) : (
          filteredJobs.map((job) => (
            <div
              key={job.id}
              className="card hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => setSelectedJob(job)}
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="font-bold text-lg text-gray-900">{job.title}</h3>
                  <p className="text-gray-600 font-medium mt-1">{job.company}</p>
                </div>
                <div className="bg-primary-100 p-2 rounded-lg">
                  <Briefcase size={20} className="text-primary-600" />
                </div>
              </div>

              <div className="space-y-2 mb-4">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <MapPin size={16} />
                  <span>{job.location}</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <DollarSign size={16} />
                  <span>{job.salary}</span>
                </div>
              </div>

              <p className="text-sm text-gray-600 mb-4 line-clamp-2">{job.description}</p>

              {job.skills && job.skills.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {job.skills.slice(0, 5).map((skill: string, index: number) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-primary-50 text-primary-700 text-xs rounded-full font-medium"
                    >
                      {skill}
                    </span>
                  ))}
                  {job.skills.length > 5 && (
                    <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                      +{job.skills.length - 5} more
                    </span>
                  )}
                </div>
              )}

              <button className="w-full btn-primary flex items-center justify-center gap-2">
                View Details
                <ExternalLink size={16} />
              </button>
            </div>
          ))
        )}
      </div>

      {/* Job Detail Modal */}
      {selectedJob && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">{selectedJob.title}</h2>
                  <p className="text-xl text-gray-600 mt-1">{selectedJob.company}</p>
                </div>
                <button
                  onClick={() => setSelectedJob(null)}
                  className="text-gray-400 hover:text-gray-600 text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="space-y-2 mb-6">
                <div className="flex items-center gap-2 text-gray-700">
                  <MapPin size={18} />
                  <span>{selectedJob.location}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-700">
                  <DollarSign size={18} />
                  <span>{selectedJob.salary}</span>
                </div>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold text-lg text-gray-900 mb-3">Description</h3>
                <p className="text-gray-600 leading-relaxed">{selectedJob.description}</p>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold text-lg text-gray-900 mb-3">Required Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedJob.skills?.map((skill: string, index: number) => (
                    <span
                      key={index}
                      className="px-3 py-1.5 bg-primary-50 text-primary-700 rounded-full font-medium"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              {selectedJob.requirements && selectedJob.requirements.length > 0 && (
                <div className="mb-6">
                  <h3 className="font-semibold text-lg text-gray-900 mb-3">Requirements</h3>
                  <ul className="space-y-2">
                    {selectedJob.requirements.map((req: string, index: number) => (
                      <li key={index} className="flex items-start gap-2 text-gray-600">
                        <span className="text-primary-600 mt-1">•</span>
                        <span>{req}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="flex gap-3 pt-4 border-t">
                <button 
                  className="flex-1 btn-primary"
                  onClick={() => handleMatchWithResume(selectedJob)}
                >
                  Match with Resume
                </button>
                <button
                  onClick={() => setSelectedJob(null)}
                  className="flex-1 btn-secondary"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Resume Selector Modal */}
      {showResumeSelector && matchingJob && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Select Resume to Match
              </h2>
              <p className="text-gray-600 mb-6">
                Choose a resume to calculate match score with <strong>{matchingJob.title}</strong>
              </p>

              {resumes.length === 0 ? (
                <div className="text-center py-8">
                  <FileText className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                  <p className="text-gray-600 mb-4">No resumes found</p>
                  <button
                    onClick={() => {
                      setShowResumeSelector(false);
                      navigate('/resumes');
                    }}
                    className="btn-primary"
                  >
                    Create Resume
                  </button>
                </div>
              ) : (
                <div className="space-y-3">
                  {resumes.map((resume) => (
                    <div
                      key={resume.id}
                      className="border rounded-lg p-4 hover:border-primary-500 hover:bg-primary-50 cursor-pointer transition-colors"
                      onClick={() => !isCalculatingMatch && handleResumeSelection(resume)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900">{resume.title}</h3>
                          {resume.skills && resume.skills.length > 0 && (
                            <div className="flex flex-wrap gap-2 mt-2">
                              {resume.skills.slice(0, 5).map((skill: string, index: number) => (
                                <span
                                  key={index}
                                  className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
                                >
                                  {skill}
                                </span>
                              ))}
                              {resume.skills.length > 5 && (
                                <span className="px-2 py-1 text-gray-500 text-xs">
                                  +{resume.skills.length - 5} more
                                </span>
                              )}
                            </div>
                          )}
                          <p className="text-sm text-gray-500 mt-2">
                            Created: {new Date(resume.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        {isCalculatingMatch && matchingResume?.id === resume.id && (
                          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <div className="flex justify-end gap-3 mt-6 pt-4 border-t">
                <button
                  onClick={() => {
                    setShowResumeSelector(false);
                    setMatchingJob(null);
                    setMatchingResume(null);
                  }}
                  className="btn-secondary"
                  disabled={isCalculatingMatch}
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Jobs;
