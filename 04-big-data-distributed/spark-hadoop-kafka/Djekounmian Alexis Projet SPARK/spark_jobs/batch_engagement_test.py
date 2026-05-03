from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("Batch_Job1_Test_Engagement") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("\n" + "="*60)
print("BATCH JOB 1 : Engagement Utilisateur - TEST MODE")
print("="*60)

try:
    # Read data from HDFS
    df = spark.read.csv(
        "hdfs://namenode:9000/data/social_media/social_media_events.csv",
        header=True,
        inferSchema=True
    )
    
    print(f"\n[OK] Donnees chargees: {df.count()} événements")
    print(f"[OK] Utilisateurs uniques: {df.select('user_id').distinct().count()}")
    
    # Calculate engagement
    engagement = df.groupBy("user_id").agg(
        F.count("*").alias("nb_actions"),
        F.round(F.avg("duration_sec"), 2).alias("duree_moyenne_sec"),
        F.countDistinct("session_id").alias("nb_sessions"),
        F.countDistinct("platform").alias("nb_plateformes")
    )
    
    # Add engagement score
    engagement = engagement.withColumn(
        "score_engagement",
        F.round(
            (F.col("nb_actions") * 0.3) +
            (F.col("nb_sessions") * 0.7),
            2
        )
    )
    
    # Show top 10
    print("\n[RESULTS] Top 10 Utilisateurs Engages:")
    print("-" * 60)
    engagement.orderBy(F.desc("score_engagement")).show(10, truncate=False)
    
    print("\n[SUCCESS] Job 1 termine avec succes!")
    
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    spark.stop()
