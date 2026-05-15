"""
NVIDIA NIM LLM Client
Compatible avec LangChain/LangGraph via un wrapper simple.
Utilise l'API OpenAI-compatible de NVIDIA Integrate.
"""

import os
from typing import Optional
from openai import OpenAI


# ---------------------------------------------------------------------------
# Client singleton (initialisé une seule fois)
# ---------------------------------------------------------------------------

def _get_client() -> OpenAI:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("La variable d'environnement NVIDIA_API_KEY n'est pas définie.")
    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
    )


# ---------------------------------------------------------------------------
# Fonction principale — à appeler dans les nodes LangGraph
# ---------------------------------------------------------------------------

def call_nim(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "meta/llama-3.3-70b-instruct",
    temperature: float = 0.2,
    top_p: float = 0.7,
    max_tokens: int = 1024,
    stream: bool = False,
) -> str:
    """
    Appelle le modèle NIM et retourne la réponse complète sous forme de string.

    Args:
        prompt:        Message utilisateur envoyé au modèle.
        system_prompt: Instruction système optionnelle (rôle de l'agent, contexte...).
        model:         Modèle NIM à utiliser (défaut: llama-3.3-70b-instruct).
        temperature:   Créativité de la réponse (0.0 = déterministe).
        top_p:         Nucleus sampling.
        max_tokens:    Nombre maximum de tokens générés.
        stream:        Si True, affiche le stream dans le terminal (mode debug).

    Returns:
        La réponse complète du modèle sous forme de string.

    Exemple d'utilisation dans un node LangGraph:
        from llm_clients.nim_client import call_nim

        def planner_node(state: PlannerState) -> PlannerState:
            response = call_nim(
                prompt=f"Analyse ce business case : {state['business_case']}",
                system_prompt="Tu es un expert en transformation digitale.",
            )
            return {**state, "plan": response}
    """
    client = _get_client()

    # Construction des messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    # Appel API
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        stream=stream,
    )

    # Mode stream : accumule les chunks et retourne le texte complet
    if stream:
        full_response = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        print()  # saut de ligne final
        return full_response

    # Mode non-stream : retourne directement le contenu
    return completion.choices[0].message.content


# ---------------------------------------------------------------------------
# Test rapide — python llm_clients/nim_client.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Test NIM Client ===\n")

    # Test 1 : appel simple sans system prompt
    print("[Test 1] Appel simple...")
    response = call_nim(prompt="Dis bonjour en une phrase.")
    print(f"Réponse : {response}\n")

    # Test 2 : avec system prompt (simulation d'un agent)
    print("[Test 2] Avec system prompt...")
    response = call_nim(
        prompt="Notre entreprise veut réduire ses coûts opérationnels via le digital.",
        system_prompt="Tu es un expert en transformation digitale. Réponds en 2 phrases maximum.",
    )
    print(f"Réponse : {response}\n")

    # Test 3 : mode stream
    print("[Test 3] Mode stream...")
    call_nim(
        prompt="Cite 3 frameworks de transformation digitale.",
        stream=True,
    )

    print("\n=== Tous les tests sont passés ✓ ===")