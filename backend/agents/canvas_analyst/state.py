"""
agents/canvas_analyst/state.py
State du Canvas Analyst Agent.
"""

from typing_extensions import TypedDict


class CanvasState(TypedDict):
    # Inputs venant du Planner + Retrieval Agent
    business_case: str
    structured_problem: str
    what_context: str           # chunks RAG sur les dimensions à transformer
    global_context: str

    # Output de cet agent
    canvas_analysis: str        # analyse structurée sur les 7 champs du canvas