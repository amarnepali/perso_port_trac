// import logo from './logo.svg';
import './App.css';
import React from 'react';
import SideBar from '../../frontend_react/src/components/Sidebar';
import NavBar from '../../frontend_react/src/components/Navbar';

// import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Reports from './pages/Reports';
import Settings from './pages/Settings';

// import Home from './components/Home';






function App() {
  return (
    // <Router>
    <div className="app">
      <SideBar />

      <div className="main-content">
        <NavBar />
        <div className="content">
          {/* <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/settings" element={<Settings />} />
            </Routes> */}
          <h1>Dashboard</h1>
          <p>This is a simple React application.</p>
          </div>

        </div>
    </div>
    // </Router>
  );
}

export default App;
