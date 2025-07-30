import React from 'react';

export default function TopList({ title, items }) {
  if (!items || items.length === 0) {
    return (
      <div style={{ width: '50%' }}>
        <h2 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem' }}>
          {title}
        </h2>
        <p>No items to display</p>
      </div>
    );
  }

  return (
    <div style={{ width: '50%' }}>
      <h2 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem' }}>
        {title}
      </h2>
      <ul style={{ listStyle: 'disc', paddingLeft: '1.25rem' }}>
        {items.slice(0, 5).map(item => (
          <li 
            key={item.id} 
            style={{ 
              display: 'flex', 
              justifyContent: 'space-between',
              marginBottom: '0.25rem'
            }}
          >
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              style={{ 
                flex: 1,
                color: '#2563eb',
                textDecoration: 'none'
              }}
            >
              {item.title}
            </a>
            <span 
              style={{ 
                marginLeft: '12px', 
                whiteSpace: 'nowrap',
                fontWeight: 'bold'
              }}
            >
              {(item.score * 100).toFixed(0)}%
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}