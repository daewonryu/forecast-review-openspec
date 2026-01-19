# Capability: Frontend Application

**Capability ID:** `frontend-app`  
**Change ID:** `add-react-frontend`

---

## ADDED Requirements

### Requirement: React Application Infrastructure

The system MUST provide a React-based single-page application (SPA) that serves as the primary user interface for FanEcho services.

**Acceptance Criteria:**
- Built with React 19+ and TypeScript
- Uses Vite as build tool for development and production
- Implements client-side routing with React Router v6
- Configurable API base URL via environment variables
- Production bundle size < 500KB (gzipped)

#### Scenario: Initialize and Load Application

**Given** a user navigates to the frontend URL  
**When** the application loads  
**Then** the React app renders within 3 seconds  
**And** the main layout with navigation is displayed  
**And** no console errors appear  
**And** the health check endpoint is called successfully

---

### Requirement: API Client Configuration

The application MUST provide a centralized HTTP client for communicating with the backend API.

**Acceptance Criteria:**
- Axios instance configured with base URL from environment
- Default headers include Content-Type: application/json
- All API endpoints have corresponding client functions
- TypeScript interfaces match backend schemas exactly
- Request/response interceptors for error handling

#### Scenario: Make API Request with Client

**Given** the frontend application is running  
**When** a component calls an API function (e.g., `generatePersonas()`)  
**Then** the request is sent to the correct backend endpoint  
**And** the base URL is prepended from environment config  
**And** proper headers are included  
**And** the response is typed according to TypeScript interfaces

---

### Requirement: State Management with React Query

The application MUST use TanStack Query (React Query) for server state management and caching.

**Acceptance Criteria:**
- QueryClientProvider wraps the application
- API calls use `useQuery` for reads and `useMutation` for writes
- Stale time configured appropriately per endpoint
- Cache invalidation on mutations (e.g., delete persona set)
- Loading and error states managed automatically

#### Scenario: Fetch Data with Caching

**Given** a user navigates to the persona library  
**When** the component mounts  
**Then** a query is executed to fetch persona sets  
**And** a loading indicator displays during fetch  
**And** the data is cached for 5 minutes  
**And** subsequent navigations to the page use cached data  
**And** errors are handled with user-friendly messages

---

### Requirement: Client-Side Routing

The application MUST implement client-side routing for seamless navigation without page reloads.

**Acceptance Criteria:**
- Routes defined for all major pages (home, personas, simulate, insights, history)
- Browser back/forward buttons work correctly
- 404 page for unknown routes
- Active route highlighted in navigation
- Route transitions complete within 500ms

#### Scenario: Navigate Between Pages

**Given** a user is on the home page  
**When** the user clicks "Personas" in navigation  
**Then** the URL changes to `/personas`  
**And** the persona management page renders  
**And** the page renders without full reload  
**And** the "Personas" link is highlighted as active  
**And** the browser back button returns to home page

---

### Requirement: Error Boundaries

The application MUST implement error boundaries to gracefully handle component errors without crashing the entire app.

**Acceptance Criteria:**
- Global error boundary wraps the application
- Route-specific error boundaries for isolated failures
- Error UI displays user-friendly message
- Error details logged to console for debugging
- "Try Again" button to recover from errors

#### Scenario: Handle Component Error

**Given** a component encounters an error during rendering  
**When** the error is thrown  
**Then** the error boundary catches it  
**And** a fallback UI displays instead of blank page  
**And** the error message is user-friendly (not technical stack trace)  
**And** the rest of the application continues working  
**And** the error is logged to console for debugging

---

### Requirement: Loading States

The application MUST provide clear visual feedback during asynchronous operations.

**Acceptance Criteria:**
- Loading spinners for page-level operations
- Skeleton loaders for content areas
- Disabled buttons with loading text during submissions
- Progress indicators for long-running operations (simulations)
- Timeout handling after 60 seconds

#### Scenario: Display Loading State During API Call

**Given** a user submits a form to generate personas  
**When** the API request is in progress  
**Then** the submit button shows "Generating..." text  
**And** the button is disabled to prevent duplicate submissions  
**And** a loading spinner displays  
**And** the form inputs are disabled  
**And** when the request completes, normal UI is restored

---

### Requirement: Environment Configuration

The application MUST support environment-specific configuration for different deployment targets.

**Acceptance Criteria:**
- `.env` file for local development configuration
- `VITE_API_URL` environment variable for backend URL
- Default fallback to `http://localhost:8000` if not set
- Build-time environment variable injection
- No secrets or sensitive data in environment files

#### Scenario: Configure API URL for Production

**Given** the application is being deployed to production  
**When** `VITE_API_URL=https://api.fanecho.com` is set  
**Then** all API calls use the production backend URL  
**And** the development default is not used  
**And** no hardcoded URLs exist in the codebase

---

## Technology Stack

- **Framework:** React 19+
- **Language:** TypeScript 5.9+
- **Build Tool:** Vite 7+
- **Routing:** React Router v6
- **State Management:** TanStack Query v5 (React Query)
- **HTTP Client:** Axios 1.6+
- **Package Manager:** npm

---

## File Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.ts          # Axios configuration and API functions
│   ├── components/            # Reusable UI components
│   ├── pages/                 # Route pages
│   ├── types/                 # TypeScript interfaces
│   │   └── index.ts           # API response types
│   ├── App.tsx                # Main app component with routing
│   ├── main.tsx               # Entry point with QueryClientProvider
│   └── index.css              # Global styles
├── public/                    # Static assets
├── .env                       # Local environment variables
├── .env.example               # Template for environment variables
├── package.json               # Dependencies and scripts
├── tsconfig.json              # TypeScript configuration
├── vite.config.ts             # Vite build configuration
└── README.md                  # Setup instructions
```

---

## Environment Variables

```bash
# .env
VITE_API_URL=http://localhost:8000
```

---

## Dependencies

**Production:**
```json
{
  "react": "^19.2.0",
  "react-dom": "^19.2.0",
  "react-router-dom": "^6.21.2",
  "@tanstack/react-query": "^5.17.19",
  "axios": "^1.6.5"
}
```

**Development:**
```json
{
  "@vitejs/plugin-react": "^5.1.1",
  "typescript": "~5.9.3",
  "vite": "^7.2.4"
}
```

---

## Performance Requirements

- Initial page load: < 3 seconds
- Route navigation: < 500ms
- API response rendering: < 2 seconds
- Production bundle: < 500KB (gzipped)
- Time to Interactive (TTI): < 5 seconds

---

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- No Internet Explorer support

---

## Build Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

---

## API Integration Patterns

### Query Pattern (GET requests)
```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['personaSets', userId],
  queryFn: () => listPersonaSets(userId),
  staleTime: 5 * 60 * 1000, // 5 minutes
});
```

### Mutation Pattern (POST/PUT/DELETE requests)
```typescript
const mutation = useMutation({
  mutationFn: (request) => generatePersonas(request),
  onSuccess: (data) => {
    queryClient.invalidateQueries(['personaSets']);
  },
});
```

---

## Security Considerations

### MVP (Current)
- No authentication implemented (user_id hard-coded to 1)
- CORS must be enabled on backend for localhost:5173
- No sensitive data stored in localStorage
- Environment variables only contain public configuration

### Post-MVP (Future)
- Implement JWT authentication
- Store tokens securely in httpOnly cookies
- Add CSRF protection
- Implement session management
- Add input sanitization
