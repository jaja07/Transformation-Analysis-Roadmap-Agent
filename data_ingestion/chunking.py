from typing import List


def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Very simple chunking by characters."""
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
