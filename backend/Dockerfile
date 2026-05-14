FROM python:3.11-slim

WORKDIR /app/

# Installation des dépendances système nécessaires pour psycopg2 (Postgres)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installation de uv (méthode officielle recommandée)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copie des fichiers de configuration uv (pour le cache des dépendances)
COPY pyproject.toml uv.lock ./

# Installation des dépendances du projet sans créer d'environnement virtuel (inutile dans Docker)
RUN uv sync --system --frozen --no-cache

# Copie du reste du code du projet
COPY . .

EXPOSE 8000

# Lancement direct via uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]