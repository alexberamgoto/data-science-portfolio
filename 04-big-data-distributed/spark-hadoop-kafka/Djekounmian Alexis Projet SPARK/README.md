#  Projet Analyse des interactions Social Media

**Architecture distribuée HDFS + Spark + Kafka sur Docker pour le traitement des données massives et en streaming**

---

## Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Prérequis](#prérequis)
- [Installation & Démarrage](#installation--démarrage)
- [Jobs disponibles](#jobs-disponibles)
- [Interfaces web](#interfaces-web)
- [Fichiers de résultats](#fichiers-de-résultats)
- [Commandes utiles](#commandes-utiles)
- [Troubleshooting](#troubleshooting)

---

## Vue d'ensemble

Architecture Big Data complète permettant le traitement batch et streaming de **millions d'événements** issus de réseaux sociaux.

###  Capabilités

**Traitements Batch (Données historiques)**
- Engagement utilisateur avec score composite
- Préférences par tranche d'âge
- Sentiment par pays et plateforme

**Traitements Streaming (Temps réel)**
- Détection de pics d'activité
- Surveillance du sentiment par thématique
- Analyse des sessions en direct

**Infrastructure distribuée**
```
1 Zookeeper + 1 Kafka
↓
1 HDFS (NameNode + Secondary + 2 DataNodes)
↓
1 Spark Cluster (Master + 2 Workers)
```

---

## installation des logiciels 
- **Docker** : v20.10+ [Installer](https://docs.docker.com/install/)

### Vérification
```bash
docker --version
docker compose version
,,, 

##  Installation & Démarrage

### Option 1 : Démarrage automatique (Recommandé)

```bash
# Rendre le script exécutable
chmod +x run_project.sh

# Lancer
./run_project.sh
```

Cela va :
1. ✓ Vérifier Docker et le CSV
2. ✓ Démarrer les 13 conteneurs
3. ✓ Charger les données dans HDFS
4. ✓ Exécuter les 3 jobs batch
5. ✓ Afficher instructions streaming


### Option 2 : Démarrage manuel

```bash
# Étape 1 : Démarrer l'infrastructure
docker compose up -d
sleep 60

# Étape 2 : Charger les données
docker exec namenode hdfs dfsadmin -safemode wait
docker exec namenode hdfs dfs -mkdir -p /data/social_media
docker cp data/social_media_events.csv namenode:/tmp/
docker exec namenode hdfs dfs -put -f /tmp/social_media_events.csv /data/social_media/

# Étape 3 : Exécuter d'un job
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /spark_jobs/batch_engagement.py
```

##  Jobs disponibles

### BATCH (Traitements historiques)

#### 1️ `batch_engagement.py` - Engagement utilisateur
**Objective**: Identifier les utilisateurs les plus actifs

**Métriques**:
- Nombre d'actions
- Temps total passé (heures)
- Sessions distinctes
- Sentiment moyen
- Score composite

**Exécution**:
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /spark_jobs/batch_engagement.py
```

**Sortie**: Top 20 utilisateurs + statistiques

---

#### 2️ `batch_preferences_age.py` - Préférences par âge
**Objective**: Comprendre les comportements différenciés par démographie

**Analyses**:
- Plateforme préférée par tranche d'âge
- Topics privilégiés par groupe d'âge
- Devices utilisés
- Matrice actions × tranches

**Exécution**:
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /spark_jobs/batch_preferences_age.py
```

---

####  `batch_sentiment.py` - Sentiment par pays/plateforme
**Objective**: Analyser la tonalité globale du contenu

**Analyses**:
- Sentiment moyen par pays
- Sentiment par plateforme
- Matrice croisée pays × plateforme
- Distribution sentiments (-1, 0, +1)
- Alertes sur zones « négatives »

**Exécution**:
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /spark_jobs/batch_sentiment.py
```

---

### STREAM (Traitement temps réel)

####  `stream_activity_spikes.py` - Détection de pics
**Objective**: Identifier les événements viraux en temps réel

**Fenêtre**: 1 minute (glissement 30 sec)
**Granularité**: Par plateforme
--- 
**Setup**:
```bash
# Terminal 1 : Producteur Kafka
docker exec spark-master pip install kafka-python --quiet
docker exec spark-master python3 /spark_jobs/../kafka/kafka_producer.py

# Terminal 2 : Consumer Spark
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /spark_jobs/stream_activity_spikes.py
```

**Sortie**: Mise à jour console toutes les 10 secondes

---

####  `stream_sentiment.py` - Sentiment par thème
**Objective**: Monitorer sentiments en continu

**Fenêtre**: 2 minutes (glissement 1 min)
**Alertes**:
- 🔴 Négatif (sentiment < -0.2)
- ⚪ Neutre
- 🟢 Positif (sentiment > +0.2)

**Exécution**:
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /spark_jobs/stream_sentiment.py
```

---

####  `stream_sessions_analysis.py` - Analyse sessions
**Objective**: Tracker l'engagement real-time

**Fenêtre**: 5 minutes (glissement 1 min)

**Trois sorties parallèles**:
1. Métriques globales (sessions, utilisateurs, events)
2. Top 5 utilisateurs les plus actifs
3. Sessions très engagées (score > 5)

**Exécution**:
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /spark_jobs/stream_sessions_analysis.py
```

---

##  Interfaces web

Toutes accessibles une fois démarrage complet :

| Service | URL | Usage |
|---------|-----|-------|
| HDFS NameNode | http://localhost:9870 | Vue cluster, blocks, usage |
| HDFS DataNode 1 | http://localhost:9864 | Détails nœud 1 |
| HDFS DataNode 2 | http://localhost:9865 | Détails nœud 2 |
| **Spark Master** | http://localhost:8080 | **Statut cluster + workers** |
| Spark Worker 1 | http://localhost:8081 | Détails worker 1 |
| Spark Worker 2 | http://localhost:8082 | Détails worker 2 |
| App UI (live) | http://localhost:4040 | Stages, tasks, performance |

---

### Résultats Batch locaux

Après exécution, disponibles dans :
```
results/
├── batch_results/
│   ├── engagement_utilisateur/
│   │   └── part-00000-*.csv
│   ├── preferences_age_platform/
│   │   └── part-00000-*.csv
│   └── preferences_age_topic/
│       └── part-00000-*.csv
└── sentiment_matrice/
    └── part-00000-*.csv
```

### Accès HDFS

```bash
# Lister
docker exec namenode hdfs dfs -ls /results/batch/

# Récupérer
docker exec namenode hdfs dfs -get \
  /results/batch/engagement_utilisateur /tmp/
docker cp namenode:/tmp/engagement_utilisateur ./
```

---

## 🔧 Commandes utiles utilisés dans notre dans nos travaux 
### Infrastructure

```bash
./run_project.sh          # Démarrage complet
./check_status.sh         # Vérifier statut
./cleanup.sh stop         # Arrêter (volumes gardés)
./cleanup.sh clean        # Tout supprimer
./cleanup.sh restart      # Redémarrer
```

### HDFS

```bash
# Safemode
docker exec namenode hdfs dfsadmin -safemode wait

# Report status
docker exec namenode hdfs dfsadmin -report

# Lister
docker exec namenode hdfs dfs -ls -R /

# Upload
docker cp file.txt namenode:/tmp/
docker exec namenode hdfs dfs -put /tmp/file.txt /hdfs/path/

# Download
docker exec namenode hdfs dfs -get /hdfs/path /tmp/
docker cp namenode:/tmp/path ./
```

### Spark

```bash
# PySpark interactif
docker exec -it spark-master pyspark

# View applications
docker exec spark-master curl http://localhost:8080/api/v1/applications

# Logs
docker compose logs -f spark-master
```

### Kafka

```bash
# Topics
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Consumer
docker exec kafka kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic social_media_events --from-beginning
```

---

##  Architecture détaillée

```
┌────────────────────────────────────────────────────────────────┐
│          DOCKER NETWORK (bigdata-net)                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌───────────────────┐  ┌────────────────────────────────┐    │
│  │  Ingestion        │  │  Traitement                    │    │
│  │  ┌─────────────┐  │  │  ┌────────────────────────┐   │    │
│  │  │ Zookeeper   │◄─┼──┼─►│ Spark Master           │   │    │
│  │  │ :2181       │  │  │  │ :7077 • :8080 • :4040  │   │    │
│  │  └─────────────┘  │  │  └────────────────────────┘   │    │
│  │  ┌─────────────┐  │  │  ┌──────────────┐             │    │
│  │  │ Kafka       │◄─├──┼─►│ Worker 1     │             │    │
│  │  │ :9092       │  │  │  │ :8081        │             │    │
│  │  └─────────────┘  │  │  └──────────────┘             │    │
│  │                   │  │  ┌──────────────┐             │    │
│  └───────────────────┘  │  │ Worker 2     │             │    │
│                         │  │ :8082        │             │    │
│                         │  └──────────────┘             │    │
│                         └────────────────────────────────┘    │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Stockage (HDFS)                                       │   │
│  │  ┌──────────┐  ┌────────────┐  ┌──────┐  ┌──────┐    │   │
│  │  │NameNode  │  │ Secondary  │  │DN 1  │  │DN 2  │    │   │
│  │  │ :9870    │  │            │  │:9864 │  │:9865 │    │   │
│  │  └──────────┘  └────────────┘  └──────┘  └──────┘    │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

##  Troubleshooting

### ``Port déjà utilisé``
```bash
./cleanup.sh clean
docker compose down -v
# Puis relancer./run_project.sh
```

### ``HDFS safe mode``
```bash
docker exec namenode hdfs dfsadmin -safemode leave
```

### ``Spark job échoue``
```bash
# Voir les logs
docker compose logs spark-master -f

# Vérifier ressources
docker stats

# Augmenter mémoire dans docker-compose.yml
```

### ``Kafka ne répond pas``
```bash
./check_status.sh  # Diagnostic complet
# Attendre 60s et réessayer
```

---

##  Documentation complète

Pour rapport détaillé : 
- Architecture & motivations
- Dataset détaillé
- Analyses techniques
- Résultats exploitables

---

##  Structure du projet

```
.
├── docker-compose.yml           Infrastructure
├── run_project.sh               Démarrage auto
├── cleanup.sh                   Arrêt/nettoyage
├── check_status.sh              Diagnostic
├── README.md                    Documentation
├── RAPPORT.md                   Rapport complet
│
├── data/social_media_events.csv À FOURNIR
├── kafka/kafka_producer.py      Producteur
├── spark_jobs/                  6 jobs
│   ├── batch_*.py               (3 jobs)
│   └── stream_*.py              (3 jobs)
└── results/                     Résultats batch
```

---

##  Quick Reference

```bash
# 1. Préparer données
mkdir -p data && cp social_media_events.csv data/

# 2. Démarrer
./run_project.sh

# 3. Attendre batch (5-15 min)

# 4. Streaming (2+ terminaux)
# Terminal A
docker exec spark-master pip install kafka-python --quiet
docker exec spark-master python3 /spark_jobs/../kafka/kafka_producer.py

# Terminal B
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /spark_jobs/stream_activity_spikes.py

# 5. Explorer résultats
# HDFS UI    : http://localhost:9870
# Spark UI   : http://localhost:8080
# App UI (live) : http://localhost:4040

# 6. Arrêter
./cleanup.sh stop
```