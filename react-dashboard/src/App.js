import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, ReferenceLine } from 'recharts';

function App() {
    const [data, setData] = useState([]);
    const [changePoint, setChangePoint] = useState(null);

    useEffect(() => {
        axios.get('http://localhost:5000/api/prices')
            .then(res => setData(res.data))
            .catch(err => console.error(err));
        axios.get('http://localhost:5000/api/change_point')
            .then(res => setChangePoint(res.data))
            .catch(err => console.error(err));
    }, []);

    return (
        <div style={{ padding: 20 }}>
            <h1>Brent Oil Dashboard (React)</h1>
            {changePoint && (
                <p>Change Point: {changePoint.date} | Impact: {changePoint.impact}%</p>
            )}
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={data}>
                    <XAxis dataKey="Date" />
                    <YAxis />
                    <Tooltip />
                    <CartesianGrid strokeDasharray="3 3" />
                    <Line type="monotone" dataKey="Price" stroke="#8884d8" />
                    {changePoint && (
                        <ReferenceLine x={changePoint.date} stroke="red" label="Change Point" />
                    )}
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}

export default App;