from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# ─── Initialisation Spark ───
spark = SparkSession.builder \
    .appName("Batch_Job1_Engagement_Utilisateur") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("=" * 60)
print("  BATCH JOB 1 : Engagement Utilisateur")
print("=" * 60)

# ─── Lecture des données depuis HDFS ───
df = spark.read.csv(
    "hdfs://namenode:9000/data/social_media/social_media_events.csv",
    header=True,
    inferSchema=True
)

print(f"Nombre total d'événements : {df.count()}")
print(f"Nombre d'utilisateurs uniques : {df.select('user_id').distinct().count()}")

# ─── Calcul de l'engagement par utilisateur ───
engagement = df.groupBy("user_id").agg(
    F.count("*").alias("nb_actions"),
    F.sum("duration_sec").alias("temps_total_sec"),
    F.round(F.sum("duration_sec") / 3600, 2).alias("temps_total_heures"),
    F.countDistinct("session_id").alias("nb_sessions"),
    F.countDistinct("platform").alias("nb_plateformes"),
    F.avg("sentiment").alias("sentiment_moyen"),
    F.avg("duration_sec").alias("duree_moyenne_sec")
)

# ─── Score d'engagement composite ───
# Score = (nb_actions * 0.3) + (temps_total_heures * 0.4) + (nb_sessions * 0.3)
engagement = engagement.withColumn(
    "score_engagement",
    F.round(
        F.col("nb_actions") * 0.3 +
        F.col("temps_total_heures") * 0.4 +
        F.col("nb_sessions") * 0.3,
        2
    )
)

# ─── Plateforme préférée par utilisateur ───
platform_counts = df.groupBy("user_id", "platform") \
    .count() \
    .withColumn(
        "rank",
        F.row_number().over(
            Window.partitionBy("user_id").orderBy(F.desc("count"))
        )
    ).filter(F.col("rank") == 1) \
    .select("user_id", F.col("platform").alias("plateforme_preferee"))

engagement = engagement.join(platform_counts, "user_id", "left")

# ─── Classement ───
engagement = engagement.withColumn(
    "rang",
    F.row_number().over(Window.orderBy(F.desc("score_engagement")))
)

# ─── Resultats ───
print("\n[TROPHY] TOP 20 UTILISATEURS LES PLUS ENGAGES :")
print("-" * 60)
engagement.orderBy(F.desc("score_engagement")).show(20, truncate=False)

# ─── Statistiques globales ───
print("\n[STATS] STATISTIQUES GLOBALES D'ENGAGEMENT :")
print("-" * 60)
engagement.select(
    F.round(F.avg("nb_actions"), 1).alias("Moy. actions"),
    F.round(F.avg("temps_total_heures"), 2).alias("Moy. heures"),
    F.round(F.avg("nb_sessions"), 1).alias("Moy. sessions"),
    F.round(F.avg("score_engagement"), 2).alias("Moy. score"),
    F.max("score_engagement").alias("Score max"),
    F.min("score_engagement").alias("Score min")
).show(truncate=False)

# ─── Distribution par plateforme preferee ───
print("\n[PLATFORM] REPARTITION DES UTILISATEURS PAR PLATEFORME PREFEREE :")
engagement.groupBy("plateforme_preferee") \
    .agg(
        F.count("*").alias("nb_utilisateurs"),
        F.round(F.avg("score_engagement"), 2).alias("score_engagement_moyen")
    ).orderBy(F.desc("nb_utilisateurs")).show()

# ─── Sauvegarde dans HDFS ───
output_path = "hdfs://namenode:9000/results/batch/engagement_utilisateur"
engagement.coalesce(1).write.mode("overwrite").parquet(output_path)
print(f"\n[OK] Resultats sauvegardes dans : {output_path}")

# ─── Sauvegarde CSV locale (pour vérification) ───
engagement.orderBy(F.desc("score_engagement")) \
    .coalesce(1).write.mode("overwrite") \
    .option("header", True) \
    .csv("/data/results/engagement_utilisateur")
print("[OK] Copie CSV locale dans /data/results/engagement_utilisateur")

spark.stop()
print("\n[DONE] Job termine avec succes !")
