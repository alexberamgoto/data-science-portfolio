# Démarrage rapide - Quick Start

## 1. Installation de l'environnement (5 minutes)

### Windows

```bash
setup_env.bat
```

### Linux / Mac

```bash
chmod +x setup_env.sh
./setup_env.sh
```

## 2. Vérifier l'installation

```bash
# Activer l'environnement (si pas encore activé)
# Windows :
.venv\Scripts\activate
# Linux/Mac :
source .venv/bin/activate

# Tester les imports
python -c "import pyspark; print(f'PySpark {pyspark.__version__}')"
python -c "from kafka import KafkaProducer; print('Kafka OK')"
python -c "import pandas; print(f'Pandas {pandas.__version__}')"
```

## 3. Préparer les données

Placez votre fichier CSV dans le dossier `data/` :
```
data/social_media_events.csv
```

Colonnes requises :
- user_id
- timestamp
- platform
- action
- session_id
- device
- country
- age_group
- lifestyle
- topic
- duration_sec
- sentiment

## 4. Lancer le projet complet

```bash
# Démarrer toute l'infrastructure Docker + jobs batch
bash run_project.sh
```

Cela va :
- ✓ Démarrer tous les conteneurs (Kafka, Zookeeper, HDFS, Spark)
- ✓ Charger les données dans HDFS
- ✓ Exécuter les 3 jobs batch
- ✓ Afficher les instructions pour les streams

## 5. Lancer les jobs de streaming (en parallèle)

Ouvrez 2-3 terminaux différents :

**Terminal 1 - Producteur Kafka :**
```bash
docker exec -it spark-master python3 /spark_jobs/../kafka/kafka_producer.py
```

**Terminal 2 - Stream 1 (Pics d'activité) :**
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /spark_jobs/stream_activity_spikes.py
```

**Terminal 3 - Stream 2 (Sentiment en temps réel) :**
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /spark_jobs/stream_sentiment.py
```

## 6. Accéder aux interfaces web

- **HDFS NameNode** : http://localhost:9870
- **Spark Master** : http://localhost:8080
- **Spark Worker 1** : http://localhost:8081
- **Spark Worker 2** : http://localhost:8082

## 7. Vérifier le statut du cluster

```bash
bash check_status.sh
```

## 8. Arrêter le projet

```bash
# Arrêter les conteneurs (données préservées)
bash cleanup.sh stop

# Nettoyer complètement (supprime tout)
bash cleanup.sh clean

# Redémarrer
bash cleanup.sh restart
```

## Troubleshooting

### Erreur : "Docker Compose n'est pas installé"
Installez Docker Desktop (Windows/Mac) ou Docker CE (Linux)

### Erreur : "Kafka pas encore prêt"
Attendez 30-60 secondes après avoir lancé `run_project.sh`. Kafka prend du temps à démarrer.

### Erreur : "CSV non trouvé"
Vérifiez que vous avez placé `social_media_events.csv` dans le dossier `data/`

### Erreur : "Port déjà utilisé"
Un autre service utilise les ports (9870, 8080, 9092, etc.). Arrêtez le service ou changez les ports dans `docker-compose.yml`.

### Problème de mémoire
Les workers Spark ont 2GB de RAM chacun. Si vous manquez de mémoire :
- Augmentez les ressources Docker
- Réduisez SPARK_WORKER_MEMORY dans `.env`

## Structure du projet

```
.
├── kafka/                    # Producteur Kafka
│   └── kafka_producer.py
├── spark_jobs/              # Jobs Spark
│   ├── batch_engagement.py
│   ├── batch_preferences_age.py
│   ├── batch_sentiment.py
│   ├── stream_activity_spikes.py
│   ├── stream_sentiment.py
│   └── stream_sessions_analysis.py
├── scripts/                 # Scripts utilitaires
│   └── upload_to_hdfs.sh
├── data/                    # Données d'entrée
│   └── social_media_events.csv
├── results/                 # Résultats (généré)
├── docker-compose.yml       # Configuration Docker
├── requirements.txt         # Dépendances Python
├── environment.yml          # Dépendances Conda
├── setup.py                 # Installation package
├── .env                     # Variables d'environnement
├── SETUP.md                 # Guide d'installation détaillé
└── setup_env.bat/sh         # Scripts d'installation
```

## Commandes utiles

```bash
# Vérifier les logs d'un conteneur
docker compose logs -f spark-master

# Entrer dans un conteneur
docker exec -it spark-master bash

# Lancer un job Spark manuellement
docker exec spark-master spark-submit /spark_jobs/batch_engagement.py

# Vérifier l'espace HDFS
docker exec namenode hdfs dfs -du -h /

# Lister les résultats
docker exec namenode hdfs dfs -ls -R /results/
```

## Configuration avancée

Modifiez `.env` pour :
- Changer les ports
- Ajuster la mémoire Spark
- Configurer un autre broker Kafka
- Modifier les chemins HDFS

## Support et documentation

- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Kafka Python](https://kafka-python.readthedocs.io/)
- [Docker Compose](https://docs.docker.com/compose/)

---

**Prêt à commencer ?** Exécutez `setup_env.bat` (Windows) ou `./setup_env.sh` (Linux/Mac) et lancez `bash run_project.sh` !
