import React, { useState, useEffect } from 'react';
import TaskCard from '../../components/TaskCard';
import TaskApi from '../../services/taskApi';
import TaskSearch from '../../components/TaskSearch';
import TaskFilters from '../../components/TaskFilters';
import TaskSorter from '../../components/TaskSorter';

const TaskListPage = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [searchResults, setSearchResults] = useState(null);
  const [filters, setFilters] = useState({});
  const [sortParams, setSortParams] = useState({});

  // Fetch tasks from API
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async (additionalParams = {}) => {
    try {
      setLoading(true);
      setError(null);
      setSearchResults(null); // Reset search results when fetching all tasks

      const params = {
        ...filters,
        ...sortParams,
        ...additionalParams
      };

      const tasksData = await TaskApi.getTasks(params);
      setTasks(tasksData);
    } catch (err) {
      setError(`Failed to fetch tasks: ${err.message}`);
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (searchTerm) => {
    if (!searchTerm.trim()) {
      setSearchResults(null);
      fetchTasks(); // Load all tasks if search is cleared
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const results = await TaskApi.searchTasks(searchTerm, { ...filters, ...sortParams });
      setSearchResults(results);
    } catch (err) {
      setError(`Search failed: ${err.message}`);
      console.error('Error searching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));

    // If we're currently showing search results, update the search with filters
    if (searchResults !== null) {
      handleSearch('', { ...newFilters, ...sortParams });
    } else {
      // Otherwise, fetch tasks with filters
      fetchTasks({ ...newFilters, ...sortParams });
    }
  };

  const handleSortChange = (newSortParams) => {
    setSortParams(prev => ({ ...prev, ...newSortParams }));

    // If we're currently showing search results, update the search with sort params
    if (searchResults !== null) {
      handleSearch('', { ...filters, ...newSortParams });
    } else {
      // Otherwise, fetch tasks with sort params
      fetchTasks({ ...filters, ...newSortParams });
    }
  };

  const handleToggleStatus = async (taskId) => {
    try {
      await TaskApi.toggleTaskStatus(taskId);
      setSuccess('Task status updated successfully!');
      // Refresh the task list
      fetchTasks();
    } catch (err) {
      setError(`Failed to update task status: ${err.message}`);
      console.error('Error toggling task status:', err);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await TaskApi.deleteTask(taskId);
        setSuccess('Task deleted successfully!');
        // Refresh the task list
        fetchTasks();
      } catch (err) {
        setError(`Failed to delete task: ${err.message}`);
        console.error('Error deleting task:', err);
      }
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-2xl font-bold mb-6">Loading Tasks...</h1>
        <p className="text-center">Please wait while we load your tasks.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-2xl font-bold mb-6">Error Loading Tasks</h1>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{error}</p>
        </div>
        <button
          onClick={fetchTasks}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Success message */}
      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          <p>{success}</p>
          <button
            onClick={() => setSuccess(null)}
            className="mt-2 text-sm underline"
          >
            Dismiss
          </button>
        </div>
      )}

      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Your Tasks</h1>
        <a
          href="/tasks/create"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Create New Task
        </a>
      </div>

      {/* Filters and Sorter components */}
      <TaskFilters onFilter={handleFilterChange} />
      <TaskSorter onSort={handleSortChange} />

      {/* Search component */}
      <TaskSearch onSearch={handleSearch} />

      {loading && !searchResults ? (
        <p className="text-center">Loading tasks...</p>
      ) : error ? (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{error}</p>
        </div>
      ) : (
        <>
          {searchResults !== null ? (
            <div>
              <h2 className="text-xl font-semibold mb-4">Search Results ({searchResults.length})</h2>
              {searchResults.length === 0 ? (
                <div className="text-center py-6">
                  <p className="text-gray-600">No tasks match your search.</p>
                  <button
                    onClick={() => {
                      setSearchResults(null);
                      fetchTasks();
                    }}
                    className="mt-2 text-blue-600 hover:text-blue-800 underline"
                  >
                    View all tasks
                  </button>
                </div>
              ) : (
                searchResults.map(task => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onToggle={handleToggleStatus}
                    onDelete={handleDeleteTask}
                  />
                ))
              )}
            </div>
          ) : tasks.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600 text-lg">No tasks yet!</p>
              <p className="text-gray-500 mt-2">Create your first task to get started.</p>
            </div>
          ) : (
            <div>
              {tasks.map(task => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onToggle={handleToggleStatus}
                  onDelete={handleDeleteTask}
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default TaskListPage;