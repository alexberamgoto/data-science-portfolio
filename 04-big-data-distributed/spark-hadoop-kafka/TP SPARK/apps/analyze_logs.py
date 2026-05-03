from pyspark import SparkContext

# Initialiser le contexte Spark
sc = SparkContext(appName="AnalyseLogsApacheRDD")

# Charger les logs depuis HDFS
log_file = "hdfs://hdfs-namenode:9000/web_server.log"
logs_rdd = sc.textFile(log_file)

# Afficher les 10 premières lignes
print("Exemple de lignes du fichier de logs :")
for line in logs_rdd.take(10):
    print(line)
