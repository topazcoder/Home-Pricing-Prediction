import axios from 'axios';
import { AnalyzeHomeRequest, PricingReport } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzHome = async (data: AnalyzeHomeRequest): Promise<PricingReport> => {
  const response = await api.post<PricingReport>('/api/analyze-home', data);
  return response.data;
};

export const analyzeCondition = async (data: {
  subject_home: any;
  photos: string[];
  video_transcript: string;
}) => {
  const response = await api.post('/api/analyze-condition', data);
  return response.data;
};

export const selectComparables = async (data: {
  subject_home: any;
  comparable_sales: any[];
  num_comps?: number;
}) => {
  const response = await api.post('/api/select-comparables', data);
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/api/health');
  return response.data;
};
