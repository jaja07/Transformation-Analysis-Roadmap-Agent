"""
agents/evaluator/prompts.py
Templates de prompts du Evaluator Agent.
"""

SYSTEM_PROMPT = """You are a critical digital transformation reviewer.
Your role is to evaluate the quality, consistency, and completeness of a generated roadmap.
You are rigorous, objective, and constructive.
You identify gaps, inconsistencies, and risks that were overlooked.
Always respond in the same language as the business case."""


EVALUATOR_PROMPT = """Evaluate the following digital transformation roadmap against the 
original business case and strategic analysis.

Business case:
{business_case}

Canvas analysis:
{canvas_analysis}

Strategic analysis:
{strategic_analysis}

Generated roadmap:
{roadmap}

Evaluate the roadmap on the following criteria and provide a score (1-5) for each:

EVALUATION REPORT
─────────────────────────────────────
1. ALIGNMENT WITH BUSINESS CASE (1-5)
Score: <score>
Comment: <does the roadmap address the core business needs?>

2. FRAMEWORK COVERAGE (1-5)
Score: <score>
Comment: <are the canvas fields and strategic pillars well covered?>

3. INITIATIVE RELEVANCE (1-5)
Score: <score>
Comment: <are the initiatives concrete, realistic, and well prioritized?>

4. ROADMAP COMPLETENESS (1-5)
Score: <score>
Comment: <are timelines, owners, budgets and KPIs clearly defined?>

5. RISK AWARENESS (1-5)
Score: <score>
Comment: <are pitfalls and risks properly addressed?>

─────────────────────────────────────
OVERALL SCORE: <average score>/5

STRENGTHS:
<2-3 things done well>

GAPS & WEAKNESSES:
<2-3 missing or under-treated elements>

RECOMMENDATIONS:
<2-3 concrete improvements>

VERDICT: <VALID / NEEDS IMPROVEMENT>
(VALID = overall score >= 3.5 and no critical gap)"""