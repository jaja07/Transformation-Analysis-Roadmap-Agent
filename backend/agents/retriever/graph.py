"""
agents/retriever/graph.py
Sous-graph LangGraph du Retrieval Agent.
"""

from langgraph.graph import StateGraph, START, END
from retriever.state import RetrievalState
from retriever.nodes import generate_queries_node, retrieve_node


# ---------------------------------------------------------------------------
# Construction du sous-graph
# ---------------------------------------------------------------------------

def build_retrieval_graph():
    """
    Construit et compile le sous-graph du Retrieval Agent.

    Structure :
        START → generate_queries → retrieve → END
    """
    graph = StateGraph(RetrievalState)

    graph.add_node("generate_queries", generate_queries_node)
    graph.add_node("retrieve", retrieve_node)

    graph.add_edge(START, "generate_queries")
    graph.add_edge("generate_queries", "retrieve")
    graph.add_edge("retrieve", END)

    return graph.compile()


# Instance compilée — importée par l'orchestrateur
retrieval_graph = build_retrieval_graph()


# ---------------------------------------------------------------------------
# Test rapide — python agents/retrieval_agent/graph.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from pathlib import Path

    print("=== Test Retrieval Agent ===\n")

    # Vérifier que ChromaDB existe
    if not Path("vector_store/chroma_db").exists():
        print("✗ ChromaDB introuvable.")
        print("  Lance d'abord : python ingestion/run_ingestion.py")
        exit(1)

    initial_state: RetrievalState = {
        "structured_problem": (
            "A mid-sized retail bank is losing customers to neobanks. "
            "It needs to modernize its mobile app, automate its loan approval process, "
            "and improve customer experience while reducing operational costs by 20%."
        ),
        "why": "Losing customers to neobanks, outdated technology, competitive pressure.",
        "what": "Mobile app, loan process, customer experience, operational efficiency.",
        "how": "Prioritize quick wins, then structural transformation over 12 months.",
        "why_context": "",
        "what_context": "",
        "how_context": "",
        "global_context": "",
    }

    print("[Test] Lancement du Retrieval Agent...\n")
    result = retrieval_graph.invoke(initial_state)

    print("── WHY CONTEXT ──")
    print(result["why_context"][:400], "...\n")

    print("── WHAT CONTEXT ──")
    print(result["what_context"][:400], "...\n")

    print("── HOW CONTEXT ──")
    print(result["how_context"][:400], "...\n")

    print("── GLOBAL CONTEXT ──")
    print(result["global_context"][:400], "...\n")

    print("=== Test terminé ✓ ===")