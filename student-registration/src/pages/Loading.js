/**
 * Loading Page Component
 * 
 * Displays a loading screen with spinner.
 * Used during route transitions or data fetching.
 * 
 * @component
 * @param {Object} props - Component props
 * @param {string} [props.message='Loading...'] - Loading message text
 * @returns {JSX.Element} The loading page
 */
import React from 'react';
import { LoadingSpinner } from '../components/LoadingSpinner';

export const Loading = ({ message = 'Loading...' }) => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <div className="text-center">
        <LoadingSpinner />
        <p className="mt-4 text-gray-600 text-lg">{message}</p>
      </div>
    </div>
  );
};

export default Loading;
