"""
agents/canvas_analyst/prompts.py
Templates de prompts du Canvas Analyst Agent.
"""

SYSTEM_PROMPT = """You are a digital transformation analyst specializing in the 
Digital Transformation Canvas framework.
Your role is to analyze a company's situation across the 7 action fields of the canvas
and identify key gaps, opportunities, and priorities for each dimension.
Be specific, concise, and grounded in the provided context.
Always respond in the same language as the business case."""


CANVAS_ANALYSIS_PROMPT = """Analyze the following business case using the 7 action fields 
of the Digital Transformation Canvas.

For each field, provide:
- Current situation (1-2 sentences)
- Key gap or opportunity (1 sentence)
- Priority level: HIGH / MEDIUM / LOW

Business case:
{business_case}

Framework context from corpus:
{what_context}

Additional context:
{global_context}

Respond in this exact format:

1. CUSTOMER CENTRICITY
Situation: <current state>
Gap/Opportunity: <key gap or opportunity>
Priority: <HIGH/MEDIUM/LOW>

2. NEW TECHNOLOGIES
Situation: <current state>
Gap/Opportunity: <key gap or opportunity>
Priority: <HIGH/MEDIUM/LOW>

3. CLOUD AND DATA
Situation: <current state>
Gap/Opportunity: <key gap or opportunity>
Priority: <HIGH/MEDIUM/LOW>

4. DIGITAL BUSINESS DEVELOPMENT
Situation: <current state>
Gap/Opportunity: <key gap or opportunity>
Priority: <HIGH/MEDIUM/LOW>

5. PROCESS ENGINEERING
Situation: <current state>
Gap/Opportunity: <key gap or opportunity>
Priority: <HIGH/MEDIUM/LOW>

6. DIGITAL LEADERSHIP & CULTURE
Situation: <current state>
Gap/Opportunity: <key gap or opportunity>
Priority: <HIGH/MEDIUM/LOW>

7. DIGITAL MARKETING
Situation: <current state>
Gap/Opportunity: <key gap or opportunity>
Priority: <HIGH/MEDIUM/LOW>"""