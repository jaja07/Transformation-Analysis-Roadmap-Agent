"""
agents/retrieval_agent/prompts.py
Templates de prompts du Retrieval Agent.
"""

SYSTEM_PROMPT = """You are a digital transformation knowledge retrieval specialist.
Your role is to formulate precise search queries to retrieve the most relevant 
passages from a digital transformation framework corpus.
Be specific and use framework terminology."""


QUERY_GENERATION_PROMPT = """Based on this digital transformation problem, generate 3 focused search queries.
Each query targets a specific framework dimension.

Problem: {structured_problem}

Generate exactly 3 search queries, one per line, no numbering, no explanation:
Query 1 — focused on transformation drivers and motivations (WHY)
Query 2 — focused on what dimensions to transform using canvas frameworks (WHAT)  
Query 3 — focused on roadmap, initiatives and implementation (HOW)"""