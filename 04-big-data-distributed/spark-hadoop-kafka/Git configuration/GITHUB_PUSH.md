# Guide de push sur GitHub

## ✓ Étape 1 : Préparation locale [COMPLÉTÉE]

Le dépôt Git local a été initialisé et un commit a été créé avec :
- 26 fichiers
- Tous les codes corrigés
- Environnement configuré
- Documentation complète

## 📋 Étape 2 : Créer un dépôt vide sur GitHub

### Option A : Via l'interface GitHub (recommandé)

1. Allez sur [github.com](https://github.com)
2. Cliquez sur **+** → **New repository**
3. Remplissez les champs :
   - **Repository name** : `spark-bigdata-project` (ou nom de votre choix)
   - **Description** : `Big Data project for social media events analysis using Spark, Kafka, and HDFS`
   - **Public** ou **Private** : selon vos préférences
   - ⚠️ **NE cochez PAS** "Add a README file", "Add .gitignore", "Choose a license"
   - Cliquez **Create repository**

### Option B : Utiliser GitHub CLI

```bash
gh repo create spark-bigdata-project --public --source=. --remote=origin --push
```

## 🚀 Étape 3 : Pousser le code (après création du repo)

Une fois le dépôt GitHub créé, exécutez ces commandes :

```bash
# Remplacer VOTRE_UTILISATEUR par votre nom d'utilisateur GitHub
cd "c:\Users\Etudiant\Desktop\ressources Data Scientist\TD systeme distribuée\Djekounmian Alexis Projet SPARK"

# Ajouter le remote GitHub
git remote add origin https://github.com/VOTRE_UTILISATEUR/spark-bigdata-project.git

# Renommer la branche en 'main' (optionnel, recommandé)
git branch -M main

# Pousser le code
git push -u origin main
```

## ✓ Vérification

Après le push, vérifiez :

```bash
# Voir le remote
git remote -v

# Voir le statut
git status
```

Vous devriez voir :
```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

## 📊 Ce qui sera poussé sur GitHub

```
spark-bigdata-project/
├── .gitignore
├── .env
├── README.md
├── QUICKSTART.md
├── SETUP.md
├── CORRECTIONS.md
├── requirements.txt
├── environment.yml
├── setup.py
├── setup_env.bat
├── setup_env.sh
├── docker-compose.yml
├── run_project.sh
├── cleanup.sh
├── check_status.sh
├── kafka/
│   └── kafka_producer.py
├── spark_jobs/
│   ├── batch_engagement.py
│   ├── batch_preferences_age.py
│   ├── batch_sentiment.py
│   ├── stream_activity_spikes.py
│   ├── stream_sentiment.py
│   └── stream_sessions_analysis.py
├── scripts/
│   └── upload_to_hdfs.sh
└── data/
    └── social_media_events.csv
```

## 🔒 Données sensibles

Les fichiers sensibles sont déjà exclus par `.gitignore` :
- `.venv/` (environnement virtuel)
- `__pycache__/` (cache Python)
- `.idea/` (IDE settings)
- `metastore_db/` (Spark)
- `results/` (résultats générés)

Le fichier `.env` est versionné (à adapter selon votre politique)

## 💡 Conseils supplémentaires

### Après le premier push

```bash
# Voir l'historique
git log --oneline

# Configurer des branches
git checkout -b develop
git checkout -b feature/nom-feature

# Faire des commits réguliers
git add .
git commit -m "Description du changement"
git push origin main
```

### Gérer les futures modifications

```bash
# Mettre à jour depuis GitHub
git pull origin main

# Pousser les modifications
git push origin main
```

### Collaborer (optionnel)

1. Allez sur GitHub → Settings → Collaborators
2. Ajoutez les emails des collaborateurs
3. Ils devront accepter l'invitation

## ⚠️ Important

Si vous recevez une erreur d'authentification :

### Option 1 : Token d'accès personnel

1. GitHub → Settings → Developer settings → Personal access tokens
2. Générez un nouveau token (cochez `repo`)
3. Utilisez le token comme mot de passe

### Option 2 : Clé SSH (recommandé)

1. Générez une clé SSH :
   ```bash
   ssh-keygen -t ed25519 -C "votre-email@example.com"
   ```
2. Ajoutez la clé à GitHub :
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   Puis GitHub → Settings → SSH and GPG keys → New SSH key
3. Changez l'URL du remote :
   ```bash
   git remote set-url origin git@github.com:VOTRE_UTILISATEUR/spark-bigdata-project.git
   ```

## 📞 Support

- [GitHub Getting Started](https://docs.github.com/en/get-started)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub CLI](https://cli.github.com/)

---

**Prêt ?** Créez votre dépôt puis exécutez les commandes de l'étape 3 ! 🚀
