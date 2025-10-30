"""
Simple test script to verify the API is working
Run this after starting the Flask server
"""
import requests
import json
from sample_data import SUBJECT_HOME, PHOTOS, VIDEO_TRANSCRIPT, COMPARABLE_SALES

API_BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("\n🏥 Testing health check endpoint...")
    response = requests.get(f"{API_BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_analyze_home():
    """Test full home analysis endpoint"""
    print("\n🏠 Testing full home analysis...")
    
    payload = {
        "subject_home": SUBJECT_HOME,
        "photos": PHOTOS,
        "video_transcript": VIDEO_TRANSCRIPT,
        "comparable_sales": COMPARABLE_SALES
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/analyze-home",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success!")
        print(f"\nRecommended Price: ${data['price_recommendation']['recommended_price']:,}")
        print(f"Confidence: {data['price_recommendation']['confidence']}")
        print(f"Condition: {data['condition_summary']['overall_condition']}")
        print(f"Number of Comparables: {len(data['top_comparables'])}")
        
        # Save full response to file
        with open('test_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("\n💾 Full response saved to test_response.json")
        
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_analyze_condition():
    """Test condition analysis endpoint"""
    print("\n🔍 Testing condition analysis...")
    
    payload = {
        "subject_home": SUBJECT_HOME,
        "photos": PHOTOS,
        "video_transcript": VIDEO_TRANSCRIPT
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/analyze-condition",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Condition: {data['condition_summary']['overall_condition']}")
        print(f"   Score: {data['condition_summary']['condition_score']}/100")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_select_comparables():
    """Test comparable selection endpoint"""
    print("\n📊 Testing comparable selection...")
    
    payload = {
        "subject_home": SUBJECT_HOME,
        "comparable_sales": COMPARABLE_SALES,
        "num_comps": 5
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/select-comparables",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Selected {len(data['comparables'])} comparables")
        for i, comp in enumerate(data['comparables'], 1):
            print(f"   {i}. {comp['address']} - Score: {comp['similarity_score']:.1f}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 API Test Suite")
    print("=" * 60)
    
    # Run all tests
    results = []
    
    try:
        results.append(("Health Check", test_health()))
        results.append(("Condition Analysis", test_analyze_condition()))
        results.append(("Comparable Selection", test_select_comparables()))
        results.append(("Full Home Analysis", test_analyze_home()))
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API server.")
        print("Make sure the Flask server is running on http://localhost:5000")
        exit(1)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:30} {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️ Some tests failed")
