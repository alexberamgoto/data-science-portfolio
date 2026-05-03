#!/bin/bash
# ═══════════════════════════════════════════════════════════
# Script : Charger les données dans HDFS
# Usage  : ./upload_to_hdfs.sh
# ═══════════════════════════════════════════════════════════

echo "============================================"
echo "  Chargement des données dans HDFS"
echo "============================================"

# Attendre que le NameNode soit prêt
echo "[1/4] Attente du NameNode..."
sleep 10
docker exec namenode hdfs dfsadmin -safemode wait

# Créer le répertoire HDFS
echo "[2/4] Création du répertoire /data/social_media sur HDFS..."
docker exec namenode hdfs dfs -mkdir -p /data/social_media

# Copier le CSV dans le conteneur, puis dans HDFS
echo "[3/4] Upload du fichier CSV vers HDFS..."
docker cp ./data/social_media_events.csv namenode:/tmp/social_media_events.csv
docker exec namenode hdfs dfs -put -f /tmp/social_media_events.csv /data/social_media/

# Vérifier
echo "[4/4] Vérification..."
docker exec namenode hdfs dfs -ls /data/social_media/
echo ""
echo "✅ Données chargées avec succès dans HDFS !"
echo "   Chemin : hdfs://namenode:9000/data/social_media/social_media_events.csv"
