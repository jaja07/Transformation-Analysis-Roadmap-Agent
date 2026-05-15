FROM python:3.11-slim

WORKDIR /app/

# Installation des dépendances système
# netcat-openbsd est ajouté pour le script d'attente de la DB
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Installation de uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copie des fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installation des paquets dans le Python système du conteneur
RUN uv sync --frozen --no-cache

# Copie de l'intégralité du code source
COPY . .

# Gestion des permissions pour le script de démarrage
RUN chmod +x start.sh

EXPOSE 8000

# Le point d'entrée est désormais le script start.sh
CMD ["./start.sh"]