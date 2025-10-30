import React from 'react';
import { PricingReport } from '../types';
import './PricingReportView.css';

interface PricingReportViewProps {
  report: PricingReport;
}

const PricingReportView: React.FC<PricingReportViewProps> = ({ report }) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  const getConfidenceBadgeClass = (confidence: string) => {
    switch (confidence) {
      case 'High':
        return 'confidence-badge high';
      case 'Medium':
        return 'confidence-badge medium';
      case 'Low':
        return 'confidence-badge low';
      default:
        return 'confidence-badge';
    }
  };

  const { subject_home, condition_summary, top_comparables, price_recommendation } = report;

  return (
    <div className="pricing-report">
      {/* Header Summary */}
      <div className="report-header">
        <div className="header-left">
          <h1 className="property-address">{subject_home.address}</h1>
          <div className="property-details">
            <span>{subject_home.bedrooms} bed</span>
            <span className="separator">•</span>
            <span>{subject_home.bathrooms} bath</span>
            <span className="separator">•</span>
            <span>{formatNumber(subject_home.square_footage)} sq ft</span>
            <span className="separator">•</span>
            <span>Built {subject_home.year_built}</span>
          </div>
        </div>
      </div>

      {/* Price Recommendation */}
      <div className="price-section card">
        <div className="price-header">
          <h2>💰 Price Recommendation</h2>
          <div className={getConfidenceBadgeClass(price_recommendation.confidence)}>
            {price_recommendation.confidence} Confidence
          </div>
        </div>
        <div className="price-content">
          <div className="recommended-price">
            <div className="price-label">Recommended List Price</div>
            <div className="price-value">{formatCurrency(price_recommendation.recommended_price)}</div>
            <div className="price-per-sqft">
              {formatCurrency(price_recommendation.price_per_sqft)} per sq ft
            </div>
          </div>
          <div className="price-range">
            <div className="range-label">Expected Sale Range</div>
            <div className="range-bar">
              <div className="range-low">
                {formatCurrency(price_recommendation.price_range.low)}
              </div>
              <div className="range-indicator"></div>
              <div className="range-high">
                {formatCurrency(price_recommendation.price_range.high)}
              </div>
            </div>
          </div>
        </div>
        <div className="adjustment-summary">
          <div className="adjustment-item">
            <span>Base Price from Comps:</span>
            <span>{formatCurrency(price_recommendation.base_price)}</span>
          </div>
          <div className="adjustment-item">
            <span>Total Adjustments:</span>
            <span className={price_recommendation.total_adjustment_pct >= 0 ? 'positive' : 'negative'}>
              {price_recommendation.total_adjustment_pct > 0 ? '+' : ''}
              {price_recommendation.total_adjustment_pct.toFixed(1)}%
            </span>
          </div>
        </div>
      </div>

      {/* Condition Summary */}
      <div className="condition-section card">
        <h2>🏡 Property Condition Assessment</h2>
        <div className="condition-overview">
          <div className="condition-rating">
            <div className="rating-label">Overall Condition</div>
            <div className="rating-value">{condition_summary.overall_condition}</div>
            <div className="rating-score">Score: {condition_summary.condition_score}/100</div>
          </div>
          <div className="condition-bar">
            <div 
              className="condition-fill" 
              style={{ width: `${condition_summary.condition_score}%` }}
            ></div>
          </div>
        </div>
        <div className="condition-details">
          <p className="condition-summary-text">{condition_summary.summary}</p>
        </div>
        
        {condition_summary.highlights && condition_summary.highlights.length > 0 && (
          <div className="condition-list">
            <h3>✨ Highlights</h3>
            <ul>
              {condition_summary.highlights.map((highlight, index) => (
                <li key={index} className="highlight-item">{highlight}</li>
              ))}
            </ul>
          </div>
        )}
        
        {condition_summary.concerns && condition_summary.concerns.length > 0 && (
          <div className="condition-list">
            <h3>⚠️ Areas of Attention</h3>
            <ul>
              {condition_summary.concerns.map((concern, index) => (
                <li key={index} className="concern-item">{concern}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Comparable Properties */}
      <div className="comparables-section card">
        <h2>📊 Comparable Properties</h2>
        <p className="section-description">
          The following {top_comparables.length} properties were selected based on similarity to the subject property.
        </p>
        <div className="comparables-grid">
          {top_comparables.map((comp, index) => (
            <div key={index} className="comparable-card">
              <div className="comparable-header">
                <div className="comparable-number">#{index + 1}</div>
                <div className="similarity-score">
                  <div className="score-value">{comp.similarity_score?.toFixed(0)}</div>
                  <div className="score-label">Match Score</div>
                </div>
              </div>
              <div className="comparable-address">{comp.address}</div>
              <div className="comparable-price">{formatCurrency(comp.sale_price)}</div>
              <div className="comparable-details">
                <div className="detail-row">
                  <span className="detail-label">Size:</span>
                  <span>{formatNumber(comp.square_footage)} sq ft</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Beds/Baths:</span>
                  <span>{comp.bedrooms} / {comp.bathrooms}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Built:</span>
                  <span>{comp.year_built}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Distance:</span>
                  <span>{comp.score_breakdown?.distance_miles.toFixed(2)} mi</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Sold:</span>
                  <span>{comp.days_since_sale} days ago</span>
                </div>
              </div>
              <div className="comparable-features">
                {comp.pool && <span className="feature-tag">Pool</span>}
                {comp.garage && <span className="feature-tag">Garage</span>}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Justification */}
      <div className="justification-section card">
        <h2>📝 Pricing Justification</h2>
        <div className="justification-content">
          {report.justification.split('\n\n').map((paragraph, index) => {
            // Check if paragraph is a heading (starts with **)
            if (paragraph.startsWith('**')) {
              const heading = paragraph.replace(/\*\*/g, '');
              return <h3 key={index} className="justification-heading">{heading}</h3>;
            }
            // Check if it's a list item
            if (paragraph.includes('\n-') || paragraph.includes('\n  -')) {
              const parts = paragraph.split('\n');
              const text = parts[0];
              const items = parts.slice(1).filter(p => p.trim().startsWith('-'));
              return (
                <div key={index}>
                  {text && <p>{text}</p>}
                  <ul className="justification-list">
                    {items.map((item, i) => (
                      <li key={i}>{item.replace(/^-\s*/, '').trim()}</li>
                    ))}
                  </ul>
                </div>
              );
            }
            return <p key={index} className="justification-paragraph">{paragraph}</p>;
          })}
        </div>
      </div>

      {/* Metadata */}
      <div className="report-footer">
        <p className="report-meta">
          Report generated on {new Date(report.generated_at).toLocaleString()} by Home AI Pricing System
        </p>
      </div>
    </div>
  );
};

export default PricingReportView;
