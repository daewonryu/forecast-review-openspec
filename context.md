# [PRD] FanEcho: Synthetic Fan Reaction Simulator (MVP)

## 1. Executive Summary
**FanEcho** is a synthetic user testing platform that allows brands to simulate fan reactions to public announcements or advertisements using AI-generated personas. The goal is to identify potential PR risks and optimize engagement before the content is published.

---

## 2. Problem Statement
* **Risk of Backlash:** Brand announcements often face unexpected negative reactions due to poor phrasing or lack of empathy for fan sentiment.
* **Lack of Testing:** Small-to-medium teams don't have the budget or time for focus group testing before every social media post or notice.
* **Groupthink:** Internal teams often fail to see how "extreme" fans might interpret a message.

---

## 3. Core Features (MVP)

### 3.1 Persona Engine
* **Persona Generation:** Based on a high-level description (e.g., "K-pop fans," "Tech enthusiasts"), the system generates 5 distinct personas.
* **Trait Definition:** Each persona includes:
    * Name/Archetype (e.g., The Veteran, The Casual, The Skeptic).
    * Loyalty Level (1-10).
    * Core Values (e.g., Transparency, Value for Money, Exclusivity).
* **Persistence:** All personas are saved to a Database for future use across different content drafts.

### 3.2 Simulation & Feedback
* **Draft Submission:** User inputs a text draft of the announcement/notice.
* **Reaction Simulation:** Each persona provides:
    * **Internal Monologue:** Their "brutally honest" internal thought.
    * **Public Comment:** What they would actually type in a comment section.
* **Quantified Scoring:**
    * **Trust:** 1-10
    * **Excitement:** 1-10
    * **Backlash Risk:** 1-10

### 3.3 Dashboard & Insights
* **Aggregated Analytics:** A summary view of the "Average Sentiment."
* **Pain Point Identification:** Highlighting which specific parts of the text caused the highest "Backlash Risk."
* **AI Improvement Tips:** 3 actionable suggestions to improve the draft based on persona scores.

---

## 4. Technical Architecture (MVP)
* **LLM Model:** OpenAI GPT-4o / Claude 3.5 Sonnet.
* **Backend:** Python (FastAPI) or Node.js.
* **Database:** PostgreSQL (to store `Users`, `Personas`, `Drafts`, and `Simulation_Results`).
* **Prompting Strategy:** Multi-agent simulation (Step 1: Persona Gen -> Step 2: Individual Reaction -> Step 3: Synthesis).

---

## 5. User Workflow
1.  **Define Audience:** User types: "Hardcore fans of a 5-year-old mobile RPG."
2.  **Review Personas:** AI generates 5 personas. User saves them to their "Brand Library."
3.  **Submit Content:** User pastes the draft of a new "Gacha System Update."
4.  **Simulate:** The system runs 5 parallel API calls.
5.  **View History:** User can view all past simulations and click to see detailed results.
6.  **Refine:** User sees that "The Veteran" persona feels cheated. User edits the text and re-runs the simulation.

---

## 6. Success Metrics
* **Content Improvement:** Users edit their content at least once after seeing simulation results.
* **Persona Consistency:** Users reuse the same persona sets for multiple simulations.
* **Speed:** Total simulation time (from input to result) under 20 seconds.

---

## 7. Future Roadmap (Post-MVP)
* **Image Analysis:** Uploading ad banners or posters for visual reaction testing.
* **Comparison Mode:** Testing two versions of a draft (A/B testing) side-by-side.
* **Community Integration:** Directly importing real community data to "train" more accurate personas.