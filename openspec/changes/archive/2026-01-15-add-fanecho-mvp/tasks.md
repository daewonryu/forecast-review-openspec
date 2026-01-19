# Implementation Tasks: Add FanEcho MVP

**Change ID:** `add-fanecho-mvp`

---

## Phase 1: Foundation & Setup

### Task 1.1: Database Schema Setup ✅
**Priority:** HIGH  
**Dependencies:** None  
**Estimated Effort:** 2-3 hours

- [x] Create `users` table (if not exists)
- [x] Create `personas` table with proper indexes
- [x] Create `drafts` table
- [x] Create `simulation_results` table
- [x] Create `insights` table (optional)
- [x] Add foreign key constraints
- [x] Write migration scripts
- [x] Test rollback procedures

**Verification:**
- All tables created successfully
- Indexes improve query performance
- Foreign keys enforce data integrity

---

### Task 1.2: FastAPI Project Scaffolding ✅
**Priority:** HIGH  
**Dependencies:** None  
**Estimated Effort:** 2-3 hours

- [x] Initialize FastAPI application structure
- [x] Set up database connection (SQLAlchemy + MySQL)
- [x] Configure environment variables (.env)
- [x] Create base models and schemas (Pydantic)
- [x] Set up logging infrastructure
- [x] Configure CORS if needed
- [x] Add health check endpoint

**Verification:**
- Server starts without errors
- Database connection successful
- `/health` endpoint returns 200

---

### Task 1.3: LLM Integration Setup ✅
**Priority:** HIGH  
**Dependencies:** Task 1.2  
**Estimated Effort:** 3-4 hours

- [x] Set up OpenAI API client (GPT-4o)
- [x] Set up Anthropic API client (Claude 3.5 Sonnet)
- [x] Create LLM service abstraction layer
- [x] Implement retry logic with exponential backoff
- [x] Add timeout handling (60s max)
- [x] Implement cost tracking/logging
- [x] Add fallback logic (OpenAI → Claude)

**Verification:**
- Can make successful API calls to both providers
- Retry logic works on transient failures
- Fallback switches providers correctly

---

## Phase 2: Persona Engine (Capability 1)

### Task 2.1: Persona Generation Endpoint ✅
**Priority:** HIGH  
**Dependencies:** Task 1.2, 1.3  
**Estimated Effort:** 4-6 hours

- [x] Implement `POST /api/personas/generate` endpoint
- [x] Design LLM prompt for persona generation
- [x] Validate audience description input (5-500 chars)
- [x] Generate exactly 5 personas via LLM
- [x] Parse LLM response into structured format
- [x] Validate persona traits (name, loyalty 1-10, core values)
- [x] Handle LLM errors gracefully

**Verification:**
- REQ-PE-001: Generate 5 unique personas within 10s
- REQ-PE-002: Each persona has required traits
- REQ-PE-004: Personas are sufficiently diverse

---

### Task 2.2: Persona Persistence ✅
**Priority:** HIGH  
**Dependencies:** Task 1.1, 2.1  
**Estimated Effort:** 2-3 hours

- [x] Implement database insert for personas
- [x] Generate unique `set_id` (UUID)
- [x] Link personas to user_id
- [x] Store audience_description with set
- [x] Add created_at timestamp
- [x] Implement `GET /api/personas/sets/{set_id}` endpoint

**Verification:**
- REQ-PE-003: Personas saved and retrievable
- Database constraints enforced
- User can access their persona sets

---

### Task 2.3: Persona Library Management ✅
**Priority:** MEDIUM  
**Dependencies:** Task 2.2  
**Estimated Effort:** 2-3 hours

- [x] Implement `GET /api/personas/sets` (list all sets for user)
- [x] Add pagination support
- [x] Add search/filter by audience_description
- [x] Implement soft delete for persona sets
- [ ] Add set metadata (title, description)

**Verification:**
- Users can browse their persona library
- Pagination works correctly
- Filtering returns relevant results

---

## Phase 3: Simulation & Feedback (Capability 2)

### Task 3.1: Draft Submission ✅
**Priority:** HIGH  
**Dependencies:** Task 1.1, 1.2  
**Estimated Effort:** 2 hours

- [x] Implement draft content validation (10-5000 chars)
- [x] Create draft record in database
- [x] Return draft_id
- [x] Link draft to user_id

**Verification:**
- REQ-SF-001: Drafts accepted and stored
- Input validation works correctly

