#!/bin/bash
# ===================================================================
# Script : Charger les donnees dans HDFS
# Usage  : ./upload_to_hdfs.sh
# ===================================================================

echo "============================================"
echo "  Chargement des donnees dans HDFS"
echo "============================================"

# Attendre que le NameNode soit pret
echo "[1/4] Attente du NameNode..."
sleep 10
docker exec namenode hdfs dfsadmin -safemode wait

# Creer le repertoire HDFS
echo "[2/4] Creation du repertoire /data/social_media sur HDFS..."
docker exec namenode hdfs dfs -mkdir -p /data/social_media

# Copier le CSV dans le conteneur, puis dans HDFS
echo "[3/4] Upload du fichier CSV vers HDFS..."
docker cp ./data/social_media_events.csv namenode:/tmp/social_media_events.csv
docker exec namenode hdfs dfs -put -f /tmp/social_media_events.csv /data/social_media/

# Verifier
echo "[4/4] Verification..."
docker exec namenode hdfs dfs -ls /data/social_media/
echo ""
echo "[OK] Donnees chargees avec succes dans HDFS !"
echo "   Chemin : hdfs://namenode:9000/data/social_media/social_media_events.csv"
