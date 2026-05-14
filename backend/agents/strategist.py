from core.state import AgentState
from routing.router import get_llm_for_task, TaskComplexity
from langchain_core.prompts import ChatPromptTemplate

def strategist_node(state: AgentState) -> dict:
    """
    Définit la trajectoire stratégique en utilisant le framework académique (Elia et al., 2024).
    Mobilise les piliers opérationnels, la valeur attendue et les risques.
    """
    print("--- [AGENT STRATEGIST] Élaboration de la Stratégie Globale ---")
    
    # Appel au routeur : Tâche COMPLEXE = Gemini Pro (pour le raisonnement profond)
    # Température légèrement augmentée pour permettre la proposition d'initiatives
    llm = get_llm_for_task(TaskComplexity.COMPLEX, temperature=0.2)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un Directeur de la Stratégie Digitale (CDO). Ton rôle est d'élaborer une "
                   "trajectoire stratégique cohérente. Utilise le framework d'Elia et al. (2024) pour structurer ta réponse : "
                   "1. Strategic Purpose (Pourquoi on le fait), "
                   "2. Operational Pillars (Process, People, Platform, Partners), "
                   "3. Expected Value (Performance, Planet, Product), "
                   "4. Pitfalls & Risks (Protection, Privacy)."),
        ("user", "Analyse initiale (Why/What/How) : {planner_analysis}\n"
                 "Grille de lecture (Canvas 7 domaines) : {canvas_analysis}\n"
                 "Contexte documentaire : {retrieved_context}\n\n"
                 "À partir de ces éléments, rédige la trajectoire stratégique complète de l'entreprise.")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({
        "planner_analysis": state.get("planner_analysis", ""),
        "canvas_analysis": state.get("canvas_analysis", ""),
        "retrieved_context": state.get("retrieved_context", "")
    })
    
    # On retourne la mise à jour pour le State
    return {"strategic_trajectory": response.content}