---

### Task 3.2: Individual Persona Simulation ✅
**Priority:** HIGH  
**Dependencies:** Task 1.3, 2.2, 3.1  
**Estimated Effort:** 6-8 hours

- [x] Design LLM prompt for persona reactions
- [x] Include persona traits in prompt context
- [x] Request dual response (internal + public)
- [x] Request quantified scores (trust, excitement, backlash)
- [x] Request reasoning for scores
- [x] Parse LLM response into structured format
- [x] Validate score ranges (1-10)
- [x] Handle edge cases (missing fields, invalid scores)

**Verification:**
- REQ-SF-002: Both response types generated
- REQ-SF-003: Scores are valid integers 1-10
- Responses reflect persona traits

---

### Task 3.3: Parallel Simulation Engine ✅
**Priority:** HIGH  
**Dependencies:** Task 3.2  
**Estimated Effort:** 4-6 hours

- [x] Implement async processing for 5 concurrent LLM calls
- [x] Use `asyncio.gather()` for parallel execution
- [x] Handle partial failures gracefully
- [x] Aggregate results after all complete
- [x] Calculate average scores
- [x] Track simulation timing
- [x] Implement `POST /api/simulations/run` endpoint

**Verification:**
- REQ-SF-004: All 5 simulations run in parallel
- Total time < 20 seconds
- Partial results returned if some fail

---

### Task 3.4: Simulation Result Persistence ✅
**Priority:** HIGH  
**Dependencies:** Task 1.1, 3.3  
**Estimated Effort:** 2-3 hours

- [x] Insert simulation results into database
- [x] Link to draft_id and persona_id
- [x] Store all scores and text responses
- [x] Generate simulation_id (UUID)
- [x] Implement `GET /api/simulations/{simulation_id}`

**Verification:**
- REQ-SF-005: All results persisted
- Historical results retrievable
- Data integrity maintained

---

### Task 3.5: Error Handling & Retry Logic ✅
**Priority:** HIGH  
**Dependencies:** Task 3.3  
**Estimated Effort:** 3-4 hours

- [x] Implement timeout after 60s per LLM call
- [x] Retry failed requests once
- [x] Return partial results if needed
- [x] Log all failures for monitoring
- [x] Return user-friendly error messages
- [x] Add status field to results ("success" | "error")

**Verification:**
- REQ-SF-006: Graceful failure handling
- Partial results work correctly
- Errors logged properly

---

## Phase 4: Dashboard & Insights (Capability 3)

### Task 4.1: Aggregate Analytics ✅
**Priority:** HIGH  
**Dependencies:** Task 3.4  
**Estimated Effort:** 2-3 hours

- [x] Calculate average scores (trust, excitement, backlash)
- [x] Determine overall sentiment (positive/neutral/negative)
- [x] Calculate score distribution
- [x] Add to simulation response payload
- [x] Implement `GET /api/insights/{simulation_id}`

**Verification:**
- REQ-DI-001: Aggregated scores displayed
- Sentiment categorization accurate

---

### Task 4.2: Pain Point Identification ✅
**Priority:** HIGH  
**Dependencies:** Task 3.4, 1.3  
**Estimated Effort:** 5-7 hours

- [x] Design LLM prompt for pain point extraction
- [x] Analyze persona reasoning/feedback
- [x] Extract problematic phrases from draft
- [x] Group similar concerns across personas
- [x] Rank by backlash score
- [x] Link pain points to specific personas
- [x] Return structured pain point list

**Verification:**
- REQ-DI-002: Problematic text highlighted
- Pain points ranked correctly
- Linked to persona feedback

---

### Task 4.3: AI Improvement Tips Generation ✅
**Priority:** HIGH  
**Dependencies:** Task 4.2, 1.3  
**Estimated Effort:** 5-7 hours

- [x] Design LLM prompt for tip generation
- [x] Synthesize all persona feedback
- [x] Generate exactly 3 actionable tips
- [x] Rank by potential impact
- [x] Include rationale for each tip
- [x] Make tips specific to draft content
- [x] Avoid generic advice

**Verification:**
- REQ-DI-003: 3 actionable tips generated
- Tips address highest backlash areas
- Tips are specific and useful

---

### Task 4.4: Persona Drill-Down View ✅
**Priority:** MEDIUM  
**Dependencies:** Task 3.4  
**Estimated Effort:** 2-3 hours

