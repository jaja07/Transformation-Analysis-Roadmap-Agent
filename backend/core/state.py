from typing import TypedDict, Optional
from schema.schemas import BusinessCaseInput, DigitalRoadmapOutput

class AgentState(TypedDict):
    # 1. Les données d'entrée
    business_case: BusinessCaseInput
    
    # 2. Les données issues du RAG (que ton binôme va populer)
    retrieved_context: str
    
    # 3. Les réflexions intermédiaires (populées par tes agents)
    planner_analysis: Optional[str]
    canvas_analysis: Optional[str]
    strategic_trajectory: Optional[str]
    
    # 4. Le résultat final
    final_roadmap: Optional[DigitalRoadmapOutput]