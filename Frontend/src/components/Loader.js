import React from 'react';
import './Loader.css'; // Import the CSS file for styling

const Loader = () => {
  return (
    <div className="loader-overlay">
      <div className="loader-content">
        <h1 className="loader-text">Auto Doc AI</h1>
      </div>
    </div>
  );
};

export default Loader;
