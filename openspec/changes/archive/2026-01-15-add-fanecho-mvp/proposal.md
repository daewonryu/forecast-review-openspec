# Proposal: Add FanEcho MVP - Synthetic Fan Reaction Simulator

**Change ID:** `add-fanecho-mvp`  
**Status:** Proposed  
**Created:** 2026-01-14

---

## Why

Brand announcements often face unexpected negative reactions due to poor phrasing or lack of empathy for fan sentiment. Small-to-medium teams don't have the budget or time for focus group testing before every social media post, and internal teams often fail to see how "extreme" fans might interpret a message. FanEcho solves this by providing AI-generated personas that simulate real fan reactions, allowing teams to identify PR risks and optimize content before publication.

---

## What Changes

- **Add Persona Engine capability:** Generate 5 distinct AI personas based on audience description, persist to database for reuse
- **Add Simulation & Feedback capability:** Execute parallel simulations with dual responses (internal monologue + public comment) and quantified scoring (Trust, Excitement, Backlash Risk)
- **Add Dashboard & Insights capability:** Provide aggregated analytics, pain point identification, and 3 actionable improvement tips
- **Database schema:** New tables for Users, Personas, Drafts, and Simulation_Results
- **LLM integration:** OpenAI GPT with async processing

## Impact

**Affected Specs:**
- `persona-engine` (new capability)
- `simulation-feedback` (new capability)
- `dashboard-insights` (new capability)

**Affected Code:**
- New FastAPI backend services
- New database migrations
- New LLM integration layer

---

## Overview

Implement the MVP version of **FanEcho**, a synthetic user testing platform that allows brands to simulate fan reactions to public announcements or advertisements using AI-generated personas. The system will identify potential PR risks and provide optimization insights before content is published.

---

## Motivation

### Problem Statement
- **Risk of Backlash:** Brand announcements often face unexpected negative reactions due to poor phrasing or lack of empathy for fan sentiment
- **Lack of Testing:** Small-to-medium teams don't have the budget or time for focus group testing before every social media post or notice
- **Groupthink:** Internal teams often fail to see how "extreme" fans might interpret a message

### Success Criteria
1. Users edit their content at least once after seeing simulation results (Content Improvement)
2. Users reuse the same persona sets for multiple simulations (Persona Consistency)
3. Total simulation time from input to result completes in under 60 seconds (Speed)

---

## Scope

### In Scope (MVP)
1. **Persona Engine**
   - Generate 5 distinct AI personas based on high-level audience description
   - Define persona traits: Name/Archetype, Loyalty Level (1-10), Core Values
   - Persist personas to database for reuse

2. **Simulation & Feedback**
   - Accept text draft submissions from users
   - Generate dual responses per persona: Internal Monologue + Public Comment
   - Score reactions on Trust (1-10), Excitement (1-10), Backlash Risk (1-10)

3. **Dashboard & Insights**
   - Display aggregated analytics and average sentiment
   - Identify pain points in text causing high Backlash Risk
   - Provide 3 actionable AI improvement tips

4. **Core User Workflow**
   - Define audience → Review personas → Submit content → Simulate → Refine

### Out of Scope (Post-MVP)
- Image analysis (ad banners, posters)
- A/B comparison mode for testing two drafts side-by-side
- Community data import for persona training
- Frontend UI (MVP focuses on API/backend)

---

## Technical Approach

### Architecture
- **Multi-agent Simulation Pattern:**
  1. Persona Generation (based on audience description)
  2. Individual Reaction Simulation (5 parallel LLM API calls)
  3. Synthesis & Aggregation (scoring + insights)

### Technology Stack
- **Backend:** FastAPI (Python)
- **Database:** MySQL (tables: Users, Personas, Drafts, Simulation_Results)
- **LLM:** OpenAI GPT
- **Performance:** Async processing for parallel LLM calls

### Key Design Decisions
1. **Parallel Processing:** Run 5 persona simulations concurrently to meet <60s requirement
2. **Prompt Engineering:** Use structured prompts for consistent scoring format
3. **Persona Persistence:** Save personas to "Brand Library" for cross-draft reuse
4. **Cost Optimization:** Monitor LLM API usage and implement rate limiting

---

## Implementation Plan

See [tasks.md](./tasks.md) for detailed breakdown.

**High-Level Phases:**
1. Database schema design and setup
2. Persona generation API
3. Simulation engine with LLM integration
4. Scoring and aggregation logic
5. Insights generation
6. Testing and optimization

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| LLM API latency > 60s | High | Parallel processing + caching + timeout handling |
| Inconsistent persona quality | Medium | Structured prompts + validation + few-shot examples |
| High LLM costs | Medium | Rate limiting + usage monitoring + response caching |
| Data privacy concerns | High | Secure storage + encryption + compliance review |

---

## Dependencies

- OpenAI API access (GPT)
- MySQL database setup
- FastAPI project structure

---

## Affected Specs

This proposal creates the following new capability specs:
- `persona-engine.md` - Persona generation and management
- `simulation-feedback.md` - Reaction simulation and scoring
- `dashboard-insights.md` - Analytics and improvement suggestions

---

## Open Questions

1. Should we support custom persona templates or stick with AI-generated ones?
2. Should personas be shareable between users or strictly private?
3. Do we need admin controls for monitoring LLM usage?

---

## Approval

- [ ] Architecture reviewed
- [ ] Security implications considered
- [ ] Performance requirements validated
- [ ] Cost estimates approved
