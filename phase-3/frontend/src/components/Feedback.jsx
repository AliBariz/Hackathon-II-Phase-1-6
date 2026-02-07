import React, { useEffect } from 'react';

const Feedback = ({ message, type = 'info', duration = 5000, onClose }) => {
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onClose && onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const getStyle = () => {
    switch (type) {
      case 'success':
        return 'bg-green-100 border-green-400 text-green-700';
      case 'error':
        return 'bg-red-100 border-red-400 text-red-700';
      case 'warning':
        return 'bg-yellow-100 border-yellow-400 text-yellow-700';
      case 'info':
      default:
        return 'bg-blue-100 border-blue-400 text-blue-700';
    }
  };

  return (
    <div className={`fixed top-4 right-4 p-4 rounded-md border ${getStyle()} shadow-lg z-50 max-w-md`}>
      <div className="flex justify-between items-start">
        <span>{message}</span>
        <button
          onClick={onClose}
          className="ml-4 text-current hover:opacity-70 focus:outline-none"
        >
          ×
        </button>
      </div>
    </div>
  );
};

export default Feedback;