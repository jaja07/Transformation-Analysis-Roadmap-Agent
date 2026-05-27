"""
agents/evaluator/graph.py
Sous-graph LangGraph du Evaluator Agent.
"""

from langgraph.graph import StateGraph, START, END
from .state import EvaluatorState
from .nodes import evaluate_node


# ---------------------------------------------------------------------------
# Construction du sous-graph
# ---------------------------------------------------------------------------

def build_evaluator_graph():
    """
    Construit et compile le sous-graph du Evaluator Agent.

    Structure :
        START → evaluate → END
    """
    graph = StateGraph(EvaluatorState)
    graph.add_node("evaluate", evaluate_node)
    graph.add_edge(START, "evaluate")
    graph.add_edge("evaluate", END)
    return graph.compile()


# Instance compilée — importée par l'orchestrateur
evaluator_graph = build_evaluator_graph()


# ---------------------------------------------------------------------------
# Test rapide — python agents/evaluator/graph.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Test Evaluator Agent ===\n")

    initial_state: EvaluatorState = {
        "business_case": (
            "Our company is a mid-sized retail bank with 500 employees. "
            "We are losing customers to neobanks because our mobile app is outdated "
            "and our loan approval process takes 5 days while competitors do it in minutes. "
            "We want to improve customer experience, reduce operational costs by 20%, "
            "and launch a fully digital loan product within 12 months."
        ),
        "structured_problem": (
            "A retail bank facing competitive pressure from neobanks needs to modernize "
            "its digital channels, automate core processes, and rebuild its customer experience."
        ),
        "canvas_analysis": (
            "1. CUSTOMER CENTRICITY — Priority: HIGH\n"
            "2. NEW TECHNOLOGIES — Priority: HIGH\n"
            "5. PROCESS ENGINEERING — Priority: HIGH"
        ),
        "strategic_analysis": (
            "PURPOSE: Become the leading digital bank for SMEs by 2026.\n"
            "PILLARS: Process automation, People upskilling, Platform migration, Fintech partners.\n"
            "VALUE: NPS +20, loan approval <1h, cost reduction 20%.\n"
            "PITFALLS: Legacy migration complexity, change management, regulatory compliance."
        ),
        "roadmap": (
            "PHASE 1 — QUICK WINS (0-3 months)\n"
            "Initiative 1.1: Redesign mobile app\n"
            "  Owner: CTO | Duration: 8 weeks | Budget: Medium | KPIs: App rating >4.5\n\n"
            "Initiative 1.2: Digital onboarding workflow\n"
            "  Owner: CDO | Duration: 6 weeks | Budget: Low | KPIs: Onboarding time -50%\n\n"
            "PHASE 2 — STRUCTURAL TRANSFORMATION (4-9 months)\n"
            "Initiative 2.1: AI-powered loan approval\n"
            "  Owner: CTO+CFO | Duration: 6 months | Budget: High | KPIs: Approval time <1h\n\n"
            "Initiative 2.2: Cloud migration\n"
            "  Owner: CTO | Duration: 6 months | Budget: High | KPIs: Infra cost -30%\n\n"
            "PHASE 3 — OPTIMIZATION (10-18 months)\n"
            "Initiative 3.1: Digital marketing automation\n"
            "  Owner: CMO | Duration: 3 months | Budget: Medium | KPIs: CAC -20%"
        ),
        "evaluation": "",
        "is_valid": False,
    }

    print("[Test] Lancement du Evaluator Agent...\n")
    result = evaluator_graph.invoke(initial_state)

    print("── EVALUATION ──")
    print(result["evaluation"])
    print(f"\n── IS VALID: {result['is_valid']} ──")
    print("\n=== Test terminé ✓ ===")