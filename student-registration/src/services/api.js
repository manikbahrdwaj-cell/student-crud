/**
 * Phase 3.1: API Service Layer
 * =============================
 * 
 * This module provides a centralized API service for all student CRUD operations.
 * It uses Axios as the HTTP client and is configured with environment variables.
 * 
 * Features:
 * - Centralized API endpoint management
 * - Error handling and logging
 * - Request/response interceptors (extensible)
 * - Type hints via JSDoc comments
 * - Consistent error format
 */

import axios from 'axios';

// ==================== CONFIGURATION ====================

/**
 * Get API base URL from environment variables
 * Defaults to localhost development server if not set
 */
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

/**
 * Create Axios instance with default configuration
 * This instance is used for all API requests
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout for requests
});

// ==================== INTERCEPTORS ====================

/**
 * Request Interceptor
 * Logs outgoing requests in development mode
 */
apiClient.interceptors.request.use(
  (config) => {
    if (process.env.REACT_APP_ENV === 'development') {
      console.log(`[API] ${config.method.toUpperCase()} ${config.url}`, config.data);
    }
    return config;
  },
  (error) => {
    console.error('[API] Request Error:', error);
    return Promise.reject(error);
  }
);

/**
 * Response Interceptor
 * Logs response data and handles global errors
 */
apiClient.interceptors.response.use(
  (response) => {
    if (process.env.REACT_APP_ENV === 'development') {
      console.log(`[API] Response ${response.status}:`, response.data);
    }
    return response;
  },
  (error) => {
    // Log error details
    const errorMessage = error.response?.data?.detail || error.message || 'Unknown error occurred';
    console.error('[API] Response Error:', {
      status: error.response?.status,
      message: errorMessage,
      error: error,
    });
    return Promise.reject(error);
  }
);

// ==================== STUDENT CRUD API METHODS ====================

/**
 * Create a new student
 * 
 * @param {Object} studentData - Student data object
 * @param {string} studentData.name - Student name (2-50 characters)
 * @param {string} studentData.email - Student email (valid email format)
 * @param {string} studentData.roll - Student roll number (1-20 characters)
 * 
 * @returns {Promise<Object>} Created student object with ID
 * @throws {AxiosError} If request fails
 * 
 * @example
 * const newStudent = await createStudent({
 *   name: 'John Doe',
 *   email: 'john@example.com',
 *   roll: 'CS001'
 * });
 */
export const createStudent = async (studentData) => {
  try {
    const response = await apiClient.post('/students', studentData);
    return response.data;
  } catch (error) {
    throw formatErrorResponse(error);
  }
};

/**
 * Fetch all students
 * 
 * @returns {Promise<Array>} Array of all student objects
 * @throws {AxiosError} If request fails
 * 
 * @example
 * const students = await getStudents();
 * console.log(students);
 */
export const getStudents = async () => {
  try {
    const response = await apiClient.get('/students');
    return response.data;
  } catch (error) {
    throw formatErrorResponse(error);
  }
};

/**
 * Fetch a single student by ID
 * 
 * @param {string} studentId - MongoDB ObjectId of the student
 * 
 * @returns {Promise<Object>} Student object
 * @throws {AxiosError} If request fails or student not found
 * 
 * @example
 * const student = await getStudent('507f1f77bcf86cd799439011');
 */
export const getStudent = async (studentId) => {
  try {
    if (!studentId) {
      throw new Error('Student ID is required');
    }
    const response = await apiClient.get(`/students/${studentId}`);
    return response.data;
  } catch (error) {
    throw formatErrorResponse(error);
  }
};

/**
 * Update an existing student
 * 
 * @param {string} studentId - MongoDB ObjectId of the student
 * @param {Object} studentData - Student data to update (partial updates allowed)
 * @param {string} [studentData.name] - Updated student name
 * @param {string} [studentData.email] - Updated student email
 * @param {string} [studentData.roll] - Updated student roll number
 * 
 * @returns {Promise<Object>} Updated student object
 * @throws {AxiosError} If request fails or student not found
 * 
 * @example
 * const updated = await updateStudent('507f1f77bcf86cd799439011', {
 *   name: 'Jane Doe',
 *   email: 'jane@example.com'
 * });
 */
