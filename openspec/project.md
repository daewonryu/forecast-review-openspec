# Project Context

## Purpose
**FanEcho**: 광고글이나 공지 내용을 등록하기 전에 해당 글에 대해서 팬들이 어떻게 반응할지를 가상의 페르소나를 생성해서 미리 simulation 해볼 수 있는 서비스.

**Key Goals:**
- 사용자가 리뷰어들의 스타일을 정의하면 정의된 스타일별로 정해진 인원(5명)의 가상의 페르소나 생성
- 해당 페르소나들이 등록하려는 내용에 대해서 평가 후 주요한 측면(Trust, Excitement, Backlash Risk)에 대해서 scoring
- 해당 score를 검토해서 등록하려는 내용 개선
- Identify potential PR backlash risks before public announcements
- Total simulation time under 20 seconds

## Tech Stack
- **Frontend:** TypeScript, React
- **Backend:** Python, FastAPI
- **Database:** MySQL (or PostgreSQL per PRD)
- **LLM Models:** OpenAI GPT-4o / Claude 3.5 Sonnet
- **Prompting Strategy:** Multi-agent simulation (Persona Gen → Individual Reaction → Synthesis)


## Project Conventions

### Code Style
**Frontend (TypeScript/React):**
- ESLint + Prettier for code formatting
- `camelCase` for variables and functions
- `PascalCase` for components and classes
- Naming conventions: Standard TypeScript/React conventions

**Backend (Python/FastAPI):**
- `snake_case` for functions and variables
- `PascalCase` for class names
- Type hints required for all function signatures
- Follow PEP 8 style guide
- Black for formatting, Ruff/Flake8 for linting

### Architecture Patterns
- **Multi-agent Simulation Pattern:**
  - Step 1: Persona Generation (5 personas per audience)
  - Step 2: Individual Reaction Simulation (parallel API calls)
  - Step 3: Synthesis & Aggregation
  
- **Database Schema:**
  - Core tables: `Users`, `Personas`, `Drafts`, `Simulation_Results`
  - Persona persistence for reuse across simulations
  
- **API Design:**
  - RESTful endpoints for persona management and simulation execution
  - Async processing for parallel LLM calls

### Testing Strategy
- **Backend:** pytest for unit and integration tests
- **Frontend:** Jest/Vitest + React Testing Library (to be determined)
- **LLM Testing:** Mock LLM responses for deterministic testing
- **Performance Target:** Total simulation time < 20 seconds
- **Integration Tests:** Database operations and API endpoints

### Git Workflow
- **Branching Strategy:** Feature branches from main
- **Commit Conventions:** Conventional Commits format
  - `feat:` for new features
  - `fix:` for bug fixes
  - `refactor:` for code restructuring
  - `docs:` for documentation
- **OpenSpec Integration:** Follow OpenSpec workflow for proposals and spec-driven development

## Domain Context
**Synthetic User Testing & AI Personas:**
- AI-generated personas that simulate real user reactions to content
- Each persona represents a distinct fan archetype (e.g., The Veteran, The Casual, The Skeptic)

**Persona Traits:**
- Name/Archetype
- Loyalty Level (1-10)
- Core Values (e.g., Transparency, Value for Money, Exclusivity)

**Reaction Metrics:**
- **Trust:** 1-10 (persona's trust level after reading content)
- **Excitement:** 1-10 (enthusiasm about the announcement)
- **Backlash Risk:** 1-10 (likelihood of negative public reaction)

**Dual Response Pattern:**
- **Internal Monologue:** Brutally honest internal thoughts
- **Public Comment:** What they would actually post in a comment section

**Use Cases:**
- K-pop fan communities
- Mobile game announcements (gacha updates, etc.)
- Brand PR and social media posts
- Any content where fan sentiment is critical

## Important Constraints
- **MVP Scope:** Text-only content analysis (no image analysis in MVP)
- **Performance:** Simulation must complete in under 20 seconds
- **Persona Count:** Generate exactly 5 personas per audience definition
- **LLM Costs:** Monitor API usage and implement rate limiting if needed
- **Data Privacy:** User drafts and simulation results must be securely stored
- **Budget Constraints:** Small-to-medium teams without focus group budgets

## External Dependencies
- **OpenAI API:** GPT-4o for persona generation and reaction simulation
- **Anthropic API:** Claude 3.5 Sonnet as alternative LLM provider
- **MySQL Database:** Data persistence for users, personas, drafts, and results
- **LLM Rate Limits:** Must handle API throttling gracefully
- **Third-party Services:** (to be added as needed)
