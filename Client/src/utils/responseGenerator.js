/**
 * ResponseGenerator utility
 * Handles generating AI responses from backend API
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Generate AI response from backend API
 * @param {string} prompt - User's input prompt
 * @returns {Promise<{content: string, charts: Array}>} Response with optional charts
 */
export const generateResponse = async (prompt) => {
  try {
    const response = await fetch(`${API_URL}/chat/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
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
  } catch (error) {
    console.error('Error generating response:', error);
    throw error;
  }
};
