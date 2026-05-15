"""
agents/retrieval_agent/state.py
State du Retrieval Agent.
"""

from typing_extensions import TypedDict


class RetrievalState(TypedDict):
    # Inputs venant du Planner
    structured_problem: str     # synthèse du planner
    why: str
    what: str
    how: str

    # Outputs de cet agent
    why_context: str            # chunks pertinents pour le WHY
    what_context: str           # chunks pertinents pour le WHAT
    how_context: str            # chunks pertinents pour le HOW
    global_context: str         # contexte global pour les agents suivants
    _queries: list