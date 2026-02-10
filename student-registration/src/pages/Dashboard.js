import React from 'react';
import StudentList from '../components/StudentList';

/**
 * Dashboard Page
 * 
 * Main page displaying the student list and dashboard statistics.
 * Features:
 * - Student statistics
 * - Quick action buttons
 * - Full StudentList component
 * 
 * @component
 * @returns {JSX.Element} The Dashboard page
 */
export const Dashboard = () => {
  return (
    <div>
      <StudentList />
    </div>
  );
};

export default Dashboard;
