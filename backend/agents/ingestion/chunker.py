"""
ingestion/chunker.py
Découpe les documents chargés en chunks pour l'indexation dans ChromaDB.
Stratégie : RecursiveCharacterTextSplitter avec overlap pour préserver le contexte.
"""

from typing import Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

Document = dict  # {"text": str, "metadata": {...}}
Chunk = dict     # {"text": str, "metadata": {..., "chunk_index": int}}


# ---------------------------------------------------------------------------
# Fonctions
# ---------------------------------------------------------------------------

def chunk_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[Chunk]:
    """
    Découpe une liste de documents en chunks.

    Args:
        documents:     Liste de documents issus du loader.
        chunk_size:    Taille maximale d'un chunk en caractères.
        chunk_overlap: Chevauchement entre chunks consécutifs (pour préserver le contexte).

    Returns:
        Liste de chunks avec texte et métadonnées enrichies.

    Choix techniques :
        - chunk_size=800  : assez grand pour avoir du contexte, assez petit pour la précision
        - chunk_overlap=150 : ~20% d'overlap pour ne pas couper les idées entre deux chunks
        - RecursiveCharacterTextSplitter : respecte les séparateurs naturels (paragraphes, phrases)
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    all_chunks = []
    for doc in documents:
        raw_chunks = splitter.split_text(doc["text"])
        for i, chunk_text in enumerate(raw_chunks):
            all_chunks.append({
                "text": chunk_text.strip(),
                "metadata": {
                    **doc["metadata"],
                    "chunk_index": i,
                    "total_chunks": len(raw_chunks),
                }
            })

    print(f"[chunker] {len(documents)} documents → {len(all_chunks)} chunks")
    print(f"[chunker] Paramètres : chunk_size={chunk_size}, overlap={chunk_overlap}\n")
    return all_chunks


# ---------------------------------------------------------------------------
# Test rapide — python ingestion/chunker.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Test Chunker ===\n")

    # Données fictives simulant la sortie du loader
    fake_documents = [
        {
            "text": (
                "Digital transformation is a process of organizational change. "
                "It is based on the use of digital technologies and digital business models. "
                "The goal is to improve performance and create value.\n\n"
                "The IMD/Cisco framework structures the transformation journey around three questions: "
                "Why transform? What to transform? How to transform?\n\n"
                "Customer centricity is the first action field of the Digital Transformation Canvas. "
                "It focuses on understanding customer needs and expectations in the digital age."
            ),
            "metadata": {"source": "wade_2015.pdf", "page": 1}
        },
        {
            "text": (
                "The Digital Transformation Canvas has 7 action fields: "
                "Customer Centricity, New Technologies, Cloud and Data, "
                "Digital Business Development, Process Engineering, "
                "Digital Leadership and Culture, Digital Marketing.\n\n"
                "Each field provides guiding questions for a workshop-type reflection. "
                "The canvas helps structure the analysis of a company's transformation needs."
            ),
            "metadata": {"source": "peter_2018.pdf", "page": 3}
        },
    ]

    # Test 1 : chunking avec paramètres par défaut
    print("[Test 1] Chunking avec paramètres par défaut...")
    chunks = chunk_documents(fake_documents)
    print(f"  ✓ {len(chunks)} chunks générés\n")

    # Test 2 : inspecter le premier chunk
    print("[Test 2] Aperçu du premier chunk :")
    first = chunks[0]
    print(f"  Source      : {first['metadata']['source']}")
    print(f"  Page        : {first['metadata']['page']}")
    print(f"  Chunk index : {first['metadata']['chunk_index']}")
    print(f"  Texte       : {first['text'][:200]}\n")

    # Test 3 : vérifier l'overlap (le début du chunk 2 doit recouper la fin du chunk 1)
    print("[Test 3] Vérification de l'overlap...")
    if len(chunks) > 1:
        end_chunk_0 = chunks[0]["text"][-50:]
        start_chunk_1 = chunks[1]["text"][:50]
        print(f"  Fin chunk 0   : ...{end_chunk_0}")
        print(f"  Début chunk 1 : {start_chunk_1}...")
    print()

    # Test 4 : chunking avec paramètres personnalisés
    print("[Test 4] Chunking avec chunk_size=300, overlap=50...")
    small_chunks = chunk_documents(fake_documents, chunk_size=300, chunk_overlap=50)
    print(f"  ✓ {len(small_chunks)} chunks générés (plus nombreux, plus petits)\n")

    print("=== Tous les tests sont passés ✓ ===")