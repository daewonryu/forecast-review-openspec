# Capability: Persona Management UI

**Capability ID:** `persona-management-ui`  
**Change ID:** `add-react-frontend`

---

## ADDED Requirements

### Requirement: Generate Personas from UI Form

The UI MUST provide a form that allows users to generate 5 AI personas by entering an audience description.

**Acceptance Criteria:**
- Textarea input for audience description (5-500 characters)
- Character counter displaying current length
- Real-time validation feedback
- Submit button with loading state
- Error messages for validation failures
- Success message with generated personas display

#### Scenario: Generate Personas Through Form

**Given** a user is on the persona generation page  
**When** the user enters "Tech enthusiasts interested in AI" (35 chars)  
**And** clicks "Generate 5 Personas" button  
**Then** the button changes to "Generating..." and is disabled  
**And** a loading indicator displays  
**And** after 5-10 seconds, 5 personas are generated  
**And** the personas display with name, archetype, loyalty, and values  
**And** a success message confirms the generation  
**And** the form resets for new input

---

### Requirement: Display Persona Details

Each generated persona MUST be displayed with all trait information in a clear, scannable format.

**Acceptance Criteria:**
- Persona card shows name and archetype prominently
- Loyalty level displayed as visual indicator (1-10 scale)
- Core values shown as chips/tags
- Audience description included in card
- Responsive card layout (grid on desktop, stack on mobile)

#### Scenario: View Generated Persona Details

**Given** 5 personas have been generated  
**When** the results are displayed  
**Then** each persona card shows:
  - Name (e.g., "The Veteran")
  - Archetype (e.g., "Long-time AI enthusiast")
  - Loyalty level with visual bar or stars (e.g., 9/10)
  - Core values as colored tags (e.g., "Transparency", "Innovation")
**And** cards are arranged in a responsive grid  
**And** all text is readable without horizontal scrolling

---

### Requirement: Browse Persona Library

The UI MUST provide a library view where users can browse all previously generated persona sets.

**Acceptance Criteria:**
- Display all persona sets for the current user
- Show audience description for each set
- Display persona count (always 5) and creation date
- Pagination support (10 sets per page, configurable up to 50)
- Click to select a set for use in simulations
- Visual indication of currently selected set

#### Scenario: Browse Saved Persona Sets

**Given** a user has generated 3 persona sets  
**When** the user navigates to "My Personas" page  
**Then** 3 persona set cards are displayed  
**And** each card shows:
  - Audience description
  - "5 personas" count
  - Creation date (formatted as "Jan 14, 2026")
**And** cards are clickable for selection  
**And** a refresh button allows manual reload

---

### Requirement: Select Persona Set for Simulation

Users MUST be able to select a persona set from the library to use in simulations.

**Acceptance Criteria:**
- Click on persona set card to select it
- Selected set has visual distinction (highlight, checkmark)
- Only one set can be selected at a time
- Selection persists during session (localStorage or state)
- Selected set ID passed to simulation form

#### Scenario: Select Persona Set

**Given** a user is viewing the persona library  
**And** 3 persona sets are available  
**When** the user clicks on the second persona set card  
**Then** that card is highlighted with a border or background color  
**And** a checkmark or "✓ Selected" badge appears  
**And** previously selected set (if any) is deselected  
**And** the selected set ID is stored in state  
**And** when navigating to simulation page, this set is pre-selected

---

### Requirement: Delete Persona Set

Users MUST be able to delete persona sets they no longer need.

**Acceptance Criteria:**
- Delete button/icon on each persona set card
- Confirmation dialog before deletion
- Loading state during deletion
- Success feedback after deletion
- Library refreshes to remove deleted set
- Error handling if deletion fails

#### Scenario: Delete Persona Set with Confirmation

**Given** a user is viewing the persona library  
**When** the user clicks the delete icon on a persona set  
**Then** a confirmation dialog appears with message:
  "Are you sure you want to delete this persona set? This action cannot be undone."
**And** the dialog has "Cancel" and "Delete" buttons  
**When** the user clicks "Delete"  
**Then** the deletion API call is made  
**And** a loading indicator appears  
**And** after success, the card is removed from view  
**And** a success message displays: "Persona set deleted"  
**And** if deletion fails, an error message displays

---

### Requirement: Form Validation and Error Handling

The persona generation form MUST validate user input and handle errors gracefully.

**Acceptance Criteria:**
- Minimum 5 characters required for audience description
- Maximum 500 characters enforced
- Real-time character count updates
- Empty form submission prevented
- API error messages displayed to user
- Network errors handled with retry option

#### Scenario: Validate Form Input

**Given** a user is on the persona generation form  
**When** the user enters only 3 characters  
**And** tries to submit the form  
**Then** the form does not submit  
**And** an error message displays: "Audience description must be at least 5 characters"  
**And** the textarea gets error styling (red border)

