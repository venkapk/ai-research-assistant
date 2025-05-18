import React from 'react';
import { useApp } from '../contexts/AppContext';
import ErrorMessage from '../components/ErrorMessage';
import LoadingButton from '../components/LoadingButton';

const VerifyPage = () => {
  const { 
    formData, 
    loading, 
    error, 
    verificationResult,
    handleInputChange, 
    handleVerify,
    handleGenerateResearch 
  } = useApp();

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
      <div className="px-4 py-5 sm:px-6">
        <h2 className="text-lg leading-6 font-medium text-gray-900">Entity Verification</h2>
        <p className="mt-1 text-sm text-gray-500">Verify an academic professional or startup founder to generate research.</p>
      </div>
      <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
        <div className="space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="John Smith"
            />
          </div>

          <div>
            <label htmlFor="affiliation" className="block text-sm font-medium text-gray-700">Affiliation</label>
            <input
              type="text"
              id="affiliation"
              name="affiliation"
              value={formData.affiliation}
              onChange={handleInputChange}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="Stanford University or Acme Inc."
            />
          </div>

          <div>
            <label htmlFor="entityType" className="block text-sm font-medium text-gray-700">Entity Type</label>
            <select
              id="entityType"
              name="entityType"
              value={formData.entityType}
              onChange={handleInputChange}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option value="academic">Academic Professional</option>
              <option value="startup">Startup Founder</option>
            </select>
          </div>

          <div>
            <LoadingButton
              onClick={handleVerify}
              isLoading={loading}
              loadingText="Verifying..."
              text="Verify Entity"
            />
          </div>
        </div>

        <ErrorMessage message={error} />

        {verificationResult && !loading && (
          <div className="mt-6 border border-gray-200 rounded-md overflow-hidden">
            <div className="px-4 py-5 bg-gray-50 sm:px-6">
              <h3 className="text-lg font-medium leading-6 text-gray-900">Verification Result</h3>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">Full Name</dt>
                  <dd className="mt-1 text-sm text-gray-900">{verificationResult.full_name}</dd>
                </div>
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">Affiliation</dt>
                  <dd className="mt-1 text-sm text-gray-900">{verificationResult.affiliation}</dd>
                </div>
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">Title</dt>
                  <dd className="mt-1 text-sm text-gray-900">{verificationResult.title}</dd>
                </div>
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">Confidence Score</dt>
                  <dd className="mt-1 text-sm text-gray-900">{verificationResult.confidence_score}%</dd>
                </div>
                <div className="sm:col-span-2">
                  <dt className="text-sm font-medium text-gray-500">Description</dt>
                  <dd className="mt-1 text-sm text-gray-900">{verificationResult.brief_description}</dd>
                </div>
              </dl>
              <div className="mt-6">
                <LoadingButton
                  onClick={handleGenerateResearch}
                  isLoading={loading}
                  loadingText="Generating Research..."
                  text="Generate Research"
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VerifyPage;