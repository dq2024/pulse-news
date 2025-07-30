// src/api.js
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export async function fetchResults(limit = 10) {
  const res = await fetch(`${API_BASE}/results?limit=${limit}`);
  if (!res.ok) throw new Error('Failed to fetch results');
  return res.json();
}

export async function fetchStats(window = 60) {
  const res = await fetch(`${API_BASE}/stats?window=${window}`);
  if (!res.ok) throw new Error('Failed to fetch stats');
  return res.json();
}