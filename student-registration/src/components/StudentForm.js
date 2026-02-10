import React, { useState, useCallback } from 'react';
import studentAPI from '../services/api';

// ==================== VALIDATION RULES (CONSTANT) ====================

/**
 * Validation rules for form fields
 * Defines constraints and patterns for name, email, and roll number fields
 */
const VALIDATION_RULES = {
  name: {
    minLength: 2,
    maxLength: 50,
    pattern: /^[a-zA-Z\s'-]+$/,
    messages: {
      required: 'Name is required',
      tooShort: 'Name must be at least 2 characters',
      tooLong: 'Name cannot exceed 50 characters',
      invalidPattern: 'Name can only contain letters, spaces, hyphens, and apostrophes',
    },
  },
  email: {
    maxLength: 100,
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    messages: {
      required: 'Email is required',
      tooLong: 'Email cannot exceed 100 characters',
      invalidPattern: 'Please enter a valid email address',
    },
  },
  roll: {
    minLength: 1,
    maxLength: 20,
    pattern: /^[a-zA-Z0-9-]+$/,
    messages: {
      required: 'Roll number is required',
      tooShort: 'Roll number must be at least 1 character',
      tooLong: 'Roll number cannot exceed 20 characters',
      invalidPattern: 'Roll number can only contain letters, numbers, and hyphens',
    },
  },
};

/**
 * StudentForm Component
 * 
 * A reusable form component for creating and editing student records.
 * Supports both create and edit modes with comprehensive validation.
 * 
 * Features:
 * - Real-time form validation
 * - Error handling and display
 * - Loading states and spinners
 * - Success feedback
 * - Accessible form structure
 * - Tailwind CSS styling
 * 
 * @component
 * @param {Object} props - Component props
 * @param {Function} [props.onSubmitSuccess] - Callback after successful submission
 * @param {Object} [props.initialData] - Initial form data for edit mode
 * @param {boolean} [props.isEdit] - Flag to determine create vs edit mode
 * 
 * @example
 * // Create mode
 * <StudentForm onSubmitSuccess={() => navigate('/dashboard')} />
 * 
 * @example
 * // Edit mode
 * <StudentForm
 *   initialData={studentData}
 *   isEdit={true}
 *   onSubmitSuccess={() => navigate('/dashboard')}
 * />
 */
const StudentForm = ({ onSubmitSuccess, initialData = null, isEdit = false }) => {

  // ==================== STATE MANAGEMENT ====================
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    email: initialData?.email || '',
    roll: initialData?.roll || '',
  });

  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [loading, setLoading] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // ==================== VALIDATION FUNCTIONS ====================

  /**
   * Validate a single field
   * @param {string} fieldName - The field to validate
   * @param {string} value - The value to validate
   * @returns {string|null} Error message or null if valid
   */
  const validateField = useCallback((fieldName, value) => {
    const rules = VALIDATION_RULES[fieldName];
    if (!rules) return null;

    // Check if field is empty
    if (!value || value.trim() === '') {
      return rules.messages.required;
    }

    // Check minimum length
    if (rules.minLength && value.length < rules.minLength) {
      return rules.messages.tooShort;
    }

    // Check maximum length
    if (rules.maxLength && value.length > rules.maxLength) {
      return rules.messages.tooLong;
    }

    // Check pattern
    if (rules.pattern && !rules.pattern.test(value)) {
      return rules.messages.invalidPattern;
    }

    return null;
  }, []);

  /**
   * Validate entire form
   * @returns {Object} Object with field errors
   */
  const validateForm = useCallback(() => {
    const newErrors = {};
    Object.keys(formData).forEach((field) => {
      const error = validateField(field, formData[field]);
      if (error) {
        newErrors[field] = error;
      }
    });
    return newErrors;
  }, [formData, validateField]);

  // ==================== EVENT HANDLERS ====================

  /**
   * Handle input changes
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }

    // Clear general submit error
    if (submitError) {
      setSubmitError('');
    }
  };

  /**
   * Handle field blur - validate and mark as touched
   */
  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched((prev) => ({
      ...prev,
      [name]: true,
    }));

    // Validate field on blur
    const error = validateField(name, formData[name]);
    setErrors((prev) => ({
      ...prev,
      [name]: error || '',
    }));
  };

  /**
   * Handle form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form
    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    setSubmitError('');
    setSuccessMessage('');

    try {
      if (isEdit && initialData?._id) {
        // Update existing student
        await studentAPI.updateStudent(initialData._id, formData);
        setSuccessMessage('Student updated successfully!');
      } else {
        // Create new student
        await studentAPI.createStudent(formData);
        setSuccessMessage('Student created successfully!');
      }

      // Call success callback after brief delay
      setTimeout(() => {
        if (onSubmitSuccess) {
          onSubmitSuccess();
        }
      }, 500);
    } catch (err) {
      console.error('Form submission error:', err);
      const errorMessage =
        err.message ||
        err.detail ||
        'An error occurred while submitting the form';
      setSubmitError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle clear/reset button
   */
  const handleClear = () => {
    if (isEdit && initialData) {
      // In edit mode, reset to original data
      setFormData({
        name: initialData.name || '',
        email: initialData.email || '',
        roll: initialData.roll || '',
      });
    } else {
      // In create mode, clear all fields
      setFormData({
        name: '',
        email: '',
        roll: '',
      });
    }
    setErrors({});
    setTouched({});
    setSubmitError('');
    setSuccessMessage('');
  };

  // ==================== HELPER COMPONENTS ====================

  /**
   * Loading Spinner Component
   */
  const LoadingSpinner = () => (
    <svg
      className="animate-spin h-5 w-5 text-white"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      ></circle>
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
  );

  /**
   * Form Field Component
   */
  const FormField = ({ label, name, type = 'text', placeholder, maxLength, pattern }) => {
    const fieldError = errors[name];
    const fieldTouched = touched[name];
    const isInvalid = fieldError && fieldTouched;

    return (
      <div className="mb-5">
        <label
          htmlFor={name}
          className="block text-sm font-semibold text-gray-700 mb-2"
        >
          {label} <span className="text-red-600 font-bold">*</span>
        </label>
        <input
          id={name}
          type={type}
          name={name}
          value={formData[name]}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder={placeholder}
          maxLength={maxLength}
          disabled={loading}
          aria-label={label}
          aria-invalid={isInvalid}
          aria-describedby={isInvalid ? `error-${name}` : `hint-${name}`}
          className={`
            w-full px-4 py-2 border rounded-lg text-gray-800
            transition-all duration-200 ease-out
            focus:outline-none focus:ring-2 focus:ring-offset-2
            disabled:opacity-50 disabled:cursor-not-allowed
            ${isInvalid
              ? 'border-red-500 bg-red-50 focus:border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
            }
          `}
        />
        <div className="flex justify-between items-center mt-1 text-xs">
          <span
            id={`hint-${name}`}
            className={`text-gray-500 ${isInvalid ? 'opacity-0' : 'opacity-100'}`}
          >
            {name === 'name' && 'Letters, spaces, hyphens, and apostrophes only'}
            {name === 'email' && 'Valid email address (e.g., user@example.com)'}
            {name === 'roll' && 'Letters, numbers, and hyphens only'}
          </span>
          <span className="text-gray-400">
            {formData[name].length}/{maxLength}
          </span>
        </div>
        {isInvalid && (
          <div
            id={`error-${name}`}
            className="mt-2 p-2 bg-red-100 border border-red-400 text-red-700 text-xs rounded animate-slideDown"
            role="alert"
          >
            <span className="font-semibold">⚠ {fieldError}</span>
          </div>
        )}
      </div>
    );
  };

  // ==================== RENDER ====================

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8 px-4">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
        {/* Header */}
        <h1 className="text-2xl font-bold text-gray-800 mb-6 text-center">
          {isEdit ? 'Edit Student' : 'Add New Student'}
        </h1>

        {/* Info Text */}
        <p className="text-xs text-gray-600 text-center mb-6">
          Fields marked with <span className="text-red-600 font-bold">*</span> are required
        </p>

        {/* Submit Error Alert */}
        {submitError && (
          <div
            className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg animate-slideDown"
            role="alert"
          >
            <p className="font-semibold text-sm">Error:</p>
            <p className="text-sm">{submitError}</p>
          </div>
        )}

        {/* Success Message */}
        {successMessage && (
          <div
            className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg animate-slideDown"
            role="status"
          >
            <p className="font-semibold text-sm">✓ {successMessage}</p>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Name Field */}
          <FormField
            label="Full Name"
            name="name"
            type="text"
            placeholder="e.g., John Doe"
            maxLength={50}
          />

          {/* Email Field */}
          <FormField
            label="Email Address"
            name="email"
            type="email"
            placeholder="e.g., john@example.com"
            maxLength={100}
          />

          {/* Roll Number Field */}
          <FormField
            label="Roll Number"
            name="roll"
            type="text"
            placeholder="e.g., CS001"
            maxLength={20}
          />

          {/* Form Actions */}
          <div className="flex gap-3 pt-4">
            <button
              type="submit"
              disabled={loading}
              className={`
                flex-1 py-3 px-4 rounded-lg font-semibold text-white
                transition-all duration-200 ease-out
                flex items-center justify-center gap-2
                ${loading
                  ? 'bg-blue-400 cursor-not-allowed opacity-75'
                  : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
                }
              `}
              aria-busy={loading}
            >
              {loading && <LoadingSpinner />}
              {loading
                ? 'Submitting...'
                : isEdit
                ? 'Update Student'
                : 'Create Student'}
            </button>

            <button
              type="button"
              onClick={handleClear}
              disabled={loading}
              className={`
                flex-1 py-3 px-4 rounded-lg font-semibold
                transition-all duration-200 ease-out
                ${loading
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300 active:scale-95'
                }
              `}
            >
              Clear
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default StudentForm;
