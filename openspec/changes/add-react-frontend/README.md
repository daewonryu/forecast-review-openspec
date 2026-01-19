# Add React Frontend UI

This change adds a complete React-based web UI for the FanEcho service.

## Files in this Change

- `proposal.md` - Full proposal with motivation, scope, and technical approach
- `tasks.md` - Implementation checklist organized by phase
- `specs/` - Detailed specifications for each UI capability:
  - `frontend-app/` - Core application infrastructure
  - `persona-management-ui/` - Persona generation and library
  - `simulation-runner-ui/` - Draft input and results display
  - `insights-dashboard-ui/` - Analytics and improvement tips

## Quick Links

- [Full Proposal](./proposal.md)
- [Task Checklist](./tasks.md)
- [Frontend App Spec](./specs/frontend-app/spec.md)
- [Persona UI Spec](./specs/persona-management-ui/spec.md)
- [Simulation UI Spec](./specs/simulation-runner-ui/spec.md)
- [Insights UI Spec](./specs/insights-dashboard-ui/spec.md)

## Status

**Current Status:** Proposed (awaiting approval)

**Progress:**
- [x] Project setup with Vite + React + TypeScript
- [x] Dependencies configured in package.json
- [ ] API client and types implementation
- [ ] Component development
- [ ] Styling and UX polish

## Next Steps

1. Review and approve this proposal
2. Install dependencies: `cd frontend && npm install`
3. Follow tasks.md sequentially
4. Run development server: `npm run dev`
5. Build for production: `npm run build`

## Dependencies

**External:**
- React 19+
- React Router v6
- TanStack Query v5
- Axios 1.6+

**Backend:**
- Requires backend API at http://localhost:8000 (configurable)
- CORS must be enabled for frontend origin

## Timeline

**Estimated:** 18-24 hours total
- Phase 1-2: Infrastructure (4 hours)
- Phase 3-5: Components (10 hours)
- Phase 6-7: Layout & Styling (4 hours)
- Phase 8-11: Polish & Deploy (4 hours)
