"""
orchestrator/runner.py
Point d'entrée du pipeline complet.

Usage :
    python orchestrator/runner.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from orchestrator.graph import orchestrator
from orchestrator.state import GlobalState


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SEPARATOR = "═" * 60


def print_section(title: str, content: str):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)
    print(content)


def run_pipeline(business_case: str) -> GlobalState:
    """
    Lance le pipeline complet et retourne le GlobalState final.

    Args:
        business_case: Description de l'entreprise et de ses enjeux.

    Returns:
        GlobalState complet avec tous les outputs des agents.
    """
    print(f"\n{SEPARATOR}")
    print("  PIPELINE MULTI-AGENT — Digital Transformation Roadmap")
    print(SEPARATOR)
    print(f"\nBusiness case reçu ({len(business_case)} chars)\n")

    initial_state: GlobalState = {
        "business_case": business_case,
        "why": "",
        "what": "",
        "how": "",
        "structured_problem": "",
        "why_context": "",
        "what_context": "",
        "how_context": "",
        "global_context": "",
        "canvas_analysis": "",
        "strategic_analysis": "",
        "roadmap": "",
        "evaluation": "",
        "is_valid": False,
    }

    print("[ 1/6 ] Planner Agent          ...", end=" ", flush=True)
    # LangGraph exécute les nodes séquentiellement
    result = orchestrator.invoke(initial_state)
    print("done")  # affiché après la fin complète du pipeline

    return result


# ---------------------------------------------------------------------------
# Entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    business_case = """
    Our company is a mid-sized retail bank with 500 employees operating in France.
    We are losing customers to neobanks because our mobile app is outdated and poorly rated (2.1/5).
    Our loan approval process is entirely manual and takes 5 business days,
    while our competitors approve loans in under 1 hour using AI.
    We want to:
    - Improve customer experience and NPS by 20 points
    - Reduce operational costs by 20% within 18 months
    - Launch a fully digital loan product within 12 months
    - Build internal digital capabilities for the long term
    """

    result = run_pipeline(business_case.strip())

    # Affichage des résultats
    print_section("PLANNER — Structured Problem", result["structured_problem"])
    print_section("CANVAS ANALYSIS", result["canvas_analysis"])
    print_section("STRATEGIC ANALYSIS", result["strategic_analysis"])
    print_section("ROADMAP", result["roadmap"])
    print_section("EVALUATION", result["evaluation"])

    print(f"\n{SEPARATOR}")
    print(f"  PIPELINE TERMINÉ — is_valid: {result['is_valid']}")
    print(SEPARATOR)