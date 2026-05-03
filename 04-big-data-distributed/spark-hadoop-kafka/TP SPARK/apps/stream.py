from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col

# 1. Créer la session Spark (driver)
spark = SparkSession.builder \
    .appName("AnalyseLogsStreaming") \
    .getOrCreate()

# 2. Lire le flux de logs depuis un socket (simule logs qui arrivent)
lines = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# 3. Parser les logs Apache (extrait IP et code HTTP)
# Regex simple pour IP et code HTTP (ex: 192.168.1.1 - - [date] "GET / HTTP/1.1" 404)
log_df = lines.select(
    regexp_extract(col("value"), r'^(\S+)', 1).alias("ip"),  # IP
    regexp_extract(col("value"), r'" \d+ (\d{3}) ', 1).alias("status")  # Code HTTP
).filter(col("status").isin("404", "500", "503"))  # Seulement erreurs

# 4. Agrégation : compter erreurs par IP (fenêtre glissante 10s)
errors_by_ip = log_df.groupBy("ip").count()

# 5. Écrire le résultat en continu vers console
query = errors_by_ip.writeStream \
    .outputMode("complete") \
    .format("console") \
    .trigger(processingTime='10 seconds') \
    .start()

query.awaitTermination()  # La requête tourne jusqu'à Ctrl+C
