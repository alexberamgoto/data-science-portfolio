# --- Étape 1 : Builder (Construction) ---
# On utilise image officielle Python 3.12 (Slim pour commencer léger)
FROM python:3.12-slim AS builder
# On définit le répertoire de travail dans le conteneur
WORKDIR /app
# --- Étape 1 : Builder (Construction) ---
# On utilise image officielle Python 3.12 (Slim pour commencer léger)
FROM python:3.12-slim AS builder
# On définit le répertoire de travail dans le conteneur
WORKDIR /app
# Optimisation Python :
# 1. Ne pas écrire de .pyc (gain de place et évite problèmes de droits)
# 2. Force l'affichage des logs dans la console (pas de buffer)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Installation des dépendances système
# (Nécessaire parfois pour compiler certaines libs comme numpy ou pandas)
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev
# Copie du fichier de dépendances
COPY requirements.txt .
# Installation des librairies Python dans un dossier local (--user)
# Cela facilitera la copie vers l'image finale
RUN pip install --user --no-cache-dir -r requirements.txt
# --- Étape 2 : Runner (Image finale) ---
# On repart de zéro avec une image propre
FROM python:3.12-slim
WORKDIR /app
# Variables d'environnement pour Python (mêmes que plus haut)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# SÉCURITÉ : Création d'un utilisateur système "appuser"
# Par défaut, Docker tourne en "root". C'est dangereux si se fait pirater.
# On crée un utilisateur simple sans droits d'administration.
RUN useradd -m appuser
# Copie des librairies installées depuis l'étape "builder"
# On les met dans le dossier .local de notre nouvel utilisateur
COPY --from=builder /root/.local /home/appuser/.local
# Mise à jour du PATH pour que le système trouve les commandes (uvicorn...)
ENV PATH=/home/appuser/.local/bin:$PATH
# Copie du code source de notre projet
# On copie QUE les fichiers .py du dossier app pour garder image propre
COPY --chown=appuser:appuser ./app/*.py .
# On bascule sur l'utilisateur sécurisé
USER appuser
# Documentation du port (informatif)
EXPOSE 8000
# Commande de démarrage
# On lance uvicorn sur le fichier main.py contenu dans le module app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
 ... (Début du fichier identique)
# Copie du code source ET des modèles
COPY --chown=appuser:appuser ./app/*.py .
COPY --chown=appuser:appuser ./app/models/. ./models
# ... (Fin du fichier identique)