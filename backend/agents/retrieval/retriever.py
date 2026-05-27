"""
retrieval/retriever.py
Interroge ChromaDB pour récupérer les chunks les plus pertinents.
Fonction utilitaire appelée par tous les agents qui ont besoin de RAG.
"""

import os
from pathlib import Path
from typing import Optional
from openai import OpenAI
import chromadb
from core.config import settings


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_EMBED_MODEL = "nvidia/nv-embedqa-e5-v5"
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CHROMA_PATH = BASE_DIR / "vector_store" / "chroma_db"
DEFAULT_COLLECTION  = "digital_transformation_corpus"
DEFAULT_N_RESULTS   = 5


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

RetrievedChunk = dict  # {"text": str, "metadata": {...}, "distance": float}


# ---------------------------------------------------------------------------
# Clients (initialisés une seule fois)
# ---------------------------------------------------------------------------

def _get_embed_client() -> OpenAI:
    api_key = settings.NVIDIA_API_KEY
    if not api_key:
        raise ValueError("La variable d'environnement NVIDIA_API_KEY n'est pas définie.")
    return OpenAI(
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1",
    )


def _get_chroma_collection(
    chroma_path: str | Path = DEFAULT_CHROMA_PATH,
    collection_name: str = DEFAULT_COLLECTION,
) -> chromadb.Collection:
    """Charge la collection ChromaDB persistante."""
    chroma_path = Path(chroma_path)
    if not chroma_path.exists():
        raise FileNotFoundError(
            f"ChromaDB introuvable : {chroma_path.resolve()}\n"
            "Lance d'abord : python ingestion/run_ingestion.py"
        )
    client = chromadb.PersistentClient(path=str(chroma_path))
    return client.get_collection(name=collection_name)


# ---------------------------------------------------------------------------
# Fonction principale
# ---------------------------------------------------------------------------

def retrieve(
    query: str,
    n_results: int = DEFAULT_N_RESULTS,
    filter_source: Optional[str] = None,
    chroma_path: str | Path = DEFAULT_CHROMA_PATH,
    collection_name: str = DEFAULT_COLLECTION,
    embed_model: str = DEFAULT_EMBED_MODEL,
) -> list[RetrievedChunk]:
    """
    Recherche les chunks les plus pertinents pour une query.

    Args:
        query:           Question ou requête en langage naturel.
        n_results:       Nombre de chunks à retourner.
        filter_source:   Filtrer par nom de fichier source (ex: "wade_2015.pdf").
        chroma_path:     Chemin vers la DB ChromaDB persistante.
        collection_name: Nom de la collection ChromaDB.
        embed_model:     Modèle d'embedding NIM.

    Returns:
        Liste de chunks triés par pertinence (distance cosinus).

    Exemple d'utilisation dans un node LangGraph :
        from retrieval.retriever import retrieve

        def analyst_node(state: CanvasState) -> CanvasState:
            chunks = retrieve("Digital Transformation Canvas 7 action fields", n_results=4)
            context = format_chunks(chunks)
            ...
    """
    # 1. Embedder la query
    embed_client = _get_embed_client()
    response = embed_client.embeddings.create(
        input=[query],
        model=embed_model,
        encoding_format="float",
        extra_body={"input_type": "query"},
    )
    query_vector = response.data[0].embedding

    # 2. Construire le filtre optionnel
    where_filter = {"source": filter_source} if filter_source else None

    # 3. Interroger ChromaDB
    collection = _get_chroma_collection(chroma_path, collection_name)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n_results,
        where=where_filter, # type: ignore
        include=["documents", "metadatas", "distances"],
    )

    # 4. Formater les résultats
    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0], # type: ignore
        results["metadatas"][0], # type: ignore
        results["distances"][0], # type: ignore
    ):
        chunks.append({
            "text": doc,
            "metadata": meta,
            "distance": round(dist, 4),  # distance cosinus (plus bas = plus pertinent)
        })

    return chunks


def format_chunks(chunks: list[RetrievedChunk], max_chars: int = 4000) -> str:
    """
    Formate les chunks en un bloc de contexte injectable dans un prompt.

    Args:
        chunks:    Liste de chunks issus de retrieve().
        max_chars: Limite de caractères pour éviter de surcharger le prompt.

    Returns:
        Texte formaté prêt à être injecté dans un prompt.
    """
    parts = []
    total_chars = 0

    for i, chunk in enumerate(chunks, start=1):
        source = chunk["metadata"].get("source", "unknown")
        page   = chunk["metadata"].get("page", "?")
        header = f"[Source {i}: {source}, page {page}]"
        block  = f"{header}\n{chunk['text']}"

        if total_chars + len(block) > max_chars:
            break

        parts.append(block)
        total_chars += len(block)

    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Test rapide — python retrieval/retriever.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    print("=== Test Retriever ===\n")

    # Vérifier que ChromaDB existe
    if not Path(DEFAULT_CHROMA_PATH).exists():
        print("✗ ChromaDB introuvable.")
        print("  Lance d'abord : python ingestion/run_ingestion.py")
        sys.exit(1)

    # Test 1 : requête générale
    print("[Test 1] Requête générale sur la transformation digitale...")
    chunks = retrieve("Why should a company start a digital transformation?", n_results=3)
    print(f"  ✓ {len(chunks)} chunks retournés\n")
    for i, chunk in enumerate(chunks, 1):
        source = chunk["metadata"].get("source", "?")
        page   = chunk["metadata"].get("page", "?")
        dist   = chunk["distance"]
        print(f"  [{i}] {source} p.{page} | distance={dist}")
        print(f"       {chunk['text'][:120]}...")
    print()

    # Test 2 : requête sur un framework spécifique
    print("[Test 2] Requête sur le Digital Transformation Canvas...")
    chunks = retrieve("Digital Transformation Canvas 7 action fields customer centricity", n_results=3)
    print(f"  ✓ {len(chunks)} chunks retournés\n")
    for i, chunk in enumerate(chunks, 1):
        source = chunk["metadata"].get("source", "?")
        print(f"  [{i}] {source} | {chunk['text'][:120]}...")
    print()

    # Test 3 : format_chunks pour injection dans un prompt
    print("[Test 3] Formatage des chunks pour injection prompt...")
    chunks = retrieve("roadmap initiatives timeline KPIs", n_results=3)
    context = format_chunks(chunks, max_chars=2000)
    print(f"  ✓ Contexte généré ({len(context)} chars)")
    print(f"  Aperçu :\n{context[:400]}...\n")

    # Test 4 : filtre par source
    print("[Test 4] Filtre par source (wade_2015.pdf)...")
    try:
        chunks = retrieve(
            "digital business transformation framework",
            n_results=3,
            filter_source="wade_2015.pdf",
        )
        print(f"  ✓ {len(chunks)} chunks retournés depuis wade_2015.pdf")
        for chunk in chunks:
            print(f"    - {chunk['metadata'].get('source')} p.{chunk['metadata'].get('page')}")
    except Exception as e:
        print(f"  ⚠ Filtre non applicable : {e}")

    print("\n=== Tous les tests sont passés ✓ ===")