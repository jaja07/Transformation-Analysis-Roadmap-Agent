"""
agents/evaluator/nodes.py
Nodes du Evaluator Agent.
"""

from evaluator.state import EvaluatorState
from evaluator.prompts import SYSTEM_PROMPT, EVALUATOR_PROMPT
from llm_clients.nim_client import call_nim


def evaluate_node(state: EvaluatorState) -> EvaluatorState:
    """
    Node principal : évalue la roadmap générée et produit un rapport critique.
    """
    prompt = EVALUATOR_PROMPT.format(
        business_case=state["business_case"],
        canvas_analysis=state["canvas_analysis"],
        strategic_analysis=state["strategic_analysis"],
        roadmap=state["roadmap"],
    )

    response = call_nim(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.1,    # très déterministe pour une évaluation rigoureuse
        max_tokens=1500,
    )

    # Détecter le verdict pour le flag is_valid
    is_valid = "VERDICT: VALID" in response.upper()

    return {
        **state,
        "evaluation": response,
        "is_valid": is_valid,
    }