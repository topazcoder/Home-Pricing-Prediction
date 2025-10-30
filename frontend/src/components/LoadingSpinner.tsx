import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <h2>Analyzing Home & Generating Report...</h2>
      <p>This may take a few moments</p>
      <div className="loading-steps">
        <div className="step">✓ Analyzing condition from photos and video</div>
        <div className="step">✓ Selecting comparable properties</div>
        <div className="step">✓ Calculating price recommendation</div>
        <div className="step">⏳ Generating justification report</div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
