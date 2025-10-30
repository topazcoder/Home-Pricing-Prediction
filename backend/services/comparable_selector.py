from typing import List, Dict, Any
import math
import numpy as np


class ComparableSelector:
    """
    K-Nearest Neighbors (KNN) algorithm for selecting comparable properties.
    
    Uses KNN with weighted Euclidean distance to find the K most similar properties
    based on multiple features:
    - Geographic location (latitude, longitude)
    - Square footage
    - Number of bedrooms
    - Number of bathrooms
    - Year built
    - Sale recency
    
    Features are normalized to ensure fair weighting.
    """
    
    # Feature weights for KNN distance calculation
    FEATURE_WEIGHTS = {
        'latitude': 0.15,
        'longitude': 0.15,
        'sqft': 0.20,
        'bedrooms': 0.12,
        'bathrooms': 0.08,
        'year_built': 0.10,
        'days_since_sale': 0.10,
        'has_pool': 0.10
    }
    
    def select_top_comparables(
        self,
        subject_home: Dict[str, Any],
        comparable_sales: List[Dict[str, Any]],
        num_comps: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Select the K most similar properties using K-Nearest Neighbors algorithm.
        
        Args:
            subject_home: The property to find comparables for
            comparable_sales: List of potential comparable properties
            num_comps: K value - number of nearest neighbors to return (default: 5)
            
        Returns:
            List of K most similar properties with KNN distances and similarity scores
        """
        if not comparable_sales:
            return []
        
        # Extract features for subject property
        subject_features = self._extract_features(subject_home)
        
        # Extract features for all comparables
        comparable_features = [self._extract_features(comp) for comp in comparable_sales]
        
        # Calculate feature statistics for normalization
        feature_stats = self._calculate_feature_stats(comparable_features)
        
        # Normalize subject features
        subject_normalized = self._normalize_features(subject_features, feature_stats)
        
        # Calculate KNN distances to all comparables
        distances = []
        for i, comp_features in enumerate(comparable_features):
            comp_normalized = self._normalize_features(comp_features, feature_stats)
            distance = self._calculate_weighted_euclidean_distance(
                subject_normalized, 
                comp_normalized
            )
            distances.append((i, distance))
        
        # Sort by distance (lower distance = more similar)
        distances.sort(key=lambda x: x[1])
        
        # Select K nearest neighbors
        k_nearest = distances[:num_comps]
        
        # Build result with KNN distances and similarity scores
        result = []
        for idx, distance in k_nearest:
            comp = comparable_sales[idx].copy()
            
            # Convert distance to similarity score (0-100)
            # Lower distance = higher similarity
            similarity_score = self._distance_to_similarity(distance)
            
            # Calculate real geographic distance in miles using Haversine formula
            real_distance_miles = self._calculate_haversine_distance(
                subject_features['latitude'],
                subject_features['longitude'],
                comparable_features[idx]['latitude'],
                comparable_features[idx]['longitude']
            )
            
            comp['similarity_score'] = similarity_score
            comp['knn_distance'] = round(distance, 4)
            comp['distance_miles'] = round(real_distance_miles, 2)  # Add real distance
            comp['score_breakdown'] = self._get_score_breakdown(
                subject_home, 
                comp,
                subject_features,
                comparable_features[idx]
            )
            result.append(comp)
        
        return result
    
    def _extract_features(self, property_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract numerical features from property data for KNN algorithm.
        
        Returns:
            Dictionary of feature names to normalized values
        """
        # Get current year for age calculations
        from datetime import datetime
        current_year = datetime.now().year
        
        # Extract and convert features
        features = {
            'latitude': float(property_data.get('latitude', 0)),
            'longitude': float(property_data.get('longitude', 0)),
            'sqft': float(property_data.get('sqft', property_data.get('square_footage', 0))),
            'bedrooms': float(property_data.get('bedrooms', 0)),
            'bathrooms': float(property_data.get('bathrooms', 0)),
            'year_built': float(property_data.get('year_built', current_year)),
            'has_pool': float(1 if (property_data.get('has_private_pool') or property_data.get('has_community_pool')) else 0),
        }

        # Calculate days since sale (0 for subject property)
        days_since_sale = property_data.get('days_since_sale', 0)
        if days_since_sale == 0 and 'sale_date' in property_data:
            # Parse sale_date if available
            try:
                from dateutil import parser
                from datetime import datetime, timezone
                sale_date = parser.parse(property_data['sale_date'])
                sale_date = sale_date.replace(tzinfo=timezone.utc)
                days_since_sale = (datetime.now(timezone.utc) - sale_date).days
            except Exception as e:
                print(e)
                days_since_sale = 90  # Default to 90 days
        
        features['days_since_sale'] = float(days_since_sale)
        print(features)
        
        return features
    
    def _calculate_feature_stats(self, all_features: List[Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """
        Calculate mean and std deviation for each feature for normalization.
        
        Returns:
            Dictionary with 'mean' and 'std' for each feature
        """
        if not all_features:
            return {}
        
        feature_names = all_features[0].keys()
        stats = {}
        
        for feature in feature_names:
            values = [f[feature] for f in all_features if feature in f]
            if values:
                mean = np.mean(values)
                std = np.std(values)
                # Avoid division by zero
                if std == 0:
                    std = 1.0
                stats[feature] = {'mean': mean, 'std': std}
        
        return stats
    
    def _normalize_features(
        self, 
        features: Dict[str, float], 
        stats: Dict[str, Dict[str, float]]
    ) -> Dict[str, float]:
        """
        Normalize features using z-score normalization (standardization).
        
        Formula: (value - mean) / std
        
        This ensures all features are on the same scale for KNN distance calculation.
        """
        normalized = {}
        for feature, value in features.items():
            if feature in stats:
                mean = stats[feature]['mean']
                std = stats[feature]['std']
                normalized[feature] = (value - mean) / std
            else:
                normalized[feature] = value
        
        return normalized
    
    def _calculate_weighted_euclidean_distance(
        self, 
        features1: Dict[str, float], 
        features2: Dict[str, float]
    ) -> float:
        """
        Calculate weighted Euclidean distance between two feature vectors.
        
        Formula: sqrt(sum(weight_i * (feature1_i - feature2_i)^2))
        
        This is the core KNN distance metric.
        """
        distance_squared = 0.0
        
        for feature, value1 in features1.items():
            if feature in features2 and feature in self.FEATURE_WEIGHTS:
                value2 = features2[feature]
                weight = self.FEATURE_WEIGHTS[feature]
                distance_squared += weight * (value1 - value2) ** 2
        
        return math.sqrt(distance_squared)
    
    def _distance_to_similarity(self, distance: float) -> float:
        """
        Convert KNN distance to similarity score (0-100).
        
        Uses exponential decay to map distance to similarity.
        Lower distance → Higher similarity
        
        Formula: 100 * exp(-distance)
        """
        # Exponential decay: similarity decreases as distance increases
        similarity = 100 * math.exp(-distance)
        return round(similarity, 2)
    
    def _score_distance(self, subject: Dict[str, Any], comp: Dict[str, Any]) -> float:
        """Score based on geographic distance (0-100)"""
        distance = self._calculate_distance(
            subject.get('latitude', 0),
            subject.get('longitude', 0),
            comp.get('latitude', 0),
            comp.get('longitude', 0)
        )
        
        # Score: 100 for <0.5 miles, decreasing to 0 at 5+ miles
        if distance < 0.5:
            return 100
        elif distance < 1:
            return 90
        elif distance < 2:
            return 70
        elif distance < 5:
            return 40
        else:
            return max(0, 40 - (distance - 5) * 5)
    
    def _calculate_haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate geographic distance in miles using Haversine formula.
        
        This is used for human-readable distance reporting, not for KNN distance.
        """
        R = 3959  # Earth's radius in miles
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _get_score_breakdown(
        self, 
        subject: Dict[str, Any], 
        comp: Dict[str, Any],
        subject_features: Dict[str, float] = None,
        comp_features: Dict[str, float] = None
    ) -> Dict[str, float]:
        """
        Get detailed breakdown of KNN feature contributions.
        
        Shows how each feature contributed to the overall distance/similarity.
        """
        # Extract features if not provided
        if subject_features is None:
            subject_features = self._extract_features(subject)
        if comp_features is None:
            comp_features = self._extract_features(comp)
        
        # Calculate geographic distance in miles
        distance_miles = self._calculate_haversine_distance(
            subject_features['latitude'],
            subject_features['longitude'],
            comp_features['latitude'],
            comp_features['longitude']
        )
        
        # Calculate feature differences (unnormalized for readability)
        breakdown = {
            'distance_miles': round(distance_miles, 2),
            'sqft_diff': abs(subject_features['sqft'] - comp_features['sqft']),
            'sqft_pct_diff': round(abs(subject_features['sqft'] - comp_features['sqft']) / subject_features['sqft'] * 100, 1) if subject_features['sqft'] > 0 else 0,
            'bedrooms_diff': abs(subject_features['bedrooms'] - comp_features['bedrooms']),
            'bathrooms_diff': abs(subject_features['bathrooms'] - comp_features['bathrooms']),
            'age_diff_years': abs(subject_features['year_built'] - comp_features['year_built']),
            'days_since_sale': comp_features['days_since_sale'],
            'has_pool_match': 1 if subject_features['has_pool'] == comp_features['has_pool'] else 0,
            'knn_method': 'Weighted Euclidean Distance'
        }
        
        return breakdown
