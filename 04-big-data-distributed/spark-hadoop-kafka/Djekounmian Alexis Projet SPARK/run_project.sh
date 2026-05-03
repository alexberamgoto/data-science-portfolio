#!/bin/bash
# ===================================================================
# SCRIPT PRINCIPAL — Execution complete du projet Big Data
# ===================================================================
# Ce script orchestre toutes les etapes du projet.
# Executez-le depuis le repertoire racine du projet.
# ===================================================================

set -e
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "===================================================="
echo "   PROJET BIG DATA — Social Media Events Analysis"
echo "   Architecture HDFS + Spark + Kafka sur Docker"
echo "====================================================="
echo ""

# ===================================================================
# ETAPE 0 : Verification des prerequis
# ===================================================================
echo "=================================================="
echo "  ETAPE 0 : Verification des prerequis"
echo "=================================================="

if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker n'est pas installe." && exit 1
fi
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "[ERROR] Docker Compose n'est pas installe." && exit 1
fi

# Verifier que le CSV existe
mkdir -p data results
if [ ! -f "data/social_media_events.csv" ]; then
    echo "[WARNING] Placez votre fichier social_media_events.csv dans le dossier data/"
    echo "   Chemin attendu : ${PROJECT_DIR}/data/social_media_events.csv"
    exit 1
fi
echo "[OK] Prerequis OK (Docker + fichier CSV present)"
echo ""

# ===================================================================
# ETAPE 1 : Demarrage de l'infrastructure
# ===================================================================
echo "=================================================="
echo "  ETAPE 1 : Demarrage des conteneurs Docker"
echo "=================================================="

# Verifier si les conteneurs tournent deja
if docker compose ps | grep -q "spark-master"; then
    echo "[WARNING] Les conteneurs tournent deja. Utilisation de l'infrastructure existante."
else
    echo "[SEND] Lancement des services Docker..."
    docker compose up -d
    echo ""
    echo "[WAIT] Attente du demarrage des services (60 sec)..."
    for i in {1..6}; do
        echo "   [TIMER] $((i*10)) secondes..."
        sleep 10
    done
fi

echo ""
echo "[SEARCH] Etat des conteneurs :"
docker compose ps
echo ""

# ===================================================================
# ETAPE 2 : Chargement des donnees dans HDFS
# ===================================================================
echo "=================================================="
echo "  ETAPE 2 : Chargement dans HDFS"
echo "=================================================="

# Attendre que HDFS sorte du safe mode
echo "[WAIT] Attente de la sortie du safe mode HDFS..."
for attempt in {1..10}; do
    if docker exec namenode hdfs dfsadmin -safemode wait 2>/dev/null; then
        echo "[OK] HDFS pret"
        break
    fi
    echo "   Tentative $attempt/10..."
    sleep 5
done

# Creer les repertoires HDFS
echo "[FOLDER] Creation des repertoires HDFS..."
docker exec namenode hdfs dfs -mkdir -p /data/social_media
docker exec namenode hdfs dfs -mkdir -p /results/batch
docker exec namenode hdfs dfs -mkdir -p /results/stream

# Copier les donnees
echo "[SEND] Upload du CSV..."
docker cp data/social_media_events.csv namenode:/tmp/social_media_events.csv 2>/dev/null || true
docker exec namenode hdfs dfs -put -f /tmp/social_media_events.csv /data/social_media/

echo ""
echo "[FOLDER] Contenu de HDFS :"
docker exec namenode hdfs dfs -ls -h /data/social_media/
echo ""
echo "[OK] Donnees chargees dans HDFS"
echo ""

# ===================================================================
# ETAPE 3 : Execution des jobs BATCH
# ===================================================================
echo "=================================================="
echo "  ETAPE 3 : Jobs Spark BATCH"
echo "=================================================="

echo ""
echo "---------------------------------------------"
echo "  BATCH 1 : Engagement Utilisateur"
echo "---------------------------------------------"
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /spark_jobs/batch_engagement.py

echo ""
sleep 5
echo "---------------------------------------------"
echo "  BATCH 2 : Preferences par tranche d'age"
echo "---------------------------------------------"
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /spark_jobs/batch_preferences_age.py

