"""
agents/canvas_analyst/graph.py
Sous-graph LangGraph du Canvas Analyst Agent.
"""

from langgraph.graph import StateGraph, START, END
from canvas_analyst.state import CanvasState
from canvas_analyst.nodes import canvas_analysis_node


# ---------------------------------------------------------------------------
# Construction du sous-graph
# ---------------------------------------------------------------------------

def build_canvas_graph():
    """
    Construit et compile le sous-graph du Canvas Analyst Agent.

    Structure :
        START → canvas_analysis → END
    """
    graph = StateGraph(CanvasState)
    graph.add_node("canvas_analysis", canvas_analysis_node)
    graph.add_edge(START, "canvas_analysis")
    graph.add_edge("canvas_analysis", END)
    return graph.compile()


# Instance compilée — importée par l'orchestrateur
canvas_graph = build_canvas_graph()


# ---------------------------------------------------------------------------
# Test rapide — python agents/canvas_analyst/graph.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Test Canvas Analyst Agent ===\n")

    initial_state: CanvasState = {
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
        "what_context": (
            "The Digital Transformation Canvas identifies 7 action fields: "
            "Customer Centricity, New Technologies, Cloud and Data, "
            "Digital Business Development, Process Engineering, "
            "Digital Leadership & Culture, and Digital Marketing. "
            "Each field requires a structured analysis of current maturity and priority gaps."
        ),
        "global_context": (
            "Digital transformation is a journey driven by customer expectations, "
            "competitive pressure, and emerging technologies. "
            "It requires aligning strategy, operations, and culture."
        ),
        "canvas_analysis": "",
    }

    print("[Test] Lancement du Canvas Analyst Agent...\n")
    result = canvas_graph.invoke(initial_state)

    print("── CANVAS ANALYSIS ──")
    print(result["canvas_analysis"])
    print("\n=== Test terminé ✓ ===")