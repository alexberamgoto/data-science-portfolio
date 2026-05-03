#!/bin/bash
# ===================================================================
# Verification du statut complet du cluster
# ===================================================================

echo "===================================================="
echo "          STATUT COMPLET DU CLUSTER BIG DATA"
echo "====================================================="
echo ""

echo "===================================================="
echo "  [DOCKER] CONTAINERS DOCKER"
echo "===================================================="
docker compose ps
echo ""

echo "===================================================="
echo "  [WORLD] HDFS STATUS"
echo "===================================================="
docker exec namenode hdfs dfsadmin -report 2>/dev/null | head -20
echo ""

echo "===================================================="
echo "  [FOLDER] HDFS FILESYSTEM"
echo "===================================================="
echo "Contenu de /data :"
docker exec namenode hdfs dfs -ls -h /data 2>/dev/null || echo "Pas de donnees"
echo ""

echo "===================================================="
echo "  [POWER] SPARK STATUS"
echo "===================================================="

# Verifier le master
if docker exec spark-master curl -s http://localhost:8080 | grep -q "Spark Master"; then
    WORKERS=$(docker exec spark-master curl -s http://localhost:8080 | grep -c "Worker" || echo "0")
    echo "[OK] Spark Master : Actif avec $WORKERS workers"
else
    echo "[ERROR] Spark Master : Inactif"
fi
echo ""

echo "===================================================="
echo "  [MAIL] KAFKA STATUS"
echo "===================================================="

# Verifier Kafka avec telnet
if timeout 3 bash -c "echo > /dev/tcp/localhost/9092" 2>/dev/null; then
    echo "[OK] Kafka : Accessible sur localhost:9092"
    echo ""
    echo "Topics disponibles :"
    docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list 2>/dev/null || echo "  (aucun topic)"
else
    echo "[WARNING] Kafka : Non accessible"
fi
echo ""

echo "===================================================="
echo "  [CHART] INTERFACES WEB"
echo "===================================================="
echo "[READY] Aceedez a : "
echo "  [WORLD] HDFS NameNode   : http://localhost:9870"
echo "  [POWER] Spark Master    : http://localhost:8080"
echo "  [POWER] Spark Worker 1  : http://localhost:8081"
echo "  [POWER] Spark Worker 2  : http://localhost:8082"
echo ""
