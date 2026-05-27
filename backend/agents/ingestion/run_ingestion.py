"""
ingestion/run_ingestion.py
Point d'entrée one-shot pour construire la base vectorielle ChromaDB.

Usage :
    python ingestion/run_ingestion.py

Ce script doit être lancé UNE SEULE FOIS (ou à chaque mise à jour du corpus).
Il charge les PDFs, les découpe, génère les embeddings et sauvegarde ChromaDB.
Les agents utilisent ensuite la DB sans relancer ce script.
"""

import sys
from pathlib import Path

# Ajouter la racine du backend au path (pour importer `agents`, `core`, ...)
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Imports nommés depuis le package racine `agents` pour cohérence
from agents.ingestion.loader import load_corpus
from agents.ingestion.chunker import chunk_documents
from agents.ingestion.embedder import save_to_chroma


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_DIR        = Path(__file__).resolve().parent.parent
CORPUS_DIR      = BASE_DIR / "data" / "corpus"
CHROMA_PATH     = BASE_DIR / "vector_store" / "chroma_db"
COLLECTION_NAME = "digital_transformation_corpus"

# Paramètres de chunking
CHUNK_SIZE    = 800
CHUNK_OVERLAP = 150


# ---------------------------------------------------------------------------
# Pipeline d'ingestion
# ---------------------------------------------------------------------------

def run_ingestion():
    print("=" * 60)
    print("  PIPELINE D'INGESTION — Digital Transformation RAG")
    print("=" * 60)
    print()

    # Étape 1 : Chargement des PDFs
    print("── Étape 1/3 : Chargement des PDFs ──")
    documents = load_corpus(CORPUS_DIR)

    # Étape 2 : Chunking
    print("── Étape 2/3 : Chunking ──")
    chunks = chunk_documents(
        documents,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # Étape 3 : Embedding + sauvegarde ChromaDB
    print("── Étape 3/3 : Embedding + sauvegarde ChromaDB ──")
    collection = save_to_chroma(
        chunks=chunks,
        chroma_path=str(CHROMA_PATH),
        collection_name=COLLECTION_NAME,
    )

    # Résumé
    print("=" * 60)
    print("  INGESTION TERMINÉE ✓")
    print(f"  Documents chargés : {len(documents)}")
    print(f"  Chunks créés      : {len(chunks)}")
    print(f"  Vecteurs indexés  : {collection.count()}")
    print(f"  DB sauvegardée    : {CHROMA_PATH.resolve()}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Vérification préalable du corpus
    if not CORPUS_DIR.exists():
        print(f"✗ Dossier corpus introuvable : {CORPUS_DIR.resolve()}")
        print("  Crée le dossier 'data/corpus/' et place tes 4 PDFs dedans.")
        sys.exit(1)

    run_ingestion()