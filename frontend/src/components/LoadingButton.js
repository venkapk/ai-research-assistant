import React from 'react';

/**
 * A button component that shows a loading state.
 * Props:
 * - isLoading: boolean – whether the button is in a loading state
 * - onClick: function – click handler function
 * - loadingText: string – text to display when loading
 * - text: string – text to display when not loading
 * - disabled: boolean – optional flag to disable the button externally
 */
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