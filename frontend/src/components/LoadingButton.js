import React from 'react';

const LoadingButton = ({ isLoading, onClick, loadingText, text, disabled }) => {
  return (
    <button
      onClick={onClick}
      className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${isLoading || disabled ? 'opacity-75 cursor-not-allowed' : ''}`}
      disabled={isLoading || disabled}
    >
      {isLoading ? loadingText : text}
    </button>
  );
};

export default LoadingButton;