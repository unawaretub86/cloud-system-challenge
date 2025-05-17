import React, { createContext, useContext, useReducer, useCallback } from 'react';
import { Task, TaskState, TaskCreatePayload } from '../types';
import { taskService } from '../services';

type TaskAction =
  | { type: 'GET_TASKS_REQUEST' }
  | { type: 'GET_TASKS_SUCCESS'; payload: Task[] }
  | { type: 'GET_TASKS_FAILURE'; payload: string }
  | { type: 'ADD_TASK_REQUEST' }
  | { type: 'ADD_TASK_SUCCESS'; payload: Task }
  | { type: 'ADD_TASK_FAILURE'; payload: string }
  | { type: 'UPDATE_TASK_REQUEST'; payload: string }
  | { type: 'UPDATE_TASK_SUCCESS'; payload: Task }
  | { type: 'UPDATE_TASK_FAILURE'; payload: string }
  | { type: 'DELETE_TASK_REQUEST'; payload: string }
  | { type: 'DELETE_TASK_SUCCESS'; payload: string }
  | { type: 'DELETE_TASK_FAILURE'; payload: string }
  | { type: 'CLEAR_ERROR' };

const initialState: TaskState = {
  tasks: [],
  loading: false,
  error: null,
  pendingOperations: {}
};


const TaskContext = createContext<{
  state: TaskState;
  getTasks: () => Promise<void>;
  addTask: (task: TaskCreatePayload) => Promise<Task | null>;
  updateTask: (id: string, task: Partial<Task>) => Promise<Task | null>;
  toggleTaskCompletion: (id: string) => Promise<Task | null>;
  deleteTask: (id: string) => Promise<boolean>;
  clearError: () => void;
  isTaskPending: (id?: string) => boolean;
}>({
  state: initialState,
  getTasks: async (): Promise<void> => {},
  addTask: async (): Promise<Task | null> => null,
  updateTask: async (): Promise<Task | null> => null,
  toggleTaskCompletion: async (): Promise<Task | null> => null,
  deleteTask: async (): Promise<boolean> => false,
  clearError: () => {},
  isTaskPending: () => false
});

const taskReducer = (state: TaskState, action: TaskAction): TaskState => {
  switch (action.type) {
    case 'GET_TASKS_REQUEST':
      return {
        ...state,
        loading: true,
        error: null
      };
    case 'GET_TASKS_SUCCESS':
      return {
        ...state,
        tasks: action.payload,
        loading: false,
        error: null
      };
    case 'GET_TASKS_FAILURE':
      return {
        ...state,
        loading: false,
        error: action.payload
      };
    case 'ADD_TASK_REQUEST':
      return {
        ...state,
        loading: true,
        error: null
      };
    case 'ADD_TASK_SUCCESS':
      return {
        ...state,
        tasks: [...state.tasks, action.payload],
        loading: false,
        error: null
      };
    case 'ADD_TASK_FAILURE':
      return {
        ...state,
        loading: false,
        error: action.payload
      };
    case 'UPDATE_TASK_REQUEST':
      return {
        ...state,
        pendingOperations: { ...state.pendingOperations, [action.payload]: true },
        error: null
      };
    case 'UPDATE_TASK_SUCCESS':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        ),
        pendingOperations: { ...state.pendingOperations, [action.payload.id]: false },
        error: null
      };
    case 'UPDATE_TASK_FAILURE':
      const taskId = typeof action.payload === 'string' && action.payload.includes(':') 
        ? action.payload.split(':')[0].trim() 
        : '';
      
      return {
        ...state,
        pendingOperations: taskId 
          ? { ...state.pendingOperations, [taskId]: false }
          : state.pendingOperations,
        error: action.payload
      };
    case 'DELETE_TASK_REQUEST':
      return {
        ...state,
        pendingOperations: { ...state.pendingOperations, [action.payload]: true },
        error: null
      };
    case 'DELETE_TASK_SUCCESS':
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload),
        pendingOperations: { ...state.pendingOperations, [action.payload]: false },
        error: null
      };
    case 'DELETE_TASK_FAILURE':
      const deleteTaskId = typeof action.payload === 'string' && action.payload.includes(':') 
        ? action.payload.split(':')[0].trim() 
        : '';
      
      return {
        ...state,
        pendingOperations: deleteTaskId 
          ? { ...state.pendingOperations, [deleteTaskId]: false }
          : state.pendingOperations,
        error: action.payload
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null
      };
    default:
      return state;
  }
};

