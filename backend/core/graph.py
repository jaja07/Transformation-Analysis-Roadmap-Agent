# from langgraph.graph import StateGraph, START, END
# from core.state import AgentState

# # Imports de tes nœuds
# from agents.planner import planner_node
# from retrieval.retriever import retriever_node
# from agents.canvas_analyst import analyst_node
# from agents.strategist import strategist_node
# from agents.generator import generator_node
# from agents.evaluator import evaluator_node

# def route_evaluation(state: AgentState) -> str:
#     """Décide si on s'arrête ou si on renvoie au générateur pour correction."""
#     if state.get("is_valid", True):
#         return "END" # Fin du graphe
#     else:
#         print(f"⚠️ Correction demandée : {state.get('evaluation_feedback')}")
#         return "generator" # On retourne au générateur
    
# # 1. Initialisation du graphe avec notre State typé
# workflow = StateGraph(AgentState)

# # 2. Ajout des Nœuds (les coureurs)
# workflow.add_node("planner", planner_node)
# workflow.add_node("retriever", retriever_node)
# workflow.add_node("analyst", analyst_node)
# workflow.add_node("strategist", strategist_node)
# workflow.add_node("generator", generator_node)
# workflow.add_node("evaluator", evaluator_node) # 👈 AJOUT DU NŒUD ÉVALUATEUR
    
# # 3. Définition du cheminement linéaire (les relais)
# workflow.add_edge(START, "planner")
# workflow.add_edge("planner", "retriever")
# workflow.add_edge("retriever", "analyst")
# workflow.add_edge("analyst", "strategist")
# workflow.add_edge("strategist", "generator")   # 👈 CORRECTION : Le Stratège passe au Générateur
# workflow.add_edge("generator", "evaluator")

# # Boucle conditionnelle finale
# workflow.add_conditional_edges(
#     "evaluator", 
#     route_evaluation, 
#     {"END": END, "generator": "generator"}
# )

# # 4. Compilation du graphe
# compiled_graph = workflow.compile()