// index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

// src/api.js
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3000';

export async function fetchResults(limit = 50) {
  const response = await axios.get(`${API_BASE}/results`, {
    params: { limit }
  });
  return response.data;
}

export async function fetchStats(window = 60) {
  const response = await axios.get(`${API_BASE}/stats`, {
    params: { window }
  });
  return response.data;
}