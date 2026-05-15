"""Data ingestion utilities: extraction and chunking."""
from .loader import load_corpus
from .chunking import chunk_documents
__all__ = ["load_corpus", "chunk_documents"]