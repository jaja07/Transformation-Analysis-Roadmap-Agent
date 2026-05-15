"""
agents/planner/state.py
State du Planner Agent.
"""

from typing import Optional
from typing_extensions import TypedDict


class PlannerState(TypedDict):
    business_case: str          # input brut de l'utilisateur
    why: str                    # motivations / drivers de transformation
    what: str                   # ce qui doit être transformé
    how: str                    # approche / logique d'action
    structured_problem: str     # synthèse structurée transmise aux agents suivants