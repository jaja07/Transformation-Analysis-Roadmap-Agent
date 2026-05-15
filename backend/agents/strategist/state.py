"""
agents/strategist/state.py
State du Strategist Agent.
"""

from typing_extensions import TypedDict


class StrategistState(TypedDict):
    # Inputs venant des agents précédents
    business_case: str
    structured_problem: str
    why: str
    canvas_analysis: str        # analyse des 7 champs du canvas
    how_context: str            # chunks RAG sur l'approche / implémentation
    global_context: str

    # Output de cet agent
    strategic_analysis: str     # purpose, pilliers, valeur, risques + initiatives