from typing import AsyncGenerator


async def get_db() -> AsyncGenerator:
    """Placeholder DB dependency (yield a session in real app)."""
    db = None
    try:
        yield db
    finally:
        pass


async def get_llm_client():
    """Placeholder LLM client dependency."""
    client = None
    return client
