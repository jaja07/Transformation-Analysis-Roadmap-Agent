from fastapi import APIRouter, HTTPException
from schema.schemas import BusinessCaseInput
from core.graph import compiled_graph

router = APIRouter()

@router.post("/analyze", summary="Réceptionne le cas d'entreprise et lance l'analyse")
async def analyze_business_case(payload: BusinessCaseInput):
    """
    Reçoit un cas d'entreprise (texte libre), valide l'entrée, 
    et initialise l'état du système multi-agents.
    """
    try:
        # 1. Initialisation de l'état LangGraph avec le payload validé
        initial_state = {
            "business_case": payload,
            "planner_analysis": None,
            "retrieved_context": None
        }
        
        # 2. Simulation de l'appel au graphe (en attendant de le coder)
        print(f"--- Réception de l'input pour : {payload.company_name} ---")
        print(f"Contexte : {payload.context_text[:50]}...")
        
        final_state = await compiled_graph.ainvoke(initial_state) # type: ignore
        return {
            "status": "success",
            "roadmap": final_state["final_roadmap"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))