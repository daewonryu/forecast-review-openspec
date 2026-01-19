import axios from 'axios';
import type {
  HealthStatus,
  PersonaGenerateRequest,
  PersonaSet,
  PersonaSetsResponse,
  SimulationRequest,
  SimulationResponse,
  Insights,
} from '../types/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health Check
export const checkHealth = async (): Promise<HealthStatus> => {
  const response = await apiClient.get('/health');
  return response.data;
};

// Personas
export const generatePersonas = async (
  request: PersonaGenerateRequest
): Promise<PersonaSet> => {
  const response = await apiClient.post('/api/personas/generate', request);
  return response.data;
};

export const getPersonaSet = async (setId: string): Promise<PersonaSet> => {
  const response = await apiClient.get(`/api/personas/sets/${setId}`);
  return response.data;
};

export const listPersonaSets = async (
  userId: number,
  page: number = 1,
  pageSize: number = 10
): Promise<PersonaSetsResponse> => {
  const response = await apiClient.get('/api/personas/sets', {
    params: { user_id: userId, page, page_size: pageSize },
  });
  return response.data;
};

export const deletePersonaSet = async (setId: string): Promise<void> => {
  await apiClient.delete(`/api/personas/sets/${setId}`);
};

// Simulations
export const runSimulation = async (
  request: SimulationRequest
): Promise<SimulationResponse> => {
  const response = await apiClient.post('/api/simulations/run', request);
  return response.data;
};

export const getSimulationResults = async (
  simulationId: string
): Promise<SimulationResponse> => {
  const response = await apiClient.get(`/api/simulations/${simulationId}`);
  return response.data;
};

export const listSimulations = async (
  userId: number,
  page: number = 1,
  pageSize: number = 10
): Promise<any> => {
  const response = await apiClient.get('/api/simulations', {
    params: { user_id: userId, page, page_size: pageSize },
  });
  return response.data;
};

// Insights
export const generateInsights = async (draftId: number): Promise<Insights> => {
  const response = await apiClient.post(`/api/insights/generate/${draftId}`);
  return response.data;
};

export const getInsights = async (draftId: number): Promise<Insights> => {
  const response = await apiClient.get(`/api/insights/draft/${draftId}`);
  return response.data;
};

export default apiClient;

