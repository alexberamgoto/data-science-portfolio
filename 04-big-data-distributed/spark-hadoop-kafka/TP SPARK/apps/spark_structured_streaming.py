from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col, udf
from pyspark.sql.types import StringType
import string

# Fonction pour nettoyer les mots
def clean_word(word):
    # Supprimer la ponctuation et les espaces
    cleaned = word.strip(string.punctuation + " ")
    return cleaned if cleaned else None  # Retourner None pour les mots vides

# Convertir la fonction en UDF
clean_word_udf = udf(clean_word, StringType())

# Initialiser SparkSession
spark = SparkSession.builder.appName("StructuredStreamingExample").getOrCreate()

# Définir le niveau de log pour réduire la verbosité
spark.sparkContext.setLogLevel("WARN")

# Créer un DataFrame de streaming qui se connecte au générateur de données
lines = spark.readStream.format("socket").option("host", "data-generator").option("port", 9998).load()

# Traiter les données
words = lines.select(
    explode(split(col("value"), " ")).alias("word")  # Diviser les lignes en mots
)

# Nettoyer les mots (supprimer la ponctuation et les espaces)
cleaned_words = words.withColumn("word", clean_word_udf(col("word")))

# Filtrer les mots vides
filtered_words = cleaned_words.filter(col("word").isNotNull())

# Compter les occurrences de chaque mot
word_counts = filtered_words.groupBy("word").count()

# Afficher les résultats
query = word_counts.writeStream.format("console").outputMode("complete").start()

# Démarrer le streaming
query.awaitTermination()