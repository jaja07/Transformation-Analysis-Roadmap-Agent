from core.state import AgentState
from schema.agent import DigitalRoadmapOutput
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from routing.router import get_llm_for_task, TaskComplexity

def generator_node(state: AgentState) -> dict:
    print("--- [AGENT GENERATOR] Génération de la Roadmap ---")
    
    llm = get_llm_for_task(TaskComplexity.COMPLEX)
    structured_llm = llm.with_structured_output(DigitalRoadmapOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Génère la roadmap finale. Assure-toi qu'elle est compatible avec "
                   "les contraintes spécifiées dans le document client."),
        ("user", "Document Client : {document_content}\n"
                 "Analyse Stratégique : {strategic_trajectory}\n"
                 "Contexte RAG : {retrieved_context}\n\n"
                 "Produis le JSON final.")
    ])
    
    chain = prompt | structured_llm
    
    roadmap = chain.invoke({
        "document_content": state["business_case"].document_content or "N/A",
        "strategic_trajectory": state.get("strategic_trajectory", ""),
        "retrieved_context": state.get("retrieved_context", "")
    })
    
    return {"final_roadmap": roadmap}