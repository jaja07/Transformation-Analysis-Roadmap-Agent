from typing import TypedDict, Optional
from schema.agent import BusinessCaseInput, DigitalRoadmapOutput

class AgentState(TypedDict):
    # 1. Les données d'entrée
    business_case: BusinessCaseInput
    
    # 2. Les données issues du RAG (populées par le binôme)
    retrieved_context: str
    
    # 3. Les réflexions intermédiaires (populées par les agents)
    planner_analysis: Optional[str]
    canvas_analysis: Optional[str]
    strategic_trajectory: Optional[str]
    
    # 4. Le contrôle qualité (populé par l'Evaluator) 👈 LES AJOUTS SONT ICI
    is_valid: Optional[bool]
    evaluation_feedback: Optional[str]
    
    # 5. Le résultat final
    final_roadmap: Optional[DigitalRoadmapOutput]