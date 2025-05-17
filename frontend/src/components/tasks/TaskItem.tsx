import React, { useState, useEffect } from 'react';
import { Task } from '../../types';
import { useTask } from '../../context/TaskContext';

interface TaskItemProps {
  task: Task;
}

const TaskItem: React.FC<TaskItemProps> = ({ task }) => {
  const { updateTask, toggleTaskCompletion, deleteTask, isTaskPending, state } = useTask();
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(task.title);
  const [editedDescription, setEditedDescription] = useState(task.description);
  const [editedPriority, setEditedPriority] = useState(task.priority);
  const [editedStatus, setEditedStatus] = useState(task.status);
  const [editedDueDate, setEditedDueDate] = useState(task.dueDate || '');
  const [editedTags, setEditedTags] = useState(task.tags || '');
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    if (!state.error) {
      setError(null);
    }
  }, [state.error]);

  const handleToggleComplete = async () => {
    try {
      await toggleTaskCompletion(task.id);
    } catch (err) {
      setError('Failed to toggle task completion');
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = async () => {
    try {
      const result = await updateTask(task.id, {
        title: editedTitle,
        description: editedDescription,
        priority: editedPriority,
        status: editedStatus,
        completed: editedStatus === 'done',
        due_date: editedDueDate || null, 
        tags: editedTags
      });
      
      if (result) {
        setIsEditing(false);
        setError(null);
      } else {
        setError('Failed to update task');
      }
    } catch (err) {
      setError('An error occurred while updating the task');
    }
  };

  const handleCancel = () => {
    setEditedTitle(task.title);
    setEditedDescription(task.description);
    setEditedPriority(task.priority);
    setEditedStatus(task.status);
    setEditedDueDate(task.dueDate || '');
    setEditedTags(task.tags || '');
    setIsEditing(false);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        const success = await deleteTask(task.id);
        if (!success) {
          setError('Failed to delete task');
        }
      } catch (err) {
        setError('An error occurred while deleting the task');
      }
    }
  };

  const isPending = isTaskPending(task.id);
  
  return (
    <div className={`task-item ${task.completed ? 'completed' : ''} ${isPending ? 'pending' : ''}`}>
      {error && <div className="task-error-message">{error}</div>}
      {isEditing ? (
        <div className="task-edit-form">
          <input
            type="text"
            value={editedTitle}
            onChange={(e) => setEditedTitle(e.target.value)}
            placeholder="Task title"
            required
          />
          <textarea
            value={editedDescription}
            onChange={(e) => setEditedDescription(e.target.value)}
            placeholder="Task description"
          />
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="edit-priority">Priority</label>
              <select
                id="edit-priority"
                value={editedPriority}
                onChange={(e) => setEditedPriority(e.target.value as 'low' | 'medium' | 'high')}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="edit-status">Status</label>
              <select
                id="edit-status"
                value={editedStatus}
                onChange={(e) => setEditedStatus(e.target.value as 'todo' | 'in_progress' | 'done')}
              >
                <option value="todo">To Do</option>
                <option value="in_progress">In Progress</option>
                <option value="done">Done</option>
              </select>
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="edit-due-date">Due Date</label>
            <input
              type="datetime-local"
              id="edit-due-date"
              value={editedDueDate}
              onChange={(e) => setEditedDueDate(e.target.value)}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="edit-tags">Tags (comma-separated)</label>
            <input
              type="text"
              id="edit-tags"
              value={editedTags}
              onChange={(e) => setEditedTags(e.target.value)}
              placeholder="e.g. work, important, project"
            />
          </div>
          
          <div className="task-edit-actions">
            <button onClick={handleSave}>Save</button>
            <button onClick={handleCancel}>Cancel</button>
          </div>
        </div>
      ) : (
        <>
          <div className="task-content">
            <div className="task-header">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={handleToggleComplete}
              />
              <h3 className={task.completed ? 'completed-text' : ''}>{task.title}</h3>
              <div className="task-badges">
                <span className={`priority-badge ${task.priority}`}>{task.priority}</span>
                <span className={`status-badge ${task.status}`}>{task.status.replace('_', ' ')}</span>
              </div>
            </div>
            
            <p className={task.completed ? 'completed-text' : ''}>{task.description}</p>
            
            {task.tags && (
              <div className="task-tags">
                {task.tags.split(',').map((tag, index) => (
                  <span key={index} className="tag">{tag.trim()}</span>
                ))}
              </div>
            )}
            
            <div className="task-dates">
              <div>Created: {new Date(task.created_at || task.createdAt || '').toLocaleDateString()}</div>
              <div>Updated: {new Date(task.updated_at || task.updatedAt || '').toLocaleDateString()}</div>
              {(task.due_date || task.dueDate) && (
                <div className="due-date">Due: {new Date(task.due_date || task.dueDate || '').toLocaleString()}</div>
              )}
            </div>
          </div>
          <div className="task-actions">
            <button 
              onClick={handleEdit} 
              disabled={isPending}
              className={isPending ? 'disabled' : ''}
            >
              {isPending ? 'Loading...' : 'Edit'}
            </button>
            <button 
              onClick={handleDelete} 
              disabled={isPending}
              className={isPending ? 'disabled' : ''}
            >
              {isPending ? 'Loading...' : 'Delete'}
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default TaskItem;
