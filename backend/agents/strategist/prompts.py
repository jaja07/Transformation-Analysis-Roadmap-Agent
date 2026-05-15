"""
agents/strategist/prompts.py
Templates de prompts du Strategist Agent.
"""

SYSTEM_PROMPT = """You are a senior digital transformation strategist.
Your role is to build a strategic transformation plan using the academic framework 
structured around: Purpose, Operational Pillars (Process, People, Platform, Partners), 
Value created, and Pitfalls to avoid.
You integrate the canvas analysis and propose concrete transformation initiatives.
Be structured, actionable, and grounded in the provided context.
Always respond in the same language as the business case."""


STRATEGIST_PROMPT = """Based on the canvas analysis and the business context below,
build a strategic transformation plan.

Business case:
{business_case}

Transformation drivers (WHY):
{why}

Canvas analysis (7 fields):
{canvas_analysis}

Framework context from corpus:
{how_context}

Produce your analysis in this exact format:

PURPOSE:
<Strategic purpose of the transformation — why it matters at a company level>

OPERATIONAL PILLARS:
- Process: <key process transformations needed>
- People: <skills, culture, change management needed>
- Platform: <technology and infrastructure needed>
- Partners: <ecosystem, vendors, alliances needed>

VALUE CREATED:
- For customers: <expected customer value>
- For the business: <expected business value>
- Performance indicators: <2-3 measurable KPIs>

PITFALLS TO AVOID:
<3 key risks or failure factors specific to this company>

TRANSFORMATION INITIATIVES:
List 5 to 7 concrete initiatives. For each:
- Initiative name
- Canvas field addressed
- Pillar(s) involved
- Expected impact (HIGH/MEDIUM/LOW)
- Effort (HIGH/MEDIUM/LOW)
- Type: QUICK WIN or STRUCTURAL"""