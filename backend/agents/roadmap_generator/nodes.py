"""
agents/roadmap_generator/nodes.py
Nodes du Roadmap Generator Agent.
"""

from roadmap_generator.state import RoadmapState
from roadmap_generator.prompts import SYSTEM_PROMPT, ROADMAP_PROMPT
from llm_clients.nim_client import call_nim


def roadmap_node(state: RoadmapState) -> RoadmapState:
    """
    Node principal : génère la roadmap structurée en 3 phases
    à partir de l'analyse stratégique et des initiatives.
    """
    prompt = ROADMAP_PROMPT.format(
        business_case=state["business_case"],
        strategic_analysis=state["strategic_analysis"],
        canvas_analysis=state["canvas_analysis"],
    )

    response = call_nim(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.2,
        max_tokens=2500,
    )

    return {**state, "roadmap": response}