echo ""
sleep 5
echo "---------------------------------------------"
echo "  BATCH 3 : Sentiment par pays/plateforme"
echo "---------------------------------------------"
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /spark_jobs/batch_sentiment.py

echo ""
echo "[OK] Tous les jobs batch sont termines !"
echo ""

# ===================================================================
# ETAPE 4 : Recuperation des resultats
# ===================================================================
echo "=================================================="
echo "  ETAPE 4 : Export des resultats"
echo "=================================================="

echo "[DOWNLOAD] Recuperation des resultats batch..."
docker exec namenode hdfs dfs -get /results/batch /tmp/batch_results 2>/dev/null || true
docker cp namenode:/tmp/batch_results ./results/ 2>/dev/null || true

echo "[OK] Resultats batch disponibles dans ./results/batch_results"
echo ""

# ===================================================================
# ETAPE 5 : Streaming (instructions manuelles)
# ===================================================================
echo "=================================================="
echo "  ETAPE 5 : Jobs Spark STREAMING"
echo "=================================================="
echo ""
echo "Pour lancer le streaming en temps reel :"
echo ""
echo "[MARKER] TERMINAL 1 — Lancer le producteur Kafka :"
echo "   docker exec -it spark-master pip install kafka-python --quiet"
echo "   docker exec -it spark-master python3 /spark_jobs/../kafka/kafka_producer.py"
echo ""
echo "[MARKER] TERMINAL 2+ — Lancer un job stream (ou plusieurs en parallele) :"
echo ""
echo "   [Option 1] Detection de pics d'activite :"
echo "   docker exec spark-master spark-submit \\"
echo "     --master spark://spark-master:7077 \\"
echo "     --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \\"
echo "     /spark_jobs/stream_activity_spikes.py"
echo ""
echo "   [Option 2] Surveillance du sentiment par topic :"
echo "   docker exec spark-master spark-submit \\"
echo "     --master spark://spark-master:7077 \\"
echo "     --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \\"
echo "     /spark_jobs/stream_sentiment.py"
echo ""
echo "   [Option 3] Analyse des sessions en temps reel :"
echo "   docker exec spark-master spark-submit \\"
echo "     --master spark://spark-master:7077 \\"
echo "     --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \\"
echo "     /spark_jobs/stream_sessions_analysis.py"
echo ""
echo "=================================================="
echo ""

# ===================================================================
# RESUME DES INTERFACES WEB
# ===================================================================
echo "===================================================="
echo "                  INTERFACES WEB"
echo "====================================================="
echo "║  🌐 HDFS NameNode  : http://localhost:9870             ║"
echo "║  🔴 HDFS DataNode 1: http://localhost:9864             ║"
echo "║  🔴 HDFS DataNode 2: http://localhost:9865             ║"
echo "║                                                          ║"
echo "║  ⚡ Spark Master   : http://localhost:8080              ║"
echo "║  ⚡ Spark Worker 1 : http://localhost:8081              ║"
echo "║  ⚡ Spark Worker 2 : http://localhost:8082              ║"
echo "║  📊 Application UI : http://localhost:4040 (pending)    ║"
echo "║                                                          ║"
echo "║  📨 Kafka          : localhost:9092                    ║"
echo "║  🔔 Zookeeper      : localhost:2181                    ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║                     COMMANDES UTILES                    ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  🛑 Arrêter tout   : docker compose down                ║"
echo "║  🗑️  Supprimer vol. : docker compose down -v             ║"
echo "║  📋 Voir les logs  : docker compose logs -f <service>  ║"
echo "║  📊 HDFS status    : docker exec namenode \\             ║"
echo "║                      hdfs dfsadmin -report              ║"
echo "║  📁 HDFS ls        : docker exec namenode \\             ║"
echo "║                      hdfs dfs -ls -R /data/            ║"
echo "║  🐚 REPL Spark     : docker exec -it spark-master \\     ║"
echo "║                      pyspark                            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "✨ PROJET PRÊT ! Les jobs batch sont terminés."
echo "   Vous pouvez maintenant lancer le streaming."
echo ""
