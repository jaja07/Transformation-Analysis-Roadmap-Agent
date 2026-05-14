from core.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from routing.router import get_llm_for_task, TaskComplexity

def analyst_node(state: AgentState) -> dict:
    """
    Analyse l'entreprise selon les 7 domaines du Digital Transformation Canvas.
    """
    print("--- [AGENT ANALYST] Analyse par Frameworks ---")
    
    llm = get_llm_for_task(TaskComplexity.SIMPLE, temperature=0.1)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un analyste stratégique. Ton rôle est d'analyser le cas client "
                   "en utilisant le 'Digital Transformation Canvas'. Tu dois identifier les éléments "
                   "pour les 7 domaines : Customer Centricity, New Technologies, Cloud and Data, "
                   "Digital Business Development, Process Engineering, Digital Leadership & Culture, "
                   "et Digital Marketing."),
        ("user", "Analyse du Planner : {planner_analysis}\n"
                 "Contexte RAG : {retrieved_context}\n\n"
                 "Produis une analyse détaillée pour chaque domaine du canvas.")
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "planner_analysis": state.get("planner_analysis", ""),
        "retrieved_context": state.get("retrieved_context", "")
    })
    
    return {"canvas_analysis": response.content}