import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import { Task } from '../types/task';
import apiClient from '../lib/api';

declare global {
  interface Window {
    searchTimeout: any;
  }
}

const DashboardPage: React.FC = () => {
  const router = useRouter();
  const [userId, setUserId] = useState<string>('');
  const [showTaskForm, setShowTaskForm] = useState<boolean>(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState<string>('');
  const [completedFilter, setCompletedFilter] = useState<string>('all'); // 'all', 'completed', 'incomplete'
  const [priorityFilter, setPriorityFilter] = useState<string>('all'); // 'all', 'high', 'medium', 'low'
  const [tagFilter, setTagFilter] = useState<string>('');
  const [sortField, setSortField] = useState<string>('created_at');
  const [sortOrder, setSortOrder] = useState<string>('desc');

  useEffect(() => {
    // Check if user is authenticated by looking for our token
    const token = localStorage.getItem('todo-app-token'); // Using the token name from our auth-client
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

  const fetchTasks = () => {
    // The TaskList component will handle the actual API call when props change
    // This function is just for the search bar to trigger updates
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-100">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mb-4"></div>
          <p className="text-gray-300">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-100">
        <div className="max-w-md w-full px-4">
          <div className="card text-center">
            <div className="mx-auto bg-red-900/30 rounded-full p-3 inline-block mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Error</h2>
            <p className="text-gray-300 mb-4">{error}</p>
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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-100">
      <Head>
        <title>Dashboard - Todo App</title>
        <meta name="description" content="Your todo dashboard" />
      </Head>

      <header className="bg-gray-800/70 backdrop-blur-sm border-b border-gray-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <div className="bg-gradient-to-r from-indigo-600 to-purple-600 w-10 h-10 rounded-lg flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h1 className="ml-3 text-xl font-bold text-white">Todo Dashboard</h1>
            </div>

            <div className="flex items-center space-x-4">
              <button
                onClick={() => {
                  setEditingTask(null);
                  setShowTaskForm(!showTaskForm);
                }}
                className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-4 py-2 rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md"
              >
                {showTaskForm ? 'Cancel' : 'Create Task'}
              </button>

              <button
                onClick={() => {
                  localStorage.removeItem('todo-app-token');
                  localStorage.removeItem('userId');
                  router.push('/login');
                }}
                className="text-gray-300 hover:text-white px-3 py-2 rounded-lg font-medium transition-colors duration-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="flex max-w-7xl mx-auto min-h-screen">
        {/* Left Sidebar - Filters, Sort & Priority */}
        <div className="w-64 bg-gray-800/90 backdrop-blur-sm border-r border-gray-700/50 p-4 hidden md:block">
          <div className="space-y-6">
            <div>
              <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">Filters</h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-gray-400 mb-1 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    Status
                  </label>
                  <select
                    value={completedFilter}
                    onChange={(e) => setCompletedFilter(e.target.value)}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  >
                    <option value="all">All Tasks</option>
                    <option value="completed">Completed</option>
                    <option value="incomplete">Incomplete</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-400 mb-1 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Priority
                  </label>
                  <select
                    value={priorityFilter}
                    onChange={(e) => setPriorityFilter(e.target.value)}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  >
                    <option value="all">All Priorities</option>
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-400 mb-1 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                    Tags
                  </label>
                  <select
                    value={tagFilter}
                    onChange={(e) => setTagFilter(e.target.value)}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  >
                    <option value="">All Tags</option>
                    <option value="work">Work</option>
                    <option value="personal">Personal</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">Sort</h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-gray-400 mb-1 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4" />
                    </svg>
                    Sort By
                  </label>
                  <select
                    value={`${sortField}-${sortOrder}`}
                    onChange={(e) => {
                      const [field, order] = e.target.value.split('-');
                      setSortField(field);
                      setSortOrder(order);
                    }}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  >
                    <option value="created_at-desc">Newest First</option>
                    <option value="created_at-asc">Oldest First</option>
                    <option value="updated_at-desc">Recently Updated</option>
                    <option value="priority-desc">Priority High-Low</option>
                    <option value="priority-asc">Priority Low-High</option>
                    <option value="title-asc">Title A-Z</option>
                    <option value="title-desc">Title Z-A</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 px-4 sm:px-6 lg:px-8 py-8">
          {showTaskForm && (
            <div className="mb-8">
              <div className="card">
                <h2 className="text-xl font-bold text-white mb-4">
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
              <h2 className="text-xl font-bold text-white">Your Tasks</h2>
              <div className="text-sm text-gray-400">
                Manage your tasks efficiently
              </div>
            </div>

            {/* Search Bar - Top of Tasks */}
            <div className="relative mb-4">
              <input
                type="text"
                placeholder="Search tasks..."
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value);
                  // Debounced search to avoid too many API calls
                  clearTimeout(window.searchTimeout);
                  window.searchTimeout = setTimeout(() => {
                    // The TaskList will automatically update via props
                  }, 300);
                }}
                onKeyPress={(e) => e.key === 'Enter' && fetchTasks()}
                className="w-full bg-gray-800/70 backdrop-blur-sm border border-gray-600 rounded-lg px-4 py-2 pl-10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>

            <TaskList
              userId={userId}
              onTaskUpdate={handleEditTask}
              onTaskDelete={handleDeleteTask}
              search={search}
              completedFilter={completedFilter}
              priorityFilter={priorityFilter}
              tagFilter={tagFilter}
              sortField={sortField}
              sortOrder={sortOrder}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;