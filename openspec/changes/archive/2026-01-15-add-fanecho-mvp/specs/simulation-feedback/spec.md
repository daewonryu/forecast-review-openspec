# Capability: Simulation & Feedback

**Capability ID:** `simulation-feedback`  
**Change ID:** `add-fanecho-mvp`

---

## ADDED Requirements

### Requirement: Accept Draft Content Submission

The system MUST accept text draft submissions from users for reaction simulation. Drafts represent announcements, advertisements, or public notices to be tested.

**Acceptance Criteria:**
- Accepts plain text content (min 10 chars, max 5000 chars)
- Validates input is not empty or whitespace-only
- Stores draft in `Drafts` table with user_id and timestamp
- Returns draft_id for tracking simulation results

#### Scenario: Submit Announcement Draft

**Given** a user wants to test a gacha system update announcement  
**When** the user submits text content via API  
**Then** the system validates the content length  
**And** assigns a unique draft_id  
**And** stores the draft in the database  
**And** returns draft_id and confirmation status

---

### Requirement: Generate Dual Persona Responses

For each persona, the system MUST generate two distinct response types:
1. **Internal Monologue:** The persona's brutally honest internal thoughts
2. **Public Comment:** What the persona would actually post in a comment section

**Acceptance Criteria:**
- Internal monologue reflects true unfiltered reaction (100-300 chars)
- Public comment reflects socially acceptable version (50-200 chars)
- Both responses use the persona's voice and perspective
- Responses may differ in tone and sentiment

#### Scenario: Veteran Persona Reacts to Price Increase

**Given** "The Veteran" persona (loyalty 9) reviews a price increase announcement  
**When** the simulation runs  
**Then** the internal monologue might be: "After 5 years of loyalty, they're squeezing us for more money. I feel betrayed. This could be the breaking point."  
**And** the public comment might be: "Disappointed with this decision. Long-time players deserve better treatment. Reconsidering my support."  
**And** the internal monologue is more emotionally raw than the public comment

---

### Requirement: Quantified Scoring System

Each persona's reaction MUST include quantified scores on three dimensions:
- **Trust:** 1-10 (how much they trust the brand after reading)
- **Excitement:** 1-10 (enthusiasm about the announcement)
- **Backlash Risk:** 1-10 (likelihood of negative public reaction)

**Acceptance Criteria:**
- All scores are integers between 1-10 (inclusive)
- Scores are consistent with response sentiment
- LLM provides reasoning for each score
- Scores are stored in `Simulation_Results` table

#### Scenario: Score Negative Reaction

**Given** "The Skeptic" persona reacts to a controversial change  
**When** the scoring is calculated  
**Then** Trust score might be 3 (low trust)  
**And** Excitement score might be 2 (very low enthusiasm)  
**And** Backlash Risk score might be 8 (high likelihood of backlash)  
**And** scores align with negative internal monologue  
**And** reasoning explains: "Lacks transparency, feels exploitative"

---

### Requirement: Parallel Persona Simulation

The system MUST execute all 5 persona simulations in parallel to meet the <20 second total time requirement.

**Acceptance Criteria:**
- Simulations run concurrently using async processing
- Maximum wait time for all 5 responses is 15 seconds
- Failed individual simulations don't block others
- Results are collected and aggregated after all complete

#### Scenario: Parallel Processing Performance

**Given** a draft with 5 personas is submitted for simulation  
**When** the simulation starts at T=0  
**Then** all 5 LLM API calls are initiated concurrently  
**And** responses arrive within 10-15 seconds  
**And** aggregation completes by T=17 seconds  
**And** total end-to-end time is under 20 seconds

---

### Requirement: Simulation Result Persistence

All simulation results MUST be persisted to the database for historical tracking and comparison across draft iterations.

**Acceptance Criteria:**
- Results stored in `Simulation_Results` table
- Links draft_id, persona_id, and scores
- Includes timestamps for auditing
- Users can retrieve past simulation results

#### Scenario: Save and Retrieve Simulation History

**Given** a user runs a simulation on draft_id "d123"  
**When** the simulation completes  
**Then** 5 records are inserted into `Simulation_Results`  
**And** each record includes draft_id, persona_id, trust, excitement, backlash_risk, internal_monologue, public_comment  
**And** the user can later query results for draft "d123"  
**And** results show iteration history if draft was simulated multiple times

---

### Requirement: Error Handling for LLM Failures

The system MUST gracefully handle LLM API failures without blocking the entire simulation.

**Acceptance Criteria:**
- Timeout after 20 seconds for individual LLM calls
- Retry failed requests once with exponential backoff
- Return partial results if some personas succeed
- Log failures for monitoring
- Return user-friendly error messages

#### Scenario: Handle Partial LLM Failure

**Given** a simulation is running with 5 personas  
**When** 3 personas succeed but 2 LLM calls timeout  
**Then** the system returns results for the 3 successful personas  
**And** marks the 2 failed personas with status "error"  
**And** provides message: "Simulation completed with 3 of 5 personas (2 failed)"  
**And** logs the failure details for debugging  
**And** user can retry the failed personas separately

---

## Data Model

### Drafts Table

```sql
CREATE TABLE drafts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_created (user_id, created_at)
);
```

### Simulation_Results Table

```sql
CREATE TABLE simulation_results (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    draft_id BIGINT NOT NULL,
    persona_id BIGINT NOT NULL,
    trust_score INT NOT NULL CHECK (trust_score BETWEEN 1 AND 10),
    excitement_score INT NOT NULL CHECK (excitement_score BETWEEN 1 AND 10),
    backlash_risk_score INT NOT NULL CHECK (backlash_risk_score BETWEEN 1 AND 10),
    internal_monologue TEXT NOT NULL,
    public_comment TEXT NOT NULL,
    reasoning TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (draft_id) REFERENCES drafts(id),
    FOREIGN KEY (persona_id) REFERENCES personas(id),
    INDEX idx_draft (draft_id)
);
```

---

## API Endpoints

### POST /api/simulations/run

Run simulation for a draft with a persona set.

**Request:**
```json
{
  "draft_content": "We're excited to announce new pricing tiers...",
  "persona_set_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "draft_id": 42,
  "simulation_id": "sim_abc123",
  "results": [
    {
      "persona_id": 1,
      "persona_name": "The Veteran",
      "internal_monologue": "After 5 years...",
      "public_comment": "Disappointed with this decision...",
      "scores": {
        "trust": 3,
        "excitement": 2,
        "backlash_risk": 8
      }
    }
    // ... 4 more persona results
  ],
  "aggregate": {
    "avg_trust": 4.2,
    "avg_excitement": 3.8,
    "avg_backlash_risk": 7.4
  },
  "completed_at": "2026-01-14T10:30:17Z",
  "duration_seconds": 16.8
}
```

### GET /api/simulations/{simulation_id}

Retrieve past simulation results.
