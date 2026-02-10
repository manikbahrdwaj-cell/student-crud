import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { FiArrowLeft, FiAlertCircle } from 'react-icons/fi';
import EditForm from '../components/EditForm';
import studentAPI from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

/**
 * EditPage Component
 * 
 * Page for editing an existing student record.
 * Fetches student data by ID and displays StudentForm in edit mode.
 * 
 * @component
 * @returns {JSX.Element} The EditPage
 */
const EditPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  /**
   * Fetch student data on component mount
   */
  useEffect(() => {
    const fetchStudent = async () => {
      try {
        setLoading(true);
        setError('');
        if (!id) {
          setError('Student ID is missing');
          setLoading(false);
          return;
        }
        const data = await studentAPI.getStudent(id);
        setStudent(data);
      } catch (err) {
        console.error('Error fetching student:', err);
        const errorMessage =
          err.message === 'Failed to fetch'
            ? 'Unable to connect to the server. Please ensure the backend API is running.'
            : err.message || 'Failed to load student. Please try again.';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchStudent();
  }, [id]);

  /**
   * Handle successful form submission
   */
  const handleSubmitSuccess = useCallback(() => {
    // Navigate to dashboard after successful update
    navigate('/dashboard');
  }, [navigate]);

  /**
   * Handle back button click
   */
  const handleBack = () => {
    navigate('/dashboard');
  };

  // ==================== RENDER LOADING STATE ====================
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <LoadingSpinner />
      </div>
    );
  }

  // ==================== RENDER ERROR STATE ====================
  if (error) {
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

          {/* Error Message */}
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="flex justify-center mb-4">
              <FiAlertCircle className="text-red-500" size={48} />
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Error</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <button
              onClick={handleBack}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
            >
              Go Back
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ==================== RENDER EDIT FORM ====================
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
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Edit Student</h1>
          <p className="text-gray-600">
            Update the student information below and click Save to apply changes.
          </p>
        </div>

        {/* Form Container */}
        <div className="bg-white rounded-lg shadow-lg p-6 md:p-8">
          {student && (
            <EditForm
              initialData={student}
              onSubmitSuccess={handleSubmitSuccess}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default EditPage;
