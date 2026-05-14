import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama

load_dotenv()

def get_local_llama(temperature: float = 0.2, model_name: str = "llama3.2") -> ChatOllama:
    """
    Instancie le modèle Llama via Ollama en local.
    Idéal pour : Tâches répétitives, expérimentations, ou traitements à faible criticité
    sans consommer de crédits API.
    """
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    return ChatOllama(
        base_url=base_url,
        model=model_name,
        temperature=temperature
    )