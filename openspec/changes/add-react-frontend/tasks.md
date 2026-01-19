# Implementation Tasks: Add React Frontend UI

**Change ID:** `add-react-frontend`  
**Status:** Not Started

Track completion by checking boxes: `- [ ]` → `- [x]`

---

## Phase 1: Project Setup ✓

- [x] Initialize Vite + React + TypeScript project in `/frontend`
- [x] Configure package.json with required dependencies
- [ ] Install dependencies (axios, react-router-dom, @tanstack/react-query)
- [ ] Create TypeScript interfaces matching backend schemas in `/src/types/`
- [ ] Set up Axios API client with base configuration in `/src/api/`
- [ ] Configure environment variables for API_BASE_URL
- [ ] Update `.gitignore` for node_modules and build outputs

---

## Phase 2: Core Infrastructure

- [ ] Set up React Router with route configuration
- [ ] Create main App.tsx with QueryClientProvider
- [ ] Create Layout component with navigation
- [ ] Set up error boundary components
- [ ] Create loading spinner/skeleton components
- [ ] Add 404 Not Found page

---

## Phase 3: Persona Management UI

### Components
- [ ] Create `PersonaGenerator.tsx` component
  - [ ] Add form with textarea for audience description
  - [ ] Add character counter (5-500 chars)
  - [ ] Add submit button with loading state
  - [ ] Display generated personas after submission
  - [ ] Handle API errors with user-friendly messages

- [ ] Create `PersonaLibrary.tsx` component
  - [ ] Fetch and display list of persona sets
  - [ ] Add pagination (10 items per page)
  - [ ] Add selection UI for choosing active set
  - [ ] Show persona count and creation date
  - [ ] Add delete functionality with confirmation

- [ ] Create `PersonaCard.tsx` reusable component
  - [ ] Display persona name and archetype
  - [ ] Show loyalty level as visual indicator (bar/stars)
  - [ ] Display core values as tags
  - [ ] Add responsive card layout

### API Integration
- [ ] Implement `generatePersonas()` API call
- [ ] Implement `getPersonaSet()` API call
- [ ] Implement `listPersonaSets()` API call
- [ ] Implement `deletePersonaSet()` API call
- [ ] Add React Query hooks for caching and invalidation

---

## Phase 4: Simulation Runner UI

### Components
- [ ] Create `SimulationForm.tsx` component
  - [ ] Add textarea for draft content (10-5000 chars)
  - [ ] Add character counter
  - [ ] Add persona set selector dropdown
  - [ ] Add "Run Simulation" button with loading state
  - [ ] Show progress indicator during 10-20 second wait

- [ ] Create `SimulationResults.tsx` component
  - [ ] Display aggregate scores (avg trust, excitement, backlash)
  - [ ] Show individual persona reactions in cards
  - [ ] Display internal reaction vs public response
  - [ ] Add score badges with color coding (green/yellow/red)
  - [ ] Show simulation metadata (duration, timestamp)

- [ ] Create `PersonaReaction.tsx` component
  - [ ] Display persona name and reaction
  - [ ] Show scores with visual indicators
  - [ ] Display reasoning text
  - [ ] Format internal vs public responses clearly

### API Integration
- [ ] Implement `runSimulation()` API call
- [ ] Implement `getSimulationResults()` API call
- [ ] Implement `listSimulations()` API call
- [ ] Add React Query mutations for simulation runs
- [ ] Handle simulation timeout errors (60s max)

---

## Phase 5: Insights Dashboard UI

### Components
- [ ] Create `InsightsDashboard.tsx` component
  - [ ] Display aggregate analytics section
  - [ ] Show overall sentiment badge
  - [ ] Display average scores with charts/progress bars
  - [ ] Add generate insights button

- [ ] Create `PainPoints.tsx` component
  - [ ] List all identified pain points
  - [ ] Show severity indicators (low/medium/high)
  - [ ] Display affected personas
  - [ ] Show reasoning for each pain point
  - [ ] Add color coding by severity

- [ ] Create `ImprovementTips.tsx` component
  - [ ] Display 3 improvement tips
  - [ ] Show priority badges (low/medium/high)
  - [ ] Display expected impact
  - [ ] Group by category
  - [ ] Add copy-to-clipboard functionality

