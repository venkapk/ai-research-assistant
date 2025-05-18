import React from 'react';
import { LogoIcon } from './icons';

const Header = ({ activePage, setActivePage, hasResearchResults }) => {
  return (
    <header className="bg-white shadow">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          <div className="flex items-center">
            <div className="w-10 h-10 bg-blue-600 rounded-md flex items-center justify-center">
              <LogoIcon />
            </div>
            <h1 className="ml-3 text-2xl font-bold text-gray-900">AI Research Tool</h1>
          </div>
          <nav className="flex space-x-4">
            <button 
              className={`px-3 py-2 rounded-md text-sm font-medium ${activePage === 'verify' ? 'bg-blue-100 text-blue-800' : 'text-gray-600 hover:text-gray-900'}`}
              onClick={() => setActivePage('verify')}
            >
              Verify Entity
            </button>
            <button 
              className={`px-3 py-2 rounded-md text-sm font-medium ${activePage === 'research' ? 'bg-blue-100 text-blue-800' : 'text-gray-600 hover:text-gray-900'}`}
              onClick={() => setActivePage('research')}
              disabled={!hasResearchResults}
            >
              Research Results
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;