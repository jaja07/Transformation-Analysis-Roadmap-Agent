"""
agents/roadmap_generator/graph.py
Sous-graph LangGraph du Roadmap Generator Agent.
"""

from langgraph.graph import StateGraph, START, END
from roadmap_generator.state import RoadmapState
from roadmap_generator.nodes import roadmap_node


# ---------------------------------------------------------------------------
# Construction du sous-graph
# ---------------------------------------------------------------------------

def build_roadmap_graph():
    """
    Construit et compile le sous-graph du Roadmap Generator Agent.

    Structure :
        START → roadmap → END
    """
    graph = StateGraph(RoadmapState)
    graph.add_node("roadmap", roadmap_node)
    graph.add_edge(START, "roadmap")
    graph.add_edge("roadmap", END)
    return graph.compile()


# Instance compilée — importée par l'orchestrateur
roadmap_graph = build_roadmap_graph()


# ---------------------------------------------------------------------------
# Test rapide — python agents/roadmap_generator/graph.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Test Roadmap Generator Agent ===\n")

    initial_state: RoadmapState = {
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
            "1. CUSTOMER CENTRICITY\n"
            "Situation: Fragmented multi-channel experience.\n"
            "Gap/Opportunity: Unified digital customer journey.\n"
            "Priority: HIGH\n\n"
            "2. NEW TECHNOLOGIES\n"
            "Situation: Legacy core banking system.\n"
            "Gap/Opportunity: API-first and cloud-native architecture.\n"
            "Priority: HIGH\n\n"
            "5. PROCESS ENGINEERING\n"
            "Situation: Manual loan approval taking 5 days.\n"
            "Gap/Opportunity: Automated credit scoring workflow.\n"
            "Priority: HIGH"
        ),
        "strategic_analysis": (
            "PURPOSE:\n"
            "Become the leading digital bank for SMEs by 2026 through radical simplification "
            "of customer journeys and full automation of core banking processes.\n\n"
            "OPERATIONAL PILLARS:\n"
            "- Process: Automate loan approval, digitize onboarding, streamline back-office\n"
            "- People: Train 200 staff on digital tools, hire 10 data engineers\n"
            "- Platform: Migrate to cloud, adopt API gateway, deploy AI credit scoring\n"
            "- Partners: Partner with fintech for credit scoring, cloud provider for infra\n\n"
            "VALUE CREATED:\n"
            "- For customers: Loan approval in under 1 hour, 24/7 digital access\n"
            "- For the business: 20% cost reduction, 15% revenue growth\n"
            "- KPIs: NPS +20, loan approval time <1h, cost-to-income ratio -20%\n\n"
            "PITFALLS TO AVOID:\n"
            "1. Underestimating legacy system migration complexity\n"
            "2. Lack of change management for frontline staff\n"
            "3. Regulatory compliance delays on AI-based credit decisions\n\n"
            "TRANSFORMATION INITIATIVES:\n"
            "1. Redesign mobile app — Customer Centricity — Platform — HIGH impact — QUICK WIN\n"
            "2. Automate loan approval with AI — Process Engineering — Platform+Process — HIGH — STRUCTURAL\n"
            "3. Cloud migration of core systems — New Technologies — Platform — HIGH — STRUCTURAL\n"
            "4. Digital onboarding workflow — Customer Centricity — Process — MEDIUM — QUICK WIN\n"
            "5. Data analytics platform — Cloud and Data — Platform+Partners — MEDIUM — STRUCTURAL\n"
            "6. Digital skills training program — Leadership & Culture — People — MEDIUM — STRUCTURAL\n"
            "7. Digital marketing automation — Digital Marketing — Platform — LOW — OPTIMIZATION"
        ),
        "global_context": (
            "Roadmaps should be phased: quick wins first to build momentum, "
            "then structural changes, then optimization. "
            "Each initiative needs a clear owner, timeline, budget, and KPIs."
        ),
        "roadmap": "",
    }

    print("[Test] Lancement du Roadmap Generator Agent...\n")
    result = roadmap_graph.invoke(initial_state)

    print("── ROADMAP ──")
    print(result["roadmap"])
    print("\n=== Test terminé ✓ ===")