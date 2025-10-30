from typing import List, Dict, Any
import re


class ConditionAnalyzer:
    """
    Analyzes home condition based on photos, video transcript, and home details
    In production, this would integrate with vision AI models (GPT-4 Vision, etc.)
    """
    
    CONDITION_KEYWORDS = {
        'excellent': ['pristine', 'immaculate', 'perfect', 'excellent', 'brand new', 'flawless', 'spotless'],
        'good': ['good', 'well-maintained', 'clean', 'updated', 'nice', 'solid', 'great'],
        'fair': ['fair', 'average', 'decent', 'okay', 'minor', 'cosmetic', 'needs paint'],
        'poor': ['poor', 'worn', 'damage', 'repair', 'replace', 'outdated', 'renovation']
    }
    
    def analyze(self, subject_home: Dict[str, Any], photos: List[str], video_transcript: str) -> Dict[str, Any]:
        """
        Analyze home condition from multiple sources
        
        Returns:
        {
            'overall_condition': 'Good/Fair/Poor/Excellent',
            'condition_score': 0-100,
            'interior_condition': {...},
            'exterior_condition': {...},
            'key_features': [...],
            'concerns': [...],
            'highlights': [...]
        }
        """
        
        # Analyze transcript for condition indicators
        condition_from_transcript = self._analyze_transcript(video_transcript)
        
        # In production, would analyze photos with vision AI
        # For now, we'll use transcript and home characteristics
        
        # Calculate condition score based on age and features
        condition_score = self._calculate_condition_score(subject_home, condition_from_transcript)
        
        # Determine overall condition
        overall_condition = self._determine_overall_condition(condition_score)
        
        # Extract key insights
        highlights = self._extract_highlights(subject_home, video_transcript)
        concerns = self._extract_concerns(video_transcript)
        key_features = self._extract_key_features(subject_home)
        
        return {
            'overall_condition': overall_condition,
            'condition_score': condition_score,
            'interior_condition': condition_from_transcript.get('interior', {}),
            'exterior_condition': condition_from_transcript.get('exterior', {}),
            'key_features': key_features,
            'concerns': concerns,
            'highlights': highlights,
            'summary': self._generate_summary(overall_condition, key_features, highlights, concerns)
        }
    
    def _analyze_transcript(self, transcript: str) -> Dict[str, Any]:
        """Analyze video transcript for condition keywords"""
        transcript_lower = transcript.lower()
        
        # Count condition indicators
        condition_counts = {
            'excellent': 0,
            'good': 0,
            'fair': 0,
            'poor': 0
        }
        
        for condition, keywords in self.CONDITION_KEYWORDS.items():
            for keyword in keywords:
                condition_counts[condition] += transcript_lower.count(keyword)
        
        # Extract specific areas mentioned
        interior_mentions = self._extract_area_mentions(transcript, ['kitchen', 'bathroom', 'bedroom', 'living', 'flooring', 'walls'])
        exterior_mentions = self._extract_area_mentions(transcript, ['roof', 'siding', 'paint', 'landscaping', 'driveway'])
        
        return {
            'condition_counts': condition_counts,
            'interior': interior_mentions,
            'exterior': exterior_mentions
        }
    
    def _extract_area_mentions(self, transcript: str, areas: List[str]) -> Dict[str, str]:
        """Extract mentions of specific areas from transcript"""
        mentions = {}
        
        for area in areas:
            # Find sentences mentioning this area
            pattern = rf'[^.!?]*\b{area}\b[^.!?]*[.!?]'
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            if matches:
                mentions[area] = ' '.join(matches[:2])  # Take first 2 mentions
        
        return mentions
    
    def _calculate_condition_score(self, home: Dict[str, Any], transcript_analysis: Dict[str, Any]) -> int:
        """Calculate 0-100 condition score"""
        base_score = 75  # Start at 75
        
        # Adjust based on age
        year_built = home.get('year_built', 2000)
        age = 2025 - year_built
        
        if age < 5:
            base_score += 15
        elif age < 10:
            base_score += 10
        elif age < 20:
            base_score += 5
        elif age > 50:
            base_score -= 10
        
        # Adjust based on transcript sentiment
        counts = transcript_analysis.get('condition_counts', {})
        base_score += counts.get('excellent', 0) * 3
        base_score += counts.get('good', 0) * 2
        base_score -= counts.get('fair', 0) * 1
        base_score -= counts.get('poor', 0) * 3
        
        # Ensure score is within 0-100
        return max(0, min(100, base_score))
    
    def _determine_overall_condition(self, score: int) -> str:
        """Determine overall condition rating from score"""
        if score >= 85:
            return 'Excellent'
        elif score >= 70:
            return 'Good'
        elif score >= 50:
            return 'Fair'
        else:
            return 'Poor'
    
    def _extract_key_features(self, home: Dict[str, Any]) -> List[str]:
        """Extract notable features from home details"""
        features = []
        
        if home.get('pool'):
            features.append(f"Pool")
        
        bedrooms = home.get('bedrooms', 0)
        bathrooms = home.get('bathrooms', 0)
        if bedrooms and bathrooms:
            features.append(f"{bedrooms} bed, {bathrooms} bath")
        
        sqft = home.get('square_footage', 0)
        if sqft:
            features.append(f"{sqft:,} sq ft")
        
        if home.get('garage'):
            features.append("Garage")
        
        return features
    
    def _extract_highlights(self, home: Dict[str, Any], transcript: str) -> List[str]:
        """Extract positive highlights"""
        highlights = []
        transcript_lower = transcript.lower()
        
        positive_phrases = [
            'recently updated', 'new', 'upgraded', 'modern', 'spacious',
            'great condition', 'well-maintained', 'beautiful', 'pristine'
        ]
        
        for phrase in positive_phrases:
            if phrase in transcript_lower:
                # Extract sentence containing this phrase
                pattern = rf'[^.!?]*\b{phrase}\b[^.!?]*[.!?]'
                matches = re.findall(pattern, transcript, re.IGNORECASE)
                if matches:
                    highlights.append(matches[0].strip())
        
        return highlights[:5]  # Return top 5
    
    def _extract_concerns(self, transcript: str) -> List[str]:
        """Extract concerns or issues"""
        concerns = []
        transcript_lower = transcript.lower()
        
        concern_phrases = [
            'needs repair', 'damage', 'worn', 'outdated', 'requires',
            'should replace', 'issue', 'problem', 'concern'
        ]
        
        for phrase in concern_phrases:
            if phrase in transcript_lower:
                pattern = rf'[^.!?]*\b{phrase}\b[^.!?]*[.!?]'
                matches = re.findall(pattern, transcript, re.IGNORECASE)
                if matches:
                    concerns.append(matches[0].strip())
        
        return concerns[:5]  # Return top 5
    
    def _generate_summary(self, condition: str, features: List[str], highlights: List[str], concerns: List[str]) -> str:
        """Generate human-readable summary"""
        summary_parts = [f"The property is in {condition.lower()} condition."]
        
        if features:
            summary_parts.append(f"Key features include {', '.join(features[:3])}.")
        
        if highlights:
            summary_parts.append(f"Notable highlights: {highlights[0]}")
        
        if concerns:
            summary_parts.append(f"Areas of concern include {concerns[0]}")
        
        return ' '.join(summary_parts)
