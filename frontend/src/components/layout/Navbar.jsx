// ============================================================================
// FILE: src/components/layout/Navbar.jsx
// PURPOSE: Top navigation bar
// ============================================================================

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../auth/useAuth';
import { ROUTES } from '../../constants/routes';
import { Activity, Edit, LogOut } from 'lucide-react';

export const Navbar = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate(ROUTES.LOGIN);
  };

  return (
    <nav className="relative backdrop-blur-md bg-white/5 border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-400 to-pink-400 rounded-xl flex items-center justify-center">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-purple-600">ICMR Nutrition</h1>
              <p className="text-xs text-purple-400">Welcome, {user?.first_name}!</p>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => navigate(ROUTES.PROFILE_EDIT)}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl transition-all flex items-center gap-2 border border-gray-300"
            >
              <Edit className="w-4 h-4" />
              <span className="hidden sm:inline">Edit Profile</span>
            </button>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-xl transition-all flex items-center gap-2 border border-red-300"
            >
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};
