import React from 'react';
import { ErrorIcon } from './icons';

const ErrorMessage = ({message}) => {
  if (!message) return null;
  return (
    <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-4">
      <div className="flex">
        <div className="flex-shrink-0">
          <ErrorIcon />
        </div>
        <div className="ml-3">
          <p className="text-sm text-red-700">{message}</p>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;