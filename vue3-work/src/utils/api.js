// src/utils/api.js
import axios from 'axios';

const apiUrl = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const createTask = (data) => api.post('/ez-note/date/create', data);


export const getTasks = (date) => api.post('/ez-note/date/get', { date });
export const deleteTask = (id) => api.post('/ez-note/date/delete', { date_id: id });
export const updateTask = (data) => api.post('/ez-note/date/modify', data);
export const updateTaskStatus = (data) => api.post('/ez-note/date/status', data);

export default api;
