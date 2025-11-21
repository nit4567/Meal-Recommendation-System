import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from './useAuth';
import { Navbar } from '../components/layout/Navbar';  
import { Footer } from '../components/layout/Footer';  

export const PrivateRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  return user ? (
    <>
      <Navbar />
      {children}
      <Footer />
    </>
  ) : <Navigate to="/login" replace />;
};