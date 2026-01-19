# Proposal: Add React Frontend UI for FanEcho

**Change ID:** `add-react-frontend`  
**Status:** Proposed  
**Created:** 2026-01-15

---

## Why

The FanEcho MVP backend API is complete and functional, but users cannot interact with the service without making direct API calls. A modern, intuitive web UI is needed to enable non-technical users to:
- Generate and manage persona sets through a guided workflow
- Submit draft content and run simulations with visual feedback
- Review simulation results with clear visualizations of scores and insights
- Iterate on content based on AI-generated improvement tips

---

## What Changes

- **Add Frontend Application capability:** React + TypeScript web application with component-based architecture
- **Add User Interaction capability:** Forms, navigation, and real-time feedback for all backend features
- **Add Data Visualization capability:** Charts and dashboards for simulation results and insights
- **New dependencies:** React Router, TanStack Query, Axios for API integration
- **Build tooling:** Vite for development and production builds

## Impact

**Affected Specs:**
- `frontend-app` (new capability)
- `persona-management-ui` (new capability)
- `simulation-runner-ui` (new capability)
- `insights-dashboard-ui` (new capability)

**Affected Code:**
- New `/frontend` directory with React application
- Integration with existing backend API endpoints
- Environment configuration for API base URL

---

## Overview

Implement a React-based web interface for **FanEcho** that provides an intuitive, responsive UI for all backend capabilities. The frontend will enable users to generate personas, run simulations, and view insights without technical knowledge of the API.

---

## Motivation

### Problem Statement
- **No User Interface:** The backend API is complete but inaccessible to non-technical users
- **Poor Developer Experience:** Testing the API requires manual API calls via curl or Postman
- **Limited Adoption:** Without a UI, the service cannot be used by the target audience (brand managers, social media teams)
- **No Visual Feedback:** Results are JSON only, making it hard to interpret scores and insights

### Success Criteria
1. Users can complete the full workflow (generate personas → run simulation → view history → view insights) without technical knowledge
2. Simulation results display within 2 seconds of API response completion
3. UI is responsive and works on desktop and tablet devices
4. All backend API endpoints have corresponding UI components

---

## Scope

### In Scope (MVP Frontend)
1. **Persona Management UI**
   - Form to generate new persona sets with audience description input
   - Library view to browse and select existing persona sets
   - Visual display of persona traits (name, archetype, loyalty, values)

2. **Simulation Runner UI**
   - Text area for draft content input with character count
   - Persona set selection from library
   - Run simulation button with loading state
   - Results display with individual persona reactions
   - Score visualization (trust, excitement, backlash risk)

3. **Insights Dashboard UI**
   - Aggregated analytics display (average scores, sentiment)
   - Pain points list with severity indicators
   - Improvement tips with priority badges
   - Visual charts for score distribution

4. **Core Navigation & Layout**
   - Main navigation between pages
   - Responsive layout with mobile-friendly design
   - Error handling and loading states
   - Health check status indicator

### Out of Scope (Post-MVP)
- User authentication and login system
- Multi-user support with user management
- Draft history and comparison view
- Advanced filtering and search in persona library
- Export results to PDF or other formats
- Real-time collaboration features
- Dark mode theme

---

## Technical Approach

### Architecture
- **Component-Based Architecture:**
  - Reusable UI components for personas, simulations, insights
  - React Router for client-side navigation
  - TanStack Query for server state management and caching
  - Axios for API communication

### Technology Stack
- **Framework:** React 19+ with TypeScript
- **Build Tool:** Vite for fast development and optimized production builds
- **Routing:** React Router v6 for SPA navigation
- **State Management:** TanStack Query (React Query) for API state
- **HTTP Client:** Axios for backend communication
- **Styling:** CSS modules with potential for Tailwind CSS

### Key Design Decisions
1. **TypeScript First:** All code uses TypeScript for type safety and better developer experience
2. **API-Driven:** UI mirrors backend API structure exactly, no custom aggregations
3. **Optimistic UI:** Show loading states immediately for better perceived performance
4. **Error Boundaries:** Graceful error handling at component and route level
5. **No Authentication (MVP):** Hard-coded user_id=1 for MVP, auth comes later

---

## User Workflows

