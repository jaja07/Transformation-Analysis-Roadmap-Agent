"""
agents/roadmap_generator/prompts.py
Templates de prompts du Roadmap Generator Agent.
"""

SYSTEM_PROMPT = """You are a digital transformation program manager.
Your role is to transform a strategic analysis and a list of initiatives 
into a structured, actionable, and exploitable digital transformation roadmap.
The roadmap must be organized by phases, with clear objectives, owners, timelines, 
budget estimates, and KPIs for each initiative.
Always respond in the same language as the business case."""


ROADMAP_PROMPT = """Based on the strategic analysis below, generate a complete and structured 
digital transformation roadmap.

Business context:
{business_case}

Strategic analysis and initiatives:
{strategic_analysis}

Canvas analysis:
{canvas_analysis}

The roadmap must be organized in 3 phases:
- Phase 1: Quick Wins (0-3 months)
- Phase 2: Structural Transformation (4-9 months)
- Phase 3: Optimization & Scale (10-18 months)

For each phase, list the relevant initiatives using this format:

═══════════════════════════════════════
DIGITAL TRANSFORMATION ROADMAP
═══════════════════════════════════════

PHASE 1 — QUICK WINS (0-3 months)
Objective: <overall objective of this phase>

Initiative 1.1: <name>
  Canvas field  : <field>
  Pillar(s)     : <Process / People / Platform / Partners>
  Owner         : <suggested role, e.g. CTO, CDO, HR Director>
  Duration      : <e.g. 6 weeks>
  Budget est.   : <e.g. Low / Medium / High or €range>
  KPIs          : <1-2 measurable indicators>
  Expected impact: <concrete outcome>

[repeat for each initiative in this phase]

─────────────────────────────────────
PHASE 2 — STRUCTURAL TRANSFORMATION (4-9 months)
Objective: <overall objective of this phase>

[same format]

─────────────────────────────────────
PHASE 3 — OPTIMIZATION & SCALE (10-18 months)
Objective: <overall objective of this phase>

[same format]

─────────────────────────────────────
ROADMAP SUMMARY
Total initiatives : <number>
Total duration    : 18 months
Key success factors: <3 critical factors>
Overall KPIs      : <3 measurable outcomes for the full transformation>"""