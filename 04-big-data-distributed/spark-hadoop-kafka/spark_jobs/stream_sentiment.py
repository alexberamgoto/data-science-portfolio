"""
═══════════════════════════════════════════════════════════════
STREAM JOB 2 : Surveillance du sentiment en temps réel
                par thématique
═══════════════════════════════════════════════════════════════
Ce traitement observe l'évolution du sentiment associé aux
contenus au fil du temps, par thématique (topic).
Il permet de repérer rapidement une montée de réactions
négatives ou positives sur un sujet donné.

Lit depuis Kafka topic "social_media_events"
═══════════════════════════════════════════════════════════════
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType
)

spark = SparkSession.builder \
    .appName("Stream_Job2_Sentiment_Temps_Reel") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("=" * 60)
print("  STREAM JOB 2 : Sentiment en temps réel par topic")
print("=" * 60)

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

raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "social_media_events") \
    .option("startingOffsets", "latest") \
    .load()

events = raw_stream \
    .selectExpr("CAST(value AS STRING) as json_str") \
    .select(F.from_json(F.col("json_str"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("event_time", F.to_timestamp("timestamp", "dd/MM/yyyy HH:mm"))

# ─── Sentiment par topic sur fenêtre de 2 minutes ───
sentiment_by_topic = events \
    .withWatermark("event_time", "3 minutes") \
    .groupBy(
        F.window("event_time", "2 minutes", "1 minute"),
        "topic"
    ).agg(
        F.count("*").alias("nb_events"),
        F.round(F.avg("sentiment"), 3).alias("sentiment_moyen"),
        F.sum(F.when(F.col("sentiment") == 1, 1).otherwise(0)).alias("positifs"),
        F.sum(F.when(F.col("sentiment") == -1, 1).otherwise(0)).alias("negatifs"),
        F.sum(F.when(F.col("sentiment") == 0, 1).otherwise(0)).alias("neutres")
    ).select(
        F.col("window.start").alias("debut_fenetre"),
        F.col("window.end").alias("fin_fenetre"),
        "topic",
        "nb_events",
        "sentiment_moyen",
        "positifs",
        "negatifs",
        "neutres",
        # Alerte si le sentiment moyen descend sous -0.2
        F.when(F.col("sentiment_moyen") < -0.2, "🔴 ALERTE NÉGATIF")
         .when(F.col("sentiment_moyen") > 0.2, "🟢 TENDANCE POSITIVE")
         .otherwise("⚪ NEUTRE").alias("alerte")
    )

query = sentiment_by_topic \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 50) \
    .trigger(processingTime="10 seconds") \
    .start()

print("\n🔴 Stream actif — surveillance du sentiment par thématique...")
print("   Alertes : 🔴 si sentiment < -0.2 | 🟢 si > +0.2")
print("   (Ctrl+C pour arrêter)\n")

query.awaitTermination()
