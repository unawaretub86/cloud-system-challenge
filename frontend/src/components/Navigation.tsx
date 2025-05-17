import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './auth/Login';
import Register from './auth/Register';
import Tasks from './tasks/Tasks';
import { useAuth } from '../context/AuthContext';

const Navigation: React.FC = () => {
  const { state } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route 
        path="/tasks" 
        element={
          state.isAuthenticated ? <Tasks /> : <Navigate to="/login" />
        } 
      />
      <Route path="/" element={<Navigate to={state.isAuthenticated ? "/tasks" : "/login"} />} />
    </Routes>
  );
};

export default Navigation;
