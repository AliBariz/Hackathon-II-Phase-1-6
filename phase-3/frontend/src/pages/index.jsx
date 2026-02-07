import React from 'react';
import Link from 'next/link';

const HomePage = () => {
  return (
    <div className="max-w-4xl mx-auto px-6 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Enhanced Todo Application</h1>
        <p className="text-xl text-gray-600">
          Manage your tasks efficiently with priorities, tags, search, filtering, and sorting
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4 text-blue-600">Features</h2>
          <ul className="space-y-2">
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Create tasks with titles, descriptions, and due dates</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Assign priorities (High, Medium, Low) to tasks</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Categorize tasks with tags (Work, Home)</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Search tasks by title or description</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Filter tasks by status, priority, or tag</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Sort tasks by due date, priority, or title</span>
            </li>
          </ul>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4 text-blue-600">Quick Actions</h2>
          <div className="space-y-4">
            <Link href="/tasks/list" legacyBehavior>
              <a className="block w-full py-3 px-6 bg-blue-600 text-white rounded-md text-center hover:bg-blue-700 transition-colors">
                View My Tasks
              </a>
            </Link>
            <Link href="/tasks/create" legacyBehavior>
              <a className="block w-full py-3 px-6 bg-green-600 text-white rounded-md text-center hover:bg-green-700 transition-colors">
                Create New Task
              </a>
            </Link>
          </div>
        </div>
      </div>

      <div className="bg-gray-50 p-6 rounded-lg">
        <h2 className="text-xl font-semibold mb-4">Getting Started</h2>
        <ol className="list-decimal pl-6 space-y-2">
          <li>Create your first task using the "Create New Task" button</li>
          <li>Assign appropriate priority and tag to organize your tasks</li>
          <li>Use search and filters to quickly find what you need</li>
          <li>Mark tasks as completed when finished</li>
        </ol>
      </div>
    </div>
  );
};

export default HomePage;