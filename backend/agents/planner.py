from core.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from routing.router import get_llm_for_task, TaskComplexity

def planner_node(state: AgentState) -> dict:
    print("--- [AGENT PLANNER] Structuration de l'intention ---")
    
    llm = get_llm_for_task(TaskComplexity.SIMPLE)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un expert en stratégie. Ton rôle est de définir le 'Why/What/How' "
                   "de la transformation en te basant sur le message et le document client."),
        ("user", "Nom de l'entreprise : {company_name}\n"
                 "Message utilisateur : {user_input}\n"
                 "Contenu du document : {document_content}\n\n" # 👈 Ajout ici
                 "Identifie les objectifs et les contraintes majeures.")
    ])
    
    chain = prompt | llm
    
    # Injection des données dans le .invoke()
    response = chain.invoke({
        "company_name": state["business_case"].company_name,
        "user_input": state["business_case"].context_text,
        # On récupère le texte extrait du PDF. Si None, on met une chaîne vide.
        "document_content": state["business_case"].document_content or "Aucun document n'a été fourni."
    })
    
    return {"planner_analysis": response.content}