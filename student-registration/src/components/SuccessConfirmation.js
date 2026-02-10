import React, { useEffect } from 'react';
import { FiCheckCircle } from 'react-icons/fi';

export const SuccessConfirmation = ({ message, onClose, duration = 3000 }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg p-8 max-w-sm w-full shadow-2xl animate-slideDown">
        <div className="flex flex-col items-center text-center">
          <div className="mb-4">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full">
              <FiCheckCircle className="text-green-600 animate-pulse" size={32} />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Success!</h2>
          <p className="text-gray-600 mb-6">{message}</p>
          <div className="w-full bg-gradient-to-r from-green-400 to-green-500 h-1 rounded-full"></div>
        </div>
      </div>
    </div>
  );
};

export default SuccessConfirmation;
