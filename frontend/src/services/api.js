// frontend/src/services/api.js
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || '"http://127.0.0.1:8000/ask"'
;

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Book content endpoints
  async getBookContents(filters = {}) {
    const queryParams = new URLSearchParams(filters).toString();
    const endpoint = queryParams ? `/book/contents?${queryParams}` : '/book/contents';
    return this.request(endpoint);
  }

  async getBookContent(contentId) {
    return this.request(`/book/contents/${contentId}`);
  }

  async getBookChapters(parentId = null) {
    const endpoint = parentId ? `/book/chapters?parent_id=${parentId}` : '/book/chapters';
    return this.request(endpoint);
  }

  // Chat endpoints
  async chatQuery(data) {
    return this.request('/chat/query', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Auth endpoints
  async login(credentials) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  // User endpoints
  async getUserProfile() {
    return this.request('/user/profile');
  }

  async updateUserProfile(data) {
    return this.request('/user/profile', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Bookmark endpoints
  async createBookmark(data) {
    return this.request('/user/bookmarks', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getUserBookmarks(userId) {
    return this.request(`/user/bookmarks?user_id=${userId}`);
  }
}

export default new ApiService();