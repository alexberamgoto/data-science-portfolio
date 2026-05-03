#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# SCRIPT PRINCIPAL — Exécution complète du projet Big Data
# ═══════════════════════════════════════════════════════════════
# Ce script orchestre toutes les étapes du projet.
# Exécutez-le depuis le répertoire racine du projet.
# ═══════════════════════════════════════════════════════════════

set -e
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   PROJET BIG DATA — Social Media Events Analysis        ║"
echo "║   Architecture HDFS + Spark + Kafka sur Docker          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════
# ÉTAPE 0 : Vérification des prérequis
# ═══════════════════════════════════════════════════════════
echo "══════════════════════════════════════════════════"
echo "  ÉTAPE 0 : Vérification des prérequis"
echo "══════════════════════════════════════════════════"

if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé." && exit 1
fi
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé." && exit 1
fi

# Vérifier que le CSV existe
mkdir -p data results
if [ ! -f "data/social_media_events.csv" ]; then
    echo "⚠️  Placez votre fichier social_media_events.csv dans le dossier data/"
    echo "   Chemin attendu : ${PROJECT_DIR}/data/social_media_events.csv"
    exit 1
fi
echo "✅ Prérequis OK"
echo ""

# ═══════════════════════════════════════════════════════════
# ÉTAPE 1 : Démarrage de l'infrastructure
# ═══════════════════════════════════════════════════════════
echo "══════════════════════════════════════════════════"
echo "  ÉTAPE 1 : Démarrage des conteneurs Docker"
echo "══════════════════════════════════════════════════"

docker compose up -d
echo ""
echo "⏳ Attente du démarrage des services (45 sec)..."
sleep 45

# Vérifier que tout tourne
echo ""
echo "🔍 État des conteneurs :"
docker compose ps
echo ""

# ═══════════════════════════════════════════════════════════
# ÉTAPE 2 : Chargement des données dans HDFS
# ═══════════════════════════════════════════════════════════
echo "══════════════════════════════════════════════════"
echo "  ÉTAPE 2 : Chargement dans HDFS"
echo "══════════════════════════════════════════════════"

# Attendre que HDFS sorte du safe mode
echo "⏳ Attente de la sortie du safe mode HDFS..."
docker exec namenode hdfs dfsadmin -safemode wait 2>/dev/null || sleep 10

docker exec namenode hdfs dfs -mkdir -p /data/social_media
docker exec namenode hdfs dfs -mkdir -p /results/batch
docker cp data/social_media_events.csv namenode:/tmp/social_media_events.csv
docker exec namenode hdfs dfs -put -f /tmp/social_media_events.csv /data/social_media/

echo ""
echo "📁 Contenu de HDFS :"
docker exec namenode hdfs dfs -ls /data/social_media/
echo ""
echo "✅ Données chargées dans HDFS"
echo ""

# ═══════════════════════════════════════════════════════════
# ÉTAPE 3 : Exécution des jobs BATCH
# ═══════════════════════════════════════════════════════════
echo "══════════════════════════════════════════════════"
echo "  ÉTAPE 3 : Jobs Spark BATCH"
echo "══════════════════════════════════════════════════"

echo ""
echo "─────────────────────────────────────────"
echo "  BATCH 1 : Engagement Utilisateur"
echo "─────────────────────────────────────────"
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /opt/spark-jobs/batch_engagement.py

echo ""
echo "─────────────────────────────────────────"
echo "  BATCH 2 : Préférences par tranche d'âge"
echo "─────────────────────────────────────────"
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /opt/spark-jobs/batch_preferences_age.py

echo ""
echo "─────────────────────────────────────────"
echo "  BATCH 3 : Sentiment par pays/plateforme"
echo "─────────────────────────────────────────"
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /opt/spark-jobs/batch_sentiment.py

echo ""
echo "✅ Tous les jobs batch sont terminés !"
echo ""

# ═══════════════════════════════════════════════════════════
# ÉTAPE 4 : Streaming (instructions manuelles)
# ═══════════════════════════════════════════════════════════
echo "══════════════════════════════════════════════════"
echo "  ÉTAPE 4 : Jobs Spark STREAMING"
echo "══════════════════════════════════════════════════"
echo ""
echo "Pour lancer le streaming, ouvrez 2 terminaux :"
echo ""
echo "📌 TERMINAL 1 — Lancer le producteur Kafka :"
echo "   docker exec -it spark-master pip install kafka-python"
echo "   docker exec -it spark-master python3 /opt/spark-jobs/../kafka/kafka_producer.py"
echo ""
echo "📌 TERMINAL 2 — Lancer un job stream (au choix) :"
echo ""
echo "   ▶ Détection de pics d'activité :"
echo "   docker exec spark-master spark-submit \\"
echo "     --master spark://spark-master:7077 \\"
echo "     --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \\"
echo "     /opt/spark-jobs/stream_activity_spikes.py"
echo ""
echo "   ▶ Surveillance du sentiment par topic :"
echo "   docker exec spark-master spark-submit \\"
echo "     --master spark://spark-master:7077 \\"
echo "     --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \\"
echo "     /opt/spark-jobs/stream_sentiment.py"
echo ""
echo "══════════════════════════════════════════════════"
echo ""

# ═══════════════════════════════════════════════════════════
# RÉSUMÉ DES INTERFACES WEB
# ═══════════════════════════════════════════════════════════
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  INTERFACES WEB                         ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  HDFS NameNode  : http://localhost:9870                 ║"
echo "║  Spark Master   : http://localhost:8080                 ║"
echo "║  Spark App UI   : http://localhost:4040 (pendant job)   ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║                     COMMANDES UTILES                    ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Arrêter tout   : docker compose down                  ║"
echo "║  Tout supprimer  : docker compose down -v              ║"
echo "║  Voir les logs  : docker compose logs -f spark-master  ║"
echo "║  HDFS status    : docker exec namenode hdfs dfsadmin -report ║"
echo "╚══════════════════════════════════════════════════════════╝"
