// src/App.jsx
import React, { useState, useEffect } from 'react';
import { fetchResults, fetchStats } from './api';
import TimeSeriesChart from './components/TimeSeriesChart';
import TopList         from './components/TopList';

function App() {
  const [results, setResults]       = useState([]);
  const [stats, setStats]           = useState(null);
  const [statsHistory, setHistory]  = useState([]);
  const [error, setError]           = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [r, s] = await Promise.all([
          fetchResults(50),   // adjust as you like
          fetchStats(15)
        ]);

        setResults(r);
        setStats(s);

        // append new point to history
        setHistory(h => [
          ...h,
          { 
            timestamp: s.end_time_utc, 
            avg_sentiment: s.average_sentiment 
          }
        ]);
      } catch (e) {
        setError(e.message);
      }
    };

    load();
    const iv = setInterval(load, 30000); // every 30s
    return () => clearInterval(iv);
  }, []);

  if (error) {
    return <div style={{ padding: 20, color: 'red' }}>
      {error}
    </div>;
  }

  // split out top positives / negatives
  const positives = results.filter(i => i.label === 'POSITIVE');
  const negatives = results.filter(i => i.label === 'NEGATIVE');

  return (
    <div style={{ padding: 20 }}>
      <h1>Reddit Major News Sentiment Dashboard</h1>

      

    {statsHistory.length > 1 && (
    <section style={{ margin: '2rem 0' }}>
        <TimeSeriesChart data={statsHistory} />
    </section>
    )}


    {statsHistory.length <= 1 && (
    <p>Loading chart data… ({statsHistory.length}/2 points)</p>
    )}

{stats ? (
        <section>
          <h3>Stats (last {stats.window_minutes} min)</h3>
          <ul>
            <li>Average sentiment: {stats.average_sentiment.toFixed(2)}</li>
            <li>Positive: {stats.positive_count}</li>
            <li>Negative: {stats.negative_count}</li>
            <li>Total: {stats.total_count}</li>
          </ul>
        </section>
      ) : (
        <p>Loading stats…</p>
      )}

      {results.length > 0 && (
        <section style={{ display: 'flex', gap: '2rem' }}>
          <TopList title="Top Positive Posts" items={positives} />
          <TopList title="Top Negative Posts" items={negatives} />
        </section>
      )}
    </div>
  );
}



export default App;

