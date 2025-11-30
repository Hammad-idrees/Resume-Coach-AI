import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FileText, Briefcase, TrendingUp, Plus, ArrowRight } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { resumeApi, jobApi, scoreApi } from '../lib/api';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    resumes: 0,
    jobs: 0,
    scores: 0,
  });
  const [recentScores, setRecentScores] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Get user's display name
  const getUserName = () => {
    if (user?.user_metadata?.name) {
      return user.user_metadata.name;
    }
    if (user?.email) {
      return user.email.split('@')[0];
    }
    return 'User';
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [resumesRes, jobsRes, scoresRes] = await Promise.all([
          resumeApi.getAll(),
          jobApi.getAll(),
          scoreApi.getHistory(),
        ]);

        setStats({
          resumes: resumesRes.data.count || 0,
          jobs: jobsRes.data.count || 0,
          scores: scoresRes.data.count || 0,
        });

        setRecentScores(scoresRes.data.scores?.slice(0, 5) || []);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const statCards = [
    {
      title: 'My Resumes',
      value: stats.resumes,
      icon: FileText,
      color: 'bg-blue-500',
      link: '/resumes',
    },
    {
      title: 'Available Jobs',
      value: stats.jobs,
      icon: Briefcase,
      color: 'bg-green-500',
      link: '/jobs',
    },
    {
      title: 'Match History',
      value: stats.scores,
      icon: TrendingUp,
      color: 'bg-purple-500',
      link: '/scores',
    },
  ];

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50';
    if (score >= 70) return 'text-blue-600 bg-blue-50';
    if (score >= 60) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
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
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {getUserName()}! 👋
        </h1>
        <p className="text-gray-500 mt-1">
          Here's your resume matching overview and recent activity.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {statCards.map((stat) => {
          const Icon = stat.icon;
          return (
            <Link
              key={stat.title}
              to={stat.link}
              className="card hover:shadow-lg transition-shadow cursor-pointer"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm font-medium">{stat.title}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon size={24} className="text-white" />
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            to="/resumes"
            className="flex items-center gap-4 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all"
          >
            <div className="bg-primary-100 p-3 rounded-lg">
              <Plus size={24} className="text-primary-600" />
            </div>
            <div>
              <p className="font-semibold text-gray-900">Upload New Resume</p>
              <p className="text-sm text-gray-500">Add a resume to get matched</p>
            </div>
          </Link>

          <Link
            to="/jobs"
            className="flex items-center gap-4 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all"
          >
            <div className="bg-primary-100 p-3 rounded-lg">
              <Briefcase size={24} className="text-primary-600" />
            </div>
            <div>
              <p className="font-semibold text-gray-900">Browse Jobs</p>
              <p className="text-sm text-gray-500">Find your perfect match</p>
            </div>
          </Link>
        </div>
      </div>

      {/* Recent Match Scores */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Recent Match Scores</h2>
          <Link to="/scores" className="text-primary-600 hover:text-primary-700 flex items-center gap-1 text-sm font-medium">
            View All
            <ArrowRight size={16} />
          </Link>
        </div>

        {recentScores.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <TrendingUp size={48} className="mx-auto mb-3 text-gray-400" />
            <p>No match scores yet</p>
            <p className="text-sm mt-1">Upload a resume and match it with jobs to see scores here</p>
          </div>
        ) : (
          <div className="space-y-3">
            {recentScores.map((score) => (
              <div
                key={score.id}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-900">
                    {score.resumes?.title || 'Resume'} × {score.jobs?.title || 'Job'}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                    {score.jobs?.company || 'Company'} • {new Date(score.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <div className={`px-4 py-2 rounded-lg font-bold ${getScoreColor(score.match_score)}`}>
                    {score.match_score.toFixed(1)}%
                  </div>
                  <span className="text-sm text-gray-500">{score.recommendation}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
