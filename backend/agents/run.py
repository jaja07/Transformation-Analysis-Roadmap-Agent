"""
run.py — Point d'entrée unique du pipeline Multi-Agent RAG
À placer et lancer depuis la racine du dossier `agents/`

Usage :
    cd agents/
    python run.py

Ce script :
    1. Vérifie les prérequis (clé API, dossier corpus)
    2. Lance l'ingestion si ChromaDB n'existe pas encore
    3. Lance le pipeline multi-agent complet
    4. Affiche une trace détaillée de chaque étape
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Chemins — tous relatifs au dossier où se trouve ce fichier (agents/)
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent          # agents/
CORPUS_DIR   = ROOT / "data" / "corpus"
CHROMA_PATH  = ROOT / "vector_store" / "chroma_db"
COLLECTION   = "digital_transformation_corpus"

# Ajouter ROOT au path Python pour que les imports fonctionnent
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# Helpers de trace
# ---------------------------------------------------------------------------

SEP  = "═" * 65
SEP2 = "─" * 65

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def section(title: str, content: str = ""):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)
    if content:
        print(content)

def step(n: int, total: int, label: str):
    print(f"\n{SEP2}")
    log(f"ÉTAPE {n}/{total} — {label}")
    print(SEP2)


# ---------------------------------------------------------------------------
# Étape 0 : Vérification des prérequis
# ---------------------------------------------------------------------------

def check_prerequisites():
    section("VÉRIFICATION DES PRÉREQUIS")
    ok = True

    # Clé API NVIDIA
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        log("✗ NVIDIA_API_KEY non définie")
        log("  → export NVIDIA_API_KEY='ta_clé_ici'")
        ok = False
    else:
        log(f"✓ NVIDIA_API_KEY détectée ({api_key[:8]}...)")

    # Dossier corpus
    if not CORPUS_DIR.exists():
        log(f"✗ Dossier corpus introuvable : {CORPUS_DIR}")
        log("  → Crée le dossier et place tes 4 PDFs dedans :")
        log("    agents/data/corpus/wade_2015.pdf")
        log("    agents/data/corpus/peter_2018.pdf")
        log("    agents/data/corpus/elia_2024.pdf")
        log("    agents/data/corpus/peter_2024.pdf")
        ok = False
    else:
        pdfs = list(CORPUS_DIR.glob("*.pdf"))
        if not pdfs:
            log(f"✗ Aucun PDF dans {CORPUS_DIR}")
            ok = False
        else:
            log(f"✓ Corpus trouvé — {len(pdfs)} PDF(s) :")
            for p in pdfs:
                log(f"    - {p.name}")

    if not ok:
        print(f"\n{SEP}")
        print("  ✗ Prérequis manquants — corrige les erreurs ci-dessus et relance.")
        print(SEP)
        sys.exit(1)

    log("✓ Tous les prérequis sont satisfaits")


# ---------------------------------------------------------------------------
# Étape 1 : Ingestion (si ChromaDB absent)
# ---------------------------------------------------------------------------

def run_ingestion_if_needed():
    section("INGESTION DU CORPUS")

    if CHROMA_PATH.exists():
        log(f"✓ ChromaDB déjà présente — ingestion ignorée")
        log(f"  Chemin : {CHROMA_PATH}")
        log("  (Supprime le dossier vector_store/chroma_db/ pour forcer la ré-ingestion)")
        return

    log("ChromaDB absente — lancement de l'ingestion...")
    t0 = time.time()

    from ingestion.loader import load_corpus
    from ingestion.chunker import chunk_documents
    from ingestion.embedder import save_to_chroma

    log("  Chargement des PDFs...")
    documents = load_corpus(str(CORPUS_DIR))
    log(f"  ✓ {len(documents)} pages chargées")

    log("  Chunking...")
    chunks = chunk_documents(documents, chunk_size=800, chunk_overlap=150)
    log(f"  ✓ {len(chunks)} chunks créés")

    log("  Génération des embeddings + sauvegarde ChromaDB...")
    collection = save_to_chroma(
        chunks=chunks,
        chroma_path=str(CHROMA_PATH),
        collection_name=COLLECTION,
    )

    elapsed = round(time.time() - t0, 1)
    log(f"  ✓ {collection.count()} vecteurs indexés en {elapsed}s")
    log(f"  ✓ ChromaDB sauvegardée : {CHROMA_PATH}")


# ---------------------------------------------------------------------------
# Étape 2 : Pipeline multi-agent
# ---------------------------------------------------------------------------

def run_pipeline(business_case: str):
    section("PIPELINE MULTI-AGENT")
    log(f"Business case : {len(business_case)} caractères\n")

    # Import ici (après que sys.path est configuré)
    from orchestrator.state import GlobalState

    initial_state: GlobalState = {
        "business_case": business_case,
        "why": "",
        "what": "",
        "how": "",
        "structured_problem": "",
        "why_context": "",
        "what_context": "",
        "how_context": "",
        "global_context": "",
        "canvas_analysis": "",
        "strategic_analysis": "",
        "roadmap": "",
        "evaluation": "",
        "is_valid": False,
    }

    # Import et exécution agent par agent avec trace
    results = dict(initial_state)

    # ── Agent 1 : Planner ──────────────────────────────────────────────────
    step(1, 6, "Planner Agent")
    t0 = time.time()
    from planner.graph import planner_graph
    r = planner_graph.invoke({
        "business_case": results["business_case"],
        "why": "", "what": "", "how": "", "structured_problem": "",
    })
    results.update({"why": r["why"], "what": r["what"],
                    "how": r["how"], "structured_problem": r["structured_problem"]})
    log(f"✓ Terminé en {round(time.time()-t0, 1)}s")
    log(f"  WHY   : {r['why'][:100]}...")
    log(f"  WHAT  : {r['what'][:100]}...")
    log(f"  HOW   : {r['how'][:100]}...")

    # ── Agent 2 : Retrieval ────────────────────────────────────────────────
    step(2, 6, "Retrieval Agent")
    t0 = time.time()
    from retriever.graph import retrieval_graph
    r = retrieval_graph.invoke({
        "structured_problem": results["structured_problem"],
        "why": results["why"], "what": results["what"], "how": results["how"],
        "why_context": "", "what_context": "", "how_context": "", "global_context": "",
    })
    results.update({
        "why_context": r["why_context"], "what_context": r["what_context"],
        "how_context": r["how_context"], "global_context": r["global_context"],
    })
    log(f"✓ Terminé en {round(time.time()-t0, 1)}s")
    log(f"  why_context    : {len(r['why_context'])} chars")
    log(f"  what_context   : {len(r['what_context'])} chars")
    log(f"  how_context    : {len(r['how_context'])} chars")
    log(f"  global_context : {len(r['global_context'])} chars")

    # ── Agent 3 : Canvas Analyst ───────────────────────────────────────────
    step(3, 6, "Canvas Analyst Agent")
    t0 = time.time()
    from canvas_analyst.graph import canvas_graph
    r = canvas_graph.invoke({
        "business_case": results["business_case"],
        "structured_problem": results["structured_problem"],
        "what_context": results["what_context"],
        "global_context": results["global_context"],
        "canvas_analysis": "",
    })
    results["canvas_analysis"] = r["canvas_analysis"]
    log(f"✓ Terminé en {round(time.time()-t0, 1)}s")
    log(f"  canvas_analysis : {len(r['canvas_analysis'])} chars")

    # ── Agent 4 : Strategist ───────────────────────────────────────────────
    step(4, 6, "Strategist Agent")
    t0 = time.time()
    from strategist.graph import strategist_graph
    r = strategist_graph.invoke({
        "business_case": results["business_case"],
        "structured_problem": results["structured_problem"],
        "why": results["why"],
        "canvas_analysis": results["canvas_analysis"],
        "how_context": results["how_context"],
        "global_context": results["global_context"],
        "strategic_analysis": "",
    })
    results["strategic_analysis"] = r["strategic_analysis"]
    log(f"✓ Terminé en {round(time.time()-t0, 1)}s")
    log(f"  strategic_analysis : {len(r['strategic_analysis'])} chars")

    # ── Agent 5 : Roadmap Generator ────────────────────────────────────────
    step(5, 6, "Roadmap Generator Agent")
    t0 = time.time()
    from roadmap_generator.graph import roadmap_graph
    r = roadmap_graph.invoke({
        "business_case": results["business_case"],
        "structured_problem": results["structured_problem"],
        "canvas_analysis": results["canvas_analysis"],
        "strategic_analysis": results["strategic_analysis"],
        "global_context": results["global_context"],
        "roadmap": "",
    })
    results["roadmap"] = r["roadmap"]
    log(f"✓ Terminé en {round(time.time()-t0, 1)}s")
    log(f"  roadmap : {len(r['roadmap'])} chars")

    # ── Agent 6 : Evaluator ────────────────────────────────────────────────
    step(6, 6, "Evaluator Agent")
    t0 = time.time()
    from evaluator.graph import evaluator_graph
    r = evaluator_graph.invoke({
        "business_case": results["business_case"],
        "structured_problem": results["structured_problem"],
        "canvas_analysis": results["canvas_analysis"],
        "strategic_analysis": results["strategic_analysis"],
        "roadmap": results["roadmap"],
        "evaluation": "", "is_valid": False,
    })
    results["evaluation"] = r["evaluation"]
    results["is_valid"]   = r["is_valid"]
    log(f"✓ Terminé en {round(time.time()-t0, 1)}s")
    log(f"  is_valid : {r['is_valid']}")

    return results


# ---------------------------------------------------------------------------
# Affichage final
# ---------------------------------------------------------------------------

def print_results(results: dict):
    section("RÉSULTATS COMPLETS")

    print(f"\n{SEP2}\n  PLANNER — Problème structuré\n{SEP2}")
    print(f"WHY  : {results['why']}")
    print(f"WHAT : {results['what']}")
    print(f"HOW  : {results['how']}")
    print(f"\nSUMMARY : {results['structured_problem']}")

    print(f"\n{SEP2}\n  CANVAS ANALYSIS\n{SEP2}")
    print(results["canvas_analysis"])

    print(f"\n{SEP2}\n  STRATEGIC ANALYSIS\n{SEP2}")
    print(results["strategic_analysis"])

    print(f"\n{SEP2}\n  ROADMAP\n{SEP2}")
    print(results["roadmap"])

    print(f"\n{SEP2}\n  EVALUATION\n{SEP2}")
    print(results["evaluation"])

    print(f"\n{SEP}")
    status = "✓ VALID" if results["is_valid"] else "⚠ NEEDS IMPROVEMENT"
    print(f"  PIPELINE TERMINÉ — Verdict : {status}")
    print(SEP)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    t_total = time.time()

    BUSINESS_CASE = """
    Our company is a mid-sized retail bank with 500 employees operating in France.
    We are losing customers to neobanks because our mobile app is outdated and poorly rated (2.1/5).
    Our loan approval process is entirely manual and takes 5 business days,
    while our competitors approve loans in under 1 hour using AI.
    We want to:
    - Improve customer experience and NPS by 20 points
    - Reduce operational costs by 20% within 18 months
    - Launch a fully digital loan product within 12 months
    - Build internal digital capabilities for the long term
    """.strip()

    check_prerequisites()
    run_ingestion_if_needed()
    results = run_pipeline(BUSINESS_CASE)
    print_results(results)

    elapsed = round(time.time() - t_total, 1)
    log(f"Durée totale : {elapsed}s")