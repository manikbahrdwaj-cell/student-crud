import React, { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiArrowLeft } from 'react-icons/fi';
import StudentForm from '../components/StudentForm';

/**
 * CreatePage Component
 * 
 * Page for creating a new student record.
 * Displays an empty StudentForm in create mode.
 * 
 * @component
 * @returns {JSX.Element} The CreatePage
 */
const CreatePage = () => {
  const navigate = useNavigate();

  /**
   * Handle successful form submission
   */
  const handleSubmitSuccess = useCallback(() => {
    // Navigate to dashboard after successful creation
    navigate('/dashboard');
  }, [navigate]);

  /**
   * Handle back button click
   */
  const handleBack = () => {
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Back Button */}
        <button
          onClick={handleBack}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-700 font-semibold mb-6 transition duration-200"
          aria-label="Go back to dashboard"
        >
          <FiArrowLeft size={20} />
          Back to Dashboard
        </button>

        {/* Page Title */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Create New Student</h1>
          <p className="text-gray-600">
            Fill in the form below to add a new student to the system.
          </p>
        </div>

        {/* Form Container */}
        <div className="bg-white rounded-lg shadow-lg p-6 md:p-8">
          <StudentForm onSubmitSuccess={handleSubmitSuccess} />
        </div>
      </div>
    </div>
  );
};

export default CreatePage;
