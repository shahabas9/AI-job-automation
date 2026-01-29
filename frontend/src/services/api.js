import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://192.168.68.135:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const extractProfile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/profile/extract', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const fetchJobs = async (profile, page = 1, size = 20) => {
    const response = await api.post(`/jobs/all?page=${page}&size=${size}`, profile);
    return response.data;
};

export const prepareApplication = async (profile, job) => {
    const response = await api.post('/apply/prepare', {
        profile,
        job: job.job || job, // Handle if job is nested or flat
    });
    return response.data;
};

export const assistApply = async (job) => {
    const response = await api.post('/apply/assist', job.job || job);
    return response.data;
};

export default api;
