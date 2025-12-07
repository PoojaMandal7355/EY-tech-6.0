/**
 * ResponseGenerator utility
 * Handles generating AI responses from backend API
 */

import { getAccessToken } from './authApi';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Generate AI response from backend API
 * @param {string} prompt - User's input prompt
 * @returns {Promise<{content: string, charts: Array}>} Response with optional charts
 */
export const generateResponse = async (prompt) => {
  const accessToken = getAccessToken();
  
  if (!accessToken) {
    throw new Error('User not authenticated. Please login first.');
  }

  try {
    // TODO: Replace endpoint with actual chat endpoint when available
    // For now, using agent endpoint as placeholder
    // const response = await fetch(`${API_URL}/chat/generate`, {
    
    // Temporary placeholder - agent endpoint will be used for now
    throw new Error('Chat API not yet configured. Please contact backend developer to implement /api/v1/chat/generate endpoint.');
    
    // When chat endpoint is ready, uncomment and use:
    /*
    const response = await fetch(`${API_URL}/chat/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify({ 
        prompt,
        session_id: 1 // Will be dynamic based on session
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to generate response');
    }

    const data = await response.json();
    return {
      content: data.content || data.response || '',
      charts: data.charts || []
    };
    */
  } catch (error) {
    console.error('Error generating response:', error);
    throw error;
  }
};
