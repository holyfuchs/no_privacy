import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import axios from 'axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [timeSeriesData, setTimeSeriesData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/time-series');
        setTimeSeriesData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  if (!timeSeriesData) {
    return <div>Loading...</div>;
  }

  const chartData = {
    labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
    datasets: [
      {
        label: 'Transaction Count',
        data: timeSeriesData.counts,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `Transaction Activity by Hour (${timeSeriesData.timezone})`,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Number of Transactions'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Hour of Day'
        }
      }
    }
  };

  return (
    <div style={{ 
      maxWidth: '1000px', 
      margin: '40px auto', 
      padding: '20px',
      backgroundColor: 'white',
      borderRadius: '10px',
      boxShadow: '0 0 10px rgba(0,0,0,0.1)'
    }}>
      <Line data={chartData} options={options} />
    </div>
  );
}

export default App;