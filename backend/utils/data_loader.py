"""
Data loader utility to read and parse JSON files from the data directory.
"""
import json
import os
from typing import Dict, List, Any

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')


def load_subject_property() -> Dict[str, Any]:
    """Load the subject property details from SUBJECT_PROPERTY_DETAILS.json"""
    file_path = os.path.join(DATA_DIR, 'SUBJECT_PROPERTY_DETAILS.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('property_details', {})
    except FileNotFoundError:
        print(f"Warning: {file_path} not found")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing {file_path}: {e}")
        return {}


def load_video_transcript() -> str:
    """Load the pre-walk video transcription from PRE_WALK_VIDEO_TRANSCRIPTION.json"""
    file_path = os.path.join(DATA_DIR, 'PRE_WALK_VIDEO_TRANSCRIPTION.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            transcript_result = data.get('transcribe_result', {})
            return transcript_result.get('transcript', '')
    except FileNotFoundError:
        print(f"Warning: {file_path} not found")
        return ''
    except json.JSONDecodeError as e:
        print(f"Error parsing {file_path}: {e}")
        return ''


def load_sales_records() -> List[Dict[str, Any]]:
    """Load Phoenix sales records from PHOENIX_SALES_RECORDS.json"""
    file_path = os.path.join(DATA_DIR, 'PHOENIX_SALES_RECORDS.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('listings', [])
    except FileNotFoundError:
        print(f"Warning: {file_path} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing {file_path}: {e}")
        return []


def normalize_subject_property(property_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize subject property data to match the expected format for the app.
    
    Args:
        property_data: Raw property details from SUBJECT_PROPERTY_DETAILS.json
        
    Returns:
        Normalized property data dictionary
    """
    address = property_data.get('property_address', {})
    
    return {
        'address': f"{address.get('street', '')}, {address.get('city', '')}, {address.get('state', '')} {address.get('zip', '')}".strip(),
        'bedrooms': property_data.get('bedrooms', 0),
        'bathrooms': property_data.get('full_bathrooms', 0),
        'sqft': property_data.get('sqft', 0),
        'year_built': property_data.get('year_built', 0),
        'lot_sqft': property_data.get('lot_sqft', 0),
        'garage_spaces': property_data.get('garage_spaces', 0),
        'has_pool': property_data.get('has_private_pool', False) or property_data.get('has_community_pool', False),
        'has_private_pool': property_data.get('has_private_pool', False),
        'has_community_pool': property_data.get('has_community_pool', False),
        'latitude': address.get('latitude', 0),
        'longitude': address.get('longitude', 0),
        'dwelling_type': property_data.get('dwelling_type', 'single_family'),
        'stories': property_data.get('exterior_stories', 1),
        'has_solar_panels': property_data.get('has_solar_panels', False),
    }


def normalize_comparable_property(listing: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a listing from sales records to match comparable property format.
    
    Args:
        listing: Raw listing data from PHOENIX_SALES_RECORDS.json
        
    Returns:
        Normalized comparable property dictionary
    """
    property_details = listing.get('property_details', {})
    address = property_details.get('property_address', {})
    
    # Parse sale price (stored in cents)
    list_price = listing.get('list_price', 0)
    sale_price = list_price / 100 if list_price else 0
    
    # Parse sale date
    sale_date = listing.get('sale_date', '')
    
    return {
        'address': f"{address.get('street', '')}, {address.get('city', '')}, {address.get('state', '')} {address.get('zip', '')}".strip(),
        'bedrooms': property_details.get('bedrooms', 0),
        'bathrooms': property_details.get('full_bathrooms', 0),
        'sqft': property_details.get('sqft', 0),
        'year_built': property_details.get('year_built', 0),
        'lot_sqft': property_details.get('lot_sqft', 0),
        'garage_spaces': property_details.get('garage_spaces', 0),
        'has_pool': property_details.get('has_private_pool', False),
        'sale_price': sale_price,
        'sale_date': sale_date,
        'latitude': address.get('latitude', 0),
        'longitude': address.get('longitude', 0),
        'days_on_market': 0,  # Not available in data
        'price_per_sqft': sale_price / property_details.get('sqft', 1) if property_details.get('sqft') else 0,
        'dwelling_type': property_details.get('dwelling_type', 'single_family'),
        'stories': property_details.get('exterior_stories', 1),
        'has_solar_panels': property_details.get('has_solar_panels', False),
    }


def get_all_comparable_properties() -> List[Dict[str, Any]]:
    """
    Load and normalize all sales records to use as comparable properties.
    
    Returns:
        List of normalized comparable properties
    """
    sales_records = load_sales_records()
    comparables = []
    
    for listing in sales_records:
        try:
            comparable = normalize_comparable_property(listing)
            # Only include properties with valid data
            if comparable['sqft'] > 0 and comparable['sale_price'] > 0:
                comparables.append(comparable)
        except Exception as e:
            print(f"Error normalizing listing: {e}")
            continue
    
    return comparables


def load_real_data() -> Dict[str, Any]:
    """
    Load all real data files and return in a structured format.
    
    Returns:
        Dictionary containing:
        - subject_property: Normalized subject property details
        - video_transcript: Pre-walk video transcript text
        - comparable_properties: List of normalized comparable properties
    """
    subject_property_raw = load_subject_property()
    subject_property = normalize_subject_property(subject_property_raw)
    
    video_transcript = load_video_transcript()
    
    comparable_properties = get_all_comparable_properties()
    
    return {
        'subject_property': subject_property,
        'video_transcript': video_transcript,
        'comparable_properties': comparable_properties,
        'raw_subject_property': subject_property_raw,  # Keep raw for reference
    }


# Test function
if __name__ == '__main__':
    print("Loading real data...")
    data = load_real_data()
    
    print(f"\n✓ Subject Property: {data['subject_property']['address']}")
    print(f"  - Bedrooms: {data['subject_property']['bedrooms']}")
    print(f"  - Bathrooms: {data['subject_property']['bathrooms']}")
    print(f"  - Sqft: {data['subject_property']['sqft']}")
    print(f"  - Year Built: {data['subject_property']['year_built']}")
    
    print(f"\n✓ Video Transcript: {len(data['video_transcript'])} characters")
    print(f"  Preview: {data['video_transcript'][:150]}...")
    
    print(f"\n✓ Comparable Properties: {len(data['comparable_properties'])} properties loaded")
    if data['comparable_properties']:
        sample = data['comparable_properties'][0]
        print(f"  Sample: {sample['address']}")
        print(f"  - Sale Price: ${sample['sale_price']:,.0f}")
        print(f"  - Sqft: {sample['sqft']}")
        print(f"  - Sale Date: {sample['sale_date']}")
