import { Bell, Search } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Header = () => {
  const { user } = useAuth();

  const getUserName = () => {
    if (user?.user_metadata?.name) {
      return user.user_metadata.name;
    }
    if (user?.email) {
      return user.email.split('@')[0];
    }
    return 'User';
  };

  const getUserInitial = () => {
    return getUserName()[0].toUpperCase();
  };

  return (
    <header className="bg-white shadow-sm h-16 fixed top-0 right-0 left-64 z-10 flex items-center justify-between px-6">
      {/* Search Bar */}
      <div className="flex-1 max-w-2xl">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search resumes, jobs..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
          />
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <button className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors">
          <Bell size={20} className="text-gray-600" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        {/* User Profile */}
        <div className="flex items-center gap-3 p-2 hover:bg-gray-100 rounded-lg cursor-pointer transition-colors">
          <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white font-bold">
            {getUserInitial()}
          </div>
          <div className="text-sm">
            <p className="font-medium text-gray-900">{getUserName()}</p>
            <p className="text-gray-500 text-xs">{user?.email || 'user@example.com'}</p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
