import React, { useState, useEffect } from 'react';
import { Task } from '../types/task';
import apiClient from '../lib/api';

interface TaskListProps {
  userId: string;
  onTaskUpdate?: (task: Task) => void;
  onTaskDelete?: (taskId: string) => void;
  search: string;
  completedFilter: string;
  priorityFilter: string;
  tagFilter: string;
  sortField: string;
  sortOrder: string;
}

const TaskList: React.FC<TaskListProps> = ({
  userId,
  onTaskUpdate,
  onTaskDelete,
  search,
  completedFilter,
  priorityFilter,
  tagFilter,
  sortField,
  sortOrder
}) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, [userId, search, completedFilter, priorityFilter, tagFilter, sortField, sortOrder]);

  const fetchTasks = async () => {
    try {
      setLoading(true);

      // Build query parameters
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (completedFilter !== 'all') {
        params.append('completed', completedFilter === 'completed' ? 'true' : 'false');
      }
      if (priorityFilter !== 'all') params.append('priority', priorityFilter);
      if (tagFilter) params.append('tag', tagFilter);
      params.append('sort', sortField);
      params.append('order', sortOrder);

      const response = await apiClient.get(`/api/${userId}/tasks`, {
        params: Object.fromEntries(params)
      });

      const data = response.data;
      setTasks(data);
    } catch (err: any) {
      setError(err.response?.data?.message || err.message || 'An error occurred while fetching tasks');
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (taskId: string) => {
    try {
      const response = await apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`);
      const updatedTask = response.data;
      setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));

      if (onTaskUpdate) {
        onTaskUpdate(updatedTask);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while updating task');
    }
  };

  const deleteTask = async (taskId: string) => {
    try {
      await apiClient.delete(`/api/${userId}/tasks/${taskId}`);

      setTasks(tasks.filter(task => task.id !== taskId));

      if (onTaskDelete) {
        onTaskDelete(taskId);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while deleting task');
    }
  };


  // Get priority color based on priority level
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-500/20 text-red-200 border-red-500/30';
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-200 border-yellow-500/30';
      case 'low':
        return 'bg-green-500/20 text-green-200 border-green-500/30';
      default:
        return 'bg-gray-500/20 text-gray-200 border-gray-500/30';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
        </svg>
        <span>{error}</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">

      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="mx-auto bg-dark-100 rounded-full p-4 inline-block mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-dark-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-dark-800 mb-1">No tasks yet</h3>
          <p className="text-dark-600 mb-4">Get started by creating your first task</p>
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task) => (
            <div
              key={task.id}
              className={`bg-gray-800/70 backdrop-blur-lg rounded-lg border p-4 transition-all duration-200 ${
                task.completed
                  ? 'border-green-700/50 bg-green-900/20 opacity-80'
                  : 'border-gray-700/50 hover:border-indigo-500/50 hover:shadow-sm'
              }`}
            >
              <div className="flex items-start">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTaskCompletion(task.id)}
                  className="mt-1 h-5 w-5 rounded border-dark-300 text-primary-600 focus:ring-primary-500"
                />

                <div className="ml-3 flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h3 className={`text-base font-medium truncate ${
                      task.completed ? 'text-gray-400 line-through' : 'text-white'
                    }`}>
                      {task.title}
                    </h3>

                    <div className="flex items-center space-x-2 ml-2">
                      {task.priority && (
                        <span className={`text-xs px-2 py-1 rounded-full border ${getPriorityColor(task.priority)}`}>
                          {task.priority}
                        </span>
                      )}

                      <div className="flex space-x-1">
                        <button
                          onClick={() => onTaskUpdate && onTaskUpdate(task)}
                          className="text-dark-400 hover:text-primary-600 p-1 rounded-full hover:bg-primary-50 transition-colors"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>

                        <button
                          onClick={() => deleteTask(task.id)}
                          className="text-dark-400 hover:text-red-600 p-1 rounded-full hover:bg-red-50 transition-colors"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>

                  {task.description && (
                    <p className={`mt-1 text-sm ${
                      task.completed ? 'text-gray-400 line-through' : 'text-gray-300'
                    }`}>
                      {task.description}
                    </p>
                  )}

                  <div className="mt-2 flex flex-wrap items-center gap-2">
                    {task.due_date && (
                      <span className="inline-flex items-center text-xs text-gray-400">
                        <svg xmlns="http://www.w3.org/2000/svg" className="mr-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        Due: {new Date(task.due_date).toLocaleDateString()}
                      </span>
                    )}

                    {task.tags && Array.isArray(task.tags) && task.tags.length > 0 && (
                      <div className="flex flex-wrap gap-1">
                        {task.tags.map((tag: string, index: number) => (
                          <span
                            key={index}
                            className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-500/20 text-indigo-200 border border-indigo-500/30"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {!loading && !error && tasks.length > 0 && (
        <div className="text-sm text-dark-500 text-center pt-4 border-t border-dark-100">
          Showing {tasks.length} of {tasks.length} tasks
        </div>
      )}
    </div>
  );
};

export default TaskList;