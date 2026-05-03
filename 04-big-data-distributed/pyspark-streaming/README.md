# PySpark — Cluster Spark dockerisé

Script de démarrage `start-spark.sh` pour un cluster Spark en conteneur (master / worker / submit), utilisé comme brique de base des projets Big Data plus complets (voir `04-big-data-distributed/spark-hadoop-kafka`).

## Usage

Le script lit la variable d'environnement `SPARK_WORKLOAD` :
- `master` → lance `org.apache.spark.deploy.master.Master`
- `worker` → lance `org.apache.spark.deploy.worker.Worker`
- `submit` → mode soumission

```bash
SPARK_WORKLOAD=master bash start-spark.sh
```
