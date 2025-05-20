import React from 'react';

/**
 * Footer component for the application.
 * Currently includes a basic centered message.
 */
const Footer = () => {
  return (
    <footer className="bg-white">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="py-8 text-center text-sm text-gray-500">
          {/* <p>© {new Date().getFullYear()} AI Research Tool. All rights reserved.</p> */}
        </div>
      </div>
    </footer>
  );
};

export default Footer;