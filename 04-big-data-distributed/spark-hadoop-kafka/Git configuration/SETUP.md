# Configuration de l'environnement

## Options d'installation

### Option 1 : Avec pip (recommandé)

```bash
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement
# Sur Windows :
.venv\Scripts\activate
# Sur Linux/Mac :
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Option 2 : Avec conda

```bash
# Créer l'environnement
conda env create -f environment.yml

# Activer l'environnement
conda activate spark-bigdata

# Ou mettre à jour si déjà existant
conda env update --file environment.yml --prune
```

### Option 3 : Installation directe (pip)

```bash
pip install pyspark==3.5.0 kafka-python==2.0.2 pandas==2.0.3 numpy==1.24.3
```

## Vérifier l'installation

```bash
# Tester PySpark
python -c "import pyspark; print(pyspark.__version__)"

# Tester Kafka
python -c "from kafka import KafkaProducer; print('Kafka OK')"

# Tester Pandas
python -c "import pandas; print(pandas.__version__)"
```

## Configuration Docker

Docker Compose prend en charge automatiquement :
- Kafka
- Zookeeper
- HDFS (NameNode + Secondary NameNode + 2 DataNodes)
- Spark (Master + 2 Workers)

## Démarrage du projet

```bash
# Exécuter le script principal
bash run_project.sh
```

## Variables d'environnement (.env)

Le fichier `.env` contient :
- Configuration Kafka
- Configuration HDFS
- Configuration Spark
- Chemins des données

Modifiez-le si vous avez des besoins spécifiques.

## Dépannage

### Problème : Module PySpark non trouvé
```bash
pip install --upgrade pyspark
```

### Problème : Kafka non accessible
Vérifiez que Docker Compose est en cours d'exécution :
```bash
docker-compose ps
```

### Problème : Erreur HDFS
```bash
# Vérifier la santé de HDFS
docker exec namenode hdfs dfsadmin -safemode get
```

## Structure des dépendances

```
spark-bigdata-project/
├── requirements.txt          # Dépendances pip
├── environment.yml          # Dépendances conda
├── setup.py                 # Installation setup
├── .env                     # Variables d'environnement
├── kafka/                   # Kafka producer
├── spark_jobs/              # Jobs Spark (batch + stream)
├── scripts/                 # Scripts utilitaires
└── data/                    # Données d'entrée
```

## Python minimum requis

- Python 3.9 ou supérieur
- Recommandé : Python 3.10 ou 3.11

## Versions des outils

- PySpark : 3.5.0
- Kafka-Python : 2.0.2
- Pandas : 2.0.3
- NumPy : 1.24.3
