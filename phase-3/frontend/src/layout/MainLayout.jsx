import React from 'react';
import Link from 'next/link';

const MainLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" legacyBehavior>
                <a className="flex-shrink-0 flex items-center">
                  <span className="text-xl font-bold text-gray-900">Enhanced Todo</span>
                </a>
              </Link>
            </div>
            <nav className="flex items-center space-x-4">
              <Link href="/" legacyBehavior>
                <a className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100">
                  Home
                </a>
              </Link>
              <Link href="/tasks/list" legacyBehavior>
                <a className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100">
                  Tasks
                </a>
              </Link>
              <Link href="/tasks/create" legacyBehavior>
                <a className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100">
                  Create Task
                </a>
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main>
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500">
            © {new Date().getFullYear()} Enhanced Todo Application. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default MainLayout;