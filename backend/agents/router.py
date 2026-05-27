import os
from enum import Enum
from agents.llm_clients import GeminiClient, LlamaClient, NIMClient

class TaskComplexity(Enum):
    SIMPLE = "simple"
    COMPLEX = "complex"
    LOCAL = "local" # Optionnel : pour forcer un modèle local sur des tâches non critiques

def get_llm_for_task(complexity: TaskComplexity, temperature: float = 0.0, **kwargs):
    """
    Route les requêtes vers le bon modèle LLM en fonction de la complexité de la tâche.
    Stratégie :
    - SIMPLE -> Gemini Flash (Rapide, pas cher, parfait pour l'extraction et l'évaluation structurée)
    - COMPLEX -> Nvidia NIM (Puissant, parfait pour la stratégie et la génération finale)
    - LOCAL -> Ollama Llama 3 (Gratuit, pour les tests ou tâches répétitives)
    """
    
    # 1. OVERRIDE DE DÉVELOPPEMENT (Pratique pour tester l'appli sans consommer de crédits)
    force_model = os.getenv("FORCE_LLM")
    if force_model == "ollama":
        print("[ROUTER] Routage forcé sur Ollama Local")
        return LlamaClient(temperature=temperature, **kwargs).get_client()
    elif force_model == "nvidia":
        print("[ROUTER] Routage forcé sur NVIDIA NIM")
        return NIMClient(temperature=temperature, **kwargs).get_client()
    elif force_model == "gemini":
        print("[ROUTER] Routage forcé sur Gemini")
        return GeminiClient(temperature=temperature, **kwargs).get_client()

    # 2. ROUTAGE INTELLIGENT BAsÉ SUR LA COMPLEXITÉ
    if complexity == TaskComplexity.SIMPLE:
        # Utilisé par : Planner, Analyst, Evaluator
        print(f"[ROUTER] Tâche {complexity.value.upper()} ⚡ Routage vers Gemini 2.5 Flash")
        # On utilise Gemini Flash car il est excellent et très rapide pour parser le RAG
        return GeminiClient(model_name="gemini-2.5-flash", temperature=temperature, **kwargs).get_client()
        
    elif complexity == TaskComplexity.COMPLEX:
        # Utilisé par : Strategist, Generator
        print(f"[ROUTER] Tâche {complexity.value.upper()} Routage vers NVIDIA NIM")
        # On garde Nvidia (qui utilise sûrement un gros modèle comme Llama 3 70B) pour la réflexion profonde
        return NIMClient(temperature=temperature, **kwargs).get_client()
        
    elif complexity == TaskComplexity.LOCAL:
        print(f"[ROUTER] Tâche {complexity.value.upper()} Routage vers Ollama Local")
        return LlamaClient(model_name="llama3", temperature=temperature, **kwargs).get_client()
        
    else:
        # Fallback de sécurité
        print(f"[ROUTER] Complexité inconnue, fallback sur Gemini Flash")
        return GeminiClient(model_name="gemini-2.5-flash", temperature=temperature, **kwargs).get_client()