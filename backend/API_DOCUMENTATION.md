# FanEcho API Documentation

## Overview

FanEcho is an AI-powered synthetic fan reaction simulator that helps content creators test their social media drafts against diverse audience personas before posting.

**Base URL:** `http://localhost:8000`

---

## Authentication

Currently, the API does not require authentication. User identification is done via `user_id` parameter.

---

## API Endpoints

### Health Check

#### `GET /health`

Check API health status and database connectivity.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-01-14T10:30:00Z"
}
```

---

## Personas

### Generate Personas

#### `POST /api/personas/generate`

Generate 5 diverse AI personas based on an audience description.

**Request Body:**
```json
{
  "audience_description": "Tech enthusiasts interested in AI and machine learning",
  "user_id": 1
}
```

**Validation:**
- `audience_description`: 5-500 characters
- `user_id`: integer

**Response (200 OK):**
```json
{
  "set_id": "550e8400-e29b-41d4-a716-446655440000",
  "personas": [
    {
      "id": 123,
      "name": "The Veteran",
      "archetype": "Long-time AI enthusiast",
      "loyalty_level": 9,
      "core_values": ["Transparency", "Innovation", "Community"],
      "traits": "Experienced, knowledgeable, expects high quality",
      "created_at": "2026-01-14T10:30:00Z"
    },
    // ... 4 more personas
  ]
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input (description too short/long)
- `500 Internal Server Error`: LLM generation failed

---

### Get Persona Set

#### `GET /api/personas/sets/{set_id}`

Retrieve a specific persona set by ID.

**Response (200 OK):**
```json
{
  "set_id": "550e8400-e29b-41d4-a716-446655440000",
  "personas": [...],
  "created_at": "2026-01-14T10:30:00Z"
}
```

**Error Responses:**
- `404 Not Found`: Persona set doesn't exist

---

### List Persona Sets

#### `GET /api/personas/sets?user_id={user_id}&page={page}&page_size={page_size}`

List all persona sets for a user with pagination.

**Query Parameters:**
- `user_id` (required): User identifier
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Results per page (default: 10, max: 50)

**Response (200 OK):**
```json
{
  "sets": [
    {
      "set_id": "...",
      "audience_description": "Tech enthusiasts",
      "persona_count": 5,
      "created_at": "2026-01-14T10:30:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "page_size": 10
}
```

---

### Delete Persona Set

#### `DELETE /api/personas/sets/{set_id}`

Delete a persona set and all associated personas.

**Response (204 No Content)**

**Error Responses:**
- `404 Not Found`: Persona set doesn't exist

---

## Simulations

### Run Simulation

#### `POST /api/simulations/run`

Run a simulation with 5 personas reacting to draft content in parallel.

**Request Body:**
```json
{
  "draft_content": "Exciting news! We're launching our revolutionary AI assistant next month. Get early access now!",
  "persona_set_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": 1
}
```

**Validation:**
- `draft_content`: 10-5000 characters
- `persona_set_id`: valid UUID
- `user_id`: integer

**Response (200 OK):**
```json
{
  "simulation_id": "660e8400-e29b-41d4-a716-446655440001",
  "draft_id": 456,
  "results": [
    {
      "persona_id": 123,
      "persona_name": "The Veteran",
      "internal_reaction": "Hmm, 'revolutionary' is a big claim. Need to see the tech specs before I get excited.",
      "public_response": "Interesting! Looking forward to learning more about the capabilities.",
      "trust_score": 6,
      "excitement_score": 7,
      "backlash_score": 3,
      "reasoning": "The announcement is intriguing but lacks technical details that would build trust.",
      "status": "success"
    },
    // ... 4 more results
  ],
  "aggregate": {
    "avg_trust": 6.4,
    "avg_excitement": 7.2,
    "avg_backlash": 2.8
  },
  "completed_at": "2026-01-14T10:30:15Z",
  "duration_seconds": 12.5
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input or persona set not found
- `500 Internal Server Error`: Simulation failed
- `504 Gateway Timeout`: Simulation exceeded 60 seconds

**Notes:**
- Simulations run in parallel across all 5 personas
- Total time is typically 10-20 seconds
- Partial results returned if some personas fail

---

### Get Simulation Results

#### `GET /api/simulations/{simulation_id}`

Retrieve completed simulation results.

**Response (200 OK):**
Same format as simulation run response.

**Error Responses:**
- `404 Not Found`: Simulation doesn't exist

---

## Insights

### Generate Insights

#### `POST /api/insights/generate/{draft_id}`

Generate AI-powered insights including pain points and improvement tips.

**Response (200 OK):**
```json
{
  "id": 789,
  "draft_id": 456,
  "aggregate_analytics": {
    "average_scores": {
      "trust": 6.4,
      "excitement": 7.2,
      "backlash": 2.8
    },
    "overall_sentiment": "positive",
    "score_distribution": [...]
  },
  "pain_points": [
    {
      "text": "revolutionary",
      "severity": "medium",
      "affected_personas": ["The Skeptic", "The Veteran"],
      "reasoning": "Overused marketing term that lacks credibility with experienced users"
    }
  ],
  "improvement_tips": [
    {
      "tip": "Replace 'revolutionary' with specific technical innovations (e.g., '40% faster response time')",
      "rationale": "Concrete metrics build more trust than marketing superlatives",
      "impact": "high",
      "addresses": ["revolutionary"]
    },
    // ... 2 more tips
  ],
  "created_at": "2026-01-14T10:30:20Z"
}
```

**Error Responses:**
- `404 Not Found`: Draft or simulation results not found
- `500 Internal Server Error`: Insight generation failed

---

### Get Insights

#### `GET /api/insights/{insight_id}`

Retrieve generated insights by ID.

**Response (200 OK):**
Same format as generate insights response.

---

### Get Insights by Draft

#### `GET /api/insights/draft/{draft_id}`

Retrieve insights for a specific draft.

**Response (200 OK):**
Same format as generate insights response.

---

### Persona Drill-Down

#### `GET /api/insights/persona/{persona_id}/drill-down?draft_id={draft_id}`

Get detailed comparison of a single persona vs. group average.

**Response (200 OK):**
```json
{
  "persona_details": {
    "id": 123,
    "name": "The Veteran",
    "loyalty_level": 9,
    "core_values": ["Transparency", "Innovation"],
    "traits": "..."
  },
  "persona_scores": {
    "trust": 8,
    "excitement": 9,
    "backlash": 2
  },
  "group_averages": {
    "trust": 6.4,
    "excitement": 7.2,
    "backlash": 2.8
  },
  "delta": {
    "trust": 1.6,
    "excitement": 1.8,
    "backlash": -0.8
  },
  "is_outlier": true,
  "reactions": {
    "internal": "...",
    "public": "...",
    "reasoning": "..."
  }
}
```

---

### Sentiment Trends

#### `GET /api/insights/trends/{persona_set_id}?user_id={user_id}`

Track sentiment improvements across multiple drafts with the same persona set.

**Response (200 OK):**
```json
{
  "persona_set_id": "550e8400-e29b-41d4-a716-446655440000",
  "simulations": [
    {
      "draft_id": 456,
      "simulation_date": "2026-01-14T10:00:00Z",
      "draft_preview": "First draft content...",
      "average_scores": {
        "trust": 5.2,
        "excitement": 6.0,
        "backlash": 4.5
      },
      "overall_sentiment": "neutral",
      "delta_from_previous": null
    },
    {
      "draft_id": 457,
      "simulation_date": "2026-01-14T11:00:00Z",
      "draft_preview": "Improved draft content...",
      "average_scores": {
        "trust": 6.8,
        "excitement": 7.5,
        "backlash": 2.3
      },
      "overall_sentiment": "positive",
      "delta_from_previous": {
        "trust": 1.6,
        "excitement": 1.5,
        "backlash": -2.2
      }
    }
  ]
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 204  | Success (No Content) |
| 400  | Bad Request - Invalid input |
| 404  | Not Found - Resource doesn't exist |
| 422  | Validation Error - Input validation failed |
| 500  | Internal Server Error |
| 504  | Gateway Timeout - Request exceeded time limit |

---

## Rate Limits

No rate limits currently enforced (MVP).

---

## Data Models

### Persona
- `id`: integer
- `set_id`: UUID string
- `name`: string (50 chars max)
- `archetype`: string (50 chars max)
- `loyalty_level`: integer (1-10)
- `core_values`: array of strings (2-4 items)
- `traits`: string
- `audience_description`: string
- `created_at`: ISO 8601 timestamp

### Simulation Result
- `persona_id`: integer
- `persona_name`: string
- `internal_reaction`: string
- `public_response`: string
- `trust_score`: integer (1-10)
- `excitement_score`: integer (1-10)
- `backlash_score`: integer (1-10)
- `reasoning`: string
- `status`: "success" | "error"
- `error_message`: string (if error)

### Insight
- `id`: integer
- `draft_id`: integer
- `aggregate_analytics`: object
- `pain_points`: array of objects
- `improvement_tips`: array of objects
- `created_at`: ISO 8601 timestamp

---

## Development

### Running Locally

1. Install dependencies:
```bash
uv pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY=your_key
export DATABASE_URL=mysql+pymysql://user:pass@localhost/fanecho
```

3. Run database migrations:
```bash
python backend/init_db.py
```

4. Start server:
```bash
uvicorn app.main:app --reload --port 8000
```

### Running Tests

```bash
pytest backend/tests/ -v --cov=app
```

---

## Support

For questions or issues, contact: support@fanecho.com
