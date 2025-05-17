import api from './api';
import { Task, TaskCreatePayload } from '../types';

const taskService = {
  getTasks: async (): Promise<Task[]> => {
    const response = await api.get<Task[]>('/tasks/');
    return response.data;
  },

  getTask: async (id: string): Promise<Task> => {
    const response = await api.get<Task>(`/tasks/${id}/`);
    return response.data;
  },

  createTask: async (task: TaskCreatePayload): Promise<Task> => {
    const response = await api.post<Task>('/tasks/', task);
    return response.data;
  },

  updateTask: async (id: string, task: Partial<Task>): Promise<Task> => {
    const response = await api.put<Task>(`/tasks/${id}/`, task);
    return response.data;
  },

  toggleTaskCompletion: async (id: string): Promise<Task> => {
    const response = await api.post<Task>(`/tasks/${id}/toggle-completed/`);
    return response.data;
  },

  deleteTask: async (id: string): Promise<void> => {
    await api.delete(`/tasks/${id}/`);
  }
};

export default taskService;
