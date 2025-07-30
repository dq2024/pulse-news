import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function TimeSeriesChart({ data }) {
  if (!data || data.length < 2) {
    return (
      <div style={{ 
        height: '300px', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        backgroundColor: '#f9f9f9',
        border: '1px solid #ddd',
        borderRadius: '8px'
      }}>
        <p>Need at least 2 data points to show chart (currently have {data?.length || 0})</p>
      </div>
    );
  }

  const labels = data.map(d => new Date(d.timestamp * 1000).toLocaleTimeString());
  const values = data.map(d => d.avg_sentiment);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Avg Sentiment',
        data: values,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
        pointRadius: 4,
        pointHoverRadius: 6
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false, // This allows us to control height
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Sentiment Over Time'
      }
    },
    scales: {
      y: {
        min: -1,
        max: 1,
        title: {
          display: true,
          text: 'Sentiment Score'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Time'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        }
      }
    }
  };

  return (
    <div style={{ height: '300px', width: '100%' }}>
      <Line data={chartData} options={options} />
    </div>
  );
}