import React from 'react';
// import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

// const sampleData = [
//   { name: 'Jan', users: 400 },
//   { name: 'Feb', users: 300 },
//   { name: 'Mar', users: 500 },
//   { name: 'Apr', users: 200 },
// ];



function Dashboard() {
  return (
    <div>
      <h2>Dashboard Overview</h2>
      {/* <LineChart
        width={600}
        height={300}
        data={sampleData}
        margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
      > 
      <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="users" stroke="#8884d8" /> 
      </LineChart> */}
    </div>
  );
}

export default Dashboard;
