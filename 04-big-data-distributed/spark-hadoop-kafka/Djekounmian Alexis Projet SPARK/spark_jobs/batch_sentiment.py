from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("Batch_Job3_Sentiment_Pays_Plateforme") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("=" * 60)
print("  BATCH JOB 3 : Sentiment par pays et plateforme")
print("=" * 60)

df = spark.read.csv(
    "hdfs://namenode:9000/data/social_media/social_media_events.csv",
    header=True,
    inferSchema=True
)

# ─── 1. Sentiment moyen par pays ───
print("\n[WORLD] SENTIMENT MOYEN PAR PAYS :")
print("-" * 60)

sentiment_pays = df.groupBy("country").agg(
    F.count("*").alias("nb_interactions"),
    F.round(F.avg("sentiment"), 4).alias("sentiment_moyen"),
    F.sum(F.when(F.col("sentiment") == 1, 1).otherwise(0)).alias("positifs"),
    F.sum(F.when(F.col("sentiment") == 0, 1).otherwise(0)).alias("neutres"),
    F.sum(F.when(F.col("sentiment") == -1, 1).otherwise(0)).alias("negatifs")
)

# Calculer le ratio de positivité
sentiment_pays = sentiment_pays.withColumn(
    "ratio_positivite",
    F.round(F.col("positifs") / F.col("nb_interactions") * 100, 2)
).withColumn(
    "ratio_negativite",
    F.round(F.col("negatifs") / F.col("nb_interactions") * 100, 2)
)

sentiment_pays.orderBy(F.desc("sentiment_moyen")).show(30, truncate=False)

# ─── 2. Sentiment moyen par plateforme ───
print("\n[PLATFORM] SENTIMENT MOYEN PAR PLATEFORME :")
print("-" * 60)

sentiment_platform = df.groupBy("platform").agg(
    F.count("*").alias("nb_interactions"),
    F.round(F.avg("sentiment"), 4).alias("sentiment_moyen"),
    F.round(F.avg("duration_sec"), 1).alias("duree_moyenne"),
    F.sum(F.when(F.col("sentiment") == 1, 1).otherwise(0)).alias("positifs"),
    F.sum(F.when(F.col("sentiment") == -1, 1).otherwise(0)).alias("negatifs")
).withColumn(
    "ratio_positivite_pct",
    F.round(F.col("positifs") / F.col("nb_interactions") * 100, 2)
)

sentiment_platform.orderBy(F.desc("sentiment_moyen")).show(truncate=False)

# ─── 3. Matrice croisee pays x plateforme ───
print("\n[MATRIX] MATRICE SENTIMENT : PAYS x PLATEFORME :")
print("-" * 60)

matrice = df.groupBy("country") \
    .pivot("platform") \
    .agg(F.round(F.avg("sentiment"), 3)) \
    .orderBy("country")
matrice.show(30, truncate=False)

# ─── 4. Sentiment par thematique ───
print("\n[TARGET] SENTIMENT MOYEN PAR THEMATIQUE :")
print("-" * 60)

sentiment_topic = df.groupBy("topic").agg(
    F.count("*").alias("nb_interactions"),
    F.round(F.avg("sentiment"), 4).alias("sentiment_moyen")
).orderBy(F.desc("sentiment_moyen"))
sentiment_topic.show(truncate=False)

# ─── 5. Combinaison pays x topic : les plus negatifs ───
print("\n[WARNING] TOP 10 COMBINAISONS PAYS x TOPIC LES PLUS NEGATIVES :")
print("-" * 60)

df.groupBy("country", "topic").agg(
    F.count("*").alias("nb"),
    F.round(F.avg("sentiment"), 4).alias("sentiment")
).filter(F.col("nb") > 50) \
 .orderBy("sentiment") \
 .show(10, truncate=False)

# ─── Sauvegarde ───
output_path = "hdfs://namenode:9000/results/batch/sentiment_pays_plateforme"
sentiment_pays.coalesce(1).write.mode("overwrite").parquet(output_path)

matrice.coalesce(1).write.mode("overwrite") \
    .option("header", True) \
    .csv("/data/results/sentiment_matrice")

print(f"\n[OK] Resultats sauvegardes dans HDFS : {output_path}")

spark.stop()
print("\n[DONE] Job termine avec succes !")
