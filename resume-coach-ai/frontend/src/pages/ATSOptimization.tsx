import { useState } from 'react';
import { Sparkles, TrendingUp, AlertCircle, CheckCircle, Target, FileText } from 'lucide-react';
import { atsApi } from '../lib/api';
import type { ATSOptimizationResponse } from '../types/ats';

const ATSOptimization = () => {
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ATSOptimizationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!resumeText.trim() || !jobDescription.trim()) {
      setError('Please provide both resume text and job description');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await atsApi.optimize({
        resume_text: resumeText,
        job_description: jobDescription,
      });

      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze. Please try again.');
      console.error('ATS optimization error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 70) return 'text-green-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 70) return 'bg-green-50 border-green-200';
    if (score >= 50) return 'bg-yellow-50 border-yellow-200';
    return 'bg-red-50 border-red-200';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
          <Sparkles className="w-8 h-8 text-primary-600" />
          ATS Optimizer
        </h1>
        <p className="mt-2 text-gray-600">
          Analyze your resume against job descriptions and get optimization suggestions for better ATS compatibility
        </p>
      </div>

      {/* Input Form */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6">
        {/* Resume Input */}
        <div className="bg-white rounded-lg shadow p-4 md:p-6">
          <div className="flex items-center gap-2 mb-4">
            <FileText className="w-5 h-5 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">Your Resume</h2>
          </div>
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste your resume text here..."
            className="w-full h-64 md:h-96 px-3 md:px-4 py-2 md:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none font-mono text-sm md:text-base"
            style={{ fontSize: '16px' }}
          />
          <p className="mt-2 text-sm text-gray-500">
            {resumeText.length} characters
          </p>
        </div>

        {/* Job Description Input */}
        <div className="bg-white rounded-lg shadow p-4 md:p-6">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">Job Description</h2>
          </div>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description you're applying to..."
            className="w-full h-64 md:h-96 px-3 md:px-4 py-2 md:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none font-mono text-sm md:text-base"
            style={{ fontSize: '16px' }}
          />
          <p className="mt-2 text-sm text-gray-500">
            {jobDescription.length} characters
          </p>
        </div>
      </div>

      {/* Analyze Button */}
      <div className="flex justify-center">
        <button
          onClick={handleAnalyze}
          disabled={loading || !resumeText.trim() || !jobDescription.trim()}
          className="px-8 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 text-lg font-semibold shadow-lg hover:shadow-xl transition-all"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Analyzing...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Analyze ATS Compatibility
            </>
          )}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-900">Error</h3>
            <p className="text-red-700">{error}</p>
          </div>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Score Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* ATS Score */}
            <div className={`bg-white rounded-lg shadow p-6 border-2 ${getScoreBgColor(result.ats_score)}`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">ATS Score</p>
                  <p className={`text-4xl font-bold ${getScoreColor(result.ats_score)} mt-2`}>
                    {result.ats_score.toFixed(1)}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">out of 100</p>
                </div>
                <TrendingUp className={`w-12 h-12 ${getScoreColor(result.ats_score)}`} />
              </div>
            </div>

            {/* Keyword Match */}
            <div className="bg-white rounded-lg shadow p-6 border-2 border-blue-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Keyword Match</p>
                  <p className="text-4xl font-bold text-blue-600 mt-2">
                    {result.keyword_match_percentage.toFixed(1)}%
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {result.matched_keywords.length} / {result.job_keyword_count} keywords
                  </p>
                </div>
                <CheckCircle className="w-12 h-12 text-blue-600" />
              </div>
            </div>

            {/* TF-IDF Similarity */}
            <div className="bg-white rounded-lg shadow p-6 border-2 border-purple-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Content Similarity</p>
                  <p className="text-4xl font-bold text-purple-600 mt-2">
                    {(result.tfidf_similarity * 100).toFixed(1)}%
                  </p>
                  <p className="text-xs text-gray-500 mt-1">TF-IDF score</p>
                </div>
                <Target className="w-12 h-12 text-purple-600" />
              </div>
            </div>
          </div>

          {/* Matched Keywords */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-600" />
              Matched Keywords ({result.matched_keywords.length})
            </h3>
            <div className="flex flex-wrap gap-2">
              {result.matched_keywords.slice(0, 20).map((keyword, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
                >
                  {keyword}
                </span>
              ))}
              {result.matched_keywords.length > 20 && (
                <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm">
                  +{result.matched_keywords.length - 20} more
                </span>
              )}
            </div>
          </div>

          {/* Missing Keywords */}
          {result.missing_keywords.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-orange-600" />
                Missing Keywords ({result.missing_keywords.length})
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.missing_keywords.map((keyword, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-medium"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
              <p className="mt-4 text-sm text-gray-600">
                💡 Consider adding these keywords to your resume where relevant and truthful
              </p>
            </div>
          )}

          {/* Suggestions */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary-600" />
              Optimization Suggestions
            </h3>
            <div className="space-y-3">
              {result.suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <span className="flex-shrink-0 w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-bold">
                    {index + 1}
                  </span>
                  <p className="text-gray-700 flex-1">{suggestion}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Stats */}
          <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg shadow p-6 border border-primary-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Analysis Details</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-600">Resume Keywords</p>
                <p className="text-2xl font-bold text-gray-900">{result.resume_keyword_count}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Job Keywords</p>
                <p className="text-2xl font-bold text-gray-900">{result.job_keyword_count}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Matched</p>
                <p className="text-2xl font-bold text-green-600">{result.matched_keywords.length}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Missing</p>
                <p className="text-2xl font-bold text-orange-600">{result.missing_keywords.length}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ATSOptimization;
