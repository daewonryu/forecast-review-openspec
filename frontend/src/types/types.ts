// API Types matching backend schemas

export interface Persona {
  id: number;
  set_id: string;
  name: string;
  archetype: string;
  loyalty_level: number;
  core_values: string[];
  audience_description: string;
  created_at: string;
}

export interface PersonaSet {
  set_id: string;
  personas: Persona[];
  created_at?: string;
}

export interface PersonaSetSummary {
  set_id: string;
  audience_description: string;
  persona_count: number;
  created_at: string;
}

export interface PersonaSetsResponse {
  sets: PersonaSetSummary[];
  total: number;
  page: number;
  page_size: number;
}

export interface PersonaGenerateRequest {
  audience_description: string;
  save_to_library?: boolean;
}

export interface Scores {
  trust: number;
  excitement: number;
  backlash_risk: number;
}

export interface SimulationResult {
  persona_id: number;
  persona_name: string;
  internal_monologue: string;
  public_comment: string;
  scores: Scores;
  reasoning?: string;
  status: string;
  error_message?: string;
}

export interface AggregateScores {
  avg_trust: number;
  avg_excitement: number;
  avg_backlash_risk: number;
}

export interface SimulationResponse {
  simulation_id: string;
  draft_id: number;
  results: SimulationResult[];
  aggregate: AggregateScores;
  completed_at: string;
  duration_seconds: number;
}

export interface SimulationRequest {
  draft_content: string;
  persona_set_id: string;
}

export interface PainPoint {
  text: string;
  severity: 'low' | 'medium' | 'high';
  affected_personas: string[];
  reasoning: string;
}

export interface ImprovementTip {
  category: string;
  suggestion: string;
  priority: 'low' | 'medium' | 'high';
  expected_impact: string;
}

export interface AggregateAnalytics {
  average_scores: {
    trust: number;
    excitement: number;
    backlash: number;
  };
  overall_sentiment: 'positive' | 'neutral' | 'negative';
  score_distribution: any[];
}

export interface Insights {
  id: number;
  simulation_id: string;
  pain_points: PainPoint[];
  improvement_tips: ImprovementTip[];
  overall_sentiment: 'positive' | 'neutral' | 'negative';
  avg_trust: number;
  avg_excitement: number;
  avg_backlash_risk: number;
  created_at: string;
}

export interface HealthStatus {
  status: string;
  database: string;
  timestamp: string;
}

