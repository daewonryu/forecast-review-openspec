# Automatic Insights Generation - Implementation

## Problem
The insights weren't automatically generated after simulations completed, and users couldn't easily access historical simulation results with insights.

## Solution Implemented

### 1. Auto-Generate Insights After Simulation ✅

**Modified:** `app/routers/simulations.py` - `POST /api/simulations/run`

Now automatically triggers insights generation in the background after a simulation completes:

```python
# After simulation completes successfully
asyncio.create_task(generate_insights_background())
```

**Benefits:**
- ✅ Insights start generating immediately after simulation
- ✅ No manual step required
- ✅ Doesn't block the simulation response (runs in background)
- ✅ Frontend can poll for completion

### 2. Added Insights Status Endpoint ✅

**New Endpoint:** `GET /api/insights/draft/{draft_id}/status`

**Purpose:** Check if insights are ready without triggering errors

**Response:**
```json
{
  "ready": true,
  "insight_id": 123,
  "draft_id": 456,
  "simulation_id": "uuid-here"
}
```

**Use Case:** Frontend can poll this endpoint to enable the "Review Insights" button when `ready: true`

### 3. Enhanced Error Messages ✅

**Modified:** `GET /api/insights/draft/{draft_id}`

Now returns a more helpful error message if insights aren't ready yet:
- Before: `"No insights found for draft {draft_id}"`
- After: `"No insights found for draft {draft_id}. They may still be generating."`

---

## Frontend Integration Guide

### Recommended Flow

#### Step 1: Run Simulation
```javascript
const response = await fetch('/api/simulations/run', {
  method: 'POST',
  body: JSON.stringify({
    draft_content: content,
    persona_set_id: setId
  })
});

const { draft_id, simulation_id } = await response.json();
```

#### Step 2: Poll for Insights Status
```javascript
// Start polling immediately
const pollInterval = setInterval(async () => {
  const statusResponse = await fetch(`/api/insights/draft/${draft_id}/status`);
  const status = await statusResponse.json();
  
  if (status.ready) {
    clearInterval(pollInterval);
    // Enable "Review Insights" button
    setInsightsReady(true);
  }
}, 2000); // Check every 2 seconds

// Stop polling after 30 seconds max
setTimeout(() => clearInterval(pollInterval), 30000);
```

#### Step 3: Fetch Insights When Ready
```javascript
const insightsResponse = await fetch(`/api/insights/draft/${draft_id}`);
const insights = await insightsResponse.json();

// Display:
// - insights.pain_points (array)
// - insights.improvement_tips (array)
// - insights.overall_sentiment
// - insights.avg_trust, avg_excitement, avg_backlash_risk
```

---

## Alternative: Simpler Polling

If you want to simplify, just poll the main insights endpoint:

```javascript
async function waitForInsights(draft_id) {
  const maxAttempts = 15; // 30 seconds (15 attempts * 2 seconds)
  
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const response = await fetch(`/api/insights/draft/${draft_id}`);
      
      if (response.ok) {
        return await response.json(); // Insights are ready!
      }
    } catch (error) {
      // Not ready yet, wait and retry
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  throw new Error('Insights generation timed out');
}
```

---

## Testing

### Manual Test

1. **Start the backend:**
   ```bash
   cd backend
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Run a simulation:**
   ```bash
   curl -X POST http://localhost:8000/api/simulations/run \
     -H "Content-Type: application/json" \
     -d '{
       "draft_content": "Test announcement",
       "persona_set_id": "your-set-id"
     }'
   ```

3. **Check insights status** (immediately after):
   ```bash
   curl http://localhost:8000/api/insights/draft/1/status
   # Should return: {"ready": false, ...}
   ```

4. **Check again** (after a few seconds):
   ```bash
   curl http://localhost:8000/api/insights/draft/1/status
   # Should return: {"ready": true, "insight_id": 1, ...}
   ```

5. **Fetch insights:**
   ```bash
   curl http://localhost:8000/api/insights/draft/1
   # Returns full insights with pain points and tips
   ```

---

## Expected Timing

- **Simulation:** ~5-15 seconds (5 parallel LLM calls)
- **Insights generation:** ~3-8 seconds (2-3 LLM calls for pain points + tips)
- **Total:** ~8-23 seconds from "Start Simulation" to insights ready

---

## Error Handling

### If Insights Generation Fails

The background task logs errors but doesn't break the simulation response. Users still get their simulation results even if insights fail.

**Recovery:**
- Frontend can manually retry: `POST /api/insights/generate/{draft_id}`
- This endpoint checks if insights already exist and returns them if so

### If Polling Times Out

Suggest showing a "Retry" button that calls:
```javascript
await fetch(`/api/insights/generate/${draft_id}`, { method: 'POST' })
```

---

## Files Modified

1. ✅ `app/routers/simulations.py` - Added auto-generation
2. ✅ `app/routers/insights.py` - Added status endpoint, improved errors

---

## Next Steps for Frontend

1. **Add state for insights readiness:**
   ```javascript
   const [insightsReady, setInsightsReady] = useState(false);
   ```

2. **Start polling after simulation completes**

3. **Navigate to History page** where users can:
   - View all past simulations
   - Click any simulation to see full details and insights

4. **Show loading indicator** while polling:
   ```
   "Generating insights... (this takes 5-10 seconds)"
   ```

---

## Benefits

✅ **Seamless UX** - No manual step needed  
✅ **Fast** - Insights start generating immediately  
✅ **Reliable** - Background task doesn't block responses  
✅ **Flexible** - Frontend can choose polling strategy  
✅ **Recoverable** - Manual retry if needed
