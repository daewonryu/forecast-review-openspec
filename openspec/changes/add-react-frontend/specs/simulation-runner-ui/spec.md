# Capability: Simulation Runner UI

**Capability ID:** `simulation-runner-ui`  
**Change ID:** `add-react-frontend`

---

## ADDED Requirements

### Requirement: Draft Content Input Form

The UI MUST provide a form for users to input draft content and configure simulation parameters.

**Acceptance Criteria:**
- Textarea for draft content (10-5000 characters)
- Character counter with min/max indicators
- Persona set selector dropdown or picker
- "Run Simulation" button with loading state
- Form validation before submission
- Clear indication of required fields

#### Scenario: Submit Draft for Simulation

**Given** a user has selected a persona set from the library  
**And** is on the simulation page  
**When** the user enters draft content: "Exciting news! We're launching our revolutionary AI assistant next month. Get early access now!" (120 chars)  
**And** the persona set is pre-selected  
**And** clicks "Run Simulation"  
**Then** the form validates successfully  
**And** the button changes to "Running Simulation..."  
**And** the button is disabled  
**And** a progress indicator appears  
**And** the simulation API call is made with correct parameters

---

### Requirement: Persona Set Selection in Simulation Form

Users MUST be able to select which persona set to use for the simulation.

**Acceptance Criteria:**
- Dropdown or card selector showing available persona sets
- Display audience description for each option
- Pre-select if coming from persona library
- Required field validation
- Error if no persona sets exist

#### Scenario: Select Persona Set in Form

**Given** a user has 3 persona sets saved  
**When** the user opens the simulation page  
**Then** a persona set selector displays all 3 options  
**And** each option shows the audience description  
**And** if a set was previously selected, it's pre-selected  
**When** the user changes selection  
**Then** the new selection is highlighted  
**And** the selected set ID is used for simulation

#### Scenario: Handle No Persona Sets

**Given** a user has no saved persona sets  
**When** the user navigates to simulation page  
**Then** a message displays: "Please generate personas first"  
**And** a link/button to navigate to persona generation  
**And** the simulation form is disabled or hidden

---

### Requirement: Real-Time Simulation Progress Feedback

During the 10-20 second simulation, users MUST receive visual feedback that the process is active.

**Acceptance Criteria:**
- Progress indicator (spinner or progress bar)
- Status message showing current phase (if available)
- Estimated time remaining (optional)
- Cancel button (optional for MVP)
- Timeout handling after 60 seconds

#### Scenario: Display Simulation Progress

**Given** a user has submitted a simulation request  
**When** the simulation is running  
**Then** a loading spinner displays prominently  
**And** the button shows "Running Simulation..." text  
**And** a message displays: "Analyzing your draft with 5 personas..."  
**And** the form inputs are disabled  
**When** 60 seconds pass without response  
**Then** a timeout error displays  
**And** the form becomes editable again

---

### Requirement: Display Simulation Results

After simulation completes, results MUST be displayed in a comprehensive, scannable format.

**Acceptance Criteria:**
- Aggregate scores displayed prominently (avg trust, excitement, backlash)
- Individual persona reactions shown in cards
- Internal reaction vs public response clearly separated
- Scores visualized with colors (green = good, yellow = caution, red = risk)
- Simulation metadata (duration, timestamp)

#### Scenario: View Completed Simulation Results

**Given** a simulation has completed successfully  
**When** the results are received  
**Then** the loading state disappears  
**And** aggregate scores display at the top:
  - Avg Trust: 6.4/10
  - Avg Excitement: 7.2/10
  - Avg Backlash Risk: 2.8/10
**And** 5 persona reaction cards display below  
**And** each card shows persona name, scores, reactions, and reasoning  
**And** simulation duration displays: "Completed in 12.5 seconds"  
**And** timestamp shows when simulation ran

---

### Requirement: Individual Persona Reaction Cards

Each persona's reaction MUST be displayed with all simulation details.

**Acceptance Criteria:**
- Persona name and archetype
- Trust, excitement, and backlash scores (1-10)
- Internal reaction (private thoughts)
- Public response (what they would post)
- Reasoning for the scores
- Visual score indicators (progress bars or badges)

