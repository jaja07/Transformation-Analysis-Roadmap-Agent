"""
ingestion/embedder.py
Génère les embeddings via NVIDIA NIM (baai/bge-m3) et les sauvegarde dans ChromaDB.
La DB est persistante : on ne recalcule les embeddings qu'une seule fois.
"""

import os
import uuid
from pathlib import Path
from typing import Optional
from openai import OpenAI
import chromadb


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_EMBED_MODEL = "nvidia/nv-embedqa-e5-v5"
DEFAULT_CHROMA_PATH = "vector_store/chroma_db"
DEFAULT_COLLECTION  = "digital_transformation_corpus"
BATCH_SIZE          = 32  # NIM accepte plusieurs textes par appel


# ---------------------------------------------------------------------------
# Client NIM embeddings
# ---------------------------------------------------------------------------

def _get_embed_client() -> OpenAI:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("La variable d'environnement NVIDIA_API_KEY n'est pas définie.")
    return OpenAI(
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1",
    )


def embed_texts(
    texts: list[str],
    model: str = DEFAULT_EMBED_MODEL,
) -> list[list[float]]:
    """
    Génère les embeddings pour une liste de textes via NIM.

    Args:
        texts: Liste de textes à embedder.
        model: Modèle d'embedding NIM.

    Returns:
        Liste de vecteurs (un par texte).
    """
    client = _get_embed_client()
    all_embeddings = []

    # Traitement par batch pour respecter les limites de l'API
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        response = client.embeddings.create(
            input=batch,
            model=model,
            encoding_format="float",
            extra_body={"input_type": "passage"},
        )
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
        print(f"[embedder] Batch {i // BATCH_SIZE + 1} — {len(batch)} textes embedidés")

    return all_embeddings


# ---------------------------------------------------------------------------
# Sauvegarde dans ChromaDB
# ---------------------------------------------------------------------------

def save_to_chroma(
    chunks: list[dict],
    chroma_path: str = DEFAULT_CHROMA_PATH,
    collection_name: str = DEFAULT_COLLECTION,
    embed_model: str = DEFAULT_EMBED_MODEL,
) -> chromadb.Collection:
    """
    Génère les embeddings des chunks et les sauvegarde dans ChromaDB.

    Args:
        chunks:          Liste de chunks issus du chunker.
        chroma_path:     Chemin de persistance de la DB.
        collection_name: Nom de la collection ChromaDB.
        embed_model:     Modèle d'embedding NIM.

    Returns:
        La collection ChromaDB créée/mise à jour.
    """
    Path(chroma_path).mkdir(parents=True, exist_ok=True)

    # Initialiser ChromaDB persistant
    chroma_client = chromadb.PersistentClient(path=chroma_path)

    # Supprimer la collection si elle existe déjà (re-ingestion propre)
    existing = [c.name for c in chroma_client.list_collections()]
    if collection_name in existing:
        chroma_client.delete_collection(collection_name)
        print(f"[embedder] Collection existante '{collection_name}' supprimée pour re-ingestion")

    collection = chroma_client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},  # similarité cosinus
    )

    # Préparer les données
    texts     = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    ids       = [str(uuid.uuid4()) for _ in chunks]

    print(f"\n[embedder] Génération des embeddings pour {len(texts)} chunks...")
    embeddings = embed_texts(texts, model=embed_model)

    # Insertion dans ChromaDB
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"\n[embedder] ✓ {len(chunks)} chunks sauvegardés dans ChromaDB")
    print(f"[embedder] Chemin : {Path(chroma_path).resolve()}")
    print(f"[embedder] Collection : '{collection_name}'\n")

    return collection


# ---------------------------------------------------------------------------
# Test rapide — python ingestion/embedder.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Test Embedder ===\n")

    # Test 1 : embedding d'un texte simple
    print("[Test 1] Embedding d'un texte simple...")
    vectors = embed_texts(["What is digital transformation?"])
    print(f"  ✓ Vecteur généré — dimension : {len(vectors[0])}\n")

    # Test 2 : embedding batch
    print("[Test 2] Embedding batch (3 textes)...")
    texts = [
        "Why transform? Customer expectations are evolving rapidly.",
        "What to transform? Processes, people, platforms and partners.",
        "How to transform? Through a structured roadmap and governance.",
    ]
    vectors = embed_texts(texts)
    print(f"  ✓ {len(vectors)} vecteurs générés — dimension : {len(vectors[0])}\n")

    # Test 3 : sauvegarde dans ChromaDB avec des chunks fictifs
    print("[Test 3] Sauvegarde dans ChromaDB...")
    fake_chunks = [
        {
            "text": "Digital transformation is a journey, not a destination.",
            "metadata": {"source": "wade_2015.pdf", "page": 1, "chunk_index": 0, "total_chunks": 2}
        },
        {
            "text": "The Digital Transformation Canvas has 7 action fields.",
            "metadata": {"source": "peter_2018.pdf", "page": 3, "chunk_index": 0, "total_chunks": 1}
        },
    ]
    collection = save_to_chroma(
        chunks=fake_chunks,
        chroma_path="vector_store/chroma_db_test",
        collection_name="test_collection",
    )
    print(f"  ✓ Collection créée — {collection.count()} documents\n")

    # Test 4 : vérifier qu'on peut requêter la collection
    print("[Test 4] Requête de test sur la collection...")
    query_vector = embed_texts(["transformation frameworks"])[0]
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=2,
    )
    print(f"  ✓ {len(results['documents'][0])} résultats retournés")
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"    - [{meta['source']}] {doc[:80]}...")

    print("\n=== Tous les tests sont passés ✓ ===")