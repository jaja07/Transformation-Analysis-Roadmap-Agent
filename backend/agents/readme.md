# Multi-Agent RAG System — Digital Transformation Roadmap Generator

> **Dossier** : `backend/agents/`  
> **Projet** : ECE MSC AI (M2) — Multi-LLM Architectures & Eco-Responsible AI  
> **Stack** : LangGraph · NVIDIA NIM · ChromaDB · pdfplumber

---

## Table des matières

1. [Vue d'ensemble](#1-vue-densemble)
2. [Architecture](#2-architecture)
3. [Structure du dossier](#3-structure-du-dossier)
4. [Prérequis & Installation](#4-prérequis--installation)
5. [Lancement](#5-lancement)
6. [Pipeline détaillé — les 6 agents](#6-pipeline-détaillé--les-6-agents)
7. [Le RAG local](#7-le-rag-local)
8. [Choix architecturaux](#8-choix-architecturaux)
9. [Limites connues & améliorations prévues](#9-limites-connues--améliorations-prévues)

---

## 1. Vue d'ensemble

Ce système transforme un **business case** (description textuelle d'une entreprise) en une **roadmap de transformation digitale structurée et actionnable**, en s'appuyant sur :

- un **corpus documentaire de référence** (4 frameworks académiques et professionnels),
- un pipeline **RAG local** (Retrieval-Augmented Generation),
- une architecture **multi-agent** avec LangGraph,
- des appels LLM via **NVIDIA NIM**.

Le système ne génère pas de texte libre — il raisonne à partir de documents, structure l'analyse selon des frameworks reconnus, et produit un livrable exploitable.

---

## 2. Architecture

```
Business Case (texte libre)
        │
        ▼
┌─────────────────┐
│  Planner Agent  │  ── Analyse le business case
│                 │      Extrait WHY / WHAT / HOW
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Retrieval Agent │  ── Génère 3 requêtes ciblées
│     (RAG)       │      Interroge ChromaDB
│                 │      Retourne contexte WHY / WHAT / HOW / GLOBAL
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Canvas Analyst │  ── Analyse selon les 7 champs
│     Agent       │      du Digital Transformation Canvas
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Strategist    │  ── Propose initiatives stratégiques
│     Agent       │      (Purpose / Pillars / Value / Pitfalls)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Roadmap      │  ── Génère la roadmap en 3 phases
│  Generator      │      avec KPIs, budgets, owners, timelines
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Evaluator     │  ── Évalue la qualité (score /5)
│     Agent       │      Vérifie cohérence et complétude
└────────┬────────┘
         │
         ▼
  Roadmap finale + Évaluation
```

---

## 3. Structure du dossier

```
agents/
├── run.py                        # Point d'entrée unique
│
├── data/
│   └── corpus/                   # Les 4 PDFs du corpus (à fournir)
│       ├── wade_2015.pdf
│       ├── peter_2018.pdf
│       ├── elia_2024.pdf
│       └── peter_2024.pdf
│
├── vector_store/
│   └── chroma_db/                # Généré automatiquement à la première exécution
│
├── ingestion/                    # Pipeline d'ingestion du corpus
│   ├── loader.py                 # Chargement des PDFs
│   ├── chunker.py                # Découpage en chunks
│   ├── embedder.py               # Génération embeddings + sauvegarde ChromaDB
│   └── run_ingestion.py          # Script d'ingestion standalone
│
├── retrieval/
│   └── retriever.py              # Interrogation ChromaDB (utilisé par tous les agents)
│
├── llm_clients/
│   ├── nim_client.py             # Client NVIDIA NIM (LLaMA)
│   ├── gemini_client.py          # Client Gemini (routing futur)
│   └── llama_client.py           # Client LLaMA local (routing futur)
│
├── orchestrator/
│   ├── state.py                  # GlobalState partagé entre tous les agents
│   ├── graph.py                  # Orchestration LangGraph globale
│   └── runner.py                 # Runner de l'orchestrateur
│
├── planner/                      # Agent 1
├── retriever/                    # Agent 2
├── canvas_analyst/               # Agent 3
├── strategist/                   # Agent 4
├── roadmap_generator/            # Agent 5
└── evaluator/                    # Agent 6
    # Chaque agent contient :
    #   graph.py    — sous-graph LangGraph
    #   nodes.py    — logique métier
    #   state.py    — TypedDict du state
    #   prompts.py  — templates de prompts
    #   edge.py     — logique de routage conditionnel
```

---

## 4. Prérequis & Installation

### Dépendances système

- Python 3.10+
- Une clé API NVIDIA NIM : [build.nvidia.com](https://build.nvidia.com)

### Installation

```bash
# 1. Se placer dans le dossier agents
cd backend/agents

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

### Corpus documentaire

Placer les 4 PDFs dans `data/corpus/` :

| Fichier | Source |
|---|---|
| `wade_2015.pdf` | [IMD/Cisco Framework](https://www.s-ge.com/sites/default/files/static/downloads/digital_business_transformation_framework_imd_0.pdf) |
| `peter_2018.pdf` | [Digital Transformation Canvas](https://marcpeter.com/wp-content/uploads/2023/01/Digital-Transformation-Canvas-Marc-K-Peter-English.pdf) |
| `elia_2024.pdf` | [Academic Canvas Framework](https://iris.unisalento.it/retrieve/64561b64-fd0f-48d8-8857-25b0b82fc83b/1-s2.0-S0007681324000454-main.pdf) |
| `peter_2024.pdf` | [Digital Roadmap Template](https://the-digital-transformation-canvas.com/wp-content/uploads/2024/02/DigitalProf-MKPeter-Digital-Roadmap-Template-Example-2024.pdf) |

### Variable d'environnement

```bash
export NVIDIA_API_KEY="nvapi-xxxxxxxxxxxx"
```

---

## 5. Lancement

```bash
# Depuis backend/agents/, avec le venv activé
source venv/bin/activate
python run.py
```

`run.py` gère automatiquement :
1. La vérification des prérequis (clé API, PDFs présents)
2. L'ingestion du corpus si ChromaDB n'existe pas encore
3. L'exécution séquentielle des 6 agents
4. L'affichage structuré des résultats

> **Note :** L'ingestion ne se relance pas si `vector_store/chroma_db/` existe déjà.  
> Pour forcer une ré-ingestion (ex: après changement de modèle d'embedding) :
> ```bash
> rm -rf vector_store/chroma_db
> python run.py
> ```

### Modifier le business case

Dans `run.py`, modifier la variable `BUSINESS_CASE` :

```python
BUSINESS_CASE = """
Votre description d'entreprise ici...
""".strip()
```

---

## 6. Pipeline détaillé — les 6 agents

### Agent 1 — Planner
**Rôle :** Comprendre le business case et structurer le problème.  
**Input :** Business case brut (texte libre)  
**Output :** WHY (drivers), WHAT (dimensions à transformer), HOW (approche), STRUCTURED SUMMARY  
**Modèle :** NIM / LLaMA (température 0.2 pour des réponses déterministes)

### Agent 2 — Retrieval
**Rôle :** Ancrer le raisonnement dans les documents de référence.  
**Input :** Structured problem du Planner  
**Output :** Contextes WHY / WHAT / HOW / GLOBAL (passages extraits du corpus)  
**Fonctionnement :**
1. Génère 3 requêtes ciblées (une par dimension WHY/WHAT/HOW)
2. Interroge ChromaDB avec chaque requête
3. Retourne les chunks les plus pertinents formatés pour injection

### Agent 3 — Canvas Analyst
**Rôle :** Analyser l'entreprise selon les 7 champs du Digital Transformation Canvas (Peter, 2018).  
**Input :** Business case + structured problem + what_context + global_context  
**Output :** Analyse structurée par champ (situation, gap, priorité)  
**Frameworks mobilisés :** Digital Transformation Canvas — Customer Centricity, New Technologies, Cloud & Data, Digital Business Development, Process Engineering, Digital Leadership & Culture, Digital Marketing

### Agent 4 — Strategist
**Rôle :** Proposer une trajectoire stratégique et des initiatives.  
**Input :** Canvas analysis + why + strategic context  
**Output :** Purpose, Operational Pillars (Process/People/Platform/Partners), Value créée, Pitfalls, liste d'initiatives priorisées  
**Frameworks mobilisés :** Elia et al. (2024) — 11P framework

### Agent 5 — Roadmap Generator
**Rôle :** Transformer l'analyse en roadmap opérationnelle.  
**Input :** Canvas analysis + strategic analysis + global context  
**Output :** Roadmap en 3 phases avec initiatives, owners, budgets, KPIs, timelines  
**Structure de sortie :**
- Phase 1 (0–3 mois) : Quick Wins
- Phase 2 (4–9 mois) : Transformation structurelle
- Phase 3 (10–18 mois) : Optimisation & Scale

### Agent 6 — Evaluator
**Rôle :** Évaluer la qualité et la cohérence du livrable final.  
**Input :** Business case + toutes les analyses + roadmap  
**Output :** Score /5 sur 5 dimensions, forces, faiblesses, recommandations, verdict VALID/NEEDS IMPROVEMENT  
**Dimensions évaluées :** Alignement business, couverture frameworks, pertinence initiatives, complétude roadmap, conscience des risques

---

## 7. Le RAG local

### Ingestion (une seule fois)

```
4 PDFs → pdfplumber → 46 pages → chunker (800 chars, overlap 150) → 227 chunks
→ nvidia/nv-embedqa-e5-v5 (embeddings) → ChromaDB (persistant)
```

### Retrieval (à chaque exécution)

```
query (texte) → embedding "query" mode → similarité cosinus → top-k chunks
```

### Pourquoi `nvidia/nv-embedqa-e5-v5` ?

Le modèle `baai/bge-m3` initialement prévu retournait une erreur 500 sur l'API NIM. `nv-embedqa-e5-v5` est un modèle **asymétrique** stable sur NIM, ce qui implique de distinguer :
- `input_type: "passage"` lors de l'indexation
- `input_type: "query"` lors de la recherche

Cette distinction améliore la pertinence des résultats en optimisant la représentation vectorielle selon le rôle du texte.

---

## 8. Choix architecturaux

### Pourquoi LangGraph plutôt que LangChain LCEL ?

LangGraph permet de modéliser le pipeline comme un **graphe d'états** avec des transitions explicites. Chaque agent est un sous-graph compilé indépendamment, ce qui offre :
- une meilleure **modularité** (chaque agent est testable seul)
- une **traçabilité** claire des états intermédiaires
- la possibilité d'ajouter des **edges conditionnels** (ex: re-boucle si évaluation insuffisante) sans refactoring majeur

### Pourquoi un TypedDict par agent ?

Chaque agent définit son propre `State` (TypedDict) plutôt qu'un état global monolithique. Cela :
- documente explicitement les **inputs/outputs** de chaque agent
- évite les **effets de bord** entre agents
- facilite les **tests unitaires** par agent

Le `GlobalState` de l'orchestrateur est l'union de tous ces états.

### Pourquoi ChromaDB plutôt que FAISS ?

ChromaDB offre une **persistance native** sans sérialisation manuelle. Une fois la base créée, elle est rechargée en une ligne sans recalculer les embeddings — essentiel pour éviter de consommer des crédits API à chaque lancement.

### Pourquoi chunker à 800 caractères avec overlap 150 ?

Les 4 documents sont des frameworks conceptuels avec des sections bien délimitées. Un chunk de 800 caractères correspond environ à 1–2 paragraphes, ce qui :
- préserve le **contexte local** d'un passage
- reste sous la limite de tokens des modèles d'embedding
- l'overlap de 150 caractères évite de couper un concept en deux chunks distincts

### Pourquoi séparer `retrieval/retriever.py` des agents ?

Le retriever est une **fonction utilitaire partagée** appelée par plusieurs agents (Retrieval Agent, potentiellement Canvas Analyst ou Strategist). Le centraliser dans `retrieval/` évite la duplication et garantit une configuration d'embedding cohérente dans tout le pipeline.

---

## 9. Limites connues & améliorations prévues

| Limite | Amélioration prévue |
|---|---|
| Un seul modèle LLM (NIM/LLaMA) | Routing multi-LLM : Gemini Flash pour tâches simples, Gemini Pro pour tâches complexes |
| Pas de cache des résultats intermédiaires | Mise en cache des contextes RAG et analyses partielles |
| Interface en ligne de commande uniquement | Dashboard Streamlit |
| Pas d'API exposée | FastAPI avec endpoints `/analyze` et `/generate-roadmap` |
| RAG non pondéré par framework | Retrieval filtré par source (ex: forcer peter_2018.pdf pour la canvas analysis) |