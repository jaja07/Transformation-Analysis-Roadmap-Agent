from enum import Enum
from llm_clients.gemini_client import get_gemini_flash, get_gemini_pro
from llm_clients.llama_client import get_local_llama

class TaskComplexity(Enum):
    """Définition des niveaux de complexité pour le routage."""
    SIMPLE = "simple"           # Reformulation, synthèse, extraction, premier jet [cite: 633]
    COMPLEX = "complex"         # Raisonnement complexe, stratégie, génération finale [cite: 634]
    REPETITIVE = "repetitive"   # Expérimentation, traitement faible criticité, local [cite: 634]

def get_llm_for_task(task_type: TaskComplexity, temperature: float = 0.2):
    """
    Route la demande vers le modèle LLM le plus adapté en fonction de la tâche.
    Optimise la latence et la consommation de crédits.
    """
    if task_type == TaskComplexity.COMPLEX:
        print("[ROUTAGE] Sélection de Gemini 2.5 Pro (Raisonnement avancé)")
        return get_gemini_pro(temperature=temperature)
        
    elif task_type == TaskComplexity.SIMPLE:
        print("[ROUTAGE] Sélection de Gemini 2.5 Flash (Rapide & Économique)")
        return get_gemini_flash(temperature=temperature)
        
    elif task_type == TaskComplexity.REPETITIVE:
        print("[ROUTAGE] Sélection de Llama Local (Zéro coût API)")
        return get_local_llama(temperature=temperature)
        
    else:
        # Fallback par défaut pour éviter les plantages
        print("[ROUTAGE] Type inconnu. Fallback sur Gemini Flash.")
        return get_gemini_flash(temperature=temperature)