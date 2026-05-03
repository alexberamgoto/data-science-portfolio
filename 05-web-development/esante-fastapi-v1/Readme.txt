# Projet E-Santé – Plateforme Web Back-End

## Réalisé par Djekounmian Beramgoto Alexis , étudiant à la formation Data Scientists à l'IDMC.

## Contexte

Ce projet s'inscrit dans le cadre du cours de **Programmation Web** de la formation **Data Scientists** de l'IDMC.  
Il s'agit d'une preuve de concept d'une plateforme de e-santé pour l'évaluation du risque de cancer du sein, destinée à des médecins et patients fictifs.[file:1]

## Objectifs

- Implémenter un service **Auth** (création de comptes médecins, authentification par JWT).
- Implémenter un service **Health** (gestion des patients, données de santé et prédictions de risque).
- Exposer des **API REST** conformes aux endpoints fournis dans l'énoncé.
- Déployer les services via **Docker Compose** sur une architecture distribuée (réseau Docker bridge).
- Tester les APIs à l'aide de **Bruno**.[file:1]

## Architecture

- Service **Auth**
  - Stack: Python, FastAPI, SQLAlchemy, MariaDB, JWT.
  - Rôle: gestion des comptes médecins, login, refresh token.
  - Exposé sur le **port 3000** de la machine hôte (gateway).[file:1]

- Service **Health**
  - Stack: Python, FastAPI, SQLAlchemy, MariaDB (ou MongoDB).
  - Rôle: création et suivi des patients, stockage des données de santé, génération de prédictions de risque.
  - Accessible uniquement via le réseau Docker (non exposé directement sur la machine hôte).[file:1]

## Arborescence

```text
e-sante-backend/
├─ README.md
├─ docker-compose.yml
├─ auth-service/
│  ├─ app/...
└─ health-service/
   ├─ app/...