- [x] Implement endpoint for persona details
- [x] Compare persona to group average
- [x] Identify outliers
- [x] Format for readable display

**Verification:**
- REQ-DI-005: Detailed persona view works
- Comparisons accurate

---

### Task 4.5: Sentiment Trend Tracking ✅
**Priority:** MEDIUM  
**Dependencies:** Task 4.1  
**Estimated Effort:** 3-4 hours

- [x] Track simulation history for same persona set
- [x] Calculate score deltas between iterations
- [x] Visualize improvement/deterioration
- [x] Identify effective tips

**Verification:**
- REQ-DI-004: Trends calculated correctly
- Improvement visible across iterations

---

## Phase 5: Testing & Optimization

### Task 5.1: Unit Tests ✅
**Priority:** HIGH  
**Dependencies:** All implementation tasks  
**Estimated Effort:** 5-8 hours

- [x] Test persona generation logic
- [x] Test simulation scoring
- [x] Test aggregation calculations
- [x] Test pain point extraction
- [x] Test tip generation
- [x] Mock LLM responses for deterministic tests
- [x] Achieve 80%+ code coverage

**Verification:**
- All tests pass
- Edge cases covered
- Mocks work correctly

---

### Task 5.2: Integration Tests ✅
**Priority:** HIGH  
**Dependencies:** Task 5.1  
**Estimated Effort:** 4-6 hours

- [x] Test end-to-end persona workflow
- [x] Test end-to-end simulation workflow
- [x] Test database operations
- [x] Test API endpoints
- [x] Test error scenarios

**Verification:**
- Full workflows work correctly
- Database state consistent
- APIs return correct responses

---

### Task 5.3: Performance Testing ✅
**Priority:** HIGH  
**Dependencies:** Task 5.2  
**Estimated Effort:** 3-4 hours

- [x] Load test parallel LLM calls
- [x] Verify <60s total time requirement
- [x] Test with slow LLM responses
- [x] Test concurrent user requests
- [x] Identify bottlenecks
- [x] Optimize database queries

**Verification:**
- Performance targets met
- System stable under load
- No memory leaks

---

### Task 5.4: LLM Prompt Optimization ✅
**Priority:** MEDIUM  
**Dependencies:** Task 5.3  
**Estimated Effort:** 4-6 hours

- [x] Test persona quality with different prompts
- [x] Tune for consistency and diversity
- [x] Test reaction accuracy
- [x] Optimize token usage (cost)
- [x] Add few-shot examples
- [x] Document final prompt templates

**Verification:**
- Persona quality high
- Reactions realistic
- Token costs optimized

---

## Phase 6: Monitoring & Documentation

### Task 6.1: Monitoring & Logging
**Priority:** MEDIUM  
**Dependencies:** All implementation  
**Estimated Effort:** 3-4 hours

- [ ] Add structured logging throughout
- [ ] Track LLM API costs per request
- [ ] Monitor response times
- [ ] Set up error alerting
- [ ] Create usage dashboard

**Verification:**
- All key events logged
- Costs tracked accurately
- Alerts trigger correctly

---

### Task 6.2: API Documentation ✅
**Priority:** MEDIUM  
**Dependencies:** All API endpoints  
**Estimated Effort:** 2-3 hours

- [x] Generate OpenAPI/Swagger docs
- [x] Add example requests/responses
- [x] Document error codes
- [x] Write API usage guide

**Verification:**
- Docs complete and accurate
- Examples work correctly

---

### Task 6.3: Deployment Preparation
**Priority:** HIGH  
**Dependencies:** All tasks  
**Estimated Effort:** 3-5 hours

- [ ] Create deployment checklist
- [ ] Set up environment configs (dev/prod)
- [ ] Configure secrets management
- [ ] Write deployment scripts
- [ ] Create backup procedures
- [ ] Document rollback process

**Verification:**
- Deployment runs smoothly
- Environment separation works
- Rollback tested

---

## Summary

**Total Estimated Effort:** 80-110 hours  
**Critical Path:** Database Setup → LLM Integration → Persona Generation → Parallel Simulation → Insights  
**MVP Timeline:** 3-4 weeks (single developer)

**Priority Breakdown:**
- HIGH priority: 18 tasks (core MVP functionality)
- MEDIUM priority: 6 tasks (quality-of-life features)
- COULD: Export features (deferred to post-MVP)
