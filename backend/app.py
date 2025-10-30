from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from typing import List, Dict, Any
import json
from datetime import datetime

from services.condition_analyzer import ConditionAnalyzer
from services.comparable_selector import ComparableSelector
from services.price_estimator import PriceEstimator
from services.justification_generator import JustificationGenerator
from utils.data_loader import load_real_data

app = Flask(__name__)
CORS(app)

# Initialize services
condition_analyzer = ConditionAnalyzer()
comparable_selector = ComparableSelector()
price_estimator = PriceEstimator()
justification_generator = JustificationGenerator()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/api/analyze-home', methods=['POST'])
def analyze_home():
    """
    Main endpoint to analyze a home and generate pricing report
    
    Expected input:
    {
        "subject_home": {...},
        "photos": [...],
        "video_transcript": "...",
        "comparable_sales": [...]
    }
    """
    try:
        data = request.get_json()
        
        subject_home = data.get('subject_home', {})
        photos = data.get('photos', [])
        video_transcript = data.get('video_transcript', '')
        comparable_sales = data.get('comparable_sales', [])
        
        # Step 1: Analyze home condition
        condition_summary = condition_analyzer.analyze(
            subject_home=subject_home,
            photos=photos,
            video_transcript=video_transcript
        )
        
        # Step 2: Select top 5 comparable homes
        top_comparables = comparable_selector.select_top_comparables(
            subject_home=subject_home,
            comparable_sales=comparable_sales,
            num_comps=5
        )
        
        # Step 3: Estimate price based on comparables
        price_recommendation = price_estimator.estimate_price(
            subject_home=subject_home,
            comparables=top_comparables,
            condition_summary=condition_summary
        )
        
        # Step 4: Generate justification
        justification = justification_generator.generate(
            subject_home=subject_home,
            comparables=top_comparables,
            price_recommendation=price_recommendation,
            condition_summary=condition_summary
        )
        
        # Compile response
        response = {
            'success': True,
            'subject_home': subject_home,
            'condition_summary': condition_summary,
            'top_comparables': top_comparables,
            'price_recommendation': price_recommendation,
            'justification': justification,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze-condition', methods=['POST'])
def analyze_condition():
    """Endpoint to analyze only home condition"""
    try:
        data = request.get_json()
        
        condition_summary = condition_analyzer.analyze(
            subject_home=data.get('subject_home', {}),
            photos=data.get('photos', []),
            video_transcript=data.get('video_transcript', '')
        )
        
        return jsonify({
            'success': True,
            'condition_summary': condition_summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/select-comparables', methods=['POST'])
def select_comparables():
    """Endpoint to select comparable homes"""
    try:
        data = request.get_json()
        
        top_comparables = comparable_selector.select_top_comparables(
            subject_home=data.get('subject_home', {}),
            comparable_sales=data.get('comparable_sales', []),
            num_comps=data.get('num_comps', 5)
        )
        
        return jsonify({
            'success': True,
            'comparables': top_comparables
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze-from-data', methods=['GET'])
def analyze_from_real_data():
    """
    Analyze the subject property using real data from the data directory.
    This endpoint automatically loads:
    - Subject property details from SUBJECT_PROPERTY_DETAILS.json
    - Video transcript from PRE_WALK_VIDEO_TRANSCRIPTION.json
    - Comparable properties from PHOENIX_SALES_RECORDS.json
    
    Returns a complete pricing report without requiring any input.
    """
    try:
        # Load all real data
        real_data = load_real_data()
        
        subject_home = real_data['subject_property']
        video_transcript = real_data['video_transcript']
        comparable_sales = real_data['comparable_properties']
        
        if not subject_home:
            return jsonify({'success': False, 'error': 'Subject property data not found'}), 400
        
        if not video_transcript:
            return jsonify({'success': False, 'error': 'Video transcript not found'}), 400
        
        if not comparable_sales:
            return jsonify({'success': False, 'error': 'No comparable properties found'}), 400
        
        # Step 1: Analyze home condition
        condition_summary = condition_analyzer.analyze(
            subject_home=subject_home,
            photos=[],  # Photos not provided in data files
            video_transcript=video_transcript
        )
        
        # Step 2: Select top 7 comparable homes
        top_comparables = comparable_selector.select_top_comparables(
            subject_home=subject_home,
            comparable_sales=comparable_sales,
            num_comps=7
        )
        
        # Step 3: Estimate price based on comparables
        price_recommendation = price_estimator.estimate_price(
            subject_home=subject_home,
            comparables=top_comparables,
            condition_summary=condition_summary
        )
        
        # Step 4: Generate justification
        justification = justification_generator.generate(
            subject_home=subject_home,
            comparables=top_comparables,
            price_recommendation=price_recommendation,
            condition_summary=condition_summary
        )
        
        # Compile response
        response = {
            'success': True,
            'subject_home': subject_home,
            'condition_summary': condition_summary,
            'top_comparables': top_comparables,
            'price_recommendation': price_recommendation,
            'justification': justification,
            'data_source': 'real_data_files',
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'type': type(e).__name__
        }), 500


@app.route('/api/data-summary', methods=['GET'])
def get_data_summary():
    """
    Get a summary of the available real data without running full analysis.
    Useful for debugging and understanding what data is loaded.
    """
    try:
        real_data = load_real_data()
        
        return jsonify({
            'success': True,
            'subject_property': {
                'address': real_data['subject_property'].get('address', 'N/A'),
                'bedrooms': real_data['subject_property'].get('bedrooms', 0),
                'bathrooms': real_data['subject_property'].get('bathrooms', 0),
                'sqft': real_data['subject_property'].get('sqft', 0),
                'year_built': real_data['subject_property'].get('year_built', 0),
            },
            'video_transcript': {
                'length': len(real_data['video_transcript']),
                'preview': real_data['video_transcript'][:200] + '...' if len(real_data['video_transcript']) > 200 else real_data['video_transcript']
            },
            'comparable_properties': {
                'count': len(real_data['comparable_properties']),
                'sample_addresses': [comp['address'] for comp in real_data['comparable_properties'][:5]]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'type': type(e).__name__
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
