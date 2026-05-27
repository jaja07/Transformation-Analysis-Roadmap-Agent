# TARA : Transformation Analysis & Roadmap Agent

**TARA** est un système d'intelligence artificielle conçu pour transformer une description d'entreprise en une **roadmap de transformation digitale structurée, cohérente et actionnable**. Le projet est développé dans le cadre du **Master of Science in AI (M2) à l'ECE Paris**.

Le dépôt contient une application complète avec un backend orienté IA, un frontend séparé, et un pipeline multi-agent fondé sur un RAG local.

## Vue d'ensemble

Le système prend un **business case** en entrée et produit une feuille de route de transformation digitale basée sur des frameworks de référence. Il combine :

- une architecture **multi-agents** orchestrée avec **LangGraph**,
- un **RAG local** reposant sur **ChromaDB**,
- des appels LLM via **NVIDIA NIM**,
- un corpus documentaire académique et professionnel servant d'ancrage au raisonnement.

Le projet ne repose pas sur de la génération libre non contrainte. Chaque agent structure l'analyse à partir de documents et d'un état partagé, afin de produire un livrable exploitable.

## Architecture

### Pipeline cognitif

```text
Business Case (texte libre)
        │
        ▼
┌─────────────────┐
│  Planner Agent  │  -> Analyse le business case
│                 │     Extrait WHY / WHAT / HOW
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Retrieval Agent │  -> Génère 3 requêtes ciblées
│     (RAG)       │     Interroge ChromaDB
│                 │     Retourne WHY / WHAT / HOW / GLOBAL
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Canvas Analyst  │  -> Analyse selon les 7 champs
│     Agent       │     du Digital Transformation Canvas
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Strategist    │  -> Propose initiatives stratégiques
│     Agent       │     (Purpose / Pillars / Value / Pitfalls)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Roadmap         │  -> Génère la roadmap en 3 phases
│ Generator       │     avec KPIs, budgets, owners, timelines
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Evaluator     │  -> Évalue la qualité globale
│     Agent       │     Vérifie cohérence et complétude
└────────┬────────┘
         │
         ▼
  Roadmap finale + évaluation
```

### Logique applicative

- Le dossier [backend/agents/](backend/agents/) contient le pipeline agentique détaillé.
- Le backend global regroupe l'API, l'orchestration, la persistance et le stockage vectoriel.
- Le frontend est séparé du moteur IA pour garder une architecture claire et modulaire.

## Structure du projet

```text
├── backend/
│   ├── api/                  # Routes FastAPI
│   ├── agents/               # Pipeline multi-agent LangGraph
│   │   ├── ingestion/        # Chargement, chunking, embeddings
│   │   ├── retrieval/        # Interrogation de la base ChromaDB
│   │   ├── orchestrator/     # État global et runner
│   │   └── ...               # Planner, Canvas Analyst, Strategist, Roadmap, Evaluator
│   ├── core/                 # Configuration et graphe global
│   ├── database/             # Modèles et session DB
│   ├── vector_store/         # Persistance ChromaDB
│   └── main.py               # Point d'entrée backend
├── frontend/                 # Interface utilisateur
├── pdfs/                     # Documents sources additionnels
└── README.md                 # Ce document
```

## Pipeline détaillé des 6 agents

### 1. Planner

Rôle : comprendre le business case et structurer le problème.

Entrée : texte libre.

Sortie : WHY, WHAT, HOW, et synthèse structurée.

### 2. Retrieval

Rôle : ancrer le raisonnement dans les documents de référence.

Fonctionnement :

1. génération de 3 requêtes ciblées,
2. interrogation de ChromaDB,
3. retour de contextes formatés pour WHY, WHAT, HOW et GLOBAL.

### 3. Canvas Analyst

Rôle : analyser l'entreprise selon les 7 champs du Digital Transformation Canvas.

Sortie : analyse structurée par champ avec situation, gap et priorité.

### 4. Strategist

Rôle : proposer une trajectoire stratégique et des initiatives concrètes.

