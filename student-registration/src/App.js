import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { MainLayout } from './components/MainLayout';
import { Dashboard } from './pages/Dashboard';
import CreatePage from './pages/CreatePage';
import EditPage from './pages/EditPage';
import NotFound from './pages/NotFound';
import { ROUTES } from './routes';

/**
 * App Component
 * 
 * Main application component with routing configuration.
 * Phase 4: Enhanced Routing & Student Feature Enhancement
 * 
 * Features:
 * - Centralized route management using ROUTES config
 * - MainLayout component for consistent structure
 * - Protected route support for future authentication
 * - 404 error page for invalid routes
 * - Proper route organization and metadata
 * 
 * @component
 * @returns {JSX.Element} The main App component
 */
function App() {
  return (
    <Router>
      <AppRoutes />
    </Router>
  );
}

/**
 * AppRoutes Component
 * 
 * Separates routing logic for better organization.
 * Uses MainLayout wrapper for all routes except special pages.
 * 
 * @component
 * @returns {JSX.Element} The app routes
 */
function AppRoutes() {
  const location = useLocation();

  // Routes that don't use MainLayout
  const specialRoutes = [ROUTES.NOT_FOUND];
  const useLayout = !specialRoutes.includes(location.pathname);

  return (
    <Routes>
      {/* Redirect home to dashboard */}
      <Route path={ROUTES.HOME} element={<Navigate to={ROUTES.DASHBOARD} replace />} />

      {/* Main application routes with layout */}
      <Route
        path={ROUTES.DASHBOARD}
        element={
          <MainLayout>
            <Dashboard />
          </MainLayout>
        }
      />
      <Route
        path={ROUTES.CREATE}
        element={
          <MainLayout>
            <CreatePage />
          </MainLayout>
        }
      />
      <Route
        path={ROUTES.EDIT}
        element={
          <MainLayout>
            <EditPage />
          </MainLayout>
        }
      />

      {/* Catch-all 404 route */}
      <Route path={ROUTES.NOT_FOUND} element={<NotFound />} />
    </Routes>
  );
}

export default App;
