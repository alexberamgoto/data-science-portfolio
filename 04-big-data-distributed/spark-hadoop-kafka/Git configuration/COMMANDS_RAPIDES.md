## 🚀 GUIDE RAPIDE — Commandes Directes

### ✅ Status: Infrastructure Déployée et Prête

---

### 📊 **LANCER LES JOBS D'ANALYSE**

#### Option 1 : Job d'Engagement (Utilisateurs)
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /spark_jobs/batch_engagement.py
```

#### Option 2 : Job Préférences par Âge
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /spark_jobs/batch_preferences_age.py
```

#### Option 3 : Job Sentiment Analysis
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  /spark_jobs/batch_sentiment.py
```

---

### 📡 **MODE STREAMING (Temps Réel)**

#### Terminal 1 : Lancer le Producteur
```bash
docker exec spark-master python3 \
  /kafka/kafka_producer.py
```

#### Terminal 2 : Consumer (Pics d'Activité)
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 \
  /spark_jobs/stream_activity_spikes.py
```

---

### 📊 **INTERFACES WEB (Monitoring)**

Accès direct dans votre navigateur :
- **HDFS** : http://localhost:9870
- **Spark** : http://localhost:8080
- **Workers** : http://localhost:8081 et http://localhost:8082

---

### 🔍 **VÉRIFIER LES RÉSULTATS**

#### Voir les fichiers dans HDFS
```bash
docker exec namenode hdfs dfs -ls /results/batch/
docker exec namenode hdfs dfs -ls /results/stream/
```

#### Télécharger les résultats
```bash
docker exec namenode hdfs dfs -get /results/batch/* ./results_batch/
docker exec namenode hdfs dfs -get /results/stream/* ./results_stream/
```

---

### 🔧 **COMMANDES UTILES**

#### État des services
```bash
docker-compose ps
```

#### Logs d'un service
```bash
docker logs spark-master    # Pour Spark Master
docker logs namenode        # Pour HDFS
docker logs kafka           # Pour Kafka
```

#### Redémarrer l'infrastructure
```bash
docker-compose down -v
docker-compose up -d
```

#### Arrêter les services
```bash
docker-compose down
```

---

### 📁 **VOS FICHIERS IMPORTANTS**

- 📄 `RESUME_EXECUTION.md` — Récapitulatif complet
- 📄 `EXECUTION_SUCCESS.md` — Détails d'exécution
- 📄 `RAPPORT_TEST_FINAL.md` — Diagnostic technique
- 📊 `data/social_media_events.csv` — Données de test

---

**✅ Infrastructure Prête | 🚀 Lancer les Commandes | 📊 Voir les Résultats**
