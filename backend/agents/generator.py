from core.state import AgentState
from schema.agent import DigitalRoadmapOutput
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from routing.router import get_llm_for_task, TaskComplexity

def generator_node(state: AgentState) -> dict:
    """
    Génère la roadmap finale en forçant le respect du schéma Pydantic.
    """
    print("--- [AGENT GENERATOR] Création de la Roadmap Structurée ---")
    
    llm = get_llm_for_task(TaskComplexity.COMPLEX, temperature=0.2)
    
    # 2. On force le LLM à répondre EXCLUSIVEMENT sous le format de notre modèle Pydantic
    structured_llm = llm.with_structured_output(DigitalRoadmapOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un consultant en stratégie digitale. À partir des analyses précédentes "
                   "et du contexte documentaire, génère une roadmap de transformation digitale complète et structurée."),
        ("user", "Analyse du Planificateur : {planner_analysis}\n"
                 "Contexte RAG : {retrieved_context}\n\n"
                 "Génère la roadmap finale.")
    ])
    
    chain = prompt | structured_llm
    
    # 3. Invocation : la réponse sera directement un objet Pydantic (DigitalRoadmapOutput)
    roadmap = chain.invoke({
        "planner_analysis": state.get("planner_analysis", "Pas d'analyse"),
        "retrieved_context": state.get("retrieved_context", "Pas de contexte")
    })
    
    return {"final_roadmap": roadmap}