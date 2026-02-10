import React, { useState } from 'react';

/**
 * Toast Context for managing toast notifications
 */
export const ToastContext = React.createContext();

/**
 * ToastContainer Component
 * 
 * Displays toast notifications for user feedback.
 * Contains a list of active toasts and handles their lifecycle.
 * 
 * @component
 * @returns {JSX.Element} The ToastContainer component
 */
export const ToastContainer = () => {
  const [toasts, setToasts] = useState([]);

  /**
   * Add a new toast notification
   */
  const addToast = (message, type = 'info', duration = 3000) => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, message, type }]);

    // Auto-remove toast after duration
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }

    return id;
  };

  /**
   * Remove a toast by ID
   */
  const removeToast = (id) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };

  /**
   * Get CSS classes based on toast type
   */
  const getToastClasses = (type) => {
    const baseClasses = 'px-4 py-3 rounded-lg shadow-lg font-semibold text-white mb-2 animate-slideDown';
    const typeClasses = {
      success: 'bg-green-500',
      error: 'bg-red-500',
      warning: 'bg-yellow-500',
      info: 'bg-blue-500',
    };
    return `${baseClasses} ${typeClasses[type] || typeClasses.info}`;
  };

  return (
    <ToastContext.Provider value={{ addToast, removeToast }}>
      <div className="fixed top-4 right-4 z-50 max-w-md">
        {toasts.map((toast) => (
          <div key={toast.id} className={getToastClasses(toast.type)}>
            {toast.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export default ToastContainer;
