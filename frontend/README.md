# FanEcho Frontend

React + TypeScript web interface for the FanEcho AI-powered fan reaction simulator.

## Features

- **Persona Management** (Step 1): Generate and manage diverse AI personas representing your audience
- **Simulation Runner** (Step 2): Test draft content and see how personas react
- **Simulation History** (Step 3): Browse past simulations and click to view detailed results with insights
- **Insights Dashboard**: View AI-generated improvement tips and pain point analysis for any simulation
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Tech Stack

- **Framework**: React 19
- **Language**: TypeScript 5.9
- **Build Tool**: Vite 7
- **Routing**: React Router v6
- **State Management**: TanStack Query (React Query) v5
- **HTTP Client**: Axios

## Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000` (or configured via environment variable)

## Installation

```bash
# Install dependencies
npm install

# Create environment file (optional - defaults to localhost:8000)
cp .env.example .env
```

## Configuration

Edit `.env` to configure the API endpoint:

```bash
VITE_API_URL=http://localhost:8000
```

## Development

```bash
# Start development server (http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## Project Structure

```
src/
├── api/
│   └── index.ts              # API client and endpoint functions
├── components/
│   ├── ErrorBoundary.tsx     # Error boundary component
│   ├── LoadingSpinner.tsx    # Loading indicator
│   ├── Layout.tsx            # Main layout with navigation
│   ├── PersonaGenerator.tsx  # Persona generation form
│   ├── PersonaLibrary.tsx    # Browse persona sets
│   ├── PersonaCard.tsx       # Display persona details
│   ├── SimulationForm.tsx    # Run simulation form
│   ├── SimulationResults.tsx # Display simulation results
│   ├── PersonaReaction.tsx   # Individual persona reaction
│   ├── InsightsDashboard.tsx # Insights overview
│   ├── PainPoints.tsx        # Pain points list
│   └── ImprovementTips.tsx   # Improvement tips list
├── pages/
│   ├── HomePage.tsx          # Landing page
│   ├── PersonasPage.tsx      # Persona management page
│   ├── SimulatePage.tsx      # Simulation runner page
│   ├── InsightsPage.tsx      # Insights dashboard page
│   ├── HistoryPage.tsx       # Simulation history page
│   └── NotFound.tsx          # 404 page
├── types/
│   └── types.ts              # TypeScript type definitions
├── App.tsx                   # Main app component with routing
├── main.tsx                  # Entry point
└── index.css                 # Global styles
```

## Usage Guide

### 1. Generate Personas

1. Navigate to "Personas" page
2. Enter an audience description (e.g., "Tech enthusiasts interested in AI")
3. Click "Generate 5 Personas"
4. Wait 5-10 seconds for generation
5. Review the generated personas in the library below
6. **Click on any persona set to view detailed individual personas** with their traits, loyalty levels, and core values

### 2. Run Simulation

1. Navigate to "Simulate" page  
2. Select a persona set from dropdown
3. Enter your draft content (10-5000 characters)
4. Click "Run Simulation"
5. Wait 10-20 seconds for results
6. Review scores and individual reactions

### 3. View Insights

1. After simulation completes, click "View Insights & Improvement Tips"
2. Review AI summary and aggregate analytics
3. Read pain points with severity levels
4. Copy improvement tips for implementation

### 4. Browse History

1. Navigate to "History" page
2. View all past simulations
3. See scores and timestamps

## API Integration

The frontend communicates with the backend API at the configured `VITE_API_URL`. All API calls include:

- Health checks every 30 seconds
- Automatic retry on failure (1 retry)
- 5-minute cache for persona sets
- Loading and error states

## User ID (MVP)

Currently hard-coded to `user_id=1` for MVP. Authentication will be added in a future release.

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- Initial page load: < 3 seconds
- Route navigation: < 500ms
- Production bundle: ~325KB (103KB gzipped)

## Troubleshooting

### API Connection Failed

- Ensure backend is running on the configured port
- Check CORS is enabled on backend for frontend origin
- Verify `VITE_API_URL` in `.env` is correct

### Build Errors

- Delete `node_modules` and `package-lock.json`, then run `npm install`
- Clear TypeScript cache: `rm -rf node_modules/.cache`
- Ensure all dependencies are installed

### Development Server Issues

- Try a different port: `npm run dev -- --port 3000`
- Clear browser cache and reload
- Check for port conflicts with other applications

## Contributing

Follow the OpenSpec change proposal process:
1. Review `/openspec/changes/add-react-frontend/`
2. Check tasks in `tasks.md`
3. Follow TypeScript conventions (camelCase, type safety)
4. Test changes with backend API

## License

Copyright © 2026 FanEcho. All rights reserved
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
