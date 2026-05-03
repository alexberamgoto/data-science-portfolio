# Rapport  du Projet  Architectures Distribuées

ce rapport présente l’intégralité du pipeline , de l’architecture aux résultats analytiques.

## 1. Introduction
Les réseaux sociaux génèrent un flux massif et continu de données. Le présent projet vise à mettre en place une architecture Big Data distribuée reposant sur Hadoop HDFS, Spark et Kafka, capable de traiter à la fois des données historiques (batch) et des données en temps réel (streaming). Cette infrastructure conteneurisée via Docker garantit scalabilité, résilience et reproductibilité.

## 2. Description du Dataset
Le fichier `social_media_events.csv` contient 50 événements de test dans les versions exécutées, mais a été conçu pour représenter des millions d’interactions potentielles. Les colonnes incluent : event_id, user_id, platform, event_type, likes, comments, shares, sentiment, country, age_group, timestamp. Ces données permettent des analyses comportementales, démographiques et émotionnelles.

## 3. Architecture du Système
L’architecture repose sur :
- **HDFS** : stockage distribué (1 NameNode, 2 DataNodes).
- **Spark** : traitement distribué (1 Master, 2 Workers).
- **Kafka + Zookeeper** : ingestion et diffusion en temps réel.
- **Docker Compose** : orchestration complète.
Les interfaces Web confirment la stabilité de l’infrastructure (HDFS UI 9870, Spark Master 8080, Workers 8081–8082, Spark UI 4040).

## 4. Outils et Technologies
Les technologies mobilisées sont : Docker, Hadoop 3.2.1, Spark 3.4.0, Kafka 7.5.0, Python, Bash. Cette combinaison permet un pipeline cohérent de l’ingestion à l’analyse.

## 5. Traitements Batch
### 5.1 Engagement Utilisateur
Basé sur un score composite (actions 30%, durée 40%, sessions 30%), ce job identifie les 20 utilisateurs les plus engagés.

### 5.2 Préférences par Tranche d’Âge
Analyse des plateformes préférées par groupe d’âge, révélant des comportements générationnels distincts.

### 5.3 Analyse de Sentiment
Calcule le sentiment moyen par pays et plateforme, permettant de repérer des zones géographiques présentant des tendances émotionnelles particulières.

## 6. Traitements Streaming
### 6.1 Détection de Pics d’Activité
Basé sur une fenêtre glissante de 5 minutes, détecte les anomalies de volume.

### 6.2 Analyse de Sentiment en Temps Réel
Fenêtre de 2 minutes, alertes si sentiment < -0.2 ou > 0.2.

### 6.3 Analyse des Sessions
Permet de suivre les sessions en direct : durée, engagement, actions.

## 7. Déploiement et Orchestration
Le déploiement via Docker Compose inclut 8 conteneurs fonctionnels. Les commandes normalisées couvrent le lancement des jobs Spark, la gestion des répertoires HDFS, l’exécution du producteur Kafka et la récupération des résultats.

## 8. Résultats
Les trois jobs batch ont été exécutés avec succès. Les dossiers générés (Parquet + CSV) sont présents dans `/results/batch/`. Les statistiques extraites démontrent :
- une forte concentration de l’engagement sur une minorité d’utilisateurs ;
- des préférences de plateformes fortement corrélées à l’âge ;
- des variations de sentiment selon les pays.

## 9. Résolution des Problèmes
Les principales difficultés rencontrées :
- ressources Spark trop élevées → optimisation (1GB, 1 core) ;
- répertoires HDFS manquants → création manuelle ;
- incompatibilité Kafka/Spark → ajustement du package.

## 10. Conclusion
Le projet est totalement opérationnel : infrastructure stable, données chargées, pipeline batch validé, pipeline stream prêt à l’emploi. L’architecture distribuée mise en place constitue un socle fiable pour l’analyse avancée de données massives.