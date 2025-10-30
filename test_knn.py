"""
Test KNN implementation directly
"""
import sys
sys.path.insert(0, 'backend')

from services.comparable_selector import ComparableSelector
from services.price_estimator import PriceEstimator
from utils.data_loader import load_real_data

def test_knn():
    print("=" * 80)
    print("TESTING KNN ALGORITHM IMPLEMENTATION")
    print("=" * 80)
    print()
    
    # Load real data
    print("📁 Loading real data...")
    data = load_real_data()
    subject = data['subject_property']
    all_comps = data['comparable_properties']
    print(f"✅ Loaded subject property: {subject['address']}")
    print(f"✅ Loaded {len(all_comps)} comparable properties")
    print()
    
    # Select comparables using KNN
    print("🔍 Selecting top 5 comparables using KNN algorithm...")
    selector = ComparableSelector()
    top_comps = selector.select_top_comparables(subject, all_comps, num_comps=5)
    print(f"✅ Selected {len(top_comps)} comparables")
    print()
    
    # Display results
    print("=" * 80)
    print("TOP 5 MOST SIMILAR PROPERTIES (K-Nearest Neighbors)")
    print("=" * 80)
    print()
    
    for i, comp in enumerate(top_comps, 1):
        print(f"#{i} - {comp['address']}")
        print(f"   KNN Distance:    {comp.get('knn_distance', 'N/A'):.4f}")
        print(f"   Similarity Score: {comp.get('similarity_score', 'N/A'):.1f}%")
        print(f"   Sale Price:      ${comp['sale_price']:,.0f}")
        print(f"   Size:            {comp['sqft']:,.0f} sqft")
        print(f"   Bedrooms:        {comp['bedrooms']}")
        print(f"   Bathrooms:       {comp['bathrooms']}")
        print(f"   Year Built:      {comp['year_built']}")
        
        # Show feature breakdown if available
        if 'score_breakdown' in comp:
            breakdown = comp['score_breakdown']
            print(f"   Feature Contributions:")
            for feature, contribution in breakdown.items():
                if feature != 'total_score':
                    if isinstance(contribution, (int, float)):
                        print(f"      - {feature}: {contribution:.2f}%")
                    else:
                        print(f"      - {feature}: {contribution}")
        print()
    
    # Estimate price using KNN regression
    print("=" * 80)
    print("PRICE ESTIMATION (KNN Regression)")
    print("=" * 80)
    print()
    
    estimator = PriceEstimator()
    condition_summary = {
        'condition_score': 8.5,
        'issues': ['Minor wear on flooring'],
        'positive_features': ['Recently renovated kitchen', 'New HVAC system']
    }
    result = estimator.estimate_price(subject, top_comps, condition_summary)
    
    print(f"Subject Property: {subject['address']}")
    print(f"Size: {subject['sqft']:,.0f} sqft")
    print(f"Bedrooms: {subject['bedrooms']}")
    print(f"Bathrooms: {subject['bathrooms']}")
    print()
    
    print(f"💰 RECOMMENDED PRICE: ${result['recommended_price']:,.0f}")
    print(f"   Base Price (KNN):   ${result['base_price']:,.0f}")
    print(f"   Total Adjustment:   {result['total_adjustment_pct']}%")
    print(f"   Price per sqft:     ${result['price_per_sqft']:.2f}")
    print(f"   Confidence Level:   {result['confidence']}")
    print()
    
    if 'price_range' in result:
        print(f"📊 PRICE RANGE:")
        print(f"   Low:  ${result['price_range']['low']:,.0f}")
        print(f"   High: ${result['price_range']['high']:,.0f}")
        print()
    
    if 'adjustments' in result:
        print(f"📐 ADJUSTMENTS:")
        print(f"   Condition: {result['adjustments']['condition_adjustment']}%")
        print(f"   Features:")
        for feature, adj in result['adjustments']['feature_adjustments'].items():
            print(f"      - {feature}: {adj}%")
        print()
    
    print("✅ KNN Algorithm Test Complete!")
    print()
    print("=" * 80)
    print("METHODOLOGY:")
    print(result.get('methodology', 'N/A'))
    print("=" * 80)

if __name__ == '__main__':
    test_knn()
