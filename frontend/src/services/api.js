// 🌍 Dynamically set API base URL
// If in production → use your hosted API
// If in development → use local FastAPI backend
const API_BASE_URL = import.meta.env.PROD
  ? 'https://api.yourdomain.com/api'   // ✅ change to your deployed backend
  : 'http://localhost:8000/api';       // ✅ local backend during development

/**
 * Generate a quiz from a Wikipedia URL
 */
export const generateQuiz = async (url) => {
  try {
    const response = await fetch(`${API_BASE_URL}/generate_quiz`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to generate quiz');
    }

    return await response.json();
  } catch (error) {
    throw new Error(error.message || 'Network error occurred');
  }
};

/**
 * Preview a Wikipedia URL (title, description, etc.)
 */
export const previewUrl = async (url) => {
  try {
    const response = await fetch(`${API_BASE_URL}/preview_url`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Preview failed');
    }

    return await response.json();
  } catch (error) {
    throw new Error(error.message || 'Network error occurred');
  }
};

/**
 * Fetch all quiz history
 */
export const getQuizHistory = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/history`);

    if (!response.ok) {
      throw new Error('Failed to fetch quiz history');
    }

    return await response.json();
  } catch (error) {
    throw new Error(error.message || 'Network error occurred');
  }
};

/**
 * Fetch specific quiz details by ID
 */
export const getQuizDetails = async (quizId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/quiz/${quizId}`);

    if (!response.ok) {
      throw new Error('Failed to fetch quiz details');
    }

    return await response.json();
  } catch (error) {
    throw new Error(error.message || 'Network error occurred');
  }
};

/**
 * Submit quiz answers for scoring
 */
export const submitQuiz = async (quizId, answers, timeTaken) => {
  try {
    const response = await fetch(`${API_BASE_URL}/submit_quiz`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        quiz_id: quizId,
        answers,
        time_taken: timeTaken,
      }),
    });

    if (!response.ok) {
      throw new Error('Submission failed');
    }

    return await response.json();
  } catch (error) {
    throw new Error(error.message || 'Network error occurred');
  }
};
