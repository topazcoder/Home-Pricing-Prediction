from typing import List, Dict, Any
import statistics
import numpy as np


class PriceEstimator:
    """
    KNN-based Price Estimator for Real Estate Valuation
    
    Uses K-Nearest Neighbors regression to estimate property prices.
    The price is calculated as a weighted average of the K most similar properties,
    where weights are inversely proportional to their KNN distances.
    
    Applies additional adjustments for:
    - Property condition
    - Key features (pool, garage, age)
    """
    
    def estimate_price(
        self,
        subject_home: Dict[str, Any],
        comparables: List[Dict[str, Any]],
        condition_summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate price recommendation with confidence intervals
        
        Returns:
        {
            'recommended_price': int,
            'price_range': {'low': int, 'high': int},
            'confidence': 'High/Medium/Low',
            'price_per_sqft': float,
            'adjustments': {...},
            'methodology': str
        }
        """
        
        if not comparables:
            raise ValueError("No comparables provided for price estimation")
        
        # Calculate base price from comparables
        base_price = self._calculate_base_price(subject_home, comparables)
        
        # Apply condition adjustments
        condition_adjustment = self._calculate_condition_adjustment(condition_summary)
        
        # Apply feature adjustments
        feature_adjustments = self._calculate_feature_adjustments(subject_home, comparables)
        
        # Calculate final price
        total_adjustment = condition_adjustment + sum(feature_adjustments.values())
        recommended_price = int(base_price * (1 + total_adjustment))
        
        # Calculate price range (confidence interval)
        price_range = self._calculate_price_range(recommended_price, comparables)
        
        # Determine confidence level
        confidence = self._determine_confidence(comparables, condition_summary)
        
        # Calculate price per sqft
        sqft = subject_home.get('sqft', subject_home.get('square_footage', 1))
        price_per_sqft = recommended_price / sqft if sqft > 0 else 0
        
        return {
            'recommended_price': recommended_price,
            'price_range': price_range,
            'confidence': confidence,
            'price_per_sqft': round(price_per_sqft, 2),
            'base_price': int(base_price),
            'total_adjustment_pct': round(total_adjustment * 100, 2),
            'adjustments': {
                'condition_adjustment': round(condition_adjustment * 100, 2),
                'feature_adjustments': {k: round(v * 100, 2) for k, v in feature_adjustments.items()}
            },
            'methodology': self._get_methodology_description(comparables)
        }
    
    def _calculate_base_price(self, subject_home: Dict[str, Any], comparables: List[Dict[str, Any]]) -> float:
        """
        Calculate base price using KNN-weighted regression.
        
        This is the core KNN regression algorithm for price estimation:
        1. Extract sale prices and KNN distances from the K nearest neighbors
        2. Calculate weights inversely proportional to distance (closer = higher weight)
        3. Adjust comparable prices for square footage differences
        4. Return weighted average price
        
        Formula: 
            predicted_price = Σ(weight_i * adjusted_price_i) / Σ(weight_i)
            where weight_i = 1 / (1 + knn_distance_i)
        """
        if not comparables:
            return 0
        
        subject_sqft = subject_home.get('sqft', subject_home.get('square_footage', 1))
        if subject_sqft == 0:
            subject_sqft = 1
        
        prices = []
        knn_weights = []
        
        for comp in comparables:
            comp_sqft = comp.get('sqft', comp.get('square_footage', 1))
            comp_price = comp.get('sale_price', 0)
            knn_distance = comp.get('knn_distance', 1.0)
            
            if comp_sqft > 0 and comp_price > 0:
                # Adjust comp price for sqft difference
                price_per_sqft = comp_price / comp_sqft
                adjusted_price = price_per_sqft * subject_sqft
                prices.append(adjusted_price)
                
                # KNN Weight: Inverse distance weighting
                # Closer neighbors (lower distance) get higher weight
                # Add 1 to distance to avoid division by zero
                weight = 1.0 / (1.0 + knn_distance)
                knn_weights.append(weight)
        
        if not prices:
            # Fallback: use unadjusted prices
            prices = [c.get('sale_price', 0) for c in comparables if c.get('sale_price', 0) > 0]
            if not prices:
                return 0
            return statistics.mean(prices)
        
        # KNN Regression: Weighted average
        total_weight = sum(knn_weights)
        if total_weight == 0:
            return statistics.mean(prices)
        
        knn_predicted_price = sum(p * w for p, w in zip(prices, knn_weights)) / total_weight
        
        return knn_predicted_price
    
    def _calculate_condition_adjustment(self, condition_summary: Dict[str, Any]) -> float:
        """
        Calculate price adjustment based on condition
        Returns adjustment as decimal (e.g., 0.05 = 5% increase)
        """
        condition = condition_summary.get('overall_condition', 'Fair')
        condition_score = condition_summary.get('condition_score', 70)
        
        # Base adjustments by condition
        condition_adjustments = {
            'Excellent': 0.08,  # +8%
            'Good': 0.03,       # +3%
            'Fair': 0.00,       # baseline
            'Poor': -0.10       # -10%
        }
        
        base_adjustment = condition_adjustments.get(condition, 0.0)
        
        # Fine-tune based on condition score
        # Every 10 points above/below 70 (Fair baseline) adds/subtracts 1%
        score_adjustment = (condition_score - 70) / 1000
        
        return base_adjustment + score_adjustment
    
    def _calculate_feature_adjustments(
        self,
        subject_home: Dict[str, Any],
        comparables: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Calculate adjustments for specific features
        Returns dict of feature: adjustment pairs
        """
        adjustments = {}
        
        # Pool adjustment
        subject_has_pool = subject_home.get('pool', False)
        comp_pool_avg = sum(1 for c in comparables if c.get('pool', False)) / len(comparables)
        
        if subject_has_pool and comp_pool_avg < 0.5:
            adjustments['pool'] = 0.03  # +3% for having pool when comps don't
        elif not subject_has_pool and comp_pool_avg > 0.5:
            adjustments['pool'] = -0.03  # -3% for not having pool when comps do
        
        # Garage adjustment
        subject_has_garage = subject_home.get('garage', False)
        comp_garage_avg = sum(1 for c in comparables if c.get('garage', False)) / len(comparables)
        
        if subject_has_garage and comp_garage_avg < 0.5:
            adjustments['garage'] = 0.02  # +2%
        elif not subject_has_garage and comp_garage_avg > 0.5:
            adjustments['garage'] = -0.02  # -2%
        
        # Age adjustment (newer homes command premium)
        subject_age = 2025 - subject_home.get('year_built', 2000)
        avg_comp_age = statistics.mean([2025 - c.get('year_built', 2000) for c in comparables])
        age_diff = avg_comp_age - subject_age
        
        # 1% adjustment per 10 years difference (up to +/-5%)
        age_adjustment = min(0.05, max(-0.05, age_diff / 10 * 0.01))
        if abs(age_adjustment) > 0.005:  # Only include if meaningful
            adjustments['age'] = age_adjustment
        
        return adjustments
    
    def _calculate_price_range(self, recommended_price: int, comparables: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate confidence interval for price recommendation"""
        
        # Calculate standard deviation of comparable prices
        comp_prices = [c.get('sale_price', 0) for c in comparables]
        
        if len(comp_prices) > 1:
            std_dev = statistics.stdev(comp_prices)
            
            # Use coefficient of variation to determine range width
            mean_price = statistics.mean(comp_prices)
            cv = std_dev / mean_price if mean_price > 0 else 0.1
            
            # Range is +/- 5-15% based on price variation
            range_pct = min(0.15, max(0.05, cv))
        else:
            range_pct = 0.10  # Default to +/- 10%
        
        return {
            'low': int(recommended_price * (1 - range_pct)),
            'high': int(recommended_price * (1 + range_pct))
        }
    
    def _determine_confidence(self, comparables: List[Dict[str, Any]], condition_summary: Dict[str, Any]) -> str:
        """Determine confidence level in price estimate"""
        
        # Check number of comparables
        if len(comparables) < 3:
            return 'Low'
        
        # Check similarity scores
        avg_similarity = statistics.mean([c.get('similarity_score', 0) for c in comparables])
        
        if avg_similarity >= 75:
            confidence = 'High'
        elif avg_similarity >= 60:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        # Adjust based on condition certainty
        if condition_summary.get('concerns', []):
            if confidence == 'High':
                confidence = 'Medium'
            elif confidence == 'Medium':
                confidence = 'Low'
        
        return confidence
    
    def _get_methodology_description(self, comparables: List[Dict[str, Any]]) -> str:
        """Generate description of pricing methodology"""
        avg_knn_distance = statistics.mean([c.get('knn_distance', 0) for c in comparables])
        return (
            f"Price estimated using K-Nearest Neighbors (KNN) regression with K={len(comparables)} "
            f"comparable properties. KNN algorithm selected the most similar properties based on "
            f"geographic location, size, bed/bath configuration, age, and sale recency. "
            f"Weighted average of sale prices using inverse distance weighting (avg distance: {avg_knn_distance:.4f}). "
            f"Additional adjustments applied for property condition and key features."
        )
