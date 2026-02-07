import React, { useState } from 'react';
import { Task } from '../types/task';
import apiClient from '../lib/api';

interface TaskFormProps {
  userId: string;
  onTaskCreated?: (task: Task) => void;
  onTaskUpdated?: (task: Task) => void;
  initialTask?: Task | null;
  onCancel?: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({
  userId,
  onTaskCreated,
  onTaskUpdated,
  initialTask = null,
  onCancel
}) => {
  const [title, setTitle] = useState<string>(initialTask?.title || '');
  const [description, setDescription] = useState<string>(initialTask?.description || '');
  const [priority, setPriority] = useState<string>(initialTask?.priority || 'medium');
  const [tags, setTags] = useState<string>(initialTask?.tags?.join(', ') || '');
  const [dueDate, setDueDate] = useState<string>(initialTask?.due_date || '');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const taskData = {
        title,
        description,
        priority,
        tags: tags.split(',').map(tag => tag.trim()).filter(tag => tag !== ''),
        due_date: dueDate || null,
        completed: initialTask?.completed || false,
      };

      let response;
      if (initialTask) {
        // Update existing task
        response = await apiClient.put(`/api/${userId}/tasks/${initialTask.id}`, taskData);
      } else {
        // Create new task
        response = await apiClient.post(`/api/${userId}/tasks`, taskData);
      }

      const task = response.data;

      if (initialTask && onTaskUpdated) {
        onTaskUpdated(task);
      } else if (!initialTask && onTaskCreated) {
        onTaskCreated(task);
      }

      // Reset form if it's a new task
      if (!initialTask) {
        setTitle('');
        setDescription('');
        setPriority('medium');
        setTags('');
        setDueDate('');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while saving the task');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    }
    // Reset form when cancelling edit
    if (initialTask) {
      setTitle(initialTask.title);
      setDescription(initialTask.description);
      setPriority(initialTask.priority);
      setTags(initialTask.tags?.join(', ') || '');
      setDueDate(initialTask.due_date || '');
    }
  };

  return (
    <div className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-dark-700 mb-1">
            Task Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            disabled={loading}
            placeholder="What needs to be done?"
            className="input-field"
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-dark-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={loading}
            placeholder="Add details about this task..."
            rows={3}
            className="input-field resize-none"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="priority" className="block text-sm font-medium text-dark-700 mb-1">
              Priority
            </label>
            <select
              id="priority"
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              disabled={loading}
              className="input-field"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div>
            <label htmlFor="dueDate" className="block text-sm font-medium text-dark-700 mb-1">
              Due Date
            </label>
            <input
              type="date"
              id="dueDate"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              disabled={loading}
              className="input-field"
            />
          </div>
        </div>

        <div>
          <label htmlFor="tags" className="block text-sm font-medium text-dark-700 mb-1">
            Tags
          </label>
          <input
            type="text"
            id="tags"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            disabled={loading}
            placeholder="Comma-separated tags (e.g., work, personal, urgent)"
            className="input-field"
          />
          <p className="mt-1 text-xs text-dark-500">Separate tags with commas</p>
        </div>

        <div className="flex items-center space-x-3 pt-2">
          <button
            type="submit"
            disabled={loading}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
              loading
                ? 'bg-primary-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-primary-600 to-secondary-600 hover:from-primary-700 hover:to-secondary-700 text-white shadow-lg hover:shadow-xl'
            }`}
          >
            {loading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </span>
            ) : (
              `${initialTask ? 'Update' : 'Create'} Task`
            )}
          </button>

          {(initialTask || onCancel) && (
            <button
              type="button"
              onClick={handleCancel}
              disabled={loading}
              className="px-4 py-2 rounded-lg font-medium text-dark-700 bg-dark-100 hover:bg-dark-200 transition-colors duration-200"
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default TaskForm;