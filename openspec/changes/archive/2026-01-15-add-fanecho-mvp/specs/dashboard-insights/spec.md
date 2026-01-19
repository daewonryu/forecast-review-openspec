# Capability: Dashboard & Insights

**Capability ID:** `dashboard-insights`  
**Change ID:** `add-fanecho-mvp`

---

## ADDED Requirements

### Requirement: Aggregate Analytics Summary

The system MUST provide aggregated analytics showing the overall sentiment across all 5 personas for a given simulation.

**Acceptance Criteria:**
- Calculate average scores for Trust, Excitement, and Backlash Risk
- Display overall sentiment category (Positive, Neutral, Negative)
- Show distribution of scores across personas
- Format results for easy interpretation

#### Scenario: View Aggregated Sentiment

**Given** a simulation completes with 5 persona results  
**When** the analytics are calculated  
**Then** the average Trust score is displayed (e.g., 4.2/10)  
**And** the average Excitement score is displayed (e.g., 3.8/10)  
**And** the average Backlash Risk score is displayed (e.g., 7.4/10)  
**And** the overall sentiment is labeled "Negative" (high backlash risk)  
**And** a visual indicator (color/icon) reflects the sentiment

---

### Requirement: Pain Point Identification

The system MUST identify and highlight specific parts of the draft text that caused the highest Backlash Risk scores across personas.

**Acceptance Criteria:**
- Analyze persona reasoning/feedback to extract problematic phrases
- Highlight text segments with backlash score ≥ 7
- Group similar concerns across multiple personas
- Present pain points in ranked order (highest risk first)

#### Scenario: Identify Problematic Pricing Language

**Given** a draft includes "mandatory subscription upgrade"  
**And** 4 out of 5 personas score backlash risk ≥ 8  
**And** their reasoning mentions "forced," "no choice," "money grab"  
**When** pain point analysis runs  
**Then** the phrase "mandatory subscription upgrade" is highlighted  
**And** annotated with: "4 personas flagged this as coercive language"  
**And** shown at the top of the pain points list  
**And** linked to the specific persona feedback

---

### Requirement: AI Improvement Tips

The system MUST generate exactly 3 actionable suggestions to improve the draft based on persona scores and feedback.

**Acceptance Criteria:**
- Tips are specific and actionable (not generic advice)
- Tips address the highest backlash risk areas
- Tips consider persona core values and priorities
- Tips are ranked by potential impact
- Generated using LLM synthesis of persona feedback

#### Scenario: Generate Improvement Tips for Pricing Announcement

**Given** a draft has average backlash risk of 7.4  
**And** personas cite lack of transparency and forced upgrades  
**When** AI tips are generated  
**Then** tip 1 might be: "Reframe 'mandatory upgrade' as 'new benefits include...' to reduce perception of force"  
**And** tip 2 might be: "Add a grandfathering clause for existing users to preserve loyalty and trust"  
**And** tip 3 might be: "Include concrete examples of value (e.g., '3x more features') to justify pricing"  
**And** each tip includes rationale: "This addresses The Veteran's concern about betrayal"

---

### Requirement: Sentiment Trend Analysis

The system SHALL track sentiment changes across multiple draft iterations to show improvement or deterioration.

**Acceptance Criteria:**
- Compare scores between simulation runs for same persona set
- Visualize trend (improving, stable, worsening)
- Show which tips were effective if draft was edited
- Encourage iterative refinement

#### Scenario: Track Improvement Across Iterations

**Given** a user simulates draft v1 with avg backlash risk 7.4  
**And** then edits the draft based on tips  
**And** simulates draft v2 with same personas  
**When** v2 results show avg backlash risk 4.2  
**Then** the system displays: "Backlash risk improved by 3.2 points"  
**And** highlights which changes had the biggest impact  
**And** shows a trend graph with v1 and v2 scores

---

### Requirement: Persona-Specific Insights

The system SHALL provide drill-down capability to view detailed insights for individual personas.

**Acceptance Criteria:**
- Users can click on a persona to see full details
- Show internal monologue, public comment, scores, and reasoning
- Compare this persona's reaction to the group average
- Identify if this persona is an outlier

#### Scenario: Drill Down on Skeptical Persona

**Given** "The Skeptic" has backlash risk of 9 (highest in group)  
**When** the user clicks on "The Skeptic" persona  
**Then** a detail view opens showing full internal monologue  
**And** displays: "Backlash Risk: 9/10 (2 points above average)"  
**And** shows reasoning: "Lacks concrete data, feels like marketing spin"  
**And** highlights this persona's specific pain points  
**And** suggests: "Address this persona by adding transparency and data"

---

### Requirement: Export and Sharing

The system MUST allow users to export simulation results and insights for sharing with team members.

**Acceptance Criteria:**
- Export to PDF or JSON format
- Include all persona results, scores, and tips
- Preserve formatting and readability
- Option to anonymize persona names

#### Scenario: Export Results for Team Review

**Given** a user completes a simulation  
**When** the user clicks "Export Results"  
**Then** a PDF is generated with:
- Draft content
- All 5 persona reactions
- Aggregated scores
- Pain points and improvement tips  
**And** the file is downloadable  
**And** formatted for presentation to stakeholders

---

## Data Model

### Insights Table (Optional - could be computed on-demand)

```sql
CREATE TABLE insights (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    simulation_id VARCHAR(36) NOT NULL,
    pain_points JSON NOT NULL,
    improvement_tips JSON NOT NULL,
    overall_sentiment ENUM('positive', 'neutral', 'negative') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_simulation (simulation_id)
);
```

---

## API Endpoints

### GET /api/insights/{simulation_id}

Retrieve insights and improvement tips for a simulation.

**Response:**
```json
{
  "simulation_id": "sim_abc123",
  "aggregate_scores": {
    "avg_trust": 4.2,
    "avg_excitement": 3.8,
    "avg_backlash_risk": 7.4
  },
  "overall_sentiment": "negative",
  "pain_points": [
    {
      "text": "mandatory subscription upgrade",
      "backlash_score": 8.5,
      "affected_personas": 4,
      "reasoning": "Perceived as coercive and exploitative"
    },
    {
      "text": "effective immediately",
      "backlash_score": 7.2,
      "affected_personas": 3,
      "reasoning": "No transition period feels disrespectful"
    }
  ],
  "improvement_tips": [
    {
      "priority": 1,
      "tip": "Reframe 'mandatory upgrade' as 'new benefits include...' to reduce perception of force",
      "rationale": "Addresses concerns from The Veteran, The Skeptic, and The Casual",
      "potential_impact": "Could reduce backlash risk by 2-3 points"
    },
    {
      "priority": 2,
      "tip": "Add a grandfathering clause for existing users to preserve loyalty and trust",
      "rationale": "Specifically helps retain The Veteran (loyalty 9)",
      "potential_impact": "Could improve trust score by 2 points"
    },
    {
      "priority": 3,
      "tip": "Include concrete examples of value (e.g., '3x more features') to justify pricing",
      "rationale": "Addresses The Analyst's need for transparency",
      "potential_impact": "Could reduce skepticism and improve excitement"
    }
  ]
}
```

### POST /api/insights/{simulation_id}/export

Export results to PDF or JSON format.

**Request:**
```json
{
  "format": "pdf",
  "include_persona_details": true,
  "anonymize": false
}
```

**Response:** File download or URL to generated export
