import React, { useState } from 'react';

const TaskFilters = ({ onFilter }) => {
  const [status, setStatus] = useState('');
  const [priority, setPriority] = useState('');
  const [tag, setTag] = useState('');

  const applyFilters = () => {
    onFilter({
      status: status || undefined,
      priority: priority || undefined,
      tag: tag || undefined
    });
  };

  const clearFilters = () => {
    setStatus('');
    setPriority('');
    setTag('');
    onFilter({});
  };

  return (
    <div className="mb-6 p-4 bg-gray-50 rounded-md">
      <h3 className="text-lg font-medium mb-3">Filter Tasks</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Tag</label>
          <select
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Tags</option>
            <option value="work">Work</option>
            <option value="home">Home</option>
          </select>
        </div>
      </div>

      <div className="mt-4 flex space-x-2">
        <button
          onClick={applyFilters}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Apply Filters
        </button>
        <button
          onClick={clearFilters}
          className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
        >
          Clear Filters
        </button>
      </div>
    </div>
  );
};

export default TaskFilters;