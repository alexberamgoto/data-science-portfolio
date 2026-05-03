# RAPPORT DE TEST — Projet SPARK

---

## Diagnostic du Projet

### Infrastructure
- OS : Windows
- Docker : v28.5.1
- Docker Compose : v2.40.0
- Docker Hub Access : BLOQUÉ (Impossible de pulls les images)

### Fichiers du Projet
```
 data/social_media_events.csv         — Créé (50 événements test)
 spark_jobs/batch_engagement.py       — Valide
 spark_jobs/batch_preferences_age.py  — Valide
 spark_jobs/batch_sentiment.py        — Valide
 spark_jobs/stream_activity_spikes.py — Valide
 spark_jobs/stream_sentiment.py       — Valide
 kafka/kafka_producer.py              — Valide
 docker-compose.yml                   — Valide
 run_project.sh                       — Valide
```

---

## ERREUR RENCONTRÉE

```
Error: failed to resolve reference "docker.io/bde2020/hadoop-namenode:2.0.0-hadoop3.3.3-java11"
```

**Cause** : Docker Hub n'est pas accessible pour télécharger les images

---

## SOLUTIONS

### Solution 1 : Redémarrer Docker Desktop (Recommandé)
1. Ouvrir Docker Desktop
2. Attendre que le statut passe à "Running"
3. Vérifier la connexion Internet
4. Relancer `docker-compose up -d`

### Solution 2 : Vérifier la Connexion Internet
```powershell
ping docker.io
ipconfig /all
```

### Solution 3 : Configurer le proxy Docker (si nécessaire)
1. Ouvrir **Docker Desktop Settings**
2. Aller dans **Resources** → **Proxies**
3. Configurer votre proxy réseau

### Solution 4 : Pré-télécharger les images
```powershell
# Sur une machine connectée à Internet :
docker pull bde2020/hadoop-namenode:2.0.0-hadoop3.3.3-java11
docker pull bde2020/hadoop-datanode:2.0.0-hadoop3.3.3-java11
docker pull bitnami/spark:latest
docker pull confluentinc/cp-zookeeper:7.5.0
docker pull confluentinc/cp-kafka:7.5.0

# Puis exporter et importer sur votre machine
docker save -o images.tar [nom-image]
docker load -i images.tar
```

---

##  RÉSUMÉ DU PROJET

### Jobs Batch (Traitement historique)
1. **batch_engagement.py**
   - Calcule le score d'engagement utilisateur
   - Formule: (actions × 0.3) + (heures × 0.4) + (sessions × 0.3)
   - Output: TOP 20 utilisateurs les plus engagés

2. **batch_preferences_age.py**
   - Analyse les préférences par tranche d'âge
   - Plateforme préférée, type de contenu, sentiment moyen

3. **batch_sentiment.py**
   - Analyse du sentiment par pays et plateforme
   - Statistiques: min, max, moyenne, écart-type

### Jobs Stream (Temps réel - via Kafka)
1. **stream_activity_spikes.py**
   - Détecte les pics d'activité en temps réel
   - Fenêtre glissante: 5 minutes

2. **stream_sentiment.py**
   - Surveillance du sentiment par thématique
   - Alertes sentiment négatif

3. **stream_sessions_analysis.py**
   - Analyse des sessions en direct
   - Durée, engagement, activités

---

##  PROCHAINES ÉTAPES

**Pour relancer le test complet :**

1.  Vérifier la connexion Internet
2.  Redémarrer Docker Desktop
3.  Exécuter: `docker-compose up -d`
4.  Attendre 2-3 minutes du démarrage
5.  Vérifier: `docker-compose ps`
6.  Lancer: `./run_project.sh` (via WSL ou Git Bash)

**Durée estimée** : 10-20 minutes (incluant le démarrage des services)

---

##  RÉSULTATS ATTENDUS

Une fois le test complet exécuté :
```
results/
├── batch_results/
│   ├── engagement_users/
│   ├── preferences_by_age/
│   └── sentiment_analysis/
└── stream_results/
    ├── activity_spikes/
    ├── sentiment_monitoring/
    └── sessions_analysis/
```

---