#### Scenario: Display Persona Reaction Details

**Given** simulation results include "The Veteran" persona  
**When** the results card is displayed  
**Then** the card shows:
  - Header: "The Veteran - Long-time AI enthusiast"
  - Scores section with colored indicators:
    - Trust: 6/10 (yellow)
    - Excitement: 7/10 (green)
    - Backlash Risk: 3/10 (green)
  - Internal Reaction: "Hmm, 'revolutionary' is a big claim..."
  - Public Response: "Interesting! Looking forward to learning more..."
  - Reasoning: "The announcement is intriguing but lacks technical details..."
**And** all text is readable and properly formatted

---

### Requirement: Score Visualization with Color Coding

Scores MUST be visualized with intuitive color coding for quick interpretation.

**Acceptance Criteria:**
- Trust: Green (8-10), Yellow (5-7), Red (1-4)
- Excitement: Green (8-10), Yellow (5-7), Red (1-4)
- Backlash Risk: Red (8-10), Yellow (5-7), Green (1-4) [inverted]
- Visual indicators: progress bars, badges, or score circles
- Aggregate scores use same color scheme

#### Scenario: Interpret Score Colors

**Given** a simulation returns varying scores  
**When** results are displayed  
**Then** Trust score of 9 shows green color  
**And** Trust score of 5 shows yellow color  
**And** Trust score of 2 shows red color  
**And** Backlash Risk of 9 shows red color (high risk)  
**And** Backlash Risk of 2 shows green color (low risk)  
**And** users can quickly identify concerning scores by color

---

### Requirement: Link to Insights Generation

After viewing simulation results, users MUST have easy access to generate insights.

**Acceptance Criteria:**
- "View Insights" or "Generate Insights" button
- Button navigates to insights page for this draft
- Draft ID passed to insights component
- Insights are generated on-demand (not automatic)

#### Scenario: Navigate to Insights from Results

**Given** a user is viewing simulation results for draft ID 456  
**When** the user clicks "View Insights" button  
**Then** the application navigates to `/insights/456`  
**And** the insights generation is triggered  
**And** the user sees the insights dashboard

---

### Requirement: Simulation History Access

Users MUST be able to access previously run simulations.

**Acceptance Criteria:**
- "View History" or "Past Simulations" page
- List of past simulations with metadata
- Click to view full results of any past simulation
- Pagination for long lists
- Show draft preview and timestamp

#### Scenario: Browse Simulation History

**Given** a user has run 5 simulations  
**When** the user navigates to simulation history page  
**Then** 5 simulation entries are listed  
**And** each entry shows:
  - Draft content preview (first 100 chars)
  - Aggregate scores summary
  - Timestamp
  - Persona set used
**When** user clicks on an entry  
**Then** the full simulation results display

---

### Requirement: Error Handling for Simulation Failures

The UI MUST gracefully handle various simulation failure scenarios.

**Acceptance Criteria:**
- API errors display user-friendly messages
- Network failures show retry option
- Timeout errors (> 60s) handled explicitly
- Partial results shown if some personas fail
- Form remains editable after errors

#### Scenario: Handle Simulation Timeout

**Given** a user has submitted a simulation  
**When** 60 seconds pass without API response  
**Then** the loading state stops  
**And** an error message displays:
  "Simulation timed out. This usually means the AI service is overloaded. Please try again."
**And** a "Try Again" button is available  
**And** the form becomes editable again

#### Scenario: Handle Partial Results

**Given** a simulation returns with 4 successful and 1 failed persona  
**When** results are displayed  
**Then** 4 persona cards show normal results  
**And** the 5th card shows an error state:
  "This persona simulation failed. Overall results are based on 4 personas."
**And** aggregate scores are calculated from successful personas only

---

### Requirement: Form Validation and Input Constraints

The simulation form MUST validate user input before submission.

**Acceptance Criteria:**
- Minimum 10 characters for draft content
- Maximum 5000 characters enforced
- Real-time character count
- Persona set selection required
- Empty form submission prevented
- Validation errors shown inline

