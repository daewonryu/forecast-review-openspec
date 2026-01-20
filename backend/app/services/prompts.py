"""
Persona generation prompts and utilities
"""
from typing import List, Dict, Any

PERSONA_GENERATION_SYSTEM_PROMPT = """You are an expert at creating realistic audience personas for market research and content testing. Your personas should represent diverse viewpoints within a target audience, ranging from enthusiastic supporters to skeptical critics.

When given an audience description, generate exactly 5 distinct personas that capture the spectrum of that audience's perspectives. Each persona should feel authentic and grounded in real human psychology."""

PERSONA_GENERATION_USER_PROMPT = """Generate exactly 5 distinct personas for the following target audience:

**Audience Description:** {audience_description}

For each persona, provide:
1. **Name/Archetype**: A memorable archetype name (e.g., "The Veteran", "The Skeptic", "The Casual Fan"). Keep archetype description concise (2-5 words preferred, max 15 words).
2. **Loyalty Level**: An integer from 1-10, where 1 is "barely interested" and 10 is "die-hard fan"
3. **Core Values**: 2-4 key values that drive their decisions (e.g., "Transparency", "Value for Money", "Exclusivity", "Community", "Innovation")

Ensure the 5 personas represent diverse perspectives:
- Include both optimistic (high loyalty) and skeptical (low loyalty) personas
- Vary the core values to represent different priorities
- Make each archetype distinct and memorable

**Example Output (for "Tech-savvy mobile game players"):**
{{
  "personas": [
    {{
      "name": "The Day-One Player",
      "archetype": "Devoted early adopter who's seen it all",
      "loyalty_level": 9,
      "core_values": ["Nostalgia", "Community", "Recognition", "Content Quality"]
    }},
    {{
      "name": "The F2P Grinder",
      "archetype": "Free-to-play purist who refuses to spend",
      "loyalty_level": 6,
      "core_values": ["Fairness", "Accessibility", "Time Investment"]
    }},
    {{
      "name": "The Whale",
      "archetype": "High spender who expects premium treatment",
      "loyalty_level": 7,
      "core_values": ["Exclusivity", "Power", "Status", "Customer Service"]
    }},
    {{
      "name": "The Casual Enjoyer",
      "archetype": "Plays for fun, not invested deeply",
      "loyalty_level": 4,
      "core_values": ["Entertainment", "Simplicity", "Convenience"]
    }},
    {{
      "name": "The Burned-Out Critic",
      "archetype": "Disappointed veteran considering quitting",
      "loyalty_level": 3,
      "core_values": ["Transparency", "Value", "Respect"]
    }}
  ]
}}

Now generate personas for: {audience_description}

Respond ONLY with valid JSON in the exact format shown above."""


PERSONA_REACTION_SYSTEM_PROMPT = """You are simulating the reaction of a specific persona to content. Your goal is to provide authentic, psychologically realistic responses that reflect the persona's traits, loyalty level, and core values.

You will provide TWO types of responses:
1. **Internal Monologue**: The persona's brutally honest, unfiltered internal thoughts
2. **Public Comment**: What they would actually type in a public comment section (may be more measured)

You will also score the content on three dimensions (1-10 scale):
- **Trust**: How much they trust the brand/creator after reading this
- **Excitement**: Their enthusiasm level about the announcement
- **Backlash Risk**: Likelihood they would publicly criticize or spread negative sentiment"""


def create_persona_reaction_prompt(
    persona: Dict[str, Any],
    content: str,
    audience_description: str
) -> str:
    """Create prompt for persona reaction to content"""
    return f"""You are simulating this persona:

**Name:** {persona['name']}
**Archetype:** {persona['archetype']}
**Loyalty Level:** {persona['loyalty_level']}/10
**Core Values:** {', '.join(persona['core_values'])}
**Audience Context:** {audience_description}

React to this content:

---
{content}
---

**Example Reaction (for reference):**
If the content was: "We're excited to announce Premium+ subscription with exclusive features!"
And the persona valued "Fairness" and "Accessibility" with loyalty 4/10, they might respond:

{{
  "internal_monologue": "Great, another paywall. They said features would stay free. I knew this was coming but it still stings.",
  "public_comment": "Disappointed to see this go behind a paywall. What happened to keeping the game accessible?",
  "scores": {{
    "trust": 3,
    "excitement": 2,
    "backlash_risk": 8
  }},
  "reasoning": "Low trust due to broken promise. Not excited about paid features. High backlash risk from F2P community feeling abandoned."
}}

Now provide YOUR response in this exact JSON format:
{{
  "internal_monologue": "Your honest, unfiltered thoughts (100-300 chars)",
  "public_comment": "What you'd actually post publicly (50-200 chars)",
  "scores": {{
    "trust": 5,
    "excitement": 3,
    "backlash_risk": 7
  }},
  "reasoning": "Brief explanation for your scores"
}}

Remember:
- Stay true to your loyalty level and core values
- Internal monologue can be more extreme than public comment
- Scores must be integers from 1-10
- Be specific about what triggered your reaction
- Consider how YOUR specific values align or conflict with the content"""


