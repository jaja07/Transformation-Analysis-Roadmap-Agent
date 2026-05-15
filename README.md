# TARA : Transformation Analysis & Roadmap Agent

**TARA** est un système d'intelligence artificielle avancé conçu pour accompagner les entreprises dans leur stratégie numérique. Ce projet, réalisé dans le cadre du **Master of Science in AI (M2) à l'ECE Paris** , vise à transformer une simple description d'entreprise en une feuille de route de transformation digitale structurée, cohérente et directement actionnable.

## 🎯 Objectifs du Projet

L'objectif est de concevoir un système capable de :

* **Analyser** un cas métier complexe pour en extraire les enjeux stratégiques.


* **Exploiter** un corpus documentaire de référence (frameworks académiques) via une architecture **RAG (Retrieval-Augmented Generation) locale**.


* **Raisonner** de manière modulaire grâce à une architecture **multi-agents** spécialisés.


* **Optimiser** les coûts et les performances via un mécanisme de **routage multi-LLM**.



## 🏗️ Architecture du Système

Le projet adopte une approche *lightweight full-stack*  séparant distinctement le moteur d'IA de l'interface utilisateur.

### 🧠 Logique Cognitive (Multi-Agents)

Le système orchestre six agents spécialisés via **LangGraph**  :

1. **Planner Agent** : Structure le problème et définit la logique "Why / What / How".


2. **Retrieval/Framework Agent** : Interroge la base vectorielle pour extraire le contexte pertinent.


3. **Canvas Analysis Agent** : Analyse l'entreprise selon les 7 domaines du *Digital Transformation Canvas*.


4. **Strategist Agent** : Définit la trajectoire stratégique et les piliers opérationnels.


5. **Roadmap Generator Agent** : Produit la feuille de route finale (initiatives, KPIs, timeline).


6. **Evaluator Agent** : Contrôle la qualité et la cohérence de la production finale.



### 🛠️ Stack Technique

* **Backend** : FastAPI, Pydantic, SQLModel.
* **Orchestration IA** : LangGraph, LangChain.
* **LLMs & Routing** : Gemini 2.5 Pro (raisonnement complexe), Gemini 2.5 Flash (tâches rapides), Llama local (expérimentation).


* **RAG** : ChromaDB (Vector Store), Sentence-Transformers (Embeddings).
* **Frontend** : Streamlit.


* **Gestionnaire de paquets** : `uv`.

## 📚 Frameworks de Référence

Le système fonde son raisonnement sur les cadres méthodologiques suivants inclus dans le corpus :

* **Wade (2015)** : Framework Why/What/How.


* **Peter (2018)** : Digital Transformation Canvas (7 domaines d'action).


* Elia et al. (2024) : Canevas stratégique et opérationnel.



## 🚀 Installation et Lancement

### Prérequis

* Python 3.13+ pour le backend local
* Node.js 18+ pour le frontend local
* Docker si tu veux lancer toute la stack en conteneurs
* `uv` installé (`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.11.14/install.ps1 | iex"`)

### 1. Installation locale

Backend :

```bash
cd backend
uv sync

```

Frontend :

```bash
cd frontend
npm install

```

### 2. Lancement local

Backend :

```bash
cd backend
uv run fastapi dev main.py

```

Frontend :

```bash
cd frontend
npm run dev

```

### 3. Configuration

Créez un fichier `.env` dans `backend/` et ajoutez vos clés API :

```env
GOOGLE_API_KEY=votre_cle_gemini
DATABASE_URL=sqlite:///./tara_database.db

```

### 4. Ingestion du corpus (RAG)

Avant le premier lancement, préparez la base vectorielle :

```bash
cd backend
uv run python -m data_ingestion.loader

```

### 5. Lancement Docker

Depuis `backend/` :

```bash
docker compose up --build

```

## 📁 Structure du Projet

```text
├── api/              # Endpoints FastAPI
├── core/             # Configuration et State LangGraph
├── schema/           # Schémas Pydantic et SQLModel
├── agents/           # Logique et Prompts des 6 agents
├── vector_store/     # Gestion de la base ChromaDB
├── retrieval/        # Logique de recherche RAG
└── routing/          # Sélecteur de modèle LLM

```

---

**Auteurs** : Jarfino & [Nom de ton binôme]

**Encadrement** : Sarah Malaeb, ECE Paris 

**Année** : 2025-2026