Sortie : Purpose, piliers opérationnels, valeur créée, pièges à éviter, initiatives priorisées.

### 5. Roadmap Generator

Rôle : transformer l'analyse en roadmap opérationnelle.

Sortie : roadmap en 3 phases avec initiatives, owners, budgets, KPI et timelines.

### 6. Evaluator

Rôle : évaluer la qualité et la cohérence du livrable final.

Sortie : score, forces, faiblesses, recommandations et verdict final.

## Le RAG local

### Ingestion

Le corpus est ingéré une seule fois avant utilisation :

```text
PDFs -> pdfplumber -> extraction du texte -> chunking -> embeddings -> ChromaDB
```

Le dossier [backend/agents/data/corpus/](backend/agents/data/corpus/) contient les documents de référence à fournir au système.

### Retrieval

À l'exécution, le système :

1. transforme la requête en embedding,
2. compare ce vecteur aux chunks indexés,
3. retourne les passages les plus pertinents.

### Choix du modèle d'embedding

Le projet utilise `nv-embedqa-e5-v5`, car il s'agit d'un modèle asymétrique stable sur NIM. Cela impose de distinguer :

- `input_type: "passage"` lors de l'indexation,
- `input_type: "query"` lors de la recherche.

Cette distinction améliore la qualité des correspondances entre la requête et les documents.

## Frameworks de référence

Le raisonnement du système s'appuie sur plusieurs cadres présents dans le corpus :

- Wade (2015) : cadre Why / What / How,
- Peter (2018) : Digital Transformation Canvas,
- Elia et al. (2024) : canevas stratégique et opérationnel.

## Installation et lancement

### Prérequis

- Python 3.13+,
- `uv` installé,
- Docker et Docker Compose,
- une clé API NVIDIA NIM,
- les documents du corpus placés dans [backend/agents/data/corpus/](backend/agents/data/corpus/).

### Installation du backend

```bash
cd backend
uv sync
```

### Lancer la base de données

Avant d'appliquer les migrations Alembic, s'assurer que PostgreSQL est démarré.

```bash
cd backend
docker compose up -d db
```

### Appliquer les migrations Alembic

```bash
cd backend
uv run alembic upgrade head
```

### Variables d'environnement

Créer un fichier `.env` dans `backend/` et ajouter les variables nécessaires au backend et à la base de données :

```env
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxx
DB_HOST=localhost
DB_PORT=5432
DB_USER=tara_user
DB_PASSWORD=tarapassword
DB_NAME=tara_db
```

### Lancement du backend

```bash
cd backend
uv run fastapi dev main.py
```

### Lancement avec Docker

Depuis [backend/](backend/) :

```bash
docker compose up --build
```

### Créer une migration Alembic

Si le schéma de base de données évolue, générer puis appliquer une migration :

```bash
cd backend
uv run alembic revision --autogenerate -m "description de la migration"
uv run alembic upgrade head
```

### Lancement du système multi-agent

Le point d'entrée principal du pipeline se trouve dans `backend/agents/run.py`.

```bash
cd backend/agents
uv run python run.py
```

Ce script gère généralement :

1. la vérification des prérequis,
2. l'ingestion du corpus si la base vectorielle n'existe pas encore,
3. l'exécution séquentielle des 6 agents,
4. l'affichage structuré des résultats.

### Refaire l'ingestion

Si le modèle d'embedding change ou si la base vectorielle doit être régénérée, supprimer le dossier de persistance ChromaDB puis relancer le pipeline.

## Dossier [backend/agents/](backend/agents/)

Le README du dossier agents documente le pipeline complet. Les répertoires principaux sont :

- `ingestion/` : chargement, chunking et indexation du corpus,
- `retrieval/` : interrogation de la base vectorielle,
- `llm_clients/` : clients NIM, Gemini et Llama,
- `orchestrator/` : état global et graphe principal,
- `planner/`, `retriever/`, `canvas_analyst/`, `strategist/`, `roadmap_generator/`, `evaluator/` : logique métier des 6 agents.


## Auteurs

- Jarfino
- DEMBA SOW Achta
