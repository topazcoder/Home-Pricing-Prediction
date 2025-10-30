# AI Home Pricing System

🏠 An AI-powered full-stack application for automating home pricing reports.

> **📚 New to the project?** Check out [INDEX.md](INDEX.md) for a complete documentation guide!  
> **⚡ Want to get started quickly?** See [QUICKSTART.md](QUICKSTART.md) for 5-minute setup!  
> **✨ Using real data files?** See [DATA_INTEGRATION.md](DATA_INTEGRATION.md) to learn how the `data/` folder is used!  
> **📋 Quick overview?** Check [SUMMARY.md](SUMMARY.md) for the TL;DR version!

## Overview

This system automates the generation of home pricing reports by:
- ✨ **Using Real Data**: Analyzes actual property at 18201 N 22nd Ave, Phoenix, AZ with 147 comparable sales
- Analyzing home condition from photos and video transcripts
- Selecting the most comparable recent sales using multi-factor algorithms
- Calculating data-driven price recommendations with confidence intervals
- Generating detailed justification reports with explainable AI

## Architecture

### Backend (Python Flask)
- **Condition Analyzer**: Analyzes property condition from photos, videos, and transcripts
- **Comparable Selector**: Uses multi-factor scoring to find most similar properties
- **Price Estimator**: Calculates price recommendations with confidence intervals
- **Justification Generator**: Creates human-readable explanations

### Frontend (React TypeScript)
- Modern, responsive UI built with React and TypeScript
- Professional pricing report view matching industry standards
- Real-time report generation with loading states
- Mobile-responsive design

## Features

✅ **Condition Analysis**
- Analyzes video transcripts for condition indicators
- Extracts highlights and areas of concern
- Generates condition scores (0-100)

✅ **Smart Comparable Selection**
- Multi-factor similarity scoring algorithm
- Considers distance, size, bed/bath, age, and sale recency
- Weights factors based on importance

✅ **Price Estimation**
- Weighted price calculation from comparables
- Condition-based adjustments
- Feature-based adjustments (pool, garage, etc.)
- Confidence levels (High/Medium/Low)

✅ **Detailed Justification**
- Executive summary
- Market analysis
- Condition assessment
- Comparable properties breakdown
- Adjustment explanations

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```powershell
cd backend
```

2. Create virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Run the server:
```powershell
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Start the development server:
```powershell
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Click "Generate Sample Report" to see the system in action
4. Review the comprehensive pricing report generated

## API Endpoints

### POST `/api/analyze-home`
Generate complete pricing report
```json
{
  "subject_home": {...},
  "photos": [...],
  "video_transcript": "...",
  "comparable_sales": [...]
}
```

### POST `/api/analyze-condition`
Analyze home condition only

### POST `/api/select-comparables`
Select comparable properties only

### GET `/api/health`
Health check endpoint

## Technology Stack

**Backend:**
- Flask - Web framework
- Python 3 - Core language
- Flask-CORS - Cross-origin requests

**Frontend:**
- React 18 - UI library
- TypeScript - Type safety
- Axios - HTTP client
- CSS3 - Styling

## Project Structure

```
ai-project/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── services/              # Business logic services
│   │   ├── condition_analyzer.py
│   │   ├── comparable_selector.py
│   │   ├── price_estimator.py
│   │   └── justification_generator.py
│   ├── requirements.txt       # Python dependencies
│   └── sample_data.py         # Sample data for testing
│
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/        # React components
    │   │   ├── PricingReportView.tsx
    │   │   ├── LoadingSpinner.tsx
    │   │   └── ErrorMessage.tsx
    │   ├── services/
    │   │   └── api.ts         # API client
    │   ├── data/
    │   │   └── sampleData.ts  # Sample data
    │   ├── types.ts           # TypeScript types
    │   ├── App.tsx            # Main app component
    │   └── index.tsx          # Entry point
    ├── package.json
    └── tsconfig.json
```

## Key Design Decisions

### 1. Multi-Factor Comparable Selection
Uses weighted scoring across 5 dimensions:
- Geographic proximity (30%)
- Square footage similarity (20%)
- Bed/bath match (15%)
- Age similarity (15%)
- Sale recency (20%)

### 2. Condition Scoring
Combines multiple signals:
- Property age
- Transcript sentiment analysis
- Keyword frequency analysis
- Explicit condition mentions

### 3. Price Adjustments
Applies data-driven adjustments for:
- Overall condition (±10%)
- Property features (pool, garage, etc.)
- Age relative to comparables
- Market positioning

### 4. Confidence Levels
Determined by:
- Number of comparables
- Average similarity score
- Condition assessment certainty

## Future Enhancements

🔮 **AI/ML Integration**
- GPT-4 Vision for photo analysis
- LLM-powered justification generation
- Sentiment analysis on transcripts
- Market trend prediction

🔮 **Data Sources**
- Real MLS integration
- Public records APIs
- Real-time market data
- Historical price trends

🔮 **Features**
- Multi-property comparison
- Market trend visualization
- Collaborative review workflow
- Export to PDF/Excel
- Email distribution

## Testing

Run backend tests:
```powershell
cd backend
python -m pytest
```

Run frontend tests:
```powershell
cd frontend
npm test
```
