# Backend Santé – API REST (TypeScript) + API ML (Python) – Docker Compose

Projet pédagogique complet : **API REST TypeScript** (patients/médecins, auth JWT, données de santé) + **API Python FastAPI** (service ML), **PostgreSQL** pour l'API REST et **DB ML optionnelle**. Le service ML n'est **pas exposé** à l'extérieur : seule l'API REST peut l'appeler via le réseau Docker.

## Démarrage rapide
```bash
# 1) Créer un fichier .env à partir de .env.example
cp .env.example .env

# 2) Lancer l'ensemble
docker compose up --build

# 3) API REST : http://localhost:3000
#    API ML : non exposée (réseau interne), accessible depuis api-rest à http://api-ml:8000
```

## Services
- `api-rest` : Node.js + TypeScript + Express + TypeORM + JWT
- `db-rest`  : PostgreSQL (stockage principal)
- `api-ml`   : FastAPI (service d'analyse ML non exposé)
- `db-ml`    : PostgreSQL (optionnel – historique prédictions)

## Endpoints principaux (API REST)
- `POST /auth/register` { role: 'DOCTOR'|'PATIENT', email, password, profile }
- `POST /auth/login` { email, password }
- `POST /patients/data` (PATIENT) – dépose des constantes (poids, tension, glycémie…)
- `GET  /patients/data/history` (PATIENT) – historique
- `GET  /doctors/patients` (DOCTOR) – liste des patients suivis
- `GET  /doctors/patients/:id/data` (DOCTOR) – données d'un patient
- `POST /analysis/request` – appelle l'API ML interne et stocke le résultat

## Comptes & rôles
- Un **User** possède un rôle `DOCTOR` ou `PATIENT`. Les profils `Doctor`/`Patient` sont liés au user.

## Sécurité
- JWT (HS256) – `JWT_SECRET` dans `.env`
- Le service `api-ml` **n'a pas de port mappé** vers l'hôte, uniquement `expose` pour le réseau docker interne.

## Base de données
- Par défaut, TypeORM `synchronize: true` pour simplifier en dev. En prod, désactiver et utiliser des migrations.

## Tests rapides (après `docker compose up`)
1. **Register patient**
```bash
curl -X POST http://localhost:3000/auth/register   -H 'Content-Type: application/json'   -d '{"role":"PATIENT","email":"pat@example.com","password":"Test!123","profile":{"firstName":"Pat","lastName":"Ent","dateOfBirth":"1990-01-01"}}'
```
2. **Login** -> récupérer `accessToken`
3. **POST patients/data** avec le token d'un patient
```bash
curl -X POST http://localhost:3000/patients/data  -H 'Authorization: Bearer <ACCESS_TOKEN>' -H 'Content-Type: application/json'  -d '{"weight":78.5,"systolic":130,"diastolic":82,"glucose":1.02,"notes":"à jeun"}'
```
4. **POST analysis/request** (patient ou médecin) -> renvoie score & risque

---
