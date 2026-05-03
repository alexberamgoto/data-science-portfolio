"""
═══════════════════════════════════════════════════════════════
BATCH JOB 2 : Préférences par tranche d'âge
═══════════════════════════════════════════════════════════════
Ce traitement met en évidence les plateformes et thématiques
les plus utilisées selon les groupes d'âge :
  - Plateforme préférée par tranche d'âge
  - Topic préféré par tranche d'âge
  - Device le plus utilisé
  - Durée moyenne et sentiment par tranche

Lecture depuis HDFS, résultats sauvegardés dans HDFS
═══════════════════════════════════════════════════════════════
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# ─── Initialisation Spark ───
spark = SparkSession.builder \
    .appName("Batch_Job2_Preferences_Age") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("=" * 60)
print("  BATCH JOB 2 : Préférences par tranche d'âge")
print("=" * 60)

# ─── Lecture des données ───
df = spark.read.csv(
    "hdfs://namenode:9000/data/social_media/social_media_events.csv",
    header=True,
    inferSchema=True
)

# ─── 1. Plateforme préférée par tranche d'âge ───
print("\n📱 PLATEFORME PRÉFÉRÉE PAR TRANCHE D'ÂGE :")
print("-" * 60)

platform_by_age = df.groupBy("age_group", "platform") \
    .agg(
        F.count("*").alias("nb_interactions"),
        F.round(F.avg("duration_sec"), 1).alias("duree_moy"),
        F.round(F.avg("sentiment"), 3).alias("sentiment_moy")
    )

w = Window.partitionBy("age_group").orderBy(F.desc("nb_interactions"))
top_platform = platform_by_age.withColumn("rank", F.row_number().over(w))

# Montrer toutes les combinaisons
platform_by_age.orderBy("age_group", F.desc("nb_interactions")).show(50, truncate=False)

print("\n🥇 PLATEFORME N°1 PAR TRANCHE :")
top_platform.filter(F.col("rank") == 1) \
    .select("age_group", "platform", "nb_interactions", "duree_moy") \
    .orderBy("age_group").show()

# ─── 2. Topic préféré par tranche d'âge ───
print("\n🎯 THÉMATIQUE PRÉFÉRÉE PAR TRANCHE D'ÂGE :")
print("-" * 60)

topic_by_age = df.groupBy("age_group", "topic") \
    .agg(
        F.count("*").alias("nb_interactions"),
        F.round(F.avg("sentiment"), 3).alias("sentiment_moy")
    )

w2 = Window.partitionBy("age_group").orderBy(F.desc("nb_interactions"))
top_topic = topic_by_age.withColumn("rank", F.row_number().over(w2))

topic_by_age.orderBy("age_group", F.desc("nb_interactions")).show(50, truncate=False)

print("\n🥇 TOPIC N°1 PAR TRANCHE :")
top_topic.filter(F.col("rank") == 1) \
    .select("age_group", "topic", "nb_interactions", "sentiment_moy") \
    .orderBy("age_group").show()

# ─── 3. Device par tranche d'âge ───
print("\n💻 APPAREIL PRÉFÉRÉ PAR TRANCHE D'ÂGE :")
print("-" * 60)

device_by_age = df.groupBy("age_group", "device") \
    .count().orderBy("age_group", F.desc("count"))
device_by_age.show(30)

# ─── 4. Profil synthétique par tranche ───
print("\n📊 PROFIL SYNTHÉTIQUE PAR TRANCHE D'ÂGE :")
print("-" * 60)

profile = df.groupBy("age_group").agg(
    F.count("*").alias("total_interactions"),
    F.countDistinct("user_id").alias("nb_utilisateurs"),
    F.round(F.avg("duration_sec"), 1).alias("duree_moyenne_sec"),
    F.round(F.sum("duration_sec") / 3600, 1).alias("temps_total_heures"),
    F.round(F.avg("sentiment"), 3).alias("sentiment_moyen"),
    F.countDistinct("topic").alias("diversite_topics")
).orderBy("age_group")

profile.show(truncate=False)

# ─── 5. Matrice croisée : action × tranche d'âge ───
print("\n🔄 RÉPARTITION DES ACTIONS PAR TRANCHE D'ÂGE :")
print("-" * 60)

action_matrix = df.groupBy("age_group") \
    .pivot("action") \
    .count() \
    .orderBy("age_group")
action_matrix.show(truncate=False)

# ─── Sauvegarde ───
output_path = "hdfs://namenode:9000/results/batch/preferences_age"
profile.coalesce(1).write.mode("overwrite").parquet(output_path)

platform_by_age.coalesce(1).write.mode("overwrite") \
    .option("header", True) \
    .csv("/data/results/preferences_age_platform")

topic_by_age.coalesce(1).write.mode("overwrite") \
    .option("header", True) \
    .csv("/data/results/preferences_age_topic")

print(f"\n✅ Résultats sauvegardés dans HDFS : {output_path}")
print("✅ Copies CSV locales dans /data/results/")

spark.stop()
print("\n🏁 Job terminé avec succès !")
