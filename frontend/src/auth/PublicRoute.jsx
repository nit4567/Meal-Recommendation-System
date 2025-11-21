import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from './useAuth';

export const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-900 via-teal-800 to-cyan-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  return !user ? children : <Navigate to="/dashboard" replace />;
};