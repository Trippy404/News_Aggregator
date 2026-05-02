import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - server might be slow');
    } else if (error.response?.status === 500) {
      console.error('Server error - check backend logs');
    } else if (error.response?.status === 404) {
      console.error('Endpoint not found');
    } else if (!error.response) {
      console.error('Network error - is the backend running on port 8000?');
    }
    return Promise.reject(error);
  }
);

export const fetchNews = async (params = {}) => {
  try {
    const defaultParams = { limit: 100, ...params };
    const response = await api.get('/api/news', { params: defaultParams });
    return response.data;
  } catch (error) {
    console.error('Error fetching news:', error.message);
    throw error;
  }
};

export const searchNews = async (query, params = {}) => {
  try {
    const defaultParams = { q: query, limit: 100, ...params };
    const response = await api.get('/api/search', { params: defaultParams });
    return response.data;
  } catch (error) {
    console.error('Error searching news:', error.message);
    throw error;
  }
};

export const getTrendingNews = async (limit = 50) => {
  try {
    const response = await api.get('/api/news/trending', { params: { limit } });
    return response.data;
  } catch (error) {
    console.error('Error fetching trending news:', error.message);
    return [];
  }
};

export const getNewsDetail = async (id) => {
  try {
    const response = await api.get(`/api/news/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching news detail:', error.message);
    throw error;
  }
};

export const shareArticle = async (id) => {
  try {
    const response = await api.post(`/api/news/${id}/share`);
    return response.data;
  } catch (error) {
    console.error('Error sharing article:', error.message);
    throw error;
  }
};

export const getFilterInfo = async () => {
  try {
    const response = await api.get('/api/news/filters/info');
    return response.data;
  } catch (error) {
    console.error('Error fetching filter info:', error.message);
    return { categories: [], sources: [], sentiments: [] };
  }
};

export default api;