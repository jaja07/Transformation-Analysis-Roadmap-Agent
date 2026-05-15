"""
agents/evaluator/state.py
State du Evaluator Agent.
"""

from typing_extensions import TypedDict


class EvaluatorState(TypedDict):
    # Inputs venant de tous les agents précédents
    business_case: str
    structured_problem: str
    canvas_analysis: str
    strategic_analysis: str
    roadmap: str

    # Output de cet agent
    evaluation: str             # critique structurée de la roadmap
    is_valid: bool              # True si la roadmap est exploitable