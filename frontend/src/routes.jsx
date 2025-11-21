import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { PrivateRoute } from './auth/PrivateRoute';
import { PublicRoute } from './auth/PublicRoute';
import { ROUTES } from './constants/routes';
import { LoginPage } from './pages/auth/LoginPage';
import { SignupPage } from './pages/auth/SignupPage';
import { ProfileWizard } from './pages/profile/ProfileWizard';
import { Dashboard } from './pages/dashboard/Dashboard';

export const AppRoutes = () => {
  return (
    <Routes>
      {/* Public Routes - Redirect to dashboard if authenticated */}
      <Route
        path={ROUTES.LOGIN}
        element={
          <PublicRoute>
            <LoginPage />
          </PublicRoute>
        }
      />
      <Route
        path={ROUTES.SIGNUP}
        element={
          <PublicRoute>
            <SignupPage />
          </PublicRoute>
        }
      />

      {/* Private Routes - Require authentication */}
      <Route
        path={ROUTES.PROFILE_CREATE}
        element={
          <PrivateRoute>
            <ProfileWizard />
          </PrivateRoute>
        }
      />
      <Route
        path={ROUTES.PROFILE_EDIT}
        element={
          <PrivateRoute>
            <ProfileWizard />
          </PrivateRoute>
        }
      />
      <Route
        path={ROUTES.DASHBOARD}
        element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        }
      />

      {/* Default redirect */}
      <Route path={ROUTES.HOME} element={<Navigate to={ROUTES.DASHBOARD} replace />} />
      
      {/* 404 - Redirect to dashboard */}
      <Route path="*" element={<Navigate to={ROUTES.DASHBOARD} replace />} />
    </Routes>
  );
};
