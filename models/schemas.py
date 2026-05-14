from pydantic import BaseModel, Field
from typing import List, Optional

# --- ENTRÉE UTILISATEUR ---
class BusinessCaseInput(BaseModel):
    company_name: str = Field(..., description="Le nom de l'entreprise étudiée")
    context_text: str = Field(..., description="Le texte brut décrivant la situation, les enjeux et les besoins de l'entreprise")

# --- SOUS-MODÈLES POUR LA ROADMAP ---
class Initiative(BaseModel):
    title: str = Field(..., description="Titre de l'initiative de transformation")
    description: str = Field(..., description="Description détaillée de l'action à mener")
    canvas_pillar: str = Field(..., description="Le pilier du Digital Transformation Canvas concerné (ex: Customer Centricity, Cloud and Data)")
    priority: str = Field(..., description="Niveau de priorité (ex: Quick Win, High, Medium)")
    budget_effort: str = Field(..., description="Estimation de l'effort ou du budget")
    timeline: str = Field(..., description="Horizon temporel (ex: Q1 2026, 6 mois)")

class TransformationRationale(BaseModel):
    why_transform: str = Field(..., description="Analyse du 'Why transform?' selon le framework IMD/Cisco")
    what_to_transform: str = Field(..., description="Analyse du 'What to transform?'")

# --- SORTIE FINALE DU SYSTÈME ---
class DigitalRoadmapOutput(BaseModel):
    rationale: TransformationRationale = Field(..., description="Le contexte stratégique de la transformation")
    initiatives: List[Initiative] = Field(..., description="La liste structurée des initiatives de la roadmap")
    overall_kpis: List[str] = Field(..., description="Les indicateurs clés de performance globaux pour suivre la transformation")