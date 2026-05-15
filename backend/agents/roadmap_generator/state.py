"""
agents/roadmap_generator/state.py
State du Roadmap Generator Agent.
"""

from typing_extensions import TypedDict


class RoadmapState(TypedDict):
    # Inputs venant des agents précédents
    business_case: str
    structured_problem: str
    canvas_analysis: str
    strategic_analysis: str     # initiatives + pilliers + valeur du strategist
    global_context: str

    # Output de cet agent
    roadmap: str                # roadmap structurée et exploitable