from pydantic import BaseModel, Field
from core.state import AgentState
from routing.router import get_llm_for_task, TaskComplexity
from langchain_core.prompts import ChatPromptTemplate

# 1. On définit ce que l'évaluateur doit répondre
class EvaluationOutput(BaseModel):
    is_valid: bool = Field(description="True si la roadmap est cohérente, complète et sans hallucinations. False si elle doit être corrigée.")
    feedback: str = Field(description="Si is_valid est False, explique ce qui manque (ex: 'Il manque les KPIs', 'Le budget est irréaliste'). Si True, écris 'Validation OK'.")

def evaluator_node(state: AgentState) -> dict:
    """
    Vérifie la cohérence et la complétude de la roadmap générée.
    """
    print("--- [AGENT EVALUATOR] Vérification de la Roadmap ---")
    
    # On utilise Flash car c'est une tâche de vérification rapide et structurée
    llm = get_llm_for_task(TaskComplexity.SIMPLE, temperature=0.1)
    structured_llm = llm.with_structured_output(EvaluationOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un auditeur interne expert en transformation digitale. "
                   "Ton rôle est de vérifier la roadmap générée. Vérifie qu'elle est cohérente "
                   "avec l'analyse initiale, qu'il n'y a pas d'hallucinations, et que tous les champs (budget, KPIs) sont réalistes. "
                   "Sois strict mais constructif."),
        ("user", "Analyse Initiale : {planner_analysis}\n"
                 "Roadmap Générée : {final_roadmap}\n\n"
                 "Évalue cette roadmap.")
    ])
    
    chain = prompt | structured_llm
    
    # On convertit l'objet roadmap en dictionnaire/string pour que le LLM puisse le lire
    roadmap_str = str(state.get("final_roadmap", ""))
    
    evaluation = chain.invoke({
        "planner_analysis": state.get("planner_analysis", ""),
        "final_roadmap": roadmap_str
    })
    
    print(f"    -> Résultat de l'évaluation : {'✅ Valide' if evaluation.is_valid else '❌ À corriger'}")
    
    # On retourne le statut d'évaluation. 
    # Assure-toi d'ajouter "evaluation_feedback" dans ton AgentState !
    return {
        "is_valid": evaluation.is_valid,
        "evaluation_feedback": evaluation.feedback
    }