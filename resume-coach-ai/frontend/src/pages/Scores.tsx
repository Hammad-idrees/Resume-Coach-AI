import { useState, useEffect } from 'react';
import { TrendingUp, Calendar, Award } from 'lucide-react';
import { scoreApi } from '../lib/api';

const Scores = () => {
  const [scores, setScores] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchScores();
  }, []);

  const fetchScores = async () => {
    try {
      const response = await scoreApi.getHistory();
      setScores(response.data.scores || []);
    } catch (error) {
      console.error('Error fetching scores:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 70) return 'text-blue-600 bg-blue-50 border-blue-200';
    if (score >= 60) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getRecommendationIcon = (recommendation: string) => {
    if (recommendation.includes('Excellent')) return '🎉';
    if (recommendation.includes('Strong')) return '💪';
    if (recommendation.includes('Good')) return '👍';
    if (recommendation.includes('Moderate')) return '👌';
    return '📊';
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
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Match History</h1>
        <p className="text-gray-500 mt-1">
          {scores.length > 0 
            ? `You have ${scores.length} matching result${scores.length > 1 ? 's' : ''} in your history` 
            : 'No match history yet. Start analyzing resumes!'}
        </p>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="bg-blue-100 p-3 rounded-lg">
              <TrendingUp size={24} className="text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">Total Matches</p>
              <p className="text-2xl font-bold text-gray-900">{scores.length}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center gap-3">
            <div className="bg-green-100 p-3 rounded-lg">
              <Award size={24} className="text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">Average Score</p>
              <p className="text-2xl font-bold text-gray-900">
                {scores.length > 0
                  ? (scores.reduce((acc, s) => acc + s.match_score, 0) / scores.length).toFixed(1)
                  : '0'}%
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center gap-3">
            <div className="bg-purple-100 p-3 rounded-lg">
              <Calendar size={24} className="text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">This Month</p>
              <p className="text-2xl font-bold text-gray-900">
                {scores.filter((s) => new Date(s.created_at).getMonth() === new Date().getMonth()).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Scores List */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">All Matches</h2>

        {scores.length === 0 ? (
          <div className="text-center py-12">
            <TrendingUp size={48} className="mx-auto mb-3 text-gray-400" />
            <p className="text-gray-500 font-medium">No match scores yet</p>
            <p className="text-sm text-gray-400 mt-1">
              Upload a resume and match it with jobs to see scores here
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {scores.map((score) => (
              <div
                key={score.id}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold text-gray-900">
                        {score.resumes?.title || 'Resume'}
                      </h3>
                      <span className="text-gray-400">×</span>
                      <h3 className="font-semibold text-gray-900">
                        {score.jobs?.title || 'Job'}
                      </h3>
                    </div>

                    <p className="text-sm text-gray-600 mb-3">
                      {score.jobs?.company || 'Company'} •{' '}
                      <span className="text-gray-400">
                        {new Date(score.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                        })}
                      </span>
                    </p>

                    {score.keywords_matched && score.keywords_matched.length > 0 && (
                      <div className="flex flex-wrap gap-2 mb-3">
                        <span className="text-xs text-gray-500 font-medium">Keywords:</span>
                        {score.keywords_matched.slice(0, 8).map((keyword: string, index: number) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-primary-50 text-primary-700 text-xs rounded-full"
                          >
                            {keyword}
                          </span>
                        ))}
                        {score.keywords_matched.length > 8 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                            +{score.keywords_matched.length - 8} more
                          </span>
                        )}
                      </div>
                    )}
                  </div>

                  <div className="flex flex-col items-end gap-2 ml-4">
                    <div
                      className={`px-6 py-3 rounded-lg border-2 ${getScoreColor(score.match_score)}`}
                    >
                      <p className="text-2xl font-bold">{score.match_score.toFixed(1)}%</p>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <span>{getRecommendationIcon(score.recommendation)}</span>
                      <span className="font-medium text-gray-700">{score.recommendation}</span>
                    </div>
                    <div className="text-xs text-gray-500">
                      Confidence: {(score.confidence * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Scores;