export const TaskProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(taskReducer, initialState);

  const isTaskPending = useCallback((id?: string): boolean => {
    if (!id) {
      return state.loading || Object.values(state.pendingOperations).some(value => value);
    }
    return !!state.pendingOperations[id];
  }, [state.loading, state.pendingOperations]);

  const getTasks = async (): Promise<void> => {
    try {
      dispatch({ type: 'GET_TASKS_REQUEST' });
      const tasks = await taskService.getTasks();
      dispatch({ type: 'GET_TASKS_SUCCESS', payload: tasks });
    } catch (error: any) {
      console.error('Error fetching tasks:', error);
      const errorMessage = error.message || 'Failed to fetch tasks';
      dispatch({ type: 'GET_TASKS_FAILURE', payload: errorMessage });
    }
  };

  const addTask = async (task: TaskCreatePayload): Promise<Task | null> => {
    try {
      dispatch({ type: 'ADD_TASK_REQUEST' });
      console.log('Sending task data:', task);
      

      const formattedTask = {
        ...task,
        due_date: task.due_date === '' ? null : task.due_date
      };
      
      console.log('Formatted task data:', formattedTask);
      const newTask = await taskService.createTask(formattedTask);
      console.log('Task created successfully:', newTask);
      dispatch({ type: 'ADD_TASK_SUCCESS', payload: newTask });
      return newTask;
    } catch (error: any) {
      console.error('Error creating task:', error);
      let errorMessage = 'Failed to add task';
      
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        console.error('Response headers:', error.response.headers);
        

        if (error.response.data) {
          if (typeof error.response.data === 'string') {
            errorMessage = error.response.data;
          } else if (error.response.data.detail) {
            errorMessage = error.response.data.detail;
          } else if (error.response.data.non_field_errors) {
            errorMessage = error.response.data.non_field_errors.join(', ');
          } else {

            const fieldErrors = Object.entries(error.response.data)
              .map(([field, errors]) => `${field}: ${Array.isArray(errors) ? errors.join(', ') : errors}`)
              .join('; ');
            
            if (fieldErrors) {
              errorMessage = `Validation errors: ${fieldErrors}`;
            }
          }
        }
      }
      
      dispatch({ type: 'ADD_TASK_FAILURE', payload: errorMessage });
      return null;
    }
  };

  const updateTask = async (id: string, task: Partial<Task>): Promise<Task | null> => {
    try {
      dispatch({ type: 'UPDATE_TASK_REQUEST', payload: id });
      const updatedTask = await taskService.updateTask(id, task);
      dispatch({ type: 'UPDATE_TASK_SUCCESS', payload: updatedTask });
      return updatedTask;
    } catch (error: any) {
      console.error(`Error updating task ${id}:`, error);
      const errorMessage = error.message || `Failed to update task ${id}`;
      dispatch({ type: 'UPDATE_TASK_FAILURE', payload: `${id}: ${errorMessage}` });
      return null;
    }
  };

  const toggleTaskCompletion = async (id: string): Promise<Task | null> => {
    try {
      dispatch({ type: 'UPDATE_TASK_REQUEST', payload: id });
      const updatedTask = await taskService.toggleTaskCompletion(id);
      dispatch({ type: 'UPDATE_TASK_SUCCESS', payload: updatedTask });
      return updatedTask;
    } catch (error: any) {
      console.error(`Error toggling task ${id} completion:`, error);
      const errorMessage = error.message || `Failed to toggle task ${id} completion`;
      dispatch({ type: 'UPDATE_TASK_FAILURE', payload: `${id}: ${errorMessage}` });
      return null;
    }
  };

  const deleteTask = async (id: string): Promise<boolean> => {
    try {
      dispatch({ type: 'DELETE_TASK_REQUEST', payload: id });
      await taskService.deleteTask(id);
      dispatch({ type: 'DELETE_TASK_SUCCESS', payload: id });
      return true;
    } catch (error: any) {
      console.error(`Error deleting task ${id}:`, error);
      const errorMessage = error.message || `Failed to delete task ${id}`;
      dispatch({ type: 'DELETE_TASK_FAILURE', payload: `${id}: ${errorMessage}` });
      return false;
    }
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  return (
    <TaskContext.Provider value={{ 
      state, 
      getTasks, 
      addTask, 
      updateTask, 
      toggleTaskCompletion, 
      deleteTask, 
      clearError,
      isTaskPending
    }}>
      {children}
    </TaskContext.Provider>
  );
};

export const useTask = () => useContext(TaskContext);
