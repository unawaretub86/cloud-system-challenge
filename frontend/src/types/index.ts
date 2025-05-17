export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string; 
  updated_at: string;
  due_date: string | null; 
  owner: string; 
  owner_username?: string; 
  priority: 'low' | 'medium' | 'high';
  status: 'todo' | 'in_progress' | 'done';
  tags: string;
  
  createdAt?: string;
  updatedAt?: string;
  dueDate?: string | null;
  userId?: string;
  ownerUsername?: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  token?: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  pendingOperations: Record<string, boolean>; 
}

export interface TaskCreatePayload {
  title: string;
  description: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  status: 'todo' | 'in_progress' | 'done';
  due_date: string | null;
  tags: string;
  created_at?: string;
  updated_at?: string;
  owner?: string;
}
