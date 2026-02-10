/**
 * Main Layout Component
 * 
 * Main layout wrapper for the application.
 * Provides consistent structure with Navigation and main content area.
 * 
 * @component
 * @param {Object} props - Component props
 * @param {JSX.Element} props.children - Child components to render
 * @returns {JSX.Element} The main layout
 */
import React from 'react';
import { Navigation } from './Navigation';
import { ToastContainer } from './ToastContainer';

export const MainLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main className="flex-1">
        {children}
      </main>
      <ToastContainer />
    </div>
  );
};

export default MainLayout;