PAIN_POINT_EXTRACTION_PROMPT = """You are analyzing persona reactions to identify problematic content in a social media draft.

**Draft Content:**
{draft_content}

**Persona Feedback (sorted by backlash score):**
{persona_feedback}

**Example Analysis:**

Draft: "We're raising prices by 30% but adding amazing new features you'll love!"

Feedback:
- The Skeptic (backlash: 9): "30% is outrageous without concrete details"
- The Budget-Conscious (backlash: 8): "Can't afford this, feeling priced out"

Pain Points:
[
  {{
    "text": "raising prices by 30%",
    "severity": "high",
    "affected_personas": ["The Skeptic", "The Budget-Conscious", "The Casual"],
    "reasoning": "Large price increase without justification triggers strong negative reactions, especially from cost-sensitive personas. Lacks transparency about what drives the increase."
  }},
  {{
    "text": "features you'll love",
    "severity": "medium",
    "affected_personas": ["The Skeptic"],
    "reasoning": "Vague marketing language without specifics undermines credibility. Personas valuing transparency view this as evasive."
  }}
]

**Now analyze the actual draft:**

**Instructions:**
Identify up to 5 pain points - specific phrases or concepts in the draft that triggered negative reactions.

For each pain point, provide:
1. "text": The exact phrase from the draft (or short paraphrase if conceptual)
2. "severity": "high" | "medium" | "low" (based on backlash scores)
3. "affected_personas": List of persona names who reacted negatively
4. "reasoning": Why this is problematic (synthesize from persona reasoning)

Rank by severity (highest first). Respond ONLY with valid JSON array. Do not include any other text.
"""


IMPROVEMENT_TIPS_PROMPT = """You are a social media strategist providing actionable advice to improve draft content.

**Draft Content:**
{draft_content}

**Aggregate Analytics:**
{aggregate_analytics}

**Persona Summaries:**
{persona_summaries}

**Identified Pain Points:**
{pain_points}

**Example Analysis:**

Draft: "Big changes coming next month!"
Pain Points: Vague language (high severity), No concrete details (high)
Analytics: Trust 4.2, Excitement 5.0, Backlash 6.8

Tips:
[
  {{
    "tip": "Replace 'Big changes' with specific feature names: e.g., 'Introducing Dark Mode, Advanced Search, and Custom Profiles'",
    "rationale": "Vague announcements trigger skepticism. Specific features build trust and give personas something concrete to evaluate.",
    "impact": "high",
    "addresses": ["vague language", "No concrete details"]
  }},
  {{
    "tip": "Add a timeline with milestones: 'Dark Mode launches March 15, other features rolling out through March 30'",
    "rationale": "Concrete dates demonstrate planning and accountability. Addresses trust concerns from skeptical personas.",
    "impact": "high",
    "addresses": ["No concrete details"]
  }},
  {{
    "tip": "Include a user benefit statement: 'These features will reduce eye strain and help you find content 3x faster'",
    "rationale": "Connecting features to tangible benefits increases excitement and shows user-centric thinking.",
    "impact": "medium",
    "addresses": ["vague language"]
  }}
]

**Now analyze and provide tips for the actual draft:**

**Instructions:**
Generate EXACTLY 3 actionable improvement tips that would most effectively improve the draft.

For each tip, provide:
1. "tip": Specific, actionable suggestion (not generic advice)
2. "rationale": Why this would help, based on the data
3. "impact": "high" | "medium" | "low" (estimated improvement potential)
4. "addresses": List of pain point texts this tip would fix

**Requirements:**
- Tips must be SPECIFIC to this draft (avoid generic advice like "be more authentic")
- Tips should address the highest severity pain points first
- Tips should be immediately actionable (e.g., "Replace phrase X with Y" or "Add section about Z")
- Rank tips by potential impact (highest first)

Respond ONLY with valid JSON array of exactly 3 tips. Do not include any other text.
"""


def validate_persona_response(data: Dict[str, Any]) -> bool:
    """Validate that persona generation response has correct structure"""
    if "personas" not in data:
        return False
    
    if len(data["personas"]) != 5:
        return False
    
    required_fields = ["name", "archetype", "loyalty_level", "core_values"]
    for persona in data["personas"]:
        if not all(field in persona for field in required_fields):
            return False
        
        if not isinstance(persona["loyalty_level"], int):
            return False
        
        if not (1 <= persona["loyalty_level"] <= 10):
            return False
        
        if not isinstance(persona["core_values"], list):
            return False
        
        if not (2 <= len(persona["core_values"]) <= 4):
            return False
    
    return True


def validate_reaction_response(data: Dict[str, Any]) -> bool:
    """Validate that reaction response has correct structure"""
    required_fields = ["internal_monologue", "public_comment", "scores", "reasoning"]
    if not all(field in data for field in required_fields):
        return False
    
    scores = data["scores"]
    required_scores = ["trust", "excitement", "backlash_risk"]
    if not all(score in scores for score in required_scores):
        return False
    
    for score_name in required_scores:
        score = scores[score_name]
        if not isinstance(score, int) or not (1 <= score <= 10):
            return False
    
    return True
