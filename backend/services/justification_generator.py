from typing import List, Dict, Any


class JustificationGenerator:
    """
    Generates human-readable justification for price recommendation
    In production, would use LLM for more natural language generation
    """
    
    def generate(
        self,
        subject_home: Dict[str, Any],
        comparables: List[Dict[str, Any]],
        price_recommendation: Dict[str, Any],
        condition_summary: Dict[str, Any]
    ) -> str:
        """
        Generate comprehensive justification for the price recommendation
        """
        
        sections = []
        
        # Executive summary
        sections.append(self._generate_summary(subject_home, price_recommendation))
        
        # Market analysis
        sections.append(self._generate_market_analysis(comparables, price_recommendation))
        
        # Property condition analysis
        sections.append(self._generate_condition_analysis(condition_summary))
        
        # Comparable properties analysis
        sections.append(self._generate_comparables_analysis(subject_home, comparables))
        
        # Key adjustments
        sections.append(self._generate_adjustments_analysis(price_recommendation))
        
        # Conclusion
        sections.append(self._generate_conclusion(price_recommendation))
        
        return '\n\n'.join(sections)
    
    def _generate_summary(self, subject_home: Dict[str, Any], price_recommendation: Dict[str, Any]) -> str:
        """Generate executive summary"""
        address = subject_home.get('address', 'Subject Property')
        price = price_recommendation['recommended_price']
        price_low = price_recommendation['price_range']['low']
        price_high = price_recommendation['price_range']['high']
        confidence = price_recommendation['confidence']
        
        return (
            f"**Executive Summary**\n\n"
            f"Based on comprehensive market analysis, we recommend listing {address} at "
            f"${price:,}. Our analysis indicates a probable sale price range of "
            f"${price_low:,} to ${price_high:,}, with {confidence.lower()} confidence in this estimate. "
            f"This valuation is supported by recent comparable sales and a thorough condition assessment."
        )
    
    def _generate_market_analysis(self, comparables: List[Dict[str, Any]], price_recommendation: Dict[str, Any]) -> str:
        """Generate market analysis section"""
        if not comparables:
            return ""
        
        comp_prices = [c.get('sale_price', 0) for c in comparables]
        avg_price = sum(comp_prices) / len(comp_prices)
        price_per_sqft = price_recommendation.get('price_per_sqft', 0)
        
        comp_sqfts = [c.get('square_footage', 1) for c in comparables]
        avg_comp_sqft = sum(comp_sqfts) / len(comp_sqfts)
        avg_comp_price_per_sqft = avg_price / avg_comp_sqft if avg_comp_sqft > 0 else 0
        
        return (
            f"**Market Analysis**\n\n"
            f"The local market shows {len(comparables)} comparable sales with an average price of "
            f"${avg_price:,.0f}. The recommended price of ${price_recommendation['recommended_price']:,} "
            f"represents ${price_per_sqft:.2f} per square foot, compared to the market average of "
            f"${avg_comp_price_per_sqft:.2f} per square foot. This pricing positions the property "
            f"competitively within the current market conditions."
        )
    
    def _generate_condition_analysis(self, condition_summary: Dict[str, Any]) -> str:
        """Generate property condition analysis"""
        condition = condition_summary.get('overall_condition', 'Fair')
        score = condition_summary.get('condition_score', 70)
        summary = condition_summary.get('summary', '')
        
        highlights = condition_summary.get('highlights', [])
        concerns = condition_summary.get('concerns', [])
        
        text = (
            f"**Property Condition Assessment**\n\n"
            f"The property is rated in {condition} condition (score: {score}/100). {summary}\n"
        )
        
        if highlights:
            text += f"\n**Positive Attributes:**\n"
            for highlight in highlights[:3]:
                text += f"- {highlight}\n"
        
        if concerns:
            text += f"\n**Areas for Attention:**\n"
            for concern in concerns[:3]:
                text += f"- {concern}\n"
        
        return text
    
    def _generate_comparables_analysis(self, subject_home: Dict[str, Any], comparables: List[Dict[str, Any]]) -> str:
        """Generate analysis of comparable properties"""
        if not comparables:
            return ""
        
        text = f"**Comparable Properties Analysis**\n\n"
        text += f"The following {len(comparables)} properties were identified as most comparable:\n\n"
        
        for i, comp in enumerate(comparables, 1):
            address = comp.get('address', f'Property {i}')
            price = comp.get('sale_price', 0)
            sqft = comp.get('square_footage', 0)
            bed = comp.get('bedrooms', 0)
            bath = comp.get('bathrooms', 0)
            similarity = comp.get('similarity_score', 0)
            distance = comp.get('score_breakdown', {}).get('distance_miles', 0)
            
            text += (
                f"{i}. **{address}**\n"
                f"   - Sale Price: ${price:,}\n"
                f"   - Size: {sqft:,} sq ft | {bed} bed, {bath} bath\n"
                f"   - Distance: {distance:.2f} miles\n"
                f"   - Similarity Score: {similarity:.1f}/100\n\n"
            )
        
        return text
    
    def _generate_adjustments_analysis(self, price_recommendation: Dict[str, Any]) -> str:
        """Generate analysis of price adjustments"""
        total_adj = price_recommendation.get('total_adjustment_pct', 0)
        adjustments = price_recommendation.get('adjustments', {})
        
        text = f"**Price Adjustments**\n\n"
        text += f"Total adjustment from base comparable average: {total_adj:+.1f}%\n\n"
        
        condition_adj = adjustments.get('condition_adjustment', 0)
        if abs(condition_adj) > 0.1:
            text += f"- Condition adjustment: {condition_adj:+.1f}%\n"
        
        feature_adjs = adjustments.get('feature_adjustments', {})
        for feature, adj in feature_adjs.items():
            if abs(adj) > 0.1:
                text += f"- {feature.title()} adjustment: {adj:+.1f}%\n"
        
        return text
    
    def _generate_conclusion(self, price_recommendation: Dict[str, Any]) -> str:
        """Generate conclusion"""
        price = price_recommendation['recommended_price']
        confidence = price_recommendation['confidence']
        
        confidence_text = {
            'High': 'strong data support and highly comparable sales',
            'Medium': 'solid comparable data with some variation',
            'Low': 'limited comparable data or significant property differences'
        }.get(confidence, 'available market data')
        
        return (
            f"**Conclusion**\n\n"
            f"The recommended listing price of ${price:,} is supported by {confidence_text}. "
            f"This pricing strategy positions the property competitively for a timely sale while "
            f"maximizing value for the seller. Regular market monitoring is recommended to adjust "
            f"pricing strategy if market conditions change significantly."
        )