- [ ] Create `ScoreChart.tsx` component (optional)
  - [ ] Visualize score distribution
  - [ ] Show comparison across personas
  - [ ] Add hover tooltips with details

### API Integration
- [ ] Implement `generateInsights()` API call
- [ ] Implement `getInsights()` API call
- [ ] Add React Query for insights caching
- [ ] Handle insights generation errors

---

## Phase 6: Navigation & Layout

### Components
- [ ] Create `Header.tsx` component
  - [ ] Add FanEcho logo/title
  - [ ] Add navigation links (Home, Personas, Simulate, History)
  - [ ] Add health status indicator
  - [ ] Make responsive for mobile

- [ ] Create `Sidebar.tsx` component (optional)
  - [ ] Show quick actions
  - [ ] Display active persona set
  - [ ] Show recent simulations

- [ ] Create `HomePage.tsx`
  - [ ] Add welcome message
  - [ ] Show getting started guide
  - [ ] Add quick action buttons
  - [ ] Display recent activity

### Routing
- [ ] Set up routes:
  - [ ] `/` - Home page
  - [ ] `/personas` - Persona management
  - [ ] `/simulate` - Run simulation
  - [ ] `/insights/:draftId` - View insights
  - [ ] `/history` - Past simulations
  - [ ] `*` - 404 page

---

## Phase 7: Styling & UX Polish

### Styling
- [ ] Create base CSS reset and typography
- [ ] Define color palette (primary, secondary, success, warning, error)
- [ ] Create reusable button styles
- [ ] Add form input styles
- [ ] Create card component styles
- [ ] Add loading skeleton animations
- [ ] Implement responsive breakpoints (mobile, tablet, desktop)

### UX Enhancements
- [ ] Add transitions for page navigation
- [ ] Add hover effects on interactive elements
- [ ] Create toast/notification system for success/error messages
- [ ] Add confirmation dialogs for destructive actions (delete)
- [ ] Implement keyboard shortcuts for common actions
- [ ] Add scroll-to-top button for long pages

---

## Phase 8: Error Handling & Edge Cases

- [ ] Add global error boundary
- [ ] Handle API connection failures
- [ ] Handle API timeout errors (simulation > 60s)
- [ ] Handle empty states (no personas, no simulations)
- [ ] Add form validation with error messages
- [ ] Handle network offline state
- [ ] Add retry logic for failed requests
- [ ] Display user-friendly error messages

---

## Phase 9: Performance Optimization

- [ ] Implement code splitting for routes
- [ ] Lazy load heavy components
- [ ] Optimize bundle size (< 500KB gzipped)
- [ ] Add React Query stale time configuration
- [ ] Implement virtual scrolling for large lists (if needed)
- [ ] Optimize re-renders with React.memo where appropriate
- [ ] Add loading states for all async operations

---

## Phase 10: Testing & Documentation

- [ ] Test all API integrations manually
- [ ] Verify error scenarios (network failures, invalid inputs)
- [ ] Test responsive design on different screen sizes
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Performance testing (Lighthouse audit)
- [ ] Create README.md for frontend setup instructions
- [ ] Document environment variables
- [ ] Add inline code comments for complex logic
- [ ] Create component documentation

---

## Phase 11: Build & Deployment

- [ ] Configure production build settings
- [ ] Test production build locally (`npm run build && npm run preview`)
- [ ] Set up environment variables for production
- [ ] Create deployment configuration
- [ ] Configure CORS on backend for production domain
- [ ] Deploy frontend to hosting platform (Vercel/Netlify)
- [ ] Verify production deployment works end-to-end
- [ ] Set up monitoring and error tracking (optional)

---

## Definition of Done

Each task is complete when:
- [ ] Code is written and working locally
- [ ] TypeScript has no errors
- [ ] Component renders correctly
- [ ] API integration works as expected
- [ ] Error states are handled gracefully
- [ ] Loading states provide user feedback
- [ ] Responsive design works on target devices
- [ ] Code follows project conventions (camelCase, PascalCase)
- [ ] No console errors or warnings

---

## Notes

- Start with Phase 1-2 for infrastructure
- Phases 3-5 can be developed in parallel by different developers
- Phase 6-7 should come after core features are working
- Phase 8-11 are polish and production-readiness

**Estimated Total Time:** 18-24 hours
