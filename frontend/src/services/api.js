/**
 * API service for communicating with the AI Research Tool backend.
 * 
 * This service connects to your Flask backend running on localhost.
 * It includes functions for verifying entities and generating research.
 */

// Base URL for API endpoints
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Helper function to handle API responses
 * @param {Response} response - The fetch API response
 * @returns {Promise} - Resolves to the JSON response or rejects with error
 */
const handleResponse = async (response) => {
  const data = await response.json();
  
  if (!response.ok) {
    // The backend returns errors in a specific format we need to handle
    console.log(data,"responsedata in api.js- handle resp")
    const errorMessage = data.error?.brief_description || 'An unexpected error occurred';
    throw new Error(errorMessage);
  }
  
  if (!data.success) {
    throw new Error(data.error || 'Request failed');
  }
  
  return data.data;
};

/**
 * Verify an entity based on name, affiliation and type
 * @param {Object} data - The entity data
 * @param {string} data.name - Entity name
 * @param {string} data.affiliation - Entity affiliation
 * @param {string} data.entityType - Either 'academic' or 'startup'
 * @returns {Promise} - The verification result
 */
export const verifyEntity = async (data) => {
  try {
    // Based on your api.py, the endpoint expects name, affiliation, and entityType
    const response = await fetch(`${API_BASE_URL}/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: data.name,
        affiliation: data.affiliation,
        entityType: data.entityType
      })
    });
    return handleResponse(response);
  } catch (error) {
    throw new Error(error.message || 'Failed to verify entity. Please try again.');
  }
};

/**
 * Generate research for a verified entity
 * @param {Object} entityInfo - The verified entity info
 * @param {string} entityType - Either 'academic' or 'startup'
 * @returns {Promise} - The research data
 */
export const generateResearch = async (entityInfo, entityType) => {
  try {
    // Based on your research_service.py, the endpoint expects entityInfo and entityType
    const response = await fetch(`${API_BASE_URL}/research`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        entityInfo: entityInfo,
        entityType: entityType
      })
    });
    
    return handleResponse(response);
  } catch (error) {
    console.error('Error in generateResearch:', error);
    throw new Error(error.message || 'Failed to generate research. Please try again.');
  }
};