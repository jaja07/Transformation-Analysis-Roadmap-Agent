def init_vector_store(path: str = "."):
    """Placeholder: initialise ou recharge la base vectorielle."""
    return None

from functools import lru_cache
from pathlib import Path
from typing import Any

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from core.config import settings
from utils import log


@lru_cache(maxsize=1)
def _get_embedder() -> HuggingFaceEmbeddings:
    """The embedder is a singleton - loading sentence-transformers takes
    ~3 seconds; we only want to pay that cost once per process."""
    log.info(f"Loading embedding model: {settings.embedding_model}")
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_index(chunks: list[Document], persist_path: Path | None = None) -> FAISS:
    """Build a fresh FAISS index from chunks and save it to disk."""
    persist_path = persist_path or settings.vector_store_path
    persist_path.mkdir(parents=True, exist_ok=True)

    log.info(f"Building FAISS index over {len(chunks)} chunks")
    embedder = _get_embedder()
    store = FAISS.from_documents(documents=chunks, embedding=embedder)
    store.save_local(str(persist_path))
    log.info(f"FAISS index saved to {persist_path}")
    return store


@lru_cache(maxsize=1)
def load_index(persist_path: Path | None = None) -> FAISS:
    """Load the persisted FAISS index. Cached so the index is loaded once
    even if multiple modules call load_index() at startup."""
    persist_path = persist_path or settings.vector_store_path
    if not (persist_path / "index.faiss").exists():
        raise FileNotFoundError(
            f"FAISS index missing at {persist_path}. "
            "Run `python build_index.py` first."
        )
    log.info(f"Loading FAISS index from {persist_path}")
    store = FAISS.load_local(
        folder_path=str(persist_path),
        embeddings=_get_embedder(),
        allow_dangerous_deserialization=True,
    )
    log.info(f"FAISS ready: {store.index.ntotal} vectors, {store.index.d} dims")
    return store


def get_index_stats(persist_path: Path | None = None) -> dict[str, Any]:
    """Return stats about the index - used by the /health endpoint."""
    persist_path = persist_path or settings.vector_store_path
    if not (persist_path / "index.faiss").exists():
        return {"exists": False}

    store = load_index(persist_path)
    by_framework: dict[str, int] = {}
    for doc in store.docstore._dict.values():
        fw = doc.metadata.get("framework", "unknown")
        by_framework[fw] = by_framework.get(fw, 0) + 1

    return {
        "exists": True,
        "total_vectors": store.index.ntotal,
        "dimensions": store.index.d,
        "by_framework": by_framework,
        "embedding_model": settings.embedding_model,
    }