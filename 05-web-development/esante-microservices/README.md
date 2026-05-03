# Projet E-Santé — Plateforme Web Back End

## Description
Plateforme Web Back End E-Santé pour médecins et patients fictifs (PoC).  
**Thème** : cancer du sein.

## Architecture Microservices

```
┌─────────────────────────────────────────────────────┐
│  Client (curl / Postman / Front)                    │
│                  │                                   │
│           port 3000 (Gateway)                       │
│  ┌───────────────┴───────────────┐                  │
│  │       AUTH SERVICE            │                  │
│  │  FastAPI + SQLAlchemy         │                  │
│  │  JWT (access + refresh)       │──── MariaDB      │
│  │  Proxy → Health Service       │                  │
│  └───────────────┬───────────────┘                  │
│           port 8000 (interne)                       │
│  ┌───────────────┴───────────────┐                  │
│  │      HEALTH SERVICE           │                  │
│  │  FastAPI + Motor (async)      │                  │
│  │  CRUD patients + données      │──── MongoDB      │
│  │  ML model (RandomForest)      │                  │
│  └───────────────────────────────┘                  │
└─────────────────────────────────────────────────────┘
```

## Lancement

```bash
docker-compose up --build
```

Le service est accessible sur **http://localhost:3000**

## Endpoints

### Auth (publics)
| Méthode | URI             | Description                   |
|---------|-----------------|-------------------------------|
| POST    | /auth/register  | Création d'un compte médecin  |
| POST    | /auth/login     | Authentification (token JWT)  |
| POST    | /auth/refresh   | Rafraîchissement du token     |

### Health (privés — JWT requis)
| Méthode | URI                              | Description                         |
|---------|----------------------------------|-------------------------------------|
| POST    | /patients                        | Créer un patient                    |
| GET     | /patients                        | Lister les patients du médecin      |
| GET     | /patients/{id}                   | Détail d'un patient                 |
| POST    | /patients/{id}/data              | Ajouter des données de santé        |
| GET     | /patients/{id}/data              | Données de santé + prédiction       |
| GET     | /patients/{id}/prediction        | Prédiction uniquement               |
| POST    | /patients/{id}/prediction        | Lancer une prédiction (async)       |

## Tests rapides (curl)

```bash
# 1. Register
curl -X POST http://localhost:3000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"dr.dupont@mail.com","password":"secret123","first_name":"Jean","last_name":"Dupont"}'

# 2. Login
TOKEN=$(curl -s -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"dr.dupont@mail.com","password":"secret123"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

# 3. Créer patient
PATIENT=$(curl -s -X POST http://localhost:3000/patients \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Marie","last_name":"Martin","date_of_birth":"1985-03-15","gender":0}')
PATIENT_ID=$(echo $PATIENT | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")

# 4. Ajouter données de santé
curl -X POST http://localhost:3000/patients/$PATIENT_ID/data \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"age":39,"gender":0,"smoking":2,"alcohol_use":1,"obesity":3,"family_history":true,"diet_red_meat":4,"diet_salted_processed":3,"fruit_veg_intake":7,"physical_activity":6,"air_pollution":2,"occupational_hazards":1,"brca_mutation":false,"h_pylori_infection":false,"calcium_intake":5,"bmi":24.5,"physical_activity_level":6}'

# 5. Lancer prédiction
curl -X POST http://localhost:3000/patients/$PATIENT_ID/prediction \
  -H "Authorization: Bearer $TOKEN"

# 6. Consulter prédiction (attendre 2-3s)
sleep 3
curl http://localhost:3000/patients/$PATIENT_ID/prediction \
  -H "Authorization: Bearer $TOKEN"
```

## References Techniques
- Python 3.11, FastAPI, Uvicorn
- SQLAlchemy + PyMySQL (MariaDB)
- Motor (MongoDB async)
- python-jose (JWT), passlib (bcrypt)
- scikit-learn, pandas, numpy (ML)
- Docker & Docker Compose

### Precision 
Certaines fonctions utilisées dans ce projet ont occasionné des erreurs ou présentaient des limites techniques que je ne maîtrisais pas totalement. Pour résoudre ces problèmes et améliorer la qualité des codes, j’ai fait appel à des documentations et  LLM afin d’obtenir une assistance sur certains points complexes pour moi.
Merci de votre compréhension dans le cadre de ce projet.
