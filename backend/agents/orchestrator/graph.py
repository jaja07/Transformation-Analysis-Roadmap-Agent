"""
orchestrator/graph.py
Graph principal — orchestre tous les sous-graphs en séquence.

Flux :
    START
      → planner
      → retrieval
      → canvas_analyst
      → strategist
      → roadmap_generator
      → evaluator
    END
"""

from langgraph.graph import StateGraph, START, END
from .state import GlobalState

# Import des sous-graphs compilés
from ..planner.graph import planner_graph
from ..retriever.graph import retrieval_graph
from ..canvas_analyst.graph import canvas_graph
from ..strategist.graph import strategist_graph
from ..roadmap_generator.graph import roadmap_graph
from ..evaluator.graph import evaluator_graph


# ---------------------------------------------------------------------------
# Nodes — chaque node appelle un sous-graph et mappe son output au GlobalState
# ---------------------------------------------------------------------------

def run_planner(state: GlobalState) -> GlobalState:
    result = planner_graph.invoke({
        "business_case": state["business_case"],
        "why": "",
        "what": "",
        "how": "",
        "structured_problem": "",
    })
    return {
        **state,
        "why": result["why"],
        "what": result["what"],
        "how": result["how"],
        "structured_problem": result["structured_problem"],
    }


def run_retrieval(state: GlobalState) -> GlobalState:
    result = retrieval_graph.invoke({
        "structured_problem": state["structured_problem"],
        "why": state["why"],
        "what": state["what"],
        "how": state["how"],
        "why_context": "",
        "what_context": "",
        "how_context": "",
        "global_context": "",
    }) # type: ignore
    return {
        **state,
        "why_context": result["why_context"],
        "what_context": result["what_context"],
        "how_context": result["how_context"],
        "global_context": result["global_context"],
    }


def run_canvas_analyst(state: GlobalState) -> GlobalState:
    result = canvas_graph.invoke({
        "business_case": state["business_case"],
        "structured_problem": state["structured_problem"],
        "what_context": state["what_context"],
        "global_context": state["global_context"],
        "canvas_analysis": "",
    })
    return {**state, "canvas_analysis": result["canvas_analysis"]}


def run_strategist(state: GlobalState) -> GlobalState:
    result = strategist_graph.invoke({
        "business_case": state["business_case"],
        "structured_problem": state["structured_problem"],
        "why": state["why"],
        "canvas_analysis": state["canvas_analysis"],
        "how_context": state["how_context"],
        "global_context": state["global_context"],
        "strategic_analysis": "",
    })
    return {**state, "strategic_analysis": result["strategic_analysis"]}


def run_roadmap_generator(state: GlobalState) -> GlobalState:
    result = roadmap_graph.invoke({
        "business_case": state["business_case"],
        "structured_problem": state["structured_problem"],
        "canvas_analysis": state["canvas_analysis"],
        "strategic_analysis": state["strategic_analysis"],
        "global_context": state["global_context"],
        "roadmap": "",
    })
    return {**state, "roadmap": result["roadmap"]}


def run_evaluator(state: GlobalState) -> GlobalState:
    result = evaluator_graph.invoke({
        "business_case": state["business_case"],
        "structured_problem": state["structured_problem"],
        "canvas_analysis": state["canvas_analysis"],
        "strategic_analysis": state["strategic_analysis"],
        "roadmap": state["roadmap"],
        "evaluation": "",
        "is_valid": False,
    })
    return {
        **state,
        "evaluation": result["evaluation"],
        "is_valid": result["is_valid"],
    }


# ---------------------------------------------------------------------------
# Construction du graph principal
# ---------------------------------------------------------------------------

def build_orchestrator():
    graph = StateGraph(GlobalState)

    graph.add_node("planner", run_planner)
    graph.add_node("retrieval", run_retrieval)
    graph.add_node("canvas_analyst", run_canvas_analyst)
    graph.add_node("strategist", run_strategist)
    graph.add_node("roadmap_generator", run_roadmap_generator)
    graph.add_node("evaluator", run_evaluator)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "retrieval")
    graph.add_edge("retrieval", "canvas_analyst")
    graph.add_edge("canvas_analyst", "strategist")
    graph.add_edge("strategist", "roadmap_generator")
    graph.add_edge("roadmap_generator", "evaluator")
    graph.add_edge("evaluator", END)

    return graph.compile()


# Instance compilée
orchestrator = build_orchestrator()