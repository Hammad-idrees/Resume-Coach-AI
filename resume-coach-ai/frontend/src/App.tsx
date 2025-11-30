import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Resumes from './pages/Resumes';
import Jobs from './pages/Jobs';
import Scores from './pages/Scores';
import ATSOptimization from './pages/ATSOptimization';
import InterviewSimulation from './pages/InterviewSimulation';

function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        
        {/* Protected routes */}
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <Layout>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/resumes" element={<Resumes />} />
                  <Route path="/jobs" element={<Jobs />} />
                  <Route path="/scores" element={<Scores />} />
                  <Route path="/ats-optimizer" element={<ATSOptimization />} />
                  <Route path="/interview" element={<InterviewSimulation />} />
                </Routes>
              </Layout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </AuthProvider>
  );
}

export default App;
