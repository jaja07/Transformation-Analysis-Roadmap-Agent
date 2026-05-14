from core.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from routing.router import get_llm_for_task, TaskComplexity

def planner_node(state: AgentState) -> dict:
    """
    Analyse le cas d'entreprise et structure la logique Why/What/How.
    """
    print("--- [AGENT PLANNER] Analyse en cours ---")
    
    # 1. Récupération des données du state
    company_name = state["business_case"].company_name
    context_text = state["business_case"].context_text
    
    # 2. Définition du modèle (utilise Flash pour les tâches rapides)
    llm = get_llm_for_task(TaskComplexity.SIMPLE, temperature=0.2)
    
    # 3. Le Prompt (idéalement à déplacer dans agents/prompts.py plus tard)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un architecte d'entreprise expert en transformation digitale. "
                   "Ton rôle est d'analyser la situation d'une entreprise et de structurer "
                   "les enjeux selon le framework IMD/Cisco : Why transform? What to transform? How to transform?"),
        ("user", "Entreprise : {company_name}\n\nContexte : {context_text}\n\n"
                 "Produis une analyse stratégique claire et structurée.")
    ])
    
    # 4. Exécution de la chaîne (Prompt -> LLM)
    chain = prompt | llm
    response = chain.invoke({
        "company_name": company_name,
        "context_text": context_text
    })
    
    # 5. Mise à jour du State
    # On retourne un dictionnaire avec la clé correspondante dans AgentState
    return {"planner_analysis": response.content}