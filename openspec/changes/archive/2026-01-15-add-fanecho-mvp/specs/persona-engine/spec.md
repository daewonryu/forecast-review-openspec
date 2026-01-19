# Capability: Persona Engine

**Capability ID:** `persona-engine`  
**Change ID:** `add-fanecho-mvp`

---

## ADDED Requirements

### Requirement: Generate AI Personas from Audience Description

The system MUST generate exactly 5 distinct AI personas when provided with a high-level audience description (e.g., "K-pop fans", "Hardcore fans of a 5-year-old mobile RPG", "Tech enthusiasts").

**Acceptance Criteria:**
- Accepts text description of target audience (min 5 chars, max 500 chars)
- Returns exactly 5 unique personas within 60 seconds
- Each persona has distinct characteristics (no duplicates in archetype)
- Uses LLM (chatGPT) for generation

#### Scenario: Generate Personas for Mobile Game Fans

**Given** a user inputs "Hardcore fans of a 5-year-old mobile RPG"  
**When** the persona generation endpoint is called  
**Then** the system returns 5 distinct personas such as:
- "The Veteran" (high loyalty, values nostalgia)
- "The Casual" (medium loyalty, values convenience)
- "The Skeptic" (low loyalty, values transparency)
- "The Whale" (high loyalty, values exclusivity)
- "The Analyst" (medium loyalty, values fairness)

**And** each persona includes all required traits  
**And** generation completes within 60 seconds

---

### Requirement: Define Persona Traits

Each generated persona MUST include the following structured traits:
- **Name/Archetype:** Descriptive label (e.g., "The Veteran", "The Skeptic")
- **Loyalty Level:** Integer score from 1-10
- **Core Values:** Array of 2-4 values (e.g., "Transparency", "Value for Money", "Exclusivity")

**Acceptance Criteria:**
- Name/Archetype is a string (max 50 chars)
- Loyalty Level is an integer between 1 and 10 (inclusive)
- Core Values is an array with 2-4 string values
- All fields are non-null and validated

#### Scenario: Validate Persona Trait Structure

**Given** a persona generation request completes  
**When** the response is validated  
**Then** each persona has a `name` field with valid archetype string  
**And** each persona has a `loyalty_level` field between 1-10  
**And** each persona has a `core_values` array with 2-4 elements  
**And** all trait values pass schema validation

---

### Requirement: Persist Personas to Database

Generated personas MUST be saved to the database for future reuse across different content drafts. Users can create a "Brand Library" of persona sets.

**Acceptance Criteria:**
- Personas stored in `Personas` table with foreign key to user
- Each persona set has a unique identifier
- Users can retrieve previously generated personas
- Personas include metadata: created_at, audience_description

#### Scenario: Save and Retrieve Persona Set

**Given** a user generates 5 personas for "K-pop fans"  
**When** the personas are saved with set_id "abc123"  
**Then** the database contains 5 persona records linked to user  
**And** each record includes name, loyalty_level, core_values, audience_description  
**And** the user can retrieve all 5 personas using set_id "abc123"  
**And** the personas persist across sessions

---

### Requirement: Persona Uniqueness Within Set

Within a single persona set, personas SHALL have distinct archetypes and sufficiently different trait combinations to represent diverse perspectives.

**Acceptance Criteria:**
- No two personas in the same set share identical archetypes
- Loyalty levels vary across the set (not all same value)
- Core values have at least 50% difference between personas
- LLM prompt includes instructions for diversity

#### Scenario: Verify Persona Diversity

**Given** a persona set is generated for "Tech enthusiasts"  
**When** the 5 personas are analyzed  
**Then** all 5 archetypes are unique  
**And** loyalty levels include at least 3 different values  
**And** no two personas share identical core_values arrays  
**And** the set represents a spectrum from optimistic to skeptical

---

## Data Model

### Personas Table

```sql
CREATE TABLE personas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    set_id VARCHAR(36) NOT NULL,
    name VARCHAR(50) NOT NULL,
    archetype VARCHAR(50) NOT NULL,
    loyalty_level INT NOT NULL CHECK (loyalty_level BETWEEN 1 AND 10),
    core_values JSON NOT NULL,
    audience_description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_set (user_id, set_id)
);
```

---

## API Endpoints

### POST /api/personas/generate

Generate a set of 5 AI personas.

**Request:**
```json
{
  "audience_description": "Hardcore fans of a 5-year-old mobile RPG",
  "save_to_library": true
}
```

**Response:**
```json
{
  "set_id": "550e8400-e29b-41d4-a716-446655440000",
  "personas": [
    {
      "id": 1,
      "name": "The Veteran",
      "archetype": "Long-time player",
      "loyalty_level": 9,
      "core_values": ["Nostalgia", "Community", "Recognition"]
    },
    {
      "id": 2,
      "name": "The Casual",
      "archetype": "Occasional player",
      "loyalty_level": 5,
      "core_values": ["Convenience", "Fun", "Value for Money"]
    }
    // ... 3 more personas
  ],
  "created_at": "2026-01-14T10:30:00Z"
}
```

### GET /api/personas/sets/{set_id}

Retrieve a previously generated persona set.

**Response:** Same as POST response above