export const updateStudent = async (studentId, studentData) => {
  try {
    if (!studentId) {
      throw new Error('Student ID is required');
    }
    const response = await apiClient.put(`/students/${studentId}`, studentData);
    return response.data;
  } catch (error) {
    throw formatErrorResponse(error);
  }
};

/**
 * Delete a student
 * 
 * @param {string} studentId - MongoDB ObjectId of the student
 * 
 * @returns {Promise<void>} Successfully deleted (HTTP 204)
 * @throws {AxiosError} If request fails or student not found
 * 
 * @example
 * await deleteStudent('507f1f77bcf86cd799439011');
 */
export const deleteStudent = async (studentId) => {
  try {
    if (!studentId) {
      throw new Error('Student ID is required');
    }
    const response = await apiClient.delete(`/students/${studentId}`);
    return response.status === 204;
  } catch (error) {
    throw formatErrorResponse(error);
  }
};

// ==================== ERROR HANDLING ====================

/**
 * Format API error responses for consistent error handling
 * 
 * @param {AxiosError} error - The error object from axios
 * 
 * @returns {Object} Formatted error object
 * @property {number} status - HTTP status code
 * @property {string} message - Error message for display
 * @property {string} detail - Detailed error information
 * @property {Object} originalError - Original error object
 */
function formatErrorResponse(error) {
  if (error.response) {
    // Server responded with error status code
    return {
      status: error.response.status,
      message: 
        error.response.data?.detail || 
        error.response.data?.message ||
        `Error: ${getErrorMessage(error.response.status)}`,
      detail: error.response.data?.detail || error.response.data,
      originalError: error,
    };
  } else if (error.request) {
    // Request was made but no response received
    return {
      status: 0,
      message: 'No response from server. Please check your connection.',
      detail: error.message,
      originalError: error,
    };
  } else {
    // Error in request setup
    return {
      status: 0,
      message: error.message || 'An error occurred',
      detail: error.message,
      originalError: error,
    };
  }
}

/**
 * Get human-readable error message for HTTP status code
 * 
 * @param {number} status - HTTP status code
 * @returns {string} Error message
 */
function getErrorMessage(status) {
  const statusMessages = {
    400: 'Bad Request - Please check your input',
    404: 'Not Found - Resource does not exist',
    409: 'Conflict - Resource already exists',
    422: 'Validation Error - Please check your input',
    500: 'Server Error - Please try again later',
    503: 'Service Unavailable - Please try again later',
  };
  return statusMessages[status] || 'An error occurred';
}

// ==================== UTILITY FUNCTIONS ====================

/**
 * Check API connectivity
 * Performs a simple health check to verify API is reachable
 * 
 * @returns {Promise<boolean>} True if API is reachable
 */
export const checkApiHealth = async () => {
  try {
    // Attempt to fetch students as health check
    await apiClient.get('/students');
    return true;
  } catch (error) {
    console.warn('[API] Health check failed:', error.message);
    return false;
  }
};

/**
 * Get configured API base URL
 * Useful for debugging or external usage
 * 
 * @returns {string} API base URL
 */
export const getApiBaseUrl = () => API_BASE_URL;

/**
 * Set custom headers for all requests
 * Useful for adding authentication tokens, etc.
 * 
 * @param {string} key - Header key
 * @param {string} value - Header value
 */
export const setApiHeader = (key, value) => {
  apiClient.defaults.headers.common[key] = value;
};

/**
 * Remove custom header from all requests
 * 
 * @param {string} key - Header key to remove
 */
export const removeApiHeader = (key) => {
  delete apiClient.defaults.headers.common[key];
};

// ==================== CONSOLIDATED API OBJECT ====================

/**
 * Consolidated API service object
 * Provides all API methods in a single namespace
 */
const studentAPI = {
  // CRUD Operations
  createStudent,
  getStudents,
  getStudent,
  updateStudent,
  deleteStudent,
  
  // Utilities
  checkApiHealth,
  getApiBaseUrl,
  setApiHeader,
  removeApiHeader,
};

// ==================== EXPORTS ====================

// Named export for destructured imports
export { studentAPI };

// Default export for default imports
export default studentAPI;
