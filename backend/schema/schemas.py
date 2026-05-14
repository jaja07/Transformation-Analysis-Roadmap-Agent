from pydantic import BaseModel, Field
from typing import List, Optional

"""Modèles Pydantic pour les requêtes/réponses de l'API """

class BusinessCaseInput(BaseModel):
    company_name: str = Field(
        default=...,
        description="Le nom de l'entreprise étudiée.",
        example="Alexandra's Bikeshop"
    ) # type: ignore
    context_text: str = Field(
        default=...,
        description="Le texte brut décrivant la situation, les enjeux et les contraintes de l'entreprise. Ce texte peut être vague ou narratif.",
        example="Notre entreprise souhaite améliorer l'expérience client et réduire les coûts opérationnels..."
    ) # type: ignore
    # Optionnel : Si vous décidez de gérer l'upload de documents plus tard
    document_path: Optional[str] = Field(
        default=None,
        description="Chemin local vers le document uploadé, si applicable."
    )

# --- SOUS-MODÈLES POUR LA ROADMAP ---
class Initiative(BaseModel):
    title: str = Field(default=..., description="Titre de l'initiative de transformation")
    description: str = Field(default=..., description="Description détaillée de l'action à mener")
    canvas_pillar: str = Field(default=..., description="Le pilier du Digital Transformation Canvas concerné (ex: Customer Centricity, Cloud and Data)")
    priority: str = Field(default=..., description="Niveau de priorité (ex: Quick Win, High, Medium)")
    budget_effort: str = Field(default=..., description="Estimation de l'effort ou du budget")
    timeline: str = Field(default=..., description="Horizon temporel (ex: Q1 2026, 6 mois)")

class TransformationRationale(BaseModel):
    why_transform: str = Field(default=..., description="Analyse du 'Why transform?' selon le framework IMD/Cisco")
    what_to_transform: str = Field(default=..., description="Analyse du 'What to transform?'")

# --- SORTIE FINALE DU SYSTÈME ---
class DigitalRoadmapOutput(BaseModel):
    rationale: TransformationRationale = Field(default=..., description="Le contexte stratégique de la transformation")
    initiatives: List[Initiative] = Field(default=..., description="La liste structurée des initiatives de la roadmap")
    overall_kpis: List[str] = Field(default=..., description="Les indicateurs clés de performance globaux pour suivre la transformation")