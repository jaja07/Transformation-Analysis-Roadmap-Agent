from typing import TypedDict, List, Optional
from pydantic import BaseModel
from models.schemas import BusinessCaseInput, DigitalRoadmapOutput

class AgentState(TypedDict):
    # 1. Input initial
    business_case: BusinessCaseInput
    
    # 2. Contexte RAG
    retrieved_documents: List[str]
    
    # 3. Analyses intermédiaires des agents
    planner_analysis: Optional[str]
    canvas_analysis: Optional[str]
    strategic_trajectory: Optional[str]
    
    # 4. Évaluation et Résultat
    validation_feedback: Optional[str] # Géré par l'Evaluator
    final_roadmap: Optional[DigitalRoadmapOutput]