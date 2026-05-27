"""
agents/canvas_analyst/nodes.py
Nodes du Canvas Analyst Agent.
"""

from .state import CanvasState
from .prompts import SYSTEM_PROMPT, CANVAS_ANALYSIS_PROMPT
from ..llm_clients.nim_client import call_nim


def canvas_analysis_node(state: CanvasState) -> CanvasState:
    """
    Node principal : analyse le business case sur les 7 champs du canvas.
    """
    prompt = CANVAS_ANALYSIS_PROMPT.format(
        business_case=state["business_case"],
        what_context=state["what_context"],
        global_context=state["global_context"],
    )

    response = call_nim(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.2,
        max_tokens=1500,
    )

    return {**state, "canvas_analysis": response}