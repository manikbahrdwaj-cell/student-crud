/**
 * Not Found (404) Page
 * 
 * Displayed when user navigates to a route that doesn't exist.
 * 
 * @component
 * @returns {JSX.Element} The 404 page
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FiAlertCircle, FiArrowLeft } from 'react-icons/fi';

export const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 text-center">
        <div className="flex justify-center">
          <div className="bg-red-100 rounded-full p-4">
            <FiAlertCircle className="text-red-600" size={48} />
          </div>
        </div>

        <h1 className="text-4xl font-bold text-gray-900">404</h1>
        <h2 className="text-2xl font-semibold text-gray-700">Page Not Found</h2>

        <p className="text-gray-600">
          The page you're looking for doesn't exist. Please check the URL or use the button below
          to return to the dashboard.
        </p>

        <div className="flex flex-col gap-3 pt-4">
          <button
            onClick={() => navigate('/dashboard')}
            className="w-full flex items-center justify-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition font-medium"
          >
            <FiArrowLeft size={18} />
            Back to Dashboard
          </button>

          <button
            onClick={() => window.history.back()}
            className="w-full flex items-center justify-center gap-2 bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition font-medium"
          >
            <FiArrowLeft size={18} />
            Go Back
          </button>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
