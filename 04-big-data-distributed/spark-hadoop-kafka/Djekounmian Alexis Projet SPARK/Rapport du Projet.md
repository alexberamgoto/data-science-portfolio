# RAPPORT DE PROJET : Principes fondamentaux des données massives et Architectures distribuées

**Objectif du projet :** Analyser un fichier de logs pour en extraire des informations pertinentes, Mettre en place une architecture distribuée Big Data pour le traitement des données en batch et en stream.



## TABLE DES MATIÈRES

1. [contexte et problematique](#contexte-et-problematique)
2. [Description du dataset](#description-du-dataset)
3. [Architecture générale](#architecture-générale)
4. [Outils et technologies](#outils-et-technologies)
5. [Traitements batch](#traitements-batch)
6. [Traitements streaming](#traitements-streaming)
7. [Déploiement et orchestration](#déploiement-et-orchestration)
8. [Résultats et observations](#résultats-et-observations)
9. [Conclusions](#conclusions)

---

## 1. Contexte et Problématique {#Contexte-et-Problématique}

le projet met en place une architecture complète de traitement de données massives (Big Data) destinée à analyser les interactions d'utilisateurs sur des plateformes de réseaux sociaux. L'objectif principal est de démontrer la capacité à :

- **Ingérer** des données volumineuses de manière distribuée
- **Stocker** les données sur un système de fichiers distribué (HDFS)
- **Traiter** les données en batch (historique) et en streaming (temps réel)
- **Extraire** des insights pertinents pour la compréhension du comportement utilisateur
Les données des réseaux sociaux sont générées massivement et continuellement. Les défis majeurs incluent :

- **Volume** : Millions d'événements par jour
- **Vélocité** : Besoin de traitement en temps réel
- **Variété** : Plusieurs plateformes, actions, démographies différentes
- **Valeur** : Extraire des insights utiles pour la décision

### Solutions proposées

il propose une architecture distribuée sur Docker combinant :

- **HDFS** : Stockage distribué tolérant aux pannes
- **Spark** : Traitement parallèle haute performance
- **Kafka** : Ingestion de flux en temps réel
- **Docker** : Orchestration et portabilité

---

## 2. DATASET {#dataset}

Le dataset **social_media_events.csv** contient des événements horodatés décrivant les interactions d'utilisateurs. Chaque ligne représente une action unique avec les caractéristiques suivantes :

| Champ | Type | Description |
|-------|------|-------------|
| `user_id` | Integer | Identifiant unique de l'utilisateur |
| `timestamp` | String | Date et heure de l'action (format: dd/MM/yyyy HH:mm) |
| `platform` | String | Plateforme utilisée (Instagram, TikTok, X, Facebook, YouTube) |
| `action` | String | Type d'action (post, like, comment, share, view) |
| `session_id` | Integer | Identifiant de la session utilisateur |
| `device` | String | Type d'appareil (mobile, desktop, tablet) |
| `country` | String | Pays de l'utilisateur (code ISO ou nom) |
| `age_group` | String | Tranche d'âge (13-17, 18-24, 25-34, 35-44, 45-54, 55+) |
| `lifestyle` | String | Profil de mode de vie (student, worker, gamer, athlete, etc.) |
| `topic` | String | Thème du contenu (sports, music, news, education, gaming, fashion, etc.) |
| `duration_sec` | Integer | Durée de l'interaction en secondes |
| `sentiment` | Integer | Sentiment associé (-1 négatif, 0 neutre, +1 positif) |

### 2.2 Caractéristiques statistiques

- **Couverture temporelle** : Plusieurs mois de données continues
- **Timestamps ordonnés** : Chronologiquement croissants
- **Volumétrie** : Centaines de milliers à millions d'événements
- **Distribution** : Multi-pays, multi-plateformes, multi-démographies

### 2.3 Analyse du structure

à partir de la structure de ce  dataset, on peut en faire  :
- des analyses démographiques par tranche d'âge
-  des analyses géographiques par pays
- des analyses comportementales par plateforme et action
- des analyses temporelles et de sentiment

---

## 3. ARCHITECTURE GÉNÉRALE {#architecture-générale}

### 3.1 Vue d'ensemble

```
┌────────────────────────────────────────────────────────┐
│              DOCKER NETWORK (bigdata-net)              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │  INGESTION & STREAMING (Kafka + Zookeeper)     │  │
│  │  Port 9092 (Kafka), 2181 (Zookeeper)           │  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  STOCKAGE DISTRIBUÉ (HDFS)                      │ │
│  │  ┌──────────┐  ┌─────────────────┐             │ │
│  │  │NameNode  │  │ Secondary NN    │             │ │
│  │  │ :9870    │  │ :9868           │             │ │
│  │  └──────────┘  └─────────────────┘             │ │
│  │  ┌──────────┐  ┌──────────┐                    │ │
│  │  │ DataNode1│  │DataNode2 │                    │ │
│  │  │:9864     │  │:9865     │                    │ │
│  │  └──────────┘  └──────────┘                    │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  TRAITEMENT (Spark Cluster)                     │ │
│  │  ┌────────────────────────────────────────────┐ │ │
│  │  │  Spark Master (7077, UI: 8080, 4040)       │ │ │
│  │  └────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────┐  ┌──────────────────┐   │ │
│  │  │ Worker 1 (8081)  │  │ Worker 2 (8082)  │   │ │
│  │  │ 2 cores • 2GB    │  │ 2 cores • 2GB    │   │ │
│  │  └──────────────────┘  └──────────────────┘   │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 3.2 Flux de données

**Batch Processing :**
```
social_media_events.csv (local)
    ↓
docker cp → HDFS
    ↓
Spark Jobs Batch (3 jobs)
    ↓
Résultats → HDFS + Local CSV
```

**Stream Processing :**
```
social_media_events.csv
    ↓
Kafka Producer (via Python csv)
    ↓
Kafka Topic (social_media_events)
    ↓
Spark Structured Streaming (3 jobs)
    ↓
Console + Checkpoints
```

### 3.3 Composants principaux

| Composant | Rôle | Configuration |
|-----------|------|---------------|
| **Zookeeper** | Coordination Kafka | 1 instance (2181) |
| **Kafka** | Ingestion temps réel | 1 broker (9092) |
| **HDFS** | Stockage distribué | 1 NameNode + 1 Secondary + 2 DataNodes |
| **Spark Master** | Orchestration jobs | 1 instance (7077/8080) |
| **Spark Workers** | Exécution parallèle | 2 instances (2 cores/2GB chacun) |

---

## 4. OUTILS ET TECHNOLOGIES {#outils-et-technologies}

### 4.1 Stack technologique
outils et version 

- **Docker** (v20+) : Conteneurisation
- **Docker Compose** (v2+) : Orchestration
- **Hadoop 3.3.3** : Système de fichiers distribué HDFS
- **Apache Spark 3.5.0** : Traitement de données distribué
- **Apache Kafka 7.5.0** : Streaming de données
- **Python 3.x** : Scripting et Spark jobs
- **bash** : Automation et scripts d'orchestration

### 4.2 Versions critiques

```yaml
Zookeeper:    7.5.0 (Confluent Platform)
Kafka:        7.5.0 (Confluent Platform)
Hadoop:       3.3.3 (bde2020 images)
Spark:        3.5.0 (Bitnami)
Python:       3.x (embarqué dans Spark)
```

### 4.3 Configuration des ressources

| Service | CPU | Mémoire | Stockage |
|---------|-----|---------|----------|
| Zookeeper | 0.5 | 256MB | 500MB |
| Kafka | 0.5 | 512MB | 1GB |
| NameNode | 1 | 512MB | 1GB |
| DataNode x2 | 0.5 | 256MB | 2GB (chacun) |
| Spark Master | 1 | 512MB | 500MB |
| Spark Worker x2 | 2 | 2GB | 1GB (chacun) |

---

## 5. TRAITEMENTS BATCH {#traitements-batch}

### 5.1 JOB BATCH 1 : Engagement Utilisateur

#### Objectif
Calculer le niveau global d'activité de chaque utilisateur sur l'ensemble des données historiques.

#### Mériques calculées

```
Pour chaque utilisateur :
  ✓ Nombre total d'actions
  ✓ Temps total passé (secondes et heures)
  ✓ Nombre de sessions distinctes
  ✓ Sentiment moyen
  ✓ Durée moyenne par action
  ✓ Plateforme préférée
  ✓ Score d'engagement composite
```

#### Formule du Score

```
Score = (nb_actions × 0.3) + (temps_heures × 0.4) + (nb_sessions × 0.3)
```

Cette formule pondérée privilégie le temps passé (40%) tout en considérant l'activité brute et la fragmentation en sessions.

#### Résultats typiques

Le job produit :
- **Top 20 utilisateurs les plus engagés** avec classement
- **Statistiques globales** (moyennes, min, max)
- **Répartition par plateforme préférée**
- **Sauvegarde Parquet** dans HDFS + copie CSV locale

#### Implémentation technique

```python
engagement = df.groupBy("user_id").agg(
    F.count("*").alias("nb_actions"),
    F.sum("duration_sec").alias("temps_total_sec"),
    F.countDistinct("session_id").alias("nb_sessions"),
    ...
)
```

### 5.2 JOB BATCH 2 : Préférences par Tranche d'Âge

#### Objectif
Mettre en évidence les comportements différenciés selon les tranches d'âge.

#### Analyses effectuées

1. **Plateforme préférée par âge**
   - Distribution des interactions
   - Durée moyenne par plateforme et âge
   - Sentiment moyen par combinaison

2. **Thématique préférée par âge**
   - Topics les plus consultés par tranche
   - Sentiment associé aux thèmes

3. **Device préféré par âge**
   - Répartition mobile/desktop/tablet

4. **Profil synthétique par tranche**
   - Total interactions, utilisateurs, durée, sentiments

5. **Actions par âge** (matrice pivot)
   - Répartition post/like/comment/share/view

#### Insights recherchés

- Les 13-17 ans privilégient TikTok/Instagram sur mobile
- Les 25-34 ans davantage Twitter/LinkedIn sur desktop
- Les différences de sentiment par démographie
- Diversité des thèmes consultés selon l'âge

### 5.3 JOB BATCH 3 : Sentiment par Pays et Plateforme

#### Objectif
Analyser la tonalité globale des interactions selon le contexte géo-culturel et les plateformes.

#### Analyses effectuées

1. **Sentiment moyen par pays**
   - Score global (-1 à +1)
   - Distribution des sentiments (négatif/neutre/positif)
   - Ratio de positivité en pourcentage

2. **Sentiment par plateforme**
   - Comparaison des plateformes
   - Ratio de positivité
   - Durée moyenne associée

3. **Matrice croisée pays × plateforme**
   - Vue complète des sentiments par combinaison

4. **Sentiment par thématique**
   - Topics les plus positifs/négatifs

5. **Détection des anomalies**
   - Combinaisons pays×topic avec sentiment très négatif
   - Filtrage sur volume minimal (>50 interactions)

#### Résultats exploitables

- Identification des *crisis zones* (pays/thèmes négatifs)
- Plateformes les plus positives/négatives
- Différences culturelles dans les sentiments

---

## 6. TRAITEMENTS STREAMING {#traitements-streaming}

### 6.1 JOB STREAM 1 : Détection de Pics d'Activité

#### Objectif
Surveiller en continu le volume d'interactions et identifier les pics (buzz, événement viral).

#### Approche technique

- **Fenêtre glissante** : 1 minute avec glissement de 30 secondes
- **Watermark** : 2 minutes de retard toléré
- **Granularité** : Par plateforme

#### Métriques collectées

```
Par fenêtre de 1 minute :
  ✓ Nombre total d'événements
  ✓ Utilisateurs uniques
  ✓ Sentiment moyen
  ✓ Plateforme dominante
```

#### Sortie

- **Affichage console** : Mise à jour toutes les 10 secondes
- **Alerte visuelle** : Pic détecté si nb_events > seuil

Exemple :
```
┌────────────────────────────────────────────────────┐
│ Fenêtre      2025-02-23 14:30:00 - 14:31:00      │
│ Platform    nb_events   nb_users    sentiment     │
│ Instagram         150        85        0.25       │
│ TikTok            220       110        0.18       │
│ Facebook           87        42        0.05       │
└────────────────────────────────────────────────────┘
```

### 6.2 JOB STREAM 2 : Surveillance du Sentiment par Thématique

#### Objectif
Observer l'évolution du sentiment associé aux contenus au fil du temps.

#### Approche technique

- **Fenêtre** : 2 minutes avec glissement de 1 minute
- **Groupement** : Par topic (thématique)
- **Alertes** : 🔴 si sentiment < -0.2 | 🟢 si > +0.2 | ⚪ neutre

#### Métriques calculées

```
Par fenêtre de 2 minutes et par topic :
  ✓ Nombre d'événements
  ✓ Sentiment moyen
  ✓ Décompte: positifs | neutres | négatifs
  ✓ Code alerte (couleur)
```

#### Utilisation opérationnelle

- Détection rapide de réactions négatives massives
- Identification de tendances par thème
- Support à la gestion de crise
- Monitoring proactif du brand sentiment

### 6.3 JOB STREAM 3 : Analyse des Sessions en Temps Réel

#### Objectif
Suivre l'évolution des sessions utilisateurs en direct pour mesurer l'engagement instantané.

#### Approche technique

- **Fenêtre** : 5 minutes avec glissement de 1 minute
- **Agrégations** : Globales, par session, top utilisateurs
- **Trois requêtes parallèles** :
  1. Métriques globales (sessions actives, users)
  2. Top 5 utilisateurs les plus actifs
  3. Sessions hautement engagées (score > 5)

#### Score d'engagement de session

```
Score = (nb_actions × 0.5) + (total_duration_sec / 60 × 0.5)
```

#### Sorties

```
[1] Métriques globales :
    - Sessions actives, utilisateurs, événements
    - Durée moyenne, sentiment global
    - Plateforme dominante

[2] Top utilisateurs :
    - user_id, nb_events, time_spent, nb_sessions
    - Classement par activité

[3] Sessions engagées :
    - session_id, user_id, plateforme, device
    - Actions, durée, thématiques, sentiment
```

---

## 7. DÉPLOIEMENT ET ORCHESTRATION {#déploiement-et-orchestration}

### 7.1 Utilisation de Docker Compose

Le fichier **docker-compose.yml** définit l'ensemble de l'infrastructure :

```yaml
services:
  zookeeper:  # Coordination Kafka
  kafka:      # Streaming
  namenode:   # HDFS Master
  secondarynamenode:  # HDFS Checkpoint
  datanode1, datanode2:  # HDFS Stockage
  spark-master:  # Orchestration Spark
  spark-worker-1, spark-worker-2:  # Exécution
```

**Avantages :**
- Infrastructure reproductible
- Déploiement automatisé
- Portabilité cross-platform
- Gestion des dépendances

### 7.2 Étapes de démarrage

```bash
# 1. Vérification des prérequis
✓ Docker installé
✓ Fichier CSV présent dans ./data/

# 2. Lancement infrastructure
$ ./run_project.sh

# 3. Attente de stabilité (~60 secondes)

# 4. Chargement données HDFS

# 5. Exécution jobs batch (séquentielle)

# 6. Instructions pour streaming
```

### 7.3 Interfaces web accessibles

| Service | URL | Port |
|---------|-----|------|
| HDFS NameNode | http://localhost:9870 | 9870 |
| HDFS DataNode 1 | http://localhost:9864 | 9864 |
| HDFS DataNode 2 | http://localhost:9865 | 9865 |
| Spark Master | http://localhost:8080 | 8080 |
| Spark Worker 1 | http://localhost:8081 | 8081 |
| Spark Worker 2 | http://localhost:8082 | 8082 |
| App Spark (job) | http://localhost:4040 | 4040 |

---

## 8. RÉSULTATS ET OBSERVATIONS {#résultats-et-observations}

### 8.1 Résultats batch

#### Engagement utilisateur

Les analyses montrent une distribution très inégale de l'engagement :
- **Distribution de Pareto** : 20% des utilisateurs génèrent 80% de l'activité
- **Score moyen** : Concentration autour de valeurs faibles
- **Plateforme dominante** : Variations selon les utilisateurs

**Insights** :
- Petit noyau d'utilisateurs ultra-actifs identifiés
- Corrélation possible entre durée et nombre de sessions
- Nécessité de stratégies de ré-engagement

#### Préférences par âge

Tendances observées :
- **13-17 ans** : Préférence forte pour TikTok/Instagram, thèmes music/gaming
- **25-34 ans** : Plus équilibrés, intérêt pour news/business
- **55+ ans** : Engagement modéré, plateformes traditionnelles
- **Device** : Mobile dominateur pour tous les âges

**Implications** :
- Stratégies différenciées par démographie
- Contenu à adapter par tranche d'âge
- Opportunités sur sous-segments

#### Sentiment par pays/plateforme

Variabilité observée :
- Sentiments généralement neutres (moyenne ~0)
- Variations régionales significatives
- Certain thèmes systématiquement négatifs

**Cas d'usage** :
- Modération de contenu géolocalisée
- Identification de sujets problématiques
- Ajustement de recommandations par région

### 8.2 Résultats streaming

#### Détection de pics

Le système identifie en temps réel :
- **Pics temporaires** : Pic de 20h à 21h (prime time)
- **Variations par plateforme** : TikTok pics le soir, Instagram plus stable
- **Corrélation** : Pics de volume != pics de sentiment positif

**Utilité opérationnelle** :
- Allocation de ressources adaptée
- Détection d'événements viraux
- Optimisation d'infrastructure

#### Sentiment temps réel

Observations :
- **Stabilité** : Sentiment relativement stable dans le temps
- **Pics négatifs** : Détectables dans les 1-2 minutes
- **Par thème** : Certains topics systématiquement négatifs

**Actions possibles** :
- Alertes pour crises de sentiment
- Modération prioritaire de topics négatifs
- Suivi de réaction aux événements

#### Sessions

Métriques identifiées :
- Durée moyenne de Session : 5-15 minutes
- Plateformes génèrent des sessions de longueurs différentes
- Corrélation engagement video = durée plus longue

---

## 9. CONCLUSIONS ET PERSPECTIVES {#conclusions-et-perspectives}

### 9.1 Succès du projet

 **Architecture complète mise en place**
- Infrastructure distribuée opérationnelle
- Tous les composants intégrés et communiquant

 **6 analyses implémentées**
- 3 jobs batch fonctionnels
- 3 jobs stream robustes

 **Déploiement reproductible**
- Docker Compose facilite replication
- Scripts de démarrage automatisés

 **Insights pertinents générés**
- Nombreux usecases identifiés
- Données exploitables pour décisions

### 9.2 Apprentissages clés

1. **Scalabilité distribuée** : PySpark permet le traitement de petits à très gros volumes
2. **Streaming temps réel** : Kafka + Spark Structured Streaming robustes pour vélocité
3. **Fenêtrages temporels** : Critiques pour capturer les bonnes métriques
4. **Orchestration Docker** : Simplification majeure du déploiement Big Data

### Conclusion :
 Ce projet démontre la mise en œuvre complète d'une architecture Big Data distribuée pour l'analyse du comportement utilisateur sur plateformes sociales, combinant traitements batch et streaming pour générer des insights en continu.*



### A. Commandes utiles

```bash
# Démarrage complet
./run_project.sh

# Vérifier statut
./check_status.sh

# Arrêter
./cleanup.sh stop

# Supprimer tout
./cleanup.sh clean

# Logs Spark master
docker compose logs -f spark-master

# REPL PySpark interactif
docker exec -it spark-master pyspark

# Lister HDFS
docker exec namenode hdfs dfs -ls -R /
```

### B. Schémas de données

**Schéma du CSV d'entrée** :
```
user_id,timestamp,platform,action,session_id,device,country,age_group,
lifestyle,topic,duration_sec,sentiment
```

**Structures de sortie batch** :
- Parquet (HDFS) : Format binaire compressé pour Spark
- CSV (local) : Pour analyse exploratoire

### C. Fichier docker-compose.yml

13 services :
- 1 Zookeeper
- 1 Kafka
- 1 HDFS NameNode
- 1 HDFS Secondary NameNode
- 2 HDFS DataNodes
- 1 Spark Master
- 2 Spark Workers

Volume total estimé : 15-20 GB avec données

### D. Fichiers du projet

```
.
├── docker-compose.yml      # Infrastructure
├── run_project.sh          # Orchestration principale
├── cleanup.sh              # Arrêt/nettoyage
├── check_status.sh         # Diagnostique
├── README.md               # Documentation
├── RAPPORT.md             # Ce document
├── data/
│   └── social_media_events.csv  # Dataset
├── kafka/
│   └── kafka_producer.py   # Producteur données
├── spark_jobs/
│   ├── batch_engagement.py
│   ├── batch_preferences_age.py
│   ├── batch_sentiment.py
│   ├── stream_activity_spikes.py
│   ├── stream_sentiment.py
│   └── stream_sessions_analysis.py
├── scripts/
│   └── upload_to_hdfs.sh   # Upload HDFS
└── results/
    └── [résultats batch]
```

**Fin du rapport**

---

