from langgraph.graph import StateGraph, START, END
from core.state import AgentState
from agents.planner import planner_node
from retrieval.retriever import retriever_node
from agents.generator import generator_node
from agents.canvas_analyst import analyst_node
from agents.strategist import strategist_node

# 1. Initialisation du graphe avec notre State typé
workflow = StateGraph(AgentState)

# 2. Ajout des Nœuds (les coureurs)
workflow.add_node("planner", planner_node)
workflow.add_node("retriever", retriever_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("strategist", strategist_node)
workflow.add_node("generator", generator_node)

# 3. Définition du cheminement linéaire (les relais)
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "retriever")
workflow.add_edge("retriever", "analyst")
workflow.add_edge("analyst", "strategist")
workflow.add_edge("retriever", "generator")
workflow.add_edge("generator", END)

# 4. Compilation du graphe
compiled_graph = workflow.compile()