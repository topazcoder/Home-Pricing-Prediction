import React, { useState } from 'react';
import './App.css';
import { PricingReport } from './types';
import { analyzHome } from './services/api';
import PricingReportView from './components/PricingReportView';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import RealDataReport from './components/RealDataReport';
import { sampleData } from './data/sampleData';

type ViewMode = 'sample' | 'real';

function App() {
  const [viewMode, setViewMode] = useState<ViewMode>('real');
  const [report, setReport] = useState<PricingReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await analyzHome(sampleData);
      setReport(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <h1>🏠 Home</h1>
          <p className="subtitle">AI-Powered Home Pricing Reports</p>
        </div>
        <div className="view-mode-tabs">
          <button 
            className={`tab-button ${viewMode === 'real' ? 'active' : ''}`}
            onClick={() => setViewMode('real')}
          >
            📁 Real Data Analysis
          </button>
          <button 
            className={`tab-button ${viewMode === 'sample' ? 'active' : ''}`}
            onClick={() => setViewMode('sample')}
          >
            🧪 Sample Data Demo
          </button>
        </div>
      </header>

      <main className="App-main">
        {viewMode === 'real' ? (
          <RealDataReport />
        ) : (
          <>
            {!report && !loading && (
              <div className="welcome-section">
                <div className="welcome-card">
                  <h2>Generate Automated Pricing Report</h2>
                  <p>
                    Our AI-powered system analyzes home characteristics, condition, and
                    comparable sales to generate accurate pricing recommendations in seconds.
                  </p>
                  <button 
                    className="analyze-button"
                    onClick={handleAnalyze}
                  >
                    Generate Sample Report
                  </button>
                  <div className="features">
                    <div className="feature">
                      <span className="feature-icon">🔍</span>
                      <span>Condition Analysis</span>
                    </div>
                    <div className="feature">
                      <span className="feature-icon">📊</span>
                      <span>Comparable Selection</span>
                    </div>
                    <div className="feature">
                      <span className="feature-icon">💰</span>
                      <span>Price Estimation</span>
                    </div>
                    <div className="feature">
                      <span className="feature-icon">📝</span>
                      <span>Justification Report</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {loading && <LoadingSpinner />}
            
            {error && <ErrorMessage message={error} onRetry={handleAnalyze} />}
            
            {report && !loading && (
              <>
                <div className="action-bar">
                  <button 
                    className="regenerate-button"
                    onClick={handleAnalyze}
                  >
                    🔄 Regenerate Report
                  </button>
                </div>
                <PricingReportView report={report} />
              </>
            )}
          </>
        )}
      </main>

      <footer className="App-footer">
        <p>© 2025 Home. Automated Home Pricing System.</p>
      </footer>
    </div>
  );
}

export default App;
