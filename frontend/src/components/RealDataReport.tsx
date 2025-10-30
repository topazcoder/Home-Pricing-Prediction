import React, { useState } from 'react';
import axios from 'axios';
import { PricingReport } from '../types';
import ProfessionalReport from './ProfessionalReport';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';
import './RealDataReport.css';

const API_BASE_URL = 'http://localhost:5000/api';

interface DataSummary {
  subject_property: {
    address: string;
    bedrooms: number;
    bathrooms: number;
    sqft: number;
    year_built: number;
  };
  video_transcript: {
    length: number;
    preview: string;
  };
  comparable_properties: {
    count: number;
    sample_addresses: string[];
  };
}

const RealDataReport: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [report, setReport] = useState<PricingReport | null>(null);
  const [dataSummary, setDataSummary] = useState<DataSummary | null>(null);
  const [showingSummary, setShowingSummary] = useState(false);

  const loadDataSummary = async () => {
    try {
      setLoading(true);
      setError(null);
      setShowingSummary(true);
      
      const response = await axios.get(`${API_BASE_URL}/data-summary`);
      
      if (response.data.success) {
        setDataSummary(response.data);
      } else {
        setError(response.data.error || 'Failed to load data summary');
      }
    } catch (err: any) {
      console.error('Error loading data summary:', err);
      setError(err.response?.data?.error || err.message || 'Failed to load data summary');
    } finally {
      setLoading(false);
    }
  };

  const analyzeRealData = async () => {
    try {
      setLoading(true);
      setError(null);
      setReport(null);
      setShowingSummary(false);
      
      const response = await axios.get(`${API_BASE_URL}/analyze-from-data`);
      
      if (response.data.success) {
        // Backend response already matches PricingReport type
        setReport(response.data as PricingReport);
      } else {
        setError(response.data.error || 'Failed to analyze property');
      }
    } catch (err: any) {
      console.error('Error analyzing property:', err);
      setError(err.response?.data?.error || err.message || 'Failed to analyze property');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setReport(null);
    setDataSummary(null);
    setShowingSummary(false);
    setError(null);
  };

  return (
    <div className="real-data-report">
      {!report && !showingSummary && (
        <div className="real-data-welcome">
          <div className="welcome-card">
            <div className="icon-large">🏠</div>
            <h1>Real Property Analysis</h1>
            <p className="subtitle">
              Analyze the subject property at <strong>18201 N 22nd Ave, Phoenix, AZ</strong> using real data
            </p>
            
            <div className="data-info">
              <div className="info-badge">
                <span className="badge-icon">📄</span>
                <span>Real Property Details</span>
              </div>
              <div className="info-badge">
                <span className="badge-icon">🎥</span>
                <span>Pre-Walk Video Transcript</span>
              </div>
              <div className="info-badge">
                <span className="badge-icon">📊</span>
                <span>147 Comparable Properties</span>
              </div>
            </div>

            <div className="button-group">
              <button 
                onClick={analyzeRealData} 
                className="btn btn-primary btn-large"
                disabled={loading}
              >
                {loading ? 'Analyzing...' : '🚀 Generate Pricing Report'}
              </button>
              
              <button 
                onClick={loadDataSummary} 
                className="btn btn-secondary"
                disabled={loading}
              >
                📋 Preview Data
              </button>
            </div>

            <div className="tech-note">
              <p>
                <strong>Data Source:</strong> This analysis uses actual data files from the <code>data/</code> directory
              </p>
            </div>
          </div>
        </div>
      )}

      {showingSummary && dataSummary && !report && (
        <div className="data-summary-view">
          <div className="summary-card">
            <h2>📊 Data Summary</h2>
            
            <div className="summary-section">
              <h3>🏠 Subject Property</h3>
              <div className="property-details">
                <p><strong>Address:</strong> {dataSummary.subject_property.address}</p>
                <div className="detail-grid">
                  <div className="detail-item">
                    <span className="detail-label">Bedrooms:</span>
                    <span className="detail-value">{dataSummary.subject_property.bedrooms}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Bathrooms:</span>
                    <span className="detail-value">{dataSummary.subject_property.bathrooms}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Sqft:</span>
                    <span className="detail-value">{dataSummary.subject_property.sqft.toLocaleString()}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Year Built:</span>
                    <span className="detail-value">{dataSummary.subject_property.year_built}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="summary-section">
              <h3>🎥 Video Transcript</h3>
              <p><strong>Length:</strong> {dataSummary.video_transcript.length.toLocaleString()} characters</p>
              <div className="transcript-preview">
                <p>{dataSummary.video_transcript.preview}</p>
              </div>
            </div>

            <div className="summary-section">
              <h3>📈 Comparable Properties</h3>
              <p><strong>Total Available:</strong> {dataSummary.comparable_properties.count} properties</p>
              <div className="sample-addresses">
                <p><strong>Sample Addresses:</strong></p>
                <ul>
                  {dataSummary.comparable_properties.sample_addresses.map((address, index) => (
                    <li key={index}>{address}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="button-group">
              <button 
                onClick={analyzeRealData} 
                className="btn btn-primary"
                disabled={loading}
              >
                🚀 Analyze This Property
              </button>
              <button 
                onClick={reset} 
                className="btn btn-secondary"
              >
                ← Back
              </button>
            </div>
          </div>
        </div>
      )}

      {loading && <LoadingSpinner />}
      
      {error && (
        <div className="error-container">
          <ErrorMessage message={error} />
          <button onClick={reset} className="btn btn-secondary">
            Try Again
          </button>
        </div>
      )}
      
      {report && !loading && (
        <div className="report-container">
          <div className="report-header">
            <button onClick={reset} className="btn btn-secondary back-btn">
              ← Analyze Another Property
            </button>
            <button onClick={() => window.print()} className="btn btn-primary">
              🖨️ Print Report
            </button>
          </div>
          <ProfessionalReport report={report} />
        </div>
      )}
    </div>
  );
};

export default RealDataReport;
