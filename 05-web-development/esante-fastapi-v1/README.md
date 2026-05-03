# E-Santé — FastAPI (v1)

Première itération du backend e-santé (cancer du sein) — service patient + auth + intégration ML.
> **Version finale microservices** : voir `05-web-development/esante-microservices/`.

## Composants
| Fichier | Rôle |
|---------|------|
| `main_health.py` | Application FastAPI principale |
| `Routes_patient_prédiction.py` | Endpoints CRUD patients + prédiction |
| `modele_health.py` | Modèles SQLAlchemy / Pydantic |
| `database(health).py` | Connexion DB |
| `Schemas_health.py` | Schémas Pydantic |
| `auth_depency_health.fs` | Dépendances JWT |
| `auth-service/` | Service d'authentification séparé |
| `Dockerfile_Health.txt` | Dockerfile du service |

## Stack
Python 3.11 · FastAPI · SQLAlchemy · Pydantic · scikit-learn · Docker
