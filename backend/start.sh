#!/bin/bash

# Arrêter le script si une commande échoue
set -e

echo "--- [TARA STARTUP] Vérification de la base de données ---"

# On attend que le service 'db' (défini dans docker-compose) réponde sur le port 5432
# 'nc' (netcat) est utilisé pour vérifier l'ouverture du port
until nc -z db 5432; do
  echo "Base de données Postgres indisponible - attente de 1 seconde..."
  sleep 1
done

echo "Base de données prête !"

echo "--- [TARA STARTUP] Exécution des migrations Alembic ---"
# On applique les dernières révisions de la base de données
python -m alembic upgrade head

echo "--- [TARA STARTUP] Démarrage de l'application FastAPI ---"
# Lancement de l'application
exec uvicorn main:app --host 0.0.0.0 --port 8000