# Projet Big Data — Analyse des interactions Social Media

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        DOCKER NETWORK                            │
│                                                                  │
│  ┌─────────────┐  ┌──────────────────┐  ┌────────────────────┐  │
│  │  ZOOKEEPER  │  │      KAFKA       │  │                    │  │
│  │  :2181      │──│  :9092           │──│   SPARK MASTER     │  │
│  └─────────────┘  │  topic:          │  │   :8080 (UI)       │  │
│                   │  social_media_   │  │   :7077 (RPC)      │  │
│                   │  events          │  │                    │  │
│                   └──────────────────┘  └────────┬───────────┘  │
│                                                  │               │
│                                         ┌────────┴───────────┐  │
│                                         │                    │  │
│                                    ┌────┴────┐  ┌────────────┤  │
│                                    │ WORKER 1│  │  WORKER 2  │  │
│                                    │  2 cores│  │  2 cores   │  │
│                                    │  2 GB   │  │  2 GB      │  │
│                                    └─────────┘  └────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    HDFS CLUSTER                             │ │
│  │  ┌──────────┐  ┌───────────────┐  ┌──────┐  ┌──────────┐  │ │
│  │  │ NAMENODE │  │ SECONDARY NN  │  │ DN 1 │  │  DN 2    │  │ │
│  │  │ :9870 UI │  │               │  │      │  │          │  │ │
│  │  │ :9000 RPC│  │               │  │      │  │          │  │ │
│  │  └──────────┘  └───────────────┘  └──────┘  └──────────┘  │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

## Structure du projet

```
bigdata_project/
├── docker-compose.yml          # Infrastructure complète
├── run_project.sh              # Script d'exécution automatique
├── README.md                   # Ce fichier
├── data/
│   └── social_media_events.csv # ⬅ PLACEZ VOTRE FICHIER ICI
├── spark_jobs/
│   ├── batch_engagement.py     # Batch 1 : Engagement utilisateur
│   ├── batch_preferences_age.py # Batch 2 : Préférences par âge
│   ├── batch_sentiment.py      # Batch 3 : Sentiment pays/plateforme
│   ├── stream_activity_spikes.py # Stream 1 : Détection de pics
│   └── stream_sentiment.py     # Stream 2 : Sentiment temps réel
├── kafka/
│   └── kafka_producer.py       # Producteur Kafka (simulateur)
└── scripts/
    └── upload_to_hdfs.sh       # Upload vers HDFS
```

## Prérequis

- Docker Desktop (avec au moins 8 GB de RAM allouée)
- Docker Compose
- Le fichier `social_media_events.csv`

## Exécution pas à pas

### Étape 1 — Préparation

```bash
# Placez votre CSV dans le dossier data/
cp /chemin/vers/social_media_events.csv data/

# Rendez les scripts exécutables
chmod +x run_project.sh scripts/upload_to_hdfs.sh
```

### Étape 2 — Démarrage de l'infrastructure

```bash
docker compose up -d
# Attendez ~45 secondes que tout démarre
```

Vérifications :
- HDFS : http://localhost:9870
- Spark : http://localhost:8080

### Étape 3 — Chargement dans HDFS

```bash
# Attendre la sortie du safe mode
docker exec namenode hdfs dfsadmin -safemode wait

# Créer les répertoires et uploader
docker exec namenode hdfs dfs -mkdir -p /data/social_media
docker cp data/social_media_events.csv namenode:/tmp/social_media_events.csv
docker exec namenode hdfs dfs -put -f /tmp/social_media_events.csv /data/social_media/

# Vérifier
docker exec namenode hdfs dfs -ls /data/social_media/
```

### Étape 4 — Jobs Batch

```bash
# Job 1 : Engagement utilisateur
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark-jobs/batch_engagement.py

# Job 2 : Préférences par tranche d'âge
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark-jobs/batch_preferences_age.py

# Job 3 : Sentiment par pays et plateforme
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark-jobs/batch_sentiment.py
```

### Étape 5 — Jobs Streaming

Ouvrez **2 terminaux** :

**Terminal 1 — Producteur Kafka :**
```bash
# Installer kafka-python dans le conteneur
docker exec spark-master pip install kafka-python

# Lancer le producteur
docker exec spark-master python3 /opt/spark-jobs/../kafka/kafka_producer.py
```

**Terminal 2 — Consumer Spark Streaming :**
```bash
# Stream 1 : Détection de pics
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /opt/spark-jobs/stream_activity_spikes.py

# OU Stream 2 : Sentiment en temps réel
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /opt/spark-jobs/stream_sentiment.py
```

### Étape 6 — Arrêt

```bash
docker compose down      # Arrêter les conteneurs
docker compose down -v   # Arrêter + supprimer les volumes
```

## Jobs implémentés

### Batch

| # | Job | Description |
|---|-----|-------------|
| 1 | Engagement utilisateur | Score d'engagement composite par user_id |
| 2 | Préférences par âge | Plateforme et topic préférés par tranche d'âge |
| 3 | Sentiment pays/plateforme | Matrice de sentiment croisée + alertes |

### Streaming

| # | Job | Description |
|---|-----|-------------|
| 1 | Détection de pics | Volume d'activité par fenêtre glissante de 1 min |
| 2 | Sentiment temps réel | Sentiment moyen par topic avec alertes |
