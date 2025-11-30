import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  Home, 
  FileText, 
  Briefcase, 
  TrendingUp,
  LogOut,
  Sparkles,
  MessageCircle,
  Menu,
  X
} from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();
  const { user, signOut } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/resumes', icon: FileText, label: 'My Resumes' },
    { path: '/jobs', icon: Briefcase, label: 'Job Listings' },
    { path: '/scores', icon: TrendingUp, label: 'Match History' },
    { path: '/ats-optimizer', icon: Sparkles, label: 'ATS Optimizer' },
    { path: '/interview', icon: MessageCircle, label: 'Interview Practice' },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-lg"
        aria-label="Toggle menu"
      >
        {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <div className={`
        w-64 bg-white h-screen shadow-lg fixed left-0 top-0 flex flex-col z-40 transition-transform duration-300
        ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0
      `}>
        {/* Logo */}
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-primary-600">ResumeCoach AI</h1>
          <p className="text-sm text-gray-500 mt-1">Smart Job Matching</p>
        </div>

        {/* User Profile Section */}
        <div className="p-4 border-b bg-gradient-to-r from-primary-50 to-blue-50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-bold text-lg">
              {(user?.user_metadata?.name || user?.email || 'U')[0].toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-gray-900 truncate">
                {user?.user_metadata?.name || user?.email?.split('@')[0] || 'User'}
              </p>
              <p className="text-xs text-gray-500 truncate">{user?.email}</p>
            </div>
          </div>
        </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive(item.path)
                      ? 'bg-primary-50 text-primary-600 font-medium'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Bottom Actions */}
      <div className="p-4 border-t">
        <button
          onClick={async () => {
            if (window.confirm('Are you sure you want to logout?')) {
              try {
                await signOut();
                setMobileMenuOpen(false);
              } catch (error) {
                console.error('Logout failed:', error);
              }
            }
          }}
          className="flex items-center gap-3 px-4 py-3 w-full text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </div>

    {/* Mobile Overlay */}
    {mobileMenuOpen && (
      <div
        className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
        onClick={() => setMobileMenuOpen(false)}
      />
    )}
    </>
  );
};

export default Sidebar;
