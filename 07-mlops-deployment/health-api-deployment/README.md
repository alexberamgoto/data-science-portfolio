# Déploiement IA — FastAPI Async (Health Service)

Cours appliqué de **déploiement IA** : conteneurisation Docker, FastAPI synchrone vs asynchrone, tests d'intégration.

## Contenu
| Fichier | Rôle |
|---------|------|
| `projet_health/` | API FastAPI + Dockerfile + docker-compose |
| `exercice_async.py` | Exercice asyncio |
| `test_sync.py` / `test_async.py` | Bench sync vs async (httpx, asyncio) |
| `requirements.txt` | Dépendances |

## Lancer
```bash
cd projet_health
docker compose up --build
```

## Stack
Python 3.11 · FastAPI · httpx · asyncio · Docker · pytest
