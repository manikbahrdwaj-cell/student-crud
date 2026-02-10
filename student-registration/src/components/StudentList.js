import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiEdit2, FiTrash2, FiUsers, FiPlus, FiAlertCircle, FiLoader } from 'react-icons/fi';
import studentAPI from '../services/api';
import LoadingSpinner from './LoadingSpinner';

/**
 * StudentList Component
 * 
 * Displays a list of all students in a table format with options to edit and delete.
 * Features include:
 * - Fetch and display all students from API
 * - Edit and delete functionality
 * - Delete confirmation modal
 * - Empty state handling
 * - Loading states
 * - Error handling with user-friendly messages
 * - Responsive table design with Tailwind CSS
 * - Icon-based action buttons
 * - Row striping and hover effects
 * 
 * @component
 * @returns {JSX.Element} The StudentList component
 * 
 * @example
 * <StudentList />
 */
const StudentList = () => {
  // ==================== STATE MANAGEMENT ====================
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleting, setDeleting] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const navigate = useNavigate();

  // ==================== FETCH STUDENTS ====================

  /**
   * Fetch all students from the API
   */
  const fetchStudents = useCallback(async () => {
    try {
      setLoading(true);
      setError('');
      const data = await studentAPI.getStudents();
      setStudents(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error fetching students:', err);
      const errorMessage =
        err.message === 'Failed to fetch' 
          ? 'Unable to connect to the server. Please ensure the backend API is running.'
          : err.message || 'Failed to load students. Please try again.';
      setError(errorMessage);
      setStudents([]);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Load students on component mount
   */
  useEffect(() => {
    fetchStudents();
  }, [fetchStudents, refreshTrigger]);

  // ==================== EVENT HANDLERS ====================

  /**
   * Handle edit button click - navigate to edit page
   */
  const handleEdit = (studentId) => {
    navigate(`/edit/${studentId}`);
  };

  /**
   * Open delete confirmation modal
   */
  const handleDeleteClick = (student) => {
    setDeleteConfirm(student);
    setShowDeleteModal(true);
  };

  /**
   * Confirm delete and remove student
   */
  const handleConfirmDelete = async () => {
    if (!deleteConfirm) return;

    try {
      setDeleting(deleteConfirm._id);
      await studentAPI.deleteStudent(deleteConfirm._id);
      // Refresh the student list after deletion
      setRefreshTrigger((prev) => prev + 1);
      setShowDeleteModal(false);
      setDeleteConfirm(null);
    } catch (err) {
      console.error('Error deleting student:', err);
      alert('Failed to delete student. Please try again.');
    } finally {
      setDeleting(null);
    }
  };

  /**
   * Cancel delete operation
   */
  const handleCancelDelete = () => {
    setShowDeleteModal(false);
    setDeleteConfirm(null);
  };

  /**
   * Navigate to create page
   */
  const handleCreateStudent = () => {
    navigate('/create');
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
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md text-center">
          <div className="flex justify-center mb-4">
            <FiAlertCircle className="text-red-500" size={48} />
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Error</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={fetchStudents}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // ==================== RENDER EMPTY STATE ====================
  if (students.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md text-center">
          <div className="flex justify-center mb-4">
            <div className="bg-blue-50 p-3 rounded-full">
              <FiUsers className="text-blue-600" size={48} />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">No Students Yet</h2>
          <p className="text-gray-600 mb-6">
            Start by creating your first student record to get started.
          </p>
          <button
            onClick={handleCreateStudent}
            className="inline-flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
          >
            <FiPlus size={20} />
            Create First Student
          </button>
        </div>
      </div>
    );
  }

  // ==================== RENDER STUDENT TABLE ====================
  return (
    <div className="w-full bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-800 flex items-center gap-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <FiUsers className="text-white" size={28} />
              </div>
              Student List
            </h1>
            <p className="text-gray-600 mt-2">
              Total Students: <span className="font-bold text-blue-600">{students.length}</span>
            </p>
          </div>
          <button
            onClick={handleCreateStudent}
            className="mt-4 md:mt-0 inline-flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
          >
            <FiPlus size={20} />
            Add Student
          </button>
        </div>

        {/* Table Container */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              {/* Table Header */}
              <thead className="bg-gradient-to-r from-blue-600 to-blue-700">
                <tr>
                  <th className="px-6 py-4 text-left text-white font-semibold">Name</th>
                  <th className="px-6 py-4 text-left text-white font-semibold">Email</th>
                  <th className="px-6 py-4 text-left text-white font-semibold">Roll Number</th>
                  <th className="px-6 py-4 text-center text-white font-semibold">Actions</th>
                </tr>
              </thead>

              {/* Table Body */}
              <tbody>
                {students.map((student, index) => (
                  <tr
                    key={student._id || index}
                    className={`border-b transition duration-200 ${
                      index % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                    } hover:bg-blue-50`}
                  >
                    {/* Name Cell */}
                    <td className="px-6 py-4 text-gray-700 font-medium">{student.name}</td>

                    {/* Email Cell */}
                    <td className="px-6 py-4 text-gray-600">{student.email}</td>

                    {/* Roll Number Cell */}
                    <td className="px-6 py-4 text-gray-600">
                      <span className="inline-block bg-blue-100 text-blue-800 text-sm font-semibold px-3 py-1 rounded-full">
                        {student.roll}
                      </span>
                    </td>

                    {/* Actions Cell */}
                    <td className="px-6 py-4 text-center">
                      <div className="flex items-center justify-center gap-3">
                        {/* Edit Button */}
                        <button
                          onClick={() => handleEdit(student._id)}
                          className="inline-flex items-center justify-center p-2 bg-blue-100 hover:bg-blue-200 text-blue-600 rounded-lg transition duration-200 shadow-sm hover:shadow-md"
                          title="Edit student"
                          aria-label={`Edit ${student.name}`}
                        >
                          <FiEdit2 size={18} />
                        </button>

                        {/* Delete Button */}
                        <button
                          onClick={() => handleDeleteClick(student)}
                          disabled={deleting === student._id}
                          className={`inline-flex items-center justify-center p-2 rounded-lg transition duration-200 shadow-sm hover:shadow-md ${
                            deleting === student._id
                              ? 'bg-red-100 text-red-400 cursor-not-allowed'
                              : 'bg-red-100 hover:bg-red-200 text-red-600'
                          }`}
                          title="Delete student"
                          aria-label={`Delete ${student.name}`}
                        >
                          {deleting === student._id ? (
                            <FiLoader size={18} className="animate-spin" />
                          ) : (
                            <FiTrash2 size={18} />
                          )}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && deleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6 animate-slideDown">
            {/* Modal Icon */}
            <div className="flex justify-center mb-4">
              <div className="bg-red-100 p-3 rounded-full">
                <FiTrash2 className="text-red-600" size={32} />
              </div>
            </div>

            {/* Modal Content */}
            <h2 className="text-2xl font-bold text-gray-800 text-center mb-2">
              Delete Student?
            </h2>
            <p className="text-gray-600 text-center mb-2">
              Are you sure you want to delete{' '}
              <span className="font-semibold text-gray-800">{deleteConfirm.name}</span>?
            </p>
            <p className="text-gray-500 text-center text-sm mb-6">
              This action cannot be undone.
            </p>

            {/* Modal Buttons */}
            <div className="flex gap-3">
              <button
                onClick={handleCancelDelete}
                disabled={deleting === deleteConfirm._id}
                className="flex-1 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold rounded-lg transition duration-200 disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmDelete}
                disabled={deleting === deleteConfirm._id}
                className={`flex-1 px-4 py-2 font-semibold rounded-lg transition duration-200 text-white flex items-center justify-center gap-2 ${
                  deleting === deleteConfirm._id
                    ? 'bg-red-400 cursor-not-allowed'
                    : 'bg-red-600 hover:bg-red-700'
                }`}
              >
                {deleting === deleteConfirm._id ? (
                  <>
                    <FiLoader size={18} className="animate-spin" />
                    Deleting...
                  </>
                ) : (
                  <>
                    <FiTrash2 size={18} />
                    Delete
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentList;
