"""
ingestion/loader.py
Charge les PDFs du corpus et retourne une liste de documents bruts.
Chaque document est un dict avec le texte et les métadonnées.
"""

import os
from pathlib import Path
from typing import Optional
import pdfplumber


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

Document = dict  # {"text": str, "metadata": {"source": str, "page": int}}


# ---------------------------------------------------------------------------
# Fonctions
# ---------------------------------------------------------------------------

def load_pdf(pdf_path: str | Path) -> list[Document]:
    """
    Charge un PDF et retourne une liste de documents (un par page).

    Args:
        pdf_path: Chemin vers le fichier PDF.

    Returns:
        Liste de documents avec texte et métadonnées.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF introuvable : {pdf_path}")

    documents = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():  # ignorer les pages vides
                documents.append({
                    "text": text.strip(),
                    "metadata": {
                        "source": pdf_path.name,
                        "source_path": str(pdf_path),
                        "page": page_num,
                    }
                })

    print(f"[loader] '{pdf_path.name}' — {len(documents)} pages chargées")
    return documents


def load_corpus(corpus_dir: str | Path) -> list[Document]:
    """
    Charge tous les PDFs d'un dossier et retourne tous les documents.

    Args:
        corpus_dir: Dossier contenant les PDFs du corpus.

    Returns:
        Liste complète de documents issus de tous les PDFs.
    """
    corpus_dir = Path(corpus_dir)
    if not corpus_dir.exists():
        raise FileNotFoundError(f"Dossier corpus introuvable : {corpus_dir}")

    pdf_files = sorted(corpus_dir.glob("*.pdf"))
    if not pdf_files:
        raise ValueError(f"Aucun PDF trouvé dans : {corpus_dir}")

    print(f"[loader] {len(pdf_files)} PDF(s) trouvé(s) dans '{corpus_dir}'")

    all_documents = []
    for pdf_file in pdf_files:
        docs = load_pdf(pdf_file)
        all_documents.extend(docs)

    print(f"[loader] Total : {len(all_documents)} pages chargées\n")
    return all_documents


# ---------------------------------------------------------------------------
# Test rapide — python ingestion/loader.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    print("=== Test Loader ===\n")

    # Chemin vers le corpus (relatif à la racine du projet)
    corpus_path = Path("data/corpus")

    # Test 1 : vérifier que le dossier existe
    print(f"[Test 1] Vérification du dossier corpus : {corpus_path.resolve()}")
    if not corpus_path.exists():
        print(f"  ✗ Dossier introuvable — crée 'data/corpus/' et place tes PDFs dedans.")
        sys.exit(1)
    print("  ✓ Dossier trouvé\n")

    # Test 2 : charger tous les PDFs
    print("[Test 2] Chargement du corpus complet...")
    documents = load_corpus(corpus_path)
    print(f"  ✓ {len(documents)} documents chargés\n")

    # Test 3 : inspecter le premier document
    print("[Test 3] Aperçu du premier document :")
    first = documents[0]
    print(f"  Source  : {first['metadata']['source']}")
    print(f"  Page    : {first['metadata']['page']}")
    print(f"  Texte   : {first['text'][:200]}...")

    print("\n=== Tous les tests sont passés ✓ ===")