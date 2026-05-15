"""
agents/planner/graph.py
Sous-graph LangGraph du Planner Agent.
"""

from langgraph.graph import StateGraph, START, END
from planner.state import PlannerState
from planner.nodes import plan_node


# ---------------------------------------------------------------------------
# Construction du sous-graph
# ---------------------------------------------------------------------------

def build_planner_graph():
    """
    Construit et compile le sous-graph du Planner Agent.

    Structure :
        START → plan_node → END
    """
    graph = StateGraph(PlannerState)
    graph.add_node("plan", plan_node)
    graph.add_edge(START, "plan")
    graph.add_edge("plan", END)
    return graph.compile()


# Instance compilée — importée par l'orchestrateur
planner_graph = build_planner_graph()


# ---------------------------------------------------------------------------
# Test rapide — python agents/planner/graph.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Test Planner Agent ===\n")

    business_case = """
    Our company is a mid-sized retail bank with 500 employees.
    We are losing customers to neobanks because our mobile app is outdated
    and our loan approval process takes 5 days while competitors do it in minutes.
    We want to improve customer experience, reduce operational costs by 20%,
    and launch a fully digital loan product within 12 months.
    """

    initial_state: PlannerState = {
        "business_case": business_case.strip(),
        "why": "",
        "what": "",
        "how": "",
        "structured_problem": "",
    }

    print("[Test] Lancement du Planner Agent...\n")
    result = planner_graph.invoke(initial_state)

    print("── WHY ──")
    print(result["why"])
    print("\n── WHAT ──")
    print(result["what"])
    print("\n── HOW ──")
    print(result["how"])
    print("\n── STRUCTURED SUMMARY ──")
    print(result["structured_problem"])
    print("\n=== Test terminé ✓ ===")