#### Scenario: Handle API Error

**Given** a user submits a valid persona generation request  
**When** the backend API returns a 500 Internal Server Error  
**Then** the loading state stops  
**And** an error message displays: "Error generating personas: [error message]"  
**And** the form remains editable  
**And** the user can try again

---

### Requirement: Empty State Handling

The library view MUST handle the case when no persona sets exist.

**Acceptance Criteria:**
- Empty state message when library is empty
- Helpful guidance on what to do next
- Call-to-action to generate first persona set
- No broken UI or blank spaces

#### Scenario: Display Empty Library State

**Given** a new user with no persona sets  
**When** the user navigates to "My Personas" page  
**Then** an empty state message displays:
  "No persona sets yet. Generate your first set above!"
**And** the message includes visual icon or illustration  
**And** no broken card components are visible

---

### Requirement: Responsive Design for Persona UI

Persona management UI MUST work on desktop, tablet, and mobile devices.

**Acceptance Criteria:**
- Form is usable on screens 768px and above
- Persona cards stack vertically on mobile (< 768px)
- Grid layout on desktop (3-4 cards per row)
- Touch-friendly buttons and inputs
- No horizontal scrolling required

#### Scenario: View Personas on Mobile Device

**Given** a user accesses the persona page on a 375px wide screen  
**When** the page loads  
**Then** the form textarea spans full width with padding  
**And** persona cards display one per row  
**And** all buttons are large enough for touch (min 44px height)  
**And** text is readable without zooming  
**And** navigation is accessible

---

## Component Structure

### PersonaGenerator Component

```typescript
interface PersonaGeneratorProps {
  userId: number;
  onPersonasGenerated?: (setId: string) => void;
}
```

**State:**
- `audienceDescription`: string
- `mutation`: useMutation hook for API call

**Behavior:**
- Validates input length (5-500 chars)
- Calls `generatePersonas()` API function
- Displays loading state during generation
- Shows success message with generated personas
- Resets form after successful generation
- Calls optional callback with generated set ID

---

### PersonaLibrary Component

```typescript
interface PersonaLibraryProps {
  userId: number;
  onSelectSet?: (setId: string) => void;
  selectedSetId?: string;
}
```

**State:**
- `data`: useQuery hook result for persona sets
- `isLoading`, `error`: Query states

**Behavior:**
- Fetches persona sets on mount
- Displays sets in grid layout
- Handles selection with callback
- Supports refresh action
- Shows empty state if no sets exist

---

### PersonaCard Component

```typescript
interface PersonaCardProps {
  persona: Persona;
  compact?: boolean;
}
```

**Display:**
- Name (h4 heading)
- Archetype (subtitle)
- Loyalty level (visual indicator: progress bar or stars)
- Core values (chip/tag list)

---

## API Integration

### Generate Personas

**API Call:**
```typescript
generatePersonas({
  audience_description: string,
  save_to_library: true,
  user_id: number
})
```

**Response:**
```typescript
{
  set_id: string,
  personas: Persona[],
  created_at: string
}
```

---

### List Persona Sets

**API Call:**
```typescript
listPersonaSets(userId: number, page: number, pageSize: number)
```

**Response:**
```typescript
{
  sets: PersonaSetSummary[],
  total: number,
  page: number,
  page_size: number
}
```

---

### Delete Persona Set

**API Call:**
```typescript
deletePersonaSet(setId: string)
```

**Response:** 204 No Content

---

## Styling Guidelines

### Colors
- **Primary:** Blue (#3B82F6) for main actions
- **Success:** Green (#10B981) for success messages
- **Error:** Red (#EF4444) for errors and warnings
- **Neutral:** Gray scale for text and borders

### Typography
- **Form Labels:** 14px, medium weight
- **Persona Names:** 18px, bold
- **Archetypes:** 14px, regular
- **Body Text:** 16px, regular

### Spacing
- **Card Padding:** 20px
- **Grid Gap:** 16px
- **Form Field Margin:** 16px bottom
- **Button Padding:** 12px 24px

### Components
- **Cards:** Border radius 8px, shadow on hover
- **Buttons:** Border radius 6px, transition 200ms
- **Inputs:** Border radius 4px, focus ring 2px
- **Tags:** Border radius 16px, padding 4px 12px

---

## User Flow

1. **Generate Personas:**
   - User enters audience description
   - Submits form
   - Sees loading state (5-10 seconds)
   - Reviews generated personas
   - Personas automatically saved to library

2. **Browse Library:**
   - User navigates to persona library
   - Views all saved persona sets
   - Clicks on a set to view details
   - Selects a set for simulation

3. **Delete Persona:**
   - User finds unwanted persona set
   - Clicks delete button
   - Confirms deletion in dialog
   - Set removed from library
