import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiHome, FiPlus, FiList } from 'react-icons/fi';
import { ROUTES, NAVIGATION_ITEMS } from '../routes';

/**
 * Navigation Component
 * 
 * Application navigation bar with links to main sections.
 * Phase 4: Enhanced with centralized route configuration
 * 
 * Features:
 * - Logo and branding
 * - Dynamic navigation links from NAVIGATION_ITEMS config
 * - Active route highlighting
 * - Responsive design
 * - Icon support for menu items
 * 
 * @component
 * @returns {JSX.Element} The Navigation component
 */
export const Navigation = () => {
  const location = useLocation();

  /**
   * Check if a route is currently active
   */
  const isActive = (path) => location.pathname === path;

  /**
   * Get CSS classes for nav link based on active state
   */
  const getLinkClasses = (path) => {
    const baseClasses = 'flex items-center gap-2 px-4 py-2 rounded-lg transition duration-200';
    return isActive(path)
      ? `${baseClasses} bg-blue-600 text-white font-semibold`
      : `${baseClasses} text-gray-700 hover:bg-blue-50 font-medium`;
  };

  /**
   * Get icon component based on icon name
   */
  const getIcon = (iconName) => {
    const iconMap = {
      FiHome: <FiHome size={18} />,
      FiPlus: <FiPlus size={18} />,
    };
    return iconMap[iconName] || null;
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-700 shadow-lg sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Brand */}
          <div className="flex items-center">
            <Link
              to={ROUTES.DASHBOARD}
              className="text-white font-bold text-xl flex items-center gap-2 hover:opacity-90 transition"
              title="Go to Dashboard"
            >
              <div className="bg-white bg-opacity-20 p-2 rounded-lg">
                <FiList size={24} />
              </div>
              <span className="hidden sm:inline">Student Portal</span>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="flex gap-2 sm:gap-4">
            {NAVIGATION_ITEMS.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={getLinkClasses(item.path)}
                title={item.description}
              >
                {getIcon(item.icon)}
                <span className="hidden sm:inline">{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
