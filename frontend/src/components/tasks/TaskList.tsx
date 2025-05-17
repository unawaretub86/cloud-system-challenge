import React, { useEffect, useState } from 'react';
import { useTask } from '../../context';
import TaskItem from './TaskItem';
import { Task } from '../../types';

const TaskList: React.FC = () => {
  const { state, getTasks } = useTask();
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);

  useEffect(() => {
    getTasks();
  }, []); 
  useEffect(() => {
    switch (filter) {
      case 'active':
        setFilteredTasks(state.tasks.filter(task => !task.completed));
        break;
      case 'completed':
        setFilteredTasks(state.tasks.filter(task => task.completed));
        break;
      default:
        setFilteredTasks(state.tasks);
    }
  }, [filter, state.tasks]);

  return (
    <div className="task-list-container">
      <div className="task-filter">
        <button
          className={filter === 'all' ? 'active' : ''}
          onClick={() => setFilter('all')}
        >
          All
        </button>
        <button
          className={filter === 'active' ? 'active' : ''}
          onClick={() => setFilter('active')}
        >
          Active
        </button>
        <button
          className={filter === 'completed' ? 'active' : ''}
          onClick={() => setFilter('completed')}
        >
          Completed
        </button>
      </div>

      {state.loading ? (
        <p>Loading tasks...</p>
      ) : state.error ? (
        <div className="error-message">{state.error}</div>
      ) : filteredTasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <div className="task-list">
          {filteredTasks.map(task => (
            <TaskItem key={task.id} task={task} />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;
