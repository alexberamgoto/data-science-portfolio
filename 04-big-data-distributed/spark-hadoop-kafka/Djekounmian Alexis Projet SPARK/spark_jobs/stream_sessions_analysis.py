from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType
)

# ─── Initialisation ───
spark = SparkSession.builder \
    .appName("Stream_Job3_Sessions_Analysis") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("=" * 70)
print("  STREAM JOB 3 : Analyse des sessions en temps réel")
print("=" * 70)

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

# ─── Parsing des événements ───
events = raw_stream \
    .selectExpr("CAST(value AS STRING) as json_str") \
    .select(F.from_json(F.col("json_str"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("event_time", F.to_timestamp("timestamp", "dd/MM/yyyy HH:mm"))

# ─── Analyse des sessions actives (fenêtre de 5 minutes) ───
sessions_analysis = events \
    .withWatermark("event_time", "5 minutes") \
    .groupBy(
        F.window("event_time", "5 minutes", "1 minute"),
        F.col("session_id")
    ).agg(
        F.first("user_id").alias("user_id"),
        F.first("platform").alias("platform"),
        F.first("device").alias("device"),
        F.count("*").alias("nb_actions"),
        F.sum("duration_sec").alias("total_duration"),
        F.round(F.avg("sentiment"), 2).alias("sentiment_moyen"),
        F.min("event_time").alias("session_start"),
        F.max("event_time").alias("session_end"),
        F.countDistinct("topic").alias("nb_topics"),
        F.countDistinct("action").alias("nb_action_types")
    ).select(
        F.col("window.start").alias("analyse_debut"),
        F.col("window.end").alias("analyse_fin"),
        "session_id",
        "user_id",
        "platform",
        "device",
        "nb_actions",
        "total_duration",
        "sentiment_moyen",
        "nb_topics",
        "nb_action_types",
        # Score simple d'engagement de session
        (F.col("nb_actions") * 0.5 + F.col("total_duration") / 60 * 0.5).alias("score_engagement")
    )

# ─── Agrégation pour vue globale ───
global_metrics = events \
    .withWatermark("event_time", "5 minutes") \
    .groupBy(
        F.window("event_time", "5 minutes", "1 minute")
    ).agg(
        F.countDistinct("session_id").alias("sessions_actives"),
        F.countDistinct("user_id").alias("users_actifs"),
        F.count("*").alias("total_events"),
        F.round(F.avg("duration_sec"), 2).alias("duree_moyenne_event"),
        F.round(F.avg("sentiment"), 3).alias("sentiment_global"),
        # Plateforme dominante
        F.first(
            F.col("platform").over(
                F.Window.partitionBy(F.window("event_time", "5 minutes", "1 minute"))
                    .orderBy(F.desc(F.count("*")))
            )
        ).alias("plateforme_dominante")
    ).select(
        F.col("window.start").alias("debut_analyse"),
        F.col("window.end").alias("fin_analyse"),
        "sessions_actives",
        "users_actifs",
        "total_events",
        "duree_moyenne_event",
        "sentiment_global",
        "plateforme_dominante"
    )

# ─── Top utilisateurs actifs (par fenêtre) ───
top_users = events \
    .withWatermark("event_time", "5 minutes") \
    .groupBy(
        F.window("event_time", "5 minutes", "1 minute"),
        "user_id"
    ).agg(
        F.count("*").alias("nb_events"),
        F.sum("duration_sec").alias("time_spent"),
        F.countDistinct("session_id").alias("nb_sessions")
    ).select(
        F.col("window.start").alias("debut"),
        F.col("window.end").alias("fin"),
        "user_id",
        "nb_events",
        "time_spent",
        "nb_sessions",
        F.rank().over(
            F.Window.partitionBy(F.col("window"))
                .orderBy(F.desc("nb_events"))
        ).alias("rang")
    ).filter(F.col("rang") <= 5)  # Top 5 users

# ─── Écriture des résultats ───
# Statistiques globales
query1 = global_metrics \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .trigger(processingTime="30 seconds") \
    .option("checkpointLocation", "/tmp/stream_global_metrics") \
    .start()

# Top utilisateurs
query2 = top_users \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 15) \
    .trigger(processingTime="30 seconds") \
    .option("checkpointLocation", "/tmp/stream_top_users") \
    .start()

# Analyse détaillée des sessions
query3 = sessions_analysis \
    .filter(F.col("score_engagement") > 5) \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 20) \
    .trigger(processingTime="30 seconds") \
    .option("checkpointLocation", "/tmp/stream_sessions") \
    .start()

print(" Streams actifs — surveillance des sessions en temps réel...")
print("   [1] Métriques globales")
print("   [2] Top 5 utilisateurs")
print("   [3] Détail des sessions engagées")
print("   (Ctrl+C pour arrêter)\n")

try:
    query1.awaitTermination()
except KeyboardInterrupt:
    print("Arrêt des streams...")
    query1.stop()
    query2.stop()
    query3.stop()
    spark.stop()
