import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import { Task } from '../types/task';
import apiClient from '../lib/api';

const DashboardPage: React.FC = () => {
  const router = useRouter();
  const [userId, setUserId] = useState<string>('');
  const [showTaskForm, setShowTaskForm] = useState<boolean>(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('jwt_token'); // Using the correct token name from login
    if (!token) {
      router.push('/login');
      return;
    }

    // Get user ID from localStorage or session
    // In a real implementation, this would come from the JWT token or user profile
    const storedUserId = localStorage.getItem('userId');
    if (storedUserId) {
      setUserId(storedUserId);
    } else {
      // If we don't have a userId, we might need to fetch it from the API
      fetchUserProfile();
    }

    setLoading(false);
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await apiClient.get('/auth/me');

      const userData = response.data;
      setUserId(userData.id);
      localStorage.setItem('userId', userData.id);
    } catch (err: any) {
      // Only redirect to login on 401/403 errors (authentication issues)
      if (err.response?.status === 401 || err.response?.status === 403) {
        localStorage.removeItem('jwt_token');
        router.push('/login');
      } else {
        // For other errors, just set the error state without redirecting
        setError(err.response?.data?.message || err.message || 'An error occurred while fetching user profile');
      }
    }
  };

  const handleTaskCreated = (task: Task) => {
    // Task was created successfully
    setShowTaskForm(false);
  };

  const handleTaskUpdated = (task: Task) => {
    // Task was updated successfully
    setEditingTask(null);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleDeleteTask = (taskId: string) => {
    // Task was deleted successfully
    console.log(`Task ${taskId} deleted`);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-white">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500 mb-4"></div>
          <p className="text-dark-700">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-white">
        <div className="max-w-md w-full px-4">
          <div className="card text-center">
            <div className="mx-auto bg-red-100 rounded-full p-3 inline-block mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h2 className="text-xl font-bold text-dark-800 mb-2">Error</h2>
            <p className="text-dark-600 mb-4">{error}</p>
            <button
              onClick={() => router.push('/login')}
              className="btn-primary"
            >
              Go to Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      <Head>
        <title>Dashboard - Todo App</title>
        <meta name="description" content="Your todo dashboard" />
      </Head>

      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <div className="bg-gradient-to-r from-primary-500 to-secondary-500 w-10 h-10 rounded-lg flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h1 className="ml-3 text-xl font-bold text-dark-800">Todo Dashboard</h1>
            </div>

            <div className="flex items-center space-x-4">
              <button
                onClick={() => {
                  setEditingTask(null);
                  setShowTaskForm(!showTaskForm);
                }}
                className="bg-gradient-to-r from-primary-600 to-secondary-600 hover:from-primary-700 hover:to-secondary-700 text-white px-4 py-2 rounded-lg font-medium transition-all duration-200 shadow-md hover:shadow-lg"
              >
                {showTaskForm ? 'Cancel' : 'Create Task'}
              </button>

              <button
                onClick={() => {
                  localStorage.removeItem('jwt_token');
                  router.push('/login');
                }}
                className="text-dark-600 hover:text-dark-800 px-3 py-2 rounded-lg font-medium transition-colors duration-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {showTaskForm && (
          <div className="mb-8">
            <div className="card">
              <h2 className="text-xl font-bold text-dark-800 mb-4">
                {editingTask ? 'Edit Task' : 'Create New Task'}
              </h2>
              <TaskForm
                userId={userId}
                initialTask={editingTask}
                onTaskCreated={handleTaskCreated}
                onTaskUpdated={handleTaskUpdated}
                onCancel={() => {
                  setShowTaskForm(false);
                  setEditingTask(null);
                }}
              />
            </div>
          </div>
        )}

        <div className="card">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-dark-800">Your Tasks</h2>
            <div className="text-sm text-dark-600">
              Manage your tasks efficiently
            </div>
          </div>

          <TaskList
            userId={userId}
            onTaskUpdate={handleEditTask}
            onTaskDelete={handleDeleteTask}
          />
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;