"""Data ingestion utilities: extraction and chunking."""
from data_ingestion.loader import load_corpus
from data_ingestion.chunking import chunk_documents
__all__ = ["load_corpus", "chunk_documents"]