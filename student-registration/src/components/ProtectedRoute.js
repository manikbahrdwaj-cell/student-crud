/**
 * Protected Route Component
 * 
 * Wraps routes that require authentication or authorization.
 * In the current version, all routes are public, but this structure
 * is ready for future authentication implementation.
 * 
 * @component
 * @param {Object} props - Component props
 * @param {JSX.Element} props.children - The component to render
 * @param {boolean} [props.isAuthenticated=true] - Whether user is authenticated
 * @param {string} [props.redirectTo='/login'] - Route to redirect if not authenticated
 * @returns {JSX.Element} The protected route
 */
import React from 'react';
import { Navigate } from 'react-router-dom';

export const ProtectedRoute = ({
  children,
  isAuthenticated = true,
  redirectTo = '/login',
}) => {
  if (!isAuthenticated) {
    return <Navigate to={redirectTo} replace />;
  }

  return children;
};

export default ProtectedRoute;
