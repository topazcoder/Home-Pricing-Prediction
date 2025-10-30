import React from 'react';
import { PricingReport } from '../types';
import './ProfessionalReport.css';

interface ProfessionalReportProps {
  report: PricingReport;
}

const ProfessionalReport: React.FC<ProfessionalReportProps> = ({ report }) => {
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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const { subject_home, condition_summary, top_comparables, price_recommendation } = report;

  return (
    <div className="professional-report">
      {/* Header / Title Page */}
      <div className="report-page title-page">
        <div className="report-logo">
          <div className="logo-icon">🏠</div>
          <h1>Home AI</h1>
          <p className="logo-subtitle">Real Estate Pricing Analysis</p>
        </div>
        
        <div className="report-title">
          <h2>AUTOMATED VALUATION REPORT</h2>
          <div className="title-divider"></div>
        </div>

        <div className="subject-property-box">
          <h3>SUBJECT PROPERTY</h3>
          <p className="property-address-large">{subject_home.address}</p>
        </div>

        <div className="report-metadata">
          <div className="metadata-row">
            <span className="metadata-label">Report Date:</span>
            <span className="metadata-value">{formatDate(report.generated_at)}</span>
          </div>
          <div className="metadata-row">
            <span className="metadata-label">Report Type:</span>
            <span className="metadata-value">Automated Comparative Market Analysis</span>
          </div>
          <div className="metadata-row">
            <span className="metadata-label">Analysis Method:</span>
            <span className="metadata-value">K-Nearest Neighbors (KNN) Algorithm</span>
          </div>
          <div className="metadata-row">
            <span className="metadata-label">Confidence Level:</span>
            <span className="metadata-value">{price_recommendation.confidence}</span>
          </div>
        </div>
      </div>

      {/* Executive Summary Page */}
      <div className="report-page">
        <h2 className="page-title">EXECUTIVE SUMMARY</h2>
        
        <div className="summary-box highlighted">
          <div className="summary-header">
            <h3>ESTIMATED MARKET VALUE</h3>
          </div>
          <div className="price-display">
            <div className="main-price">{formatCurrency(price_recommendation.recommended_price)}</div>
            <div className="price-details">
              <span>{formatCurrency(price_recommendation.price_per_sqft)} per square foot</span>
            </div>
          </div>
          <div className="price-range-display">
            <div className="range-header">VALUE RANGE</div>
            <div className="range-values">
              <span className="range-low">
                <span className="range-label">Low</span>
                <span className="range-amount">{formatCurrency(price_recommendation.price_range.low)}</span>
              </span>
              <span className="range-divider">—</span>
              <span className="range-high">
                <span className="range-label">High</span>
                <span className="range-amount">{formatCurrency(price_recommendation.price_range.high)}</span>
              </span>
            </div>
          </div>
        </div>

        <div className="summary-box">
          <h3>PROPERTY CHARACTERISTICS</h3>
          <div className="characteristics-grid">
            <div className="char-item">
              <span className="char-label">Address</span>
              <span className="char-value">{subject_home.address}</span>
            </div>
            <div className="char-item">
              <span className="char-label">Living Area</span>
              <span className="char-value">{formatNumber(subject_home.square_footage)} sq ft</span>
            </div>
            <div className="char-item">
              <span className="char-label">Bedrooms</span>
              <span className="char-value">{subject_home.bedrooms}</span>
            </div>
            <div className="char-item">
              <span className="char-label">Bathrooms</span>
              <span className="char-value">{subject_home.bathrooms}</span>
            </div>
            <div className="char-item">
              <span className="char-label">Year Built</span>
              <span className="char-value">{subject_home.year_built}</span>
            </div>
            <div className="char-item">
              <span className="char-label">Lot Size</span>
              <span className="char-value">{formatNumber(subject_home.lot_size || 0)} sq ft</span>
            </div>
            {subject_home.pool && (
              <div className="char-item">
                <span className="char-label">Pool</span>
                <span className="char-value">Yes</span>
              </div>
            )}
            {subject_home.garage && (
              <div className="char-item">
                <span className="char-label">Garage</span>
                <span className="char-value">Yes</span>
              </div>
            )}
          </div>
        </div>

        <div className="summary-box">
          <h3>CONDITION ASSESSMENT</h3>
          <div className="condition-rating-bar">
            <div className="rating-labels">
              <span>Poor</span>
              <span>Fair</span>
              <span>Average</span>
              <span>Good</span>
              <span>Excellent</span>
            </div>
            <div className="rating-bar">
              <div 
                className="rating-fill" 
                style={{ width: `${condition_summary.condition_score}%` }}
              >
                <span className="rating-marker">{condition_summary.overall_condition}</span>
              </div>
            </div>
            <div className="rating-score">Score: {condition_summary.condition_score}/100</div>
          </div>
          <p className="condition-description">{condition_summary.summary}</p>
        </div>
      </div>

      {/* Comparable Sales Analysis Page */}
      <div className="report-page">
        <h2 className="page-title">COMPARABLE SALES ANALYSIS</h2>
        
        <p className="page-intro">
          The following {top_comparables.length} properties were selected using K-Nearest Neighbors (KNN) 
          algorithm based on location, size, features, and recent sale dates. These properties represent 
          the most similar properties to the subject.
        </p>

        <div className="comparables-table">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Address</th>
                <th>Sale Price</th>
                <th>Sqft</th>
                <th>$/Sqft</th>
                <th>Bed/Bath</th>
                <th>Year</th>
                <th>Pool</th>
                <th>Distance</th>
                <th>Match</th>
              </tr>
            </thead>
            <tbody>
              {top_comparables.map((comp, index) => (
                <tr key={index}>
                  <td className="comp-number">{index + 1}</td>
                  <td className="comp-address">{comp.address}</td>
                  <td className="comp-price">{formatCurrency(comp.sale_price)}</td>
                  <td>{formatNumber(comp.square_footage)}</td>
                  <td>{formatCurrency(comp.sale_price / comp.square_footage)}</td>
                  <td>{comp.bedrooms}/{comp.bathrooms}</td>
                  <td>{comp.year_built}</td>
                  <td>{comp.pool ? '✓' : '—'}</td>
                  <td>{comp.distance_miles?.toFixed(2)} mi</td>
                  <td className="match-score">{comp.similarity_score?.toFixed(0)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Detailed Comparable Cards */}
        <div className="comparables-detailed">
          {top_comparables.map((comp, index) => (
            <div key={index} className="comparable-detail-card">
              <div className="comparable-detail-header">
                <h4>Comparable #{index + 1}</h4>
                <div className="similarity-badge">{comp.similarity_score?.toFixed(0)}% Match</div>
              </div>
              
              <div className="comparable-detail-body">
                <div className="detail-section">
                  <h5>Property Information</h5>
                  <table className="detail-table">
                    <tbody>
                      <tr>
                        <td>Address:</td>
                        <td><strong>{comp.address}</strong></td>
                      </tr>
                      <tr>
                        <td>Sale Price:</td>
                        <td><strong>{formatCurrency(comp.sale_price)}</strong></td>
                      </tr>
                      <tr>
                        <td>Sale Date:</td>
                        <td>{comp.days_since_sale} days ago</td>
                      </tr>
                      <tr>
                        <td>Living Area:</td>
                        <td>{formatNumber(comp.square_footage)} sq ft</td>
                      </tr>
                      <tr>
                        <td>Price per Sq Ft:</td>
                        <td>{formatCurrency(comp.sale_price / comp.square_footage)}</td>
                      </tr>
                      <tr>
                        <td>Bedrooms:</td>
                        <td>{comp.bedrooms}</td>
                      </tr>
                      <tr>
                        <td>Bathrooms:</td>
                        <td>{comp.bathrooms}</td>
                      </tr>
                      <tr>
                        <td>Year Built:</td>
                        <td>{comp.year_built}</td>
                      </tr>
                      <tr>
                        <td>Pool:</td>
                        <td>{comp.pool ? 'Yes' : 'No'}</td>
                      </tr>
                      <tr>
                        <td>Distance from Subject:</td>
                        <td>
                          <strong>
                            {(comp.distance_miles || comp.score_breakdown?.distance_miles)?.toFixed(2)} miles
                          </strong>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                {comp.score_breakdown && (
                  <div className="detail-section">
                    <h5>Similarity Analysis</h5>
                    <div className="similarity-factors">
                      <div className="factor-item">
                        <span>📍 Geographic Distance:</span>
                        <span><strong>{(comp.distance_miles || comp.score_breakdown?.distance_miles)?.toFixed(2)} miles</strong></span>
                      </div>
                      <div className="factor-item">
                        <span>📐 Size Difference:</span>
                        <span>{Math.abs(comp.square_footage - subject_home.square_footage)} sq ft</span>
                      </div>
                      <div className="factor-item">
                        <span>📅 Age Difference:</span>
                        <span>{Math.abs(comp.year_built - subject_home.year_built)} years</span>
                      </div>
                      <div className="factor-item">
                        <span>� Pool Match:</span>
                        <span>{comp.score_breakdown?.has_pool_match ? 'Yes ✓' : 'No ✗'}</span>
                      </div>
                      <div className="factor-item">
                        <span>�🎯 KNN Distance Score:</span>
                        <span>{comp.knn_distance?.toFixed(4)}</span>
                      </div>
                    </div>
                  </div>
                )}

                {(comp.pool || comp.garage) && (
                  <div className="detail-section">
                    <h5>Features</h5>
                    <div className="feature-tags">
                      {comp.pool && <span className="feature-tag">🏊 Pool</span>}
                      {comp.garage && <span className="feature-tag">🚗 Garage</span>}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Valuation Methodology Page */}
      <div className="report-page">
        <h2 className="page-title">VALUATION METHODOLOGY</h2>
        
        <div className="methodology-box">
          <h3>Approach to Value</h3>
          <p>
            This automated valuation model employs a <strong>Sales Comparison Approach</strong> using 
            K-Nearest Neighbors (KNN) machine learning algorithm to identify and weight the most 
            comparable properties in the market.
          </p>
        </div>

        <div className="methodology-box">
          <h3>Data Sources</h3>
          <ul>
            <li>Multiple Listing Service (MLS) data</li>
            <li>Public records and tax assessor information</li>
            <li>Property inspection video analysis</li>
            <li>Recent comparable sales within market area</li>
          </ul>
        </div>

        <div className="methodology-box">
          <h3>Algorithm Details</h3>
          <p>
            The KNN algorithm evaluates properties based on eight key features:
          </p>
          <ul>
            <li><strong>Geographic Location</strong> (30%): Latitude and longitude coordinates</li>
            <li><strong>Living Area Size</strong> (20%): Square footage</li>
            <li><strong>Bedroom Count</strong> (12%): Number of bedrooms</li>
            <li><strong>Pool Amenity</strong> (10%): Private or community pool</li>
            <li><strong>Sale Recency</strong> (10%): Days since sale</li>
            <li><strong>Property Age</strong> (10%): Year built</li>
            <li><strong>Bathroom Count</strong> (8%): Number of bathrooms</li>
          </ul>
          <p>
            Each comparable is assigned a weighted distance score, with inverse distance weighting 
            applied to calculate the final price estimate.
          </p>
        </div>

        <div className="methodology-box">
          <h3>Adjustments Applied</h3>
          <table className="adjustments-table">
            <thead>
              <tr>
                <th>Adjustment Category</th>
                <th>Percentage</th>
                <th>Impact</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Base Price from Comparables</td>
                <td>—</td>
                <td>{formatCurrency(price_recommendation.base_price)}</td>
              </tr>
              <tr>
                <td>Condition Adjustment</td>
                <td>{price_recommendation.adjustments.condition_adjustment > 0 ? '+' : ''}
                    {price_recommendation.adjustments.condition_adjustment}%</td>
                <td>{formatCurrency(price_recommendation.base_price * price_recommendation.adjustments.condition_adjustment / 100)}</td>
              </tr>
              {Object.entries(price_recommendation.adjustments.feature_adjustments).map(([feature, pct]) => (
                <tr key={feature}>
                  <td>{feature.charAt(0).toUpperCase() + feature.slice(1)} Adjustment</td>
                  <td>{pct > 0 ? '+' : ''}{pct}%</td>
                  <td>{formatCurrency(price_recommendation.base_price * (pct as number) / 100)}</td>
                </tr>
              ))}
              <tr className="total-row">
                <td><strong>Total Adjusted Value</strong></td>
                <td><strong>{price_recommendation.total_adjustment_pct > 0 ? '+' : ''}
                    {price_recommendation.total_adjustment_pct}%</strong></td>
                <td><strong>{formatCurrency(price_recommendation.recommended_price)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="methodology-box">
          <h3>Confidence Assessment</h3>
          <div className="confidence-explanation">
            <div className="confidence-level-box">
              <span className="confidence-label">Confidence Level:</span>
              <span className={`confidence-value ${price_recommendation.confidence.toLowerCase()}`}>
                {price_recommendation.confidence}
              </span>
            </div>
            <p>
              {price_recommendation.confidence === 'High' && 
                'Multiple highly comparable properties with recent sales data provide strong support for this valuation.'}
              {price_recommendation.confidence === 'Medium' && 
                'Adequate comparable properties available, though some adjustments were necessary for differences in features or condition.'}
              {price_recommendation.confidence === 'Low' && 
                'Limited comparable properties or significant differences require caution. Additional market research recommended.'}
            </p>
          </div>
        </div>
      </div>

      {/* Property Condition Page */}
      <div className="report-page">
        <h2 className="page-title">PROPERTY CONDITION ASSESSMENT</h2>
        
        <div className="condition-detail-box">
          <div className="condition-header-row">
            <div className="condition-rating-large">
              <div className="rating-number">{condition_summary.condition_score}</div>
              <div className="rating-max">/100</div>
            </div>
            <div className="condition-grade">
              <div className="grade-label">Overall Rating</div>
              <div className="grade-value">{condition_summary.overall_condition}</div>
            </div>
          </div>

          <div className="condition-summary-text">
            <h3>Summary</h3>
            <p>{condition_summary.summary}</p>
          </div>
        </div>

        {condition_summary.highlights && condition_summary.highlights.length > 0 && (
          <div className="condition-detail-box">
            <h3>✨ Positive Features</h3>
            <ul className="condition-list highlights">
              {condition_summary.highlights.map((highlight, index) => (
                <li key={index}>{highlight}</li>
              ))}
            </ul>
          </div>
        )}

        {condition_summary.concerns && condition_summary.concerns.length > 0 && (
          <div className="condition-detail-box">
            <h3>⚠️ Areas Requiring Attention</h3>
            <ul className="condition-list concerns">
              {condition_summary.concerns.map((concern, index) => (
                <li key={index}>{concern}</li>
              ))}
            </ul>
          </div>
        )}

        {report.video_analysis && (
          <div className="condition-detail-box">
            <h3>📹 Video Inspection Analysis</h3>
            <p className="video-analysis-text">{report.video_analysis}</p>
          </div>
        )}
      </div>

      {/* Justification Page */}
      <div className="report-page">
        <h2 className="page-title">PRICING JUSTIFICATION</h2>
        
        <div className="justification-content">
          {report.justification.split('\n\n').map((paragraph, index) => {
            if (paragraph.startsWith('**')) {
              const heading = paragraph.replace(/\*\*/g, '');
              return <h3 key={index} className="justification-subheading">{heading}</h3>;
            }
            if (paragraph.includes('\n-') || paragraph.includes('\n  -')) {
              const parts = paragraph.split('\n');
              const text = parts[0];
              const items = parts.slice(1).filter(p => p.trim().startsWith('-'));
              return (
                <div key={index} className="justification-section">
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

      {/* Footer / Disclaimer Page */}
      <div className="report-page footer-page">
        <h2 className="page-title">LIMITING CONDITIONS & DISCLAIMERS</h2>
        
        <div className="disclaimer-box">
          <h3>Report Purpose</h3>
          <p>
            This Automated Valuation Report is provided for informational purposes to assist in 
            determining a market-competitive listing price. This report should not be used as a 
            substitute for a formal appraisal.
          </p>
        </div>

        <div className="disclaimer-box">
          <h3>Limitations</h3>
          <ul>
            <li>No physical inspection of the property interior was conducted by a licensed appraiser</li>
            <li>Valuation is based on algorithmic analysis of comparable sales data</li>
            <li>Market conditions may change rapidly, affecting property values</li>
            <li>Actual sale price may vary based on negotiation, marketing, and market timing</li>
            <li>Property-specific factors may not be fully captured by automated analysis</li>
          </ul>
        </div>

        <div className="disclaimer-box">
          <h3>Data Sources & Currency</h3>
          <p>
            Comparable sales data sourced from public records and MLS databases. Every effort has 
            been made to ensure accuracy, but data completeness and currency cannot be guaranteed.
          </p>
        </div>

        <div className="disclaimer-box">
          <h3>Recommended Actions</h3>
          <ul>
            <li>Consult with a licensed real estate professional for market-specific insights</li>
            <li>Consider obtaining a formal appraisal for lending or legal purposes</li>
            <li>Review current market conditions and recent comparable sales</li>
            <li>Adjust pricing strategy based on property-specific factors and selling timeline</li>
          </ul>
        </div>

        <div className="report-signature">
          <div className="signature-line">
            <span>Generated by</span>
            <strong>Home AI Automated Valuation System</strong>
          </div>
          <div className="signature-line">
            <span>Report Date</span>
            <strong>{formatDate(report.generated_at)}</strong>
          </div>
          <div className="signature-line">
            <span>Report ID</span>
            <strong>{`AVM-${Date.parse(report.generated_at).toString(36).toUpperCase()}`}</strong>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfessionalReport;
