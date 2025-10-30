export interface SubjectHome {
  address: string;
  latitude: number;
  longitude: number;
  square_footage: number;
  bedrooms: number;
  bathrooms: number;
  year_built: number;
  pool?: boolean;
  garage?: boolean;
  lot_size?: number;
  property_type?: string;
}

export interface ComparableHome {
  address: string;
  latitude: number;
  longitude: number;
  square_footage: number;
  bedrooms: number;
  bathrooms: number;
  year_built: number;
  pool?: boolean;
  garage?: boolean;
  sale_price: number;
  days_since_sale: number;
  sale_date: string;
  similarity_score?: number;
  knn_distance?: number;
  distance_miles?: number;  // Real geographic distance in miles (Haversine formula)
  score_breakdown?: {
    distance: number;
    sqft_similarity: number;
    bed_bath_match: number;
    age_similarity: number;
    sale_recency: number;
    distance_miles: number;
    has_pool_match?: number;
  };
}

export interface ConditionSummary {
  overall_condition: string;
  condition_score: number;
  interior_condition: Record<string, string>;
  exterior_condition: Record<string, string>;
  key_features: string[];
  concerns: string[];
  highlights: string[];
  summary: string;
}

export interface PriceRecommendation {
  recommended_price: number;
  price_range: {
    low: number;
    high: number;
  };
  confidence: 'High' | 'Medium' | 'Low';
  price_per_sqft: number;
  base_price: number;
  total_adjustment_pct: number;
  adjustments: {
    condition_adjustment: number;
    feature_adjustments: Record<string, number>;
  };
  methodology: string;
}

export interface PricingReport {
  success: boolean;
  subject_home: SubjectHome;
  condition_summary: ConditionSummary;
  top_comparables: ComparableHome[];
  price_recommendation: PriceRecommendation;
  justification: string;
  video_analysis?: string;
  generated_at: string;
}

export interface AnalyzeHomeRequest {
  subject_home: SubjectHome;
  photos: string[];
  video_transcript: string;
  comparable_sales: ComparableHome[];
}
