import React from 'react';
import { HashRouter as Router } from 'react-router-dom';
import './App.css';
import Navigation from './components/Navigation';
import { AuthProvider } from './context/AuthContext';
import { TaskProvider } from './context/TaskContext';

function App() {
  return (
    <Router>
      <AuthProvider>
        <TaskProvider>
          <div className="App">
            <Navigation />
          </div>
        </TaskProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
