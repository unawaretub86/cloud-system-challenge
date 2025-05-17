import React from 'react';
import TaskForm from './TaskForm';
import TaskList from './TaskList';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Tasks.css';

const Tasks: React.FC = () => {
  const { state, logout } = useAuth();
  const navigate = useNavigate();

  if (!state.isAuthenticated) {
    navigate('/login');
    return null;
  }

  return (
    <div className="tasks-container">
      <div className="tasks-header">
        <h1>Task Management</h1>
        <button className="logout-button" onClick={logout}>
          Logout
        </button>
      </div>
      <div className="tasks-content">
        <TaskForm />
        <TaskList />
      </div>
    </div>
  );
};

export default Tasks;
