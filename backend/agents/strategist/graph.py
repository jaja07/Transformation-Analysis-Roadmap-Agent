"""
agents/strategist/graph.py
Sous-graph LangGraph du Strategist Agent.
"""

from langgraph.graph import StateGraph, START, END
from strategist.state import StrategistState
from strategist.nodes import strategist_node


# ---------------------------------------------------------------------------
# Construction du sous-graph
# ---------------------------------------------------------------------------

def build_strategist_graph():
    """
    Construit et compile le sous-graph du Strategist Agent.

    Structure :
        START → strategist → END
    """
    graph = StateGraph(StrategistState)
    graph.add_node("strategist", strategist_node)
    graph.add_edge(START, "strategist")
    graph.add_edge("strategist", END)
    return graph.compile()


# Instance compilée — importée par l'orchestrateur
strategist_graph = build_strategist_graph()


# ---------------------------------------------------------------------------
# Test rapide — python agents/strategist/graph.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Test Strategist Agent ===\n")

    initial_state: StrategistState = {
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
        "why": (
            "Losing market share to neobanks, outdated mobile app, "
            "slow manual processes, growing customer expectations for digital-first services."
        ),
        "canvas_analysis": (
            "1. CUSTOMER CENTRICITY\n"
            "Situation: Customer experience is fragmented across channels.\n"
            "Gap/Opportunity: Build a unified digital customer journey.\n"
            "Priority: HIGH\n\n"
            "2. NEW TECHNOLOGIES\n"
            "Situation: Legacy core banking system limits agility.\n"
            "Gap/Opportunity: Adopt API-first architecture and cloud-native services.\n"
            "Priority: HIGH\n\n"
            "5. PROCESS ENGINEERING\n"
            "Situation: Loan approval is fully manual, taking 5 days.\n"
            "Gap/Opportunity: Automate credit scoring and approval workflow.\n"
            "Priority: HIGH"
        ),
        "how_context": (
            "Digital transformation roadmaps typically follow a phased approach: "
            "quick wins in the first 3 months to build momentum, "
            "structural changes in months 4-12, "
            "and continuous optimization beyond. "
            "Key success factors include executive sponsorship, agile delivery, "
            "and a clear governance model."
        ),
        "global_context": (
            "The IMD/Cisco framework emphasizes that transformation must address "
            "Why, What and How simultaneously. "
            "The academic canvas framework adds Purpose, Pillars, Value and Pitfalls "
            "as essential dimensions of any credible transformation strategy."
        ),
        "strategic_analysis": "",
    }

    print("[Test] Lancement du Strategist Agent...\n")
    result = strategist_graph.invoke(initial_state)

    print("── STRATEGIC ANALYSIS ──")
    print(result["strategic_analysis"])
    print("\n=== Test terminé ✓ ===")