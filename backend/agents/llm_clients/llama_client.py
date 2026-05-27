import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from core.config import settings

def get_local_llama(temperature: float = 0.2, model_name: str = "llama3.2") -> ChatOllama:
    """
    Instancie le modèle Llama via Ollama en local.
    Idéal pour : Tâches répétitives, expérimentations, ou traitements à faible criticité
    sans consommer de crédits API.
    """

    base_url = settings.OLLAMA_BASE_URL
    return ChatOllama(
        base_url=base_url,
        model=model_name,
        temperature=temperature
    )