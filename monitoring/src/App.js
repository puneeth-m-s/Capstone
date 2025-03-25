import React from "react";
import "./App.css"

const Dashboard = () => {
  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Sidebar */}
      <div className="w-1/6 bg-gray-800 p-4">
        <h1 className="text-xl font-bold mb-6">Analyzer</h1>
        <ul>
          <li className="bg-green-600 p-2 rounded mb-2">Dashboard</li>
          <li className="p-2 rounded hover:bg-gray-700">Settings</li>
          <li className="p-2 rounded hover:bg-gray-700">History</li>
        </ul>
      </div>
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Navbar */}
        <div className="flex justify-between bg-gray-800 p-4">
          <div className="flex space-x-4">
            <span className="text-green-400">Dashboard</span>
            <span className="text-gray-400">Settings</span>
            <span className="text-gray-400">Trends</span>
          </div>
        </div>

        {/* Metrics Section */}
        <div className="p-4 grid grid-cols-3 gap-4">
          <div className="bg-gray-700 p-4 rounded text-center">
            <h2 className="text-lg">CPU Usage</h2>
            <p className="text-xl font-bold">45%</p>
          </div>
          <div className="bg-gray-700 p-4 rounded text-center">
            <h2 className="text-lg">GPU Usage</h2>
            <p className="text-xl font-bold">60%</p>
          </div>
          <div className="bg-gray-700 p-4 rounded text-center">
            <h2 className="text-lg">Temperature</h2>
            <p className="text-xl font-bold text-red-500">65°C</p>
          </div>
        </div>

        {/* Graphs Section */}
        <div className="p-4 grid grid-cols-2 gap-4">
          <div className="bg-gray-700 p-10 rounded">Performance Trends</div>
          <div className="bg-gray-700 p-10 rounded">Power Usage</div>
        </div>
        
        {/* Footer */}
        <div className="text-center text-gray-400 p-4 text-sm border-t border-gray-700">
          System Info: Windows 11 | Intel i7 | Version 1.0
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