### Primary Workflow: First-Time User
1. User lands on home page with welcome message
2. User navigates to "Generate Personas" section
3. User enters audience description (e.g., "Tech enthusiasts interested in AI")
4. System generates 5 personas and displays them visually
5. User navigates to "Run Simulation" section
6. User selects the persona set from library
7. User enters draft content for testing
8. User clicks "Run Simulation"
9. System shows loading indicator (10-20 seconds)
10. Results display with scores and individual reactions
11. User navigates to "History" to see all past simulations
12. User clicks on any simulation to view detailed insights and improvement tips
13. User iterates on content based on suggestions

### Secondary Workflow: Returning User
1. User navigates to "My Personas" section
2. User sees library of previously generated persona sets
3. User selects an existing set
4. User proceeds directly to simulation with new content
5. User compares results across multiple simulation runs

---

## Dependencies

### External Dependencies
- React (UI framework)
- React DOM (rendering)
- React Router DOM (routing)
- Axios (HTTP client)
- TanStack Query (state management)
- Vite (build tooling)

### Internal Dependencies
- Backend API must be running at `http://localhost:8000` (configurable via env)
- All backend endpoints must support CORS for local development

---

## Security Considerations

### MVP Approach
- No authentication (user_id hard-coded to 1)
- No authorization checks
- No sensitive data validation beyond backend validation
- CORS enabled for localhost development

### Post-MVP Requirements
- Add JWT-based authentication
- Implement user session management
- Add CSRF protection
- Validate all user inputs client-side
- Add rate limiting awareness

---

## Performance Requirements

- Initial page load: < 3 seconds
- Navigation between pages: < 500ms
- API response rendering: < 2 seconds
- Simulation status updates: Real-time feedback during 10-20 second simulation
- Persona library pagination: 50 items per page max

---

## Open Questions

1. **Styling Approach:** Should we use Tailwind CSS, plain CSS, or CSS-in-JS?
   - *Recommendation:* Start with plain CSS modules, add Tailwind if needed
2. **User ID Management:** How should we handle user_id in MVP without auth?
   - *Recommendation:* Hard-code to 1, add localStorage for future multi-user testing
3. **Error Recovery:** Should we implement retry logic for failed API calls?
   - *Recommendation:* Yes, TanStack Query provides built-in retry with exponential backoff
4. **Mobile Support:** What's the minimum screen size to support?
   - *Recommendation:* 768px (tablet) minimum, desktop-optimized

---

## Success Metrics

### User Experience Metrics
- Users complete full workflow without errors: > 90%
- Average time to first simulation: < 3 minutes
- User satisfaction with results display: > 4/5 rating

### Technical Metrics
- API call success rate: > 99%
- Frontend error rate: < 1%
- Average page load time: < 3 seconds
- Bundle size: < 500KB (gzipped)

---

## Timeline Estimate

- **Phase 1:** Project setup and API client (2 hours)
- **Phase 2:** Persona management components (3 hours)
- **Phase 3:** Simulation runner components (4 hours)
- **Phase 4:** Insights dashboard components (3 hours)
- **Phase 5:** Layout, routing, and styling (4 hours)
- **Phase 6:** Testing and polish (2 hours)

**Total Estimate:** 18 hours

---

## Rollout Plan

1. **Development:** Build UI in `/frontend` directory alongside existing backend
2. **Local Testing:** Run backend on :8000 and frontend on :5173 concurrently
3. **Integration Testing:** Verify all API endpoints work correctly from UI
4. **Deployment:** Deploy frontend as static site (Vercel/Netlify) pointing to backend API
5. **Monitoring:** Track API call patterns and error rates from UI

---

## Alternatives Considered

### Alternative 1: Server-Side Rendered (SSR) with Next.js
**Pros:** Better SEO, faster initial page load
**Cons:** More complex setup, overkill for MVP, requires Node.js server
**Decision:** Rejected - MVP doesn't need SEO, SPA is simpler

### Alternative 2: Vue.js or Svelte
**Pros:** Smaller bundle size, simpler syntax
**Cons:** Less ecosystem support, team less familiar
**Decision:** Rejected - React has better TypeScript support and larger community

### Alternative 3: Plain HTML/CSS/JS without framework
**Pros:** No build step, faster to prototype
**Cons:** Hard to maintain, no component reuse, manual state management
**Decision:** Rejected - MVP needs maintainable, scalable architecture

---

## References

- Backend API Documentation: `/backend/API_DOCUMENTATION.md`
- Backend Schemas: `/backend/app/schemas.py`
- Project Context: `/openspec/project.md`
- Archived Backend Proposal: `/openspec/changes/archive/2026-01-15-add-fanecho-mvp/`
