"""
orchestrator/state.py
State global de l'orchestrateur — agrège tous les champs de tous les agents.
"""

from typing_extensions import TypedDict


class GlobalState(TypedDict):
    # Input utilisateur
    business_case: str

    # Planner
    why: str
    what: str
    how: str
    structured_problem: str

    # Retrieval Agent
    why_context: str
    what_context: str
    how_context: str
    global_context: str

    # Canvas Analyst
    canvas_analysis: str

    # Strategist
    strategic_analysis: str

    # Roadmap Generator
    roadmap: str

    # Evaluator
    evaluation: str
    is_valid: bool