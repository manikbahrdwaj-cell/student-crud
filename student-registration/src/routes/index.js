/**
 * Route Configuration
 * 
 * Centralized route definitions for the application.
 * Provides constants for all routes to maintain consistency.
 * 
 * @module routes
 */

export const ROUTES = {
  // Public routes
  DASHBOARD: '/dashboard',
  CREATE: '/create',
  EDIT: '/edit/:id',
  
  // Pages
  NOT_FOUND: '*',
  LOADING: '/loading',
  
  // Home/Index
  HOME: '/',
};

/**
 * Navigation items for the main menu
 * @type {Array<{label: string, path: string, icon: string, description: string}>}
 */
export const NAVIGATION_ITEMS = [
  {
    label: 'Dashboard',
    path: ROUTES.DASHBOARD,
    icon: 'FiHome',
    description: 'View all students',
  },
  {
    label: 'Add Student',
    path: ROUTES.CREATE,
    icon: 'FiPlus',
    description: 'Add a new student',
  },
];

/**
 * Route metadata for additional info
 * @type {Object}
 */
export const ROUTE_META = {
  [ROUTES.DASHBOARD]: {
    title: 'Dashboard',
    description: 'View and manage all students',
    publicRoute: true,
  },
  [ROUTES.CREATE]: {
    title: 'Create Student',
    description: 'Add a new student to the system',
    publicRoute: true,
  },
  [ROUTES.EDIT]: {
    title: 'Edit Student',
    description: 'Edit student information',
    publicRoute: true,
  },
};

/**
 * Get route title
 * @param {string} route - The route path
 * @returns {string} The title for the route
 */
export const getRouteTitle = (route) => {
  return ROUTE_META[route]?.title || 'Student Portal';
};

/**
 * Get route description
 * @param {string} route - The route path
 * @returns {string} The description for the route
 */
export const getRouteDescription = (route) => {
  return ROUTE_META[route]?.description || '';
};

/**
 * Check if route is public
 * @param {string} route - The route path
 * @returns {boolean} Whether the route is public
 */
export const isPublicRoute = (route) => {
  return ROUTE_META[route]?.publicRoute ?? true;
};

export default ROUTES;
