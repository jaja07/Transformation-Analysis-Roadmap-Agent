"""
agents/strategist/nodes.py
Nodes du Strategist Agent.
"""

from strategist.state import StrategistState
from strategist.prompts import SYSTEM_PROMPT, STRATEGIST_PROMPT
from llm_clients.nim_client import call_nim


def strategist_node(state: StrategistState) -> StrategistState:
    """
    Node principal : produit l'analyse stratégique et les initiatives
    en mobilisant le framework Purpose / Pillars / Value / Pitfalls.
    """
    prompt = STRATEGIST_PROMPT.format(
        business_case=state["business_case"],
        why=state["why"],
        canvas_analysis=state["canvas_analysis"],
        how_context=state["how_context"],
    )

    response = call_nim(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.3,
        max_tokens=2000,
    )

    return {**state, "strategic_analysis": response}