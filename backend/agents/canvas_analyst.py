from core.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from routing.router import get_llm_for_task, TaskComplexity

def analyst_node(state: AgentState) -> dict:
    print("--- [AGENT ANALYST] Analyse des 7 domaines ---")
    
    llm = get_llm_for_task(TaskComplexity.SIMPLE)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Analyse l'entreprise via le Digital Transformation Canvas."),
        ("user", "Document Client : {document_content}\n" # 👈 Priorité au document
                 "Analyse du Planner : {planner_analysis}\n"
                 "Extraits de la littérature (RAG) : {retrieved_context}\n\n"
                 "Remplis les 7 domaines du canvas.")
    ])
    
    chain = prompt | llm
    
    # On passe les trois sources d'informations
    response = chain.invoke({
        "document_content": state["business_case"].document_content or "N/A",
        "planner_analysis": state.get("planner_analysis", ""),
        "retrieved_context": state.get("retrieved_context", "")
    })
    
    return {"canvas_analysis": response.content}