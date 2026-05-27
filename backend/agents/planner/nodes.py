"""
agents/planner/nodes.py
Nodes du Planner Agent.
"""

from .state import PlannerState
from .prompts import SYSTEM_PROMPT, PLANNER_PROMPT
from ..llm_clients.nim_client import call_nim


def parse_planner_response(response: str) -> dict:
    """
    Parse la réponse structurée du LLM en champs distincts.
    """
    sections = {"WHY": "", "WHAT": "", "HOW": "", "STRUCTURED SUMMARY": ""}
    current = None

    for line in response.splitlines():
        line = line.strip()
        matched = False
        for key in sections:
            if line.upper().startswith(key + ":"):
                current = key
                # Texte inline après le label (ex: "WHY: blah")
                inline = line[len(key) + 1:].strip()
                if inline:
                    sections[key] = inline
                matched = True
                break
        if not matched and current:
            sections[current] = (sections[current] + "\n" + line).strip()

    return sections


def plan_node(state: PlannerState) -> PlannerState:
    """
    Node principal : analyse le business case et structure le problème.
    """
    prompt = PLANNER_PROMPT.format(business_case=state["business_case"])

    response = call_nim(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.2,
        max_tokens=1024,
    )

    parsed = parse_planner_response(response)

    return {
        **state,
        "why": parsed["WHY"],
        "what": parsed["WHAT"],
        "how": parsed["HOW"],
        "structured_problem": parsed["STRUCTURED SUMMARY"],
    }