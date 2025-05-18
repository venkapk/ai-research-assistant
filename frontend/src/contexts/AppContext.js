import React, { createContext, useState, useContext } from 'react';
import { verifyEntity, generateResearch } from '../services/api';

// Create context
const AppContext = createContext();

// Create provider component
export const AppProvider = ({ children }) => {
  const [activePage, setActivePage] = useState('verify');
  const [formData, setFormData] = useState({
    name: '',
    affiliation: '',
    entityType: 'academic'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [verificationResult, setVerificationResult] = useState(null);
  const [researchResult, setResearchResult] = useState(null);

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  // Handle verification
  const handleVerify = async () => {
    // Validation
    if (!formData.name || !formData.affiliation) {
      setError('Name and affiliation are required fields');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await verifyEntity(formData);
      setVerificationResult(result);
      setLoading(false);
    } catch (err) {
      console.log(err,"err inside AppContext ")
      setError(err?.message || 'Failed to verify entity. Please try again.');
      setLoading(false);
    }
  };

  // Handle research generation
  const handleGenerateResearch = async () => {
    if (!verificationResult) {
      setError('Please verify an entity first');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await generateResearch(
        verificationResult, 
        formData.entityType
      );
      setResearchResult(result);
      setActivePage('research');
      setLoading(false);
    } catch (err) {
      setError(err.message || 'Failed to generate research. Please try again.');
      setLoading(false);
    }
  };

  // Values to be provided
  const value = {
    activePage,
    setActivePage,
    formData,
    loading,
    error,
    verificationResult,
    researchResult,
    handleInputChange,
    handleVerify,
    handleGenerateResearch,
    setError
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook for using the context
export const useApp = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};