#### Scenario: Validate Draft Content Length

**Given** a user enters only 5 characters in draft content  
**When** the user tries to submit  
**Then** form does not submit  
**And** error message displays: "Draft content must be at least 10 characters"  
**And** the textarea gets error styling (red border)

#### Scenario: Validate Persona Set Selection

**Given** no persona set is selected  
**When** user tries to submit simulation  
**Then** form does not submit  
**And** error message displays: "Please select a persona set"  
**And** the selector is highlighted with error styling

---

### Requirement: Responsive Design for Simulation UI

Simulation UI MUST work across different screen sizes.

**Acceptance Criteria:**
- Form is usable on tablets (768px+)
- Results display properly on mobile (stack vertically)
- Score indicators readable on small screens
- Buttons touch-friendly (min 44px)
- No horizontal scrolling

#### Scenario: View Results on Tablet

**Given** a user views simulation results on a 768px screen  
**When** results are displayed  
**Then** aggregate scores show in a row at top  
**And** persona cards stack 2 per row or single column  
**And** all text is readable without zooming  
**And** buttons are large enough for touch interaction

---

## Component Structure

### SimulationForm Component

```typescript
interface SimulationFormProps {
  userId: number;
  preSelectedSetId?: string;
  onSimulationComplete?: (simulationId: string) => void;
}
```

**State:**
- `draftContent`: string
- `selectedSetId`: string | null
- `mutation`: useMutation hook

**Behavior:**
- Validates form inputs
- Calls `runSimulation()` API
- Shows progress during 10-20s wait
- Displays results on completion

---

### SimulationResults Component

```typescript
interface SimulationResultsProps {
  simulationId?: string;
  results?: SimulationResponse;
  onGenerateInsights?: () => void;
}
```

**Display:**
- Aggregate scores section
- Individual persona reaction cards
- Metadata (duration, timestamp)
- "View Insights" button

---

### PersonaReaction Component

```typescript
interface PersonaReactionProps {
  result: SimulationResult;
}
```

**Display:**
- Persona name and archetype
- Score badges with colors
- Internal reaction (formatted)
- Public response (formatted)
- Reasoning text

---

## API Integration

### Run Simulation

**API Call:**
```typescript
runSimulation({
  draft_content: string,
  persona_set_id: string,
  user_id: number
})
```

**Response:**
```typescript
{
  simulation_id: string,
  draft_id: number,
  results: SimulationResult[],
  aggregate: AggregateScores,
  completed_at: string,
  duration_seconds: number
}
```

---

### Get Simulation Results

**API Call:**
```typescript
getSimulationResults(simulationId: string)
```

**Response:** Same as run simulation

---

### List Simulations

**API Call:**
```typescript
listSimulations(userId: number, page: number, pageSize: number)
```

---

## Styling Guidelines

### Score Colors
- **Green (Good):** #10B981 - Trust/Excitement 8-10, Backlash 1-4
- **Yellow (Caution):** #F59E0B - Trust/Excitement 5-7, Backlash 5-7
- **Red (Risk):** #EF4444 - Trust/Excitement 1-4, Backlash 8-10

### Layout
- **Form Width:** Max 600px, centered
- **Results Container:** Full width with max 1200px
- **Persona Cards:** Grid, 2-3 per row on desktop
- **Card Padding:** 24px

### Typography
- **Aggregate Scores:** 32px, bold
- **Section Headers:** 24px, semi-bold
- **Persona Names:** 18px, bold
- **Reaction Text:** 14px, regular, line-height 1.6

---

## User Flow

1. **Start Simulation:**
   - User enters draft content
   - Selects persona set (or uses pre-selected)
   - Clicks "Run Simulation"

2. **Wait for Results:**
   - Sees loading indicator
   - Progress message updates
   - 10-20 seconds typical wait

3. **Review Results:**
   - Aggregate scores at a glance
   - Read individual persona reactions
   - Identify concerning scores (red/yellow)

4. **Take Action:**
   - Click "View Insights" for improvement tips
   - Or edit draft and re-run simulation
   - Or save results and move on
