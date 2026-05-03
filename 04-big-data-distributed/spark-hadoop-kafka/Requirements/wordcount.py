from pyspark import SparkConf, SparkContext

# Étape 1 : Configuration de Spark
# Nous définissons le nom de l'application et configurons Spark.
conf = SparkConf().setAppName("WordCount")
sc = SparkContext(conf=conf)

# Étape 2 : Charger les données d'entrée
# Charger un fichier texte en tant que RDD.
# Le fichier est placé dans le répertoire partagé monté via Docker.
input_file = "/opt/spark-data/test.txt"
text_file = sc.textFile(input_file)  # RDD contenant les lignes du fichier texte.
print(f"Nombre de partitions : {text_file.getNumPartitions()}")

# Étape 3 : Transformation 1 - Découper les lignes en mots
# flatMap transforme chaque ligne de texte en une liste de mots.
# La fonction `line.split(" ")` divise chaque ligne par les espaces.
words = text_file.flatMap(lambda line: line.split(" "))

# Étape 4 : Transformation 2 - Mapper chaque mot à la valeur 1
# map transforme chaque mot en un tuple (mot, 1).
word_pairs = words.map(lambda word: (word, 1))

# Étape 5 : Transformation 3 - Réduire les paires par clé
# reduceByKey regroupe les mots identiques et additionne leurs valeurs (1 pour chaque occurrence).
word_counts = word_pairs.reduceByKey(lambda a, b: a + b)

# Étape 6 : Sauvegarder les résultats
# Sauvegarde les résultats dans un répertoire de sortie.
output_file = "/opt/spark-data/output"
word_counts.saveAsTextFile(output_file)

# Étape 7 : Afficher les résultats dans la console
# collect() ramène les données du cluster au driver sous forme de liste.
# Cette étape est utilisée pour afficher les résultats localement.
for word, count in word_counts.collect():
    print(f"{word}: {count}")

# Étape 8 : Arrêter la session Spark
# Toujours arrêter le contexte Spark après exécution.
sc.stop()
