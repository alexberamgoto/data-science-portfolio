"""
═══════════════════════════════════════════════════════════════
STREAM JOB 1 : Détection de pic d'activité en temps réel
═══════════════════════════════════════════════════════════════
Ce traitement surveille en continu le volume d'interactions
par fenêtre glissante de 1 minute pour détecter les pics
d'activité (buzz, événement viral).

Lit depuis Kafka topic "social_media_events"
Résultats affichés en console + sauvegardés
═══════════════════════════════════════════════════════════════
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, TimestampType
)

# ─── Initialisation ───
spark = SparkSession.builder \
    .appName("Stream_Job1_Detection_Pics") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("=" * 60)
print("  STREAM JOB 1 : Détection de pics d'activité")
print("=" * 60)

# ─── Schéma des événements ───
schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("timestamp", StringType()),
    StructField("platform", StringType()),
    StructField("action", StringType()),
    StructField("session_id", IntegerType()),
    StructField("device", StringType()),
    StructField("country", StringType()),
    StructField("age_group", StringType()),
    StructField("lifestyle", StringType()),
    StructField("topic", StringType()),
    StructField("duration_sec", IntegerType()),
    StructField("sentiment", IntegerType())
])

# ─── Lecture du stream Kafka ───
raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "social_media_events") \
    .option("startingOffsets", "latest") \
    .load()

# Parser le JSON
events = raw_stream \
    .selectExpr("CAST(value AS STRING) as json_str") \
    .select(F.from_json(F.col("json_str"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("event_time", F.to_timestamp("timestamp", "dd/MM/yyyy HH:mm"))

# ─── Agrégation par fenêtre glissante ───
# Fenêtre de 1 minute, glissement toutes les 30 secondes
activity_counts = events \
    .withWatermark("event_time", "2 minutes") \
    .groupBy(
        F.window("event_time", "1 minute", "30 seconds"),
        "platform"
    ).agg(
        F.count("*").alias("nb_events"),
        F.countDistinct("user_id").alias("nb_users"),
        F.avg("sentiment").alias("sentiment_moyen")
    ).select(
        F.col("window.start").alias("fenetre_debut"),
        F.col("window.end").alias("fenetre_fin"),
        "platform",
        "nb_events",
        "nb_users",
        F.round("sentiment_moyen", 3).alias("sentiment_moy")
    )

# ─── Écriture en console ───
query = activity_counts \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 50) \
    .trigger(processingTime="10 seconds") \
    .start()

print("\n🔴 Stream actif — surveillance des pics d'activité...")
print("   (Ctrl+C pour arrêter)\n")

query.awaitTermination()
