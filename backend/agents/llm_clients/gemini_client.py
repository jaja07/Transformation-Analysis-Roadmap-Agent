import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Chargement des variables d'environnement
load_dotenv()

def get_gemini_flash(temperature: float = 0.2) -> ChatGoogleGenerativeAI:
    """
    Instancie Gemini 2.5 Flash.
    Idéal pour : Tâches simples, reformulation, synthèse, extraction rapide.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=temperature,
        max_retries=2
    )

def get_gemini_pro(temperature: float = 0.1) -> ChatGoogleGenerativeAI:
    """
    Instancie Gemini 2.5 Pro.
    Idéal pour : Raisonnement complexe, stratégie, génération de la roadmap finale.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=temperature,
        max_retries=2
    )