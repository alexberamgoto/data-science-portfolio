# 📘 DOSSIER TECHNIQUE

## Projet : Prédiction de Réussite Étudiante - Plateforme ARCHE

**Formation :** FC Data Scientist 2025-2026  
**Institution :** Université de Lorraine - IDMC  
**Date :** Février 2026

---

## 📋 Table des Matières

1. [Conception du Logiciel](#1-conception-du-logiciel)
2. [Conception de l'Interface Utilisateur](#2-conception-de-linterface-utilisateur)
3. [Principaux Algorithmes](#3-principaux-algorithmes)
4. [Architecture Technique](#4-architecture-technique)
5. [Technologies Utilisées](#5-technologies-utilisées)

---

## 1. Conception du Logiciel

### 1.1 Architecture Globale

Le projet est divisé en **deux parties principales** :

```
┌─────────────────────────────────────────────────────────────┐
│                    PARTIE 1 : TRAIN                         │
│                  (Entraînement du Modèle)                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │ databuilder  │───▶│   Features   │───▶│ main.ipynb   │ │
│  │     .py      │    │     .py      │    │              │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                   │                    │         │
│         ▼                   ▼                    ▼         │
│    Nettoyage          Extraction           Entraînement    │
│    des données        de features          & Évaluation    │
│                                                             │
│                           OUTPUT                            │
│                      ┌──────────────┐                      │
│                      │ model_lr.pkl │                      │
│                      └──────────────┘                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  PARTIE 2 : APPLICATION                     │
│                (Déploiement avec Streamlit)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│     Architecture MVC (Modèle-Vue-Contrôleur)               │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   modele.py  │◀───│ controleur   │───▶│    vue.py    │ │
│  │              │    │     .py      │    │              │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                   │                    │         │
│         ▼                   ▼                    ▼         │
│  Gestion des          Logique métier      Interface        │
│  modèles ML           & coordination       utilisateur     │
│                                                             │
│                    Point d'entrée                          │
│                  ┌──────────────────┐                      │
│                  │ application.py   │                      │
│                  └──────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Principe de Programmation Orientée Objet

#### Classes Principales

##### **Partie 1 - Entraînement**

**1. Classe `DataBuilder`**
```python
Responsabilité : Gestion des données brutes
├── charger_donnees()
├── nettoyer_logs()
├── nettoyer_notes()
├── valider_colonnes()
├── obtenir_statistiques()
└── pipeline_complet()
```

**Attributs :**
- `logs` : DataFrame des logs bruts
- `notes` : DataFrame des notes brutes
- `logs_propres` : DataFrame nettoyé
- `notes_propres` : DataFrame nettoyé

**Méthodes clés :**
- Détection automatique des colonnes de date
- Suppression des valeurs manquantes et doublons
- Validation de la structure
- Génération de statistiques descriptives

---

**2. Classe `Features`**
```python
Responsabilité : Extraction des caractéristiques
├── calculer_features_base()
├── fusionner_avec_notes()
├── afficher_statistiques()
├── afficher_correlations()
├── obtenir_X_y()
└── sauvegarder_donnees()
```

**Attributs :**
- `logs` : Logs nettoyés
- `notes` : Notes nettoyées
- `features` : Features calculées
- `donnees_completes` : Données fusionnées

**Features extraites :**
1. `nb_actions` : Nombre total d'événements
2. `nb_connexions` : Nombre de login
3. `nb_ressources` : Nombre de contextes uniques

---

##### **Partie 2 - Application**

**3. Classe `Modele` (M dans MVC)**
```python
Responsabilité : Gestion des modèles ML
├── charger_modele_lr()
├── predire_note()
├── obtenir_coefficients()
└── valider_inputs()
```

**Attributs :**
- `modele_lr` : Instance du modèle LinearRegression
- `modele_charge` : Statut du chargement

**Méthodes clés :**
- Chargement du modèle .pkl
- Prédiction à partir des features
- Validation des entrées utilisateur
- Extraction des coefficients

---

**4. Classe `Vue` (V dans MVC)**
```python
Responsabilité : Interface utilisateur
├── afficher_entete()
├── afficher_formulaire()
├── afficher_resultats()
├── afficher_interpretation()
├── afficher_coefficients()
├── afficher_sidebar()
└── afficher_footer()
```

**Attributs :** Aucun (affichage pur)

**Méthodes clés :**
- Composants Streamlit (formulaires, métriques, graphiques)
- Styles CSS personnalisés
- Visualisations matplotlib/seaborn
- Messages d'erreur et validation

---

**5. Classe `Controleur` (C dans MVC)**
```python
Responsabilité : Logique métier
├── initialiser_application()
├── executer()
├── faire_prediction()
├── analyser_profil()
└── generer_recommandations()
```

**Attributs :**
- `modele` : Instance de Modele
- `vue` : Instance de Vue
- `modele_charge` : Statut

**Méthodes clés :**
- Coordination Modèle ↔ Vue
- Orchestration du flux applicatif
- Logique métier (validation, recommandations)

---

### 1.3 Diagramme de Classes UML

```
┌─────────────────────────┐
│     DataBuilder         │
├─────────────────────────┤
│ - logs: DataFrame       │
│ - notes: DataFrame      │
│ - logs_propres          │
│ - notes_propres         │
├─────────────────────────┤
│ + charger_donnees()     │
│ + nettoyer_logs()       │
│ + nettoyer_notes()      │
│ + pipeline_complet()    │
└─────────────────────────┘
           │
           │ produit
           ↓
┌─────────────────────────┐
│       Features          │
├─────────────────────────┤
│ - logs: DataFrame       │
│ - notes: DataFrame      │
│ - features: DataFrame   │
│ - donnees_completes     │
├─────────────────────────┤
│ + calculer_features()   │
│ + fusionner_notes()     │
│ + pipeline_complet()    │
└─────────────────────────┘
           │
           │ génère
           ↓
    model_lr.pkl
           │
           │ utilisé par
           ↓
┌─────────────────────────┐         ┌─────────────────────────┐
│        Modele           │◀───────│     Controleur          │
├─────────────────────────┤         ├─────────────────────────┤
│ - modele_lr             │         │ - modele: Modele        │
│ - modele_charge         │         │ - vue: Vue              │
├─────────────────────────┤         ├─────────────────────────┤
│ + charger_modele()      │         │ + executer()            │
│ + predire_note()        │         │ + faire_prediction()    │
│ + valider_inputs()      │         │ + analyser_profil()     │
└─────────────────────────┘         └─────────────────────────┘
                                              │
                                              │ utilise
                                              ↓
                                    ┌─────────────────────────┐
                                    │         Vue             │
                                    ├─────────────────────────┤
                                    │ (pas d'attributs)       │
                                    ├─────────────────────────┤
                                    │ + afficher_entete()     │
                                    │ + afficher_formulaire() │
                                    │ + afficher_resultats()  │
                                    └─────────────────────────┘
```

---

### 1.4 Flux de Données

```
Étape 1 : ETL
logs.csv + notes.csv
        ↓
   DataBuilder
   ├── Détection colonnes
   ├── Nettoyage
   ├── Validation
   └── Statistiques
        ↓
logs_propres + notes_propres

Étape 2 : Feature Engineering
        ↓
    Features
   ├── Groupby pseudo
   ├── Agrégation
   ├── Fusion notes
   └── Corrélations
        ↓
data_features.csv

Étape 3 : Modélisation
        ↓
    main.ipynb
   ├── Train/Test split
   ├── Régression Linéaire
   ├── Random Forest
   ├── Évaluation (RMSE, Accuracy)
   └── Sauvegarde
        ↓
   model_lr.pkl

Étape 4 : Déploiement
        ↓
  Application Streamlit
   ├── Charger modèle
   ├── Interface utilisateur
   ├── Prédiction temps réel
   └── Visualisation résultats
```

---

### 1.5 Gestion des Erreurs

**Stratégie de robustesse :**

1. **Try-Except** dans toutes les opérations critiques
2. **Validation des inputs** avant traitement
3. **Messages d'erreur explicites** en français
4. **Logs de débogage** avec emojis pour faciliter le suivi

**Exemples :**

```python
# DataBuilder
try:
    self.logs = pd.read_csv(chemin_logs)
except Exception as e:
    print(f"❌ Erreur lors du chargement : {e}")
    return None, None

# Modele
def valider_inputs(self, nb_actions, nb_connexions, nb_ressources):
    if nb_connexions > nb_actions:
        return False, "Le nombre de connexions ne peut pas dépasser les actions"
    return True, "OK"
```

---

## 2. Conception de l'Interface Utilisateur

### 2.1 Wireframe de l'Application

```
┌────────────────────────────────────────────────────────────────┐
│  SIDEBAR                    │  MAIN CONTENT                     │
├────────────────────────────────────────────────────────────────┤
│  ℹ️ Informations            │  🎓 Prédiction de Réussite       │
│                             │  Plateforme ARCHE                 │
│  📚 Features Utilisées      │  ────────────────────────────────│
│  • nb_actions               │                                   │
│  • nb_connexions            │  📋 À propos                      │
│  • nb_ressources            │  [Description du projet]          │
│                             │                                   │
│  🎯 Seuil de Réussite      │  ────────────────────────────────│
│  Note ≥ 10/20              │                                   │
│                             │  📝 Profil de l'Étudiant          │
│  📊 À propos du Modèle     │                                   │
│  Type : Régression         │  ┌──────┐  ┌──────┐  ┌──────┐   │
│  Linéaire Multiple         │  │ 📊   │  │ 🔑   │  │ 📚   │   │
│                             │  │Actions│  │Connx │  │Rsrcs │   │
│  👨‍🎓 Projet                │  │ 100  │  │  10  │  │  5   │   │
│  FC Data Scientist         │  └──────┘  └──────┘  └──────┘   │
│  2025-2026                  │                                   │
│                             │  ┌─────────────────────────────┐│
│                             │  │  🔮 Prédire la Réussite     ││
│                             │  └─────────────────────────────┘│
│                             │                                   │
│                             │  ────────────────────────────────│
│                             │                                   │
│                             │  📊 Résultats de la Prédiction   │
│                             │                                   │
│                             │  ┌──────────┐  ┌──────────────┐ │
│                             │  │Note : XX │  │✅ RÉUSSITE   │ │
│                             │  │   /20    │  │ PROBABLE     │ │
│                             │  └──────────┘  └──────────────┘ │
│                             │                                   │
│                             │  📈 [Barre de progression]        │
│                             │  [━━━━━━━━━━━━━━━━━━━━]         │
│                             │                                   │
│                             │  💡 Interprétation                │
│                             │  [Recommandations personnalisées] │
│                             │                                   │
│                             │  📊 Coefficients du Modèle        │
│                             │  [Équation + Graphique]           │
│                             │                                   │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 Composants de l'Interface

#### **2.2.1 En-tête**
- **Titre** : Gradient violet/bleu
- **Sous-titre** : Institution
- **Séparateur** visuel

#### **2.2.2 Formulaire de Saisie**
- **3 colonnes** : nb_actions, nb_connexions, nb_ressources
- **Inputs numériques** avec :
  - Min/Max définis
  - Valeurs par défaut
  - Tooltips explicatives
  - Incréments appropriés

#### **2.2.3 Bouton d'Action**
- **Style** : Primary (bleu)
- **Taille** : Full width
- **Icône** : 🔮
- **État** : Activé seulement si validation OK

#### **2.2.4 Affichage des Résultats**
- **Métriques** : Note prédite + Statut
- **Barre de progression** : Visualisation 0-20
- **Jauge colorée** : Rouge (0-10), Orange (10-12), Jaune (12-16), Vert (16-20)
- **Interprétation** : Box colorée selon le niveau

#### **2.2.5 Section Avancée (Expandable)**
- **Équation LaTeX** de régression
- **Coefficients** : 4 métriques (β₀, β₁, β₂, β₃)
- **Graphique** : Barres horizontales des coefficients

#### **2.2.6 Sidebar**
- **Informations fixes** : Toujours visibles
- **Sections** : Features, Seuil, Modèle, Projet
- **Scroll indépendant** du contenu principal

---

### 2.3 Palette de Couleurs

```
Couleurs principales :
- Primaire (Bleu)   : #3b82f6
- Secondaire (Violet): #667eea, #764ba2
- Succès (Vert)     : #2ecc71
- Avertissement     : #f39c12
- Danger (Rouge)    : #e74c3c
- Neutre (Gris)     : #666666

Gradient header : linear-gradient(90deg, #667eea 0%, #764ba2 100%)
```

---

### 2.4 Responsive Design

L'application utilise le système de **colonnes Streamlit** :

```python
# Layout adaptatif
col1, col2, col3 = st.columns(3)  # 3 colonnes égales
col1, col2 = st.columns([2, 1])   # Colonnes pondérées
```

**Breakpoints automatiques** gérés par Streamlit :
- Desktop : 3 colonnes
- Tablet : 2 colonnes
- Mobile : 1 colonne (stack vertical)

---

## 3. Principaux Algorithmes

### 3.1 Algorithme de Nettoyage des Données

```python
ALGORITHME: nettoyer_donnees()
ENTRÉE: logs.csv, notes.csv
SORTIE: logs_propres, notes_propres

DÉBUT
    # 1. Chargement
    CHARGER logs.csv DANS logs
    CHARGER notes.csv DANS notes
    
    # 2. Détection colonnes de date
    POUR CHAQUE colonne DANS ['heure', 'date', 'time', 'timestamp'] FAIRE
        SI colonne EXISTE DANS logs ALORS
            CONVERTIR logs[colonne] EN datetime
            SORTIR DE BOUCLE
        FIN SI
    FIN POUR
    
    # 3. Suppression valeurs manquantes
    logs ← SUPPRIMER_NA(logs)
    notes ← SUPPRIMER_NA(notes)
    
    # 4. Suppression doublons
    logs ← SUPPRIMER_DOUBLONS(logs)
    notes ← SUPPRIMER_DOUBLONS(notes, sur='pseudo')
    
    # 5. Conversion types
    logs['pseudo'] ← CONVERTIR_EN_TEXTE(logs['pseudo'])
    notes['pseudo'] ← CONVERTIR_EN_TEXTE(notes['pseudo'])
    notes['note'] ← CONVERTIR_EN_NUMERIQUE(notes['note'])
    
    # 6. Validation notes (0-20)
    notes ← FILTRER(notes, note >= 0 ET note <= 20)
    
    RETOURNER logs, notes
FIN
```

**Complexité :** O(n log n) avec n = nombre de lignes

---

### 3.2 Algorithme d'Extraction de Features

```python
ALGORITHME: extraire_features()
ENTRÉE: logs_propres, notes_propres
SORTIE: donnees_completes

DÉBUT
    # 1. Agrégation par étudiant
    features ← VIDE
    
    POUR CHAQUE etudiant DANS UNIQUE(logs['pseudo']) FAIRE
        logs_etudiant ← FILTRER(logs, pseudo == etudiant)
        
        # Calcul des indicateurs
        nb_actions ← COMPTER(logs_etudiant)
        nb_connexions ← COMPTER(logs_etudiant OÙ composant == "login")
        nb_ressources ← COMPTER_UNIQUE(logs_etudiant['contexte'])
        
        # Stocker
        AJOUTER_LIGNE(features, {
            'pseudo': etudiant,
            'nb_actions': nb_actions,
            'nb_connexions': nb_connexions,
            'nb_ressources': nb_ressources
        })
    FIN POUR
    
    # 2. Fusion avec les notes
    donnees_completes ← FUSIONNER(features, notes, sur='pseudo')
    
    # 3. Créer variable binaire
    donnees_completes['reussite'] ← (donnees_completes['note'] >= 10)
    
    RETOURNER donnees_completes
FIN
```

**Complexité :** O(n) avec n = nombre de lignes dans logs

---

### 3.3 Algorithme de Régression Linéaire Multiple

**Principe :** Moindres Carrés Ordinaires (OLS)

**Équation :**
```
y = β₀ + β₁·x₁ + β₂·x₂ + β₃·x₃ + ε

Où :
- y  = note (variable dépendante)
- x₁ = nb_actions
- x₂ = nb_connexions
- x₃ = nb_ressources
- β₀, β₁, β₂, β₃ = coefficients à estimer
- ε  = erreur résiduelle
```

**Algorithme de calcul des coefficients :**

```python
ALGORITHME: regression_lineaire()
ENTRÉE: X (matrice features n×p), y (vecteur target n×1)
SORTIE: β (vecteur coefficients p×1)

DÉBUT
    # 1. Ajouter colonne de 1 pour l'intercept
    X_augmente ← AJOUTER_COLONNE_UNS(X)
    
    # 2. Calcul par formule matricielle
    # β = (X^T X)^(-1) X^T y
    
    X_transpose ← TRANSPOSER(X_augmente)
    produit ← MULTIPLIER_MATRICES(X_transpose, X_augmente)
    inverse ← INVERSER_MATRICE(produit)
    beta ← MULTIPLIER_MATRICES(inverse, X_transpose, y)
    
    # 3. Extraire coefficients
    β₀ ← beta[0]  # Intercept
    β₁ ← beta[1]  # Coef nb_actions
    β₂ ← beta[2]  # Coef nb_connexions
    β₃ ← beta[3]  # Coef nb_ressources
    
    RETOURNER β₀, β₁, β₂, β₃
FIN
```

**Complexité :** O(p² · n) où p = nombre de features, n = nombre d'observations

---

### 3.4 Algorithme de Prédiction

```python
ALGORITHME: predire()
ENTRÉE: nb_actions, nb_connexions, nb_ressources, modele
SORTIE: note_predite

DÉBUT
    # 1. Créer vecteur de features
    X_new ← [nb_actions, nb_connexions, nb_ressources]
    
    # 2. Appliquer l'équation de régression
    note_predite ← modele.intercept_ + 
                   modele.coef_[0] * nb_actions +
                   modele.coef_[1] * nb_connexions +
                   modele.coef_[2] * nb_ressources
    
    # 3. Borner la note entre 0 et 20
    note_predite ← MAX(0, MIN(20, note_predite))
    
    RETOURNER note_predite
FIN
```

**Complexité :** O(p) = O(1) car p est constant (3 features)

---

### 3.5 Métriques d'Évaluation

#### **RMSE (Root Mean Squared Error)**

```python
ALGORITHME: calculer_rmse()
ENTRÉE: y_true (notes réelles), y_pred (notes prédites)
SORTIE: rmse

DÉBUT
    n ← TAILLE(y_true)
    somme_carres ← 0
    
    POUR i DE 1 À n FAIRE
        erreur ← y_true[i] - y_pred[i]
        somme_carres ← somme_carres + erreur²
    FIN POUR
    
    mse ← somme_carres / n
    rmse ← RACINE_CARREE(mse)
    
    RETOURNER rmse
FIN
```

**Formule mathématique :**
```
RMSE = √(1/n · Σ(yᵢ - ŷᵢ)²)
```

**Interprétation :** Erreur moyenne en points (plus faible = meilleur)

---

#### **R² Score (Coefficient de détermination)**

```python
ALGORITHME: calculer_r2()
ENTRÉE: y_true, y_pred
SORTIE: r2

DÉBUT
    y_moyenne ← MOYENNE(y_true)
    
    # Somme des carrés totale
    ss_tot ← SOMME((y_true - y_moyenne)²)
    
    # Somme des carrés résiduelle
    ss_res ← SOMME((y_true - y_pred)²)
    
    # Calcul R²
    r2 ← 1 - (ss_res / ss_tot)
    
    RETOURNER r2
FIN
```

**Formule mathématique :**
```
R² = 1 - (SS_res / SS_tot)
```

**Interprétation :** 
- R² = 1 : Ajustement parfait
- R² = 0 : Modèle pas meilleur qu'une moyenne
- R² < 0 : Modèle pire qu'une moyenne

---

## 4. Architecture Technique

### 4.1 Structure des Fichiers

```
projet-arche/
│
├── 📂 TRAIN/                      # Partie 1 : Entraînement
│   ├── databuilder.py             # Classe nettoyage données
│   ├── Features.py                # Classe extraction features
│   ├── main.ipynb                 # Notebook principal
│   ├── logs.csv                   # Données d'entrée
│   ├── notes.csv                  # Données d'entrée
│   ├── data_features.csv          # Données avec features (généré)
│   ├── model_lr.pkl               # Modèle entraîné (généré)
│   └── model_rf.pkl               # Modèle RF (optionnel, généré)
│
├── 📂 APP/                        # Partie 2 : Application
│   ├── application.py             # Point d'entrée (version simple)
│   ├── controleur.py              # Contrôleur MVC
│   ├── modele.py                  # Modèle MVC
│   ├── vue.py                     # Vue MVC
│   └── model_lr.pkl               # Copie du modèle entraîné
│
├── 📂 DOCS/                       # Documentation
│   ├── DOSSIER_TECHNIQUE.md       # Ce document
│   └── DOSSIER_ANALYSE.md         # Analyse du projet
│
├── requirements.txt               # Dépendances Python
├── README.md                      # Guide utilisateur
└── .gitignore                     # Fichiers à ignorer
```

---

### 4.2 Diagramme de Séquence - Utilisation

```
Utilisateur    │   Application   │  Contrôleur  │   Modèle    │    Vue
     │         │       (UI)      │              │             │
     │         │                 │              │             │
     ├─────────▶ Ouvrir app      │              │             │
     │         ├─────────────────▶ initialiser()│             │
     │         │                 ├──────────────▶ charger_    │
     │         │                 │              │  modele()   │
     │         │                 ◀──────────────┤             │
     │         │                 │  modele OK   │             │
     │         │                 ├──────────────┼─────────────▶
     │         │                 │              │    afficher_│
     │         │                 │              │    entete() │
     │         ◀─────────────────┴──────────────┴─────────────┘
     │         │  Interface affichée                          │
     │         │                                               │
     ├─────────▶ Entrer données                               │
     │         │  (100, 10, 5)                                │
     │         │                                               │
     ├─────────▶ Clic "Prédire"                               │
     │         ├─────────────────▶ faire_       │             │
     │         │                 │  prediction()│             │
     │         │                 ├──────────────▶ predire_    │
     │         │                 │              │  note()     │
     │         │                 ◀──────────────┤             │
     │         │                 │  note=14.5   │             │
     │         │                 ├──────────────┼─────────────▶
     │         │                 │              │   afficher_ │
     │         │                 │              │   resultats()│
     │         ◀─────────────────┴──────────────┴─────────────┘
     │         │  Résultat affiché                            │
```

---

## 5. Technologies Utilisées

### 5.1 Langages et Frameworks

| Technologie | Version | Usage |
|-------------|---------|-------|
| **Python** | 3.10+ | Langage principal |
| **Jupyter** | Latest | Notebooks interactifs |
| **Streamlit** | 1.20+ | Interface web |
| **Pandas** | 1.5+ | Manipulation données |
| **NumPy** | 1.23+ | Calculs numériques |
| **Scikit-learn** | 1.2+ | Machine Learning |
| **Matplotlib** | 3.6+ | Visualisations |
| **Seaborn** | 0.12+ | Visualisations statistiques |
| **Joblib** | 1.2+ | Sauvegarde modèles |

---

### 5.2 Bibliothèques Spécifiques

#### **Pandas - Manipulation de Données**
```python
# Fonctionnalités utilisées :
- pd.read_csv()           # Lecture CSV
- pd.to_datetime()        # Conversion dates
- DataFrame.groupby()     # Agrégation
- DataFrame.merge()       # Fusion
- DataFrame.describe()    # Statistiques
- DataFrame.corr()        # Corrélations
```

#### **Scikit-learn - Machine Learning**
```python
# Modules utilisés :
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
```

#### **Streamlit - Interface Web**
```python
# Composants utilisés :
st.title()               # Titres
st.markdown()            # Texte formaté
st.number_input()        # Inputs numériques
st.button()              # Boutons
st.metric()              # Métriques
st.progress()            # Barres de progression
st.columns()             # Layout colonnes
st.sidebar               # Barre latérale
st.pyplot()              # Graphiques matplotlib
```

---

### 5.3 Environnement de Développement

**IDE Recommandés :**
- Visual Studio Code (avec extensions Python, Jupyter)
- PyCharm Professional
- Jupyter Lab

**Structure requirements.txt :**
```txt
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
matplotlib>=3.6.0
seaborn>=0.12.0
streamlit>=1.20.0
joblib>=1.2.0
```

**Installation :**
```bash
pip install -r requirements.txt
```

---

### 5.4 Déploiement

**Options de déploiement :**

1. **Local** (pour développement)
```bash
streamlit run application.py
```

2. **Streamlit Cloud** (gratuit)
- Connecter repository GitHub
- Configuration automatique
- URL publique générée

3. **Docker** (pour production)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "application.py"]
```

---

## 📝 Conclusion Technique

Ce projet démontre une **architecture modulaire et maintenable** basée sur :

✅ **Programmation Orientée Objet** : Classes réutilisables et extensibles  
✅ **Séparation des préoccupations** : ETL ≠ ML ≠ UI  
✅ **Pattern MVC** : Modèle-Vue-Contrôleur pour l'application  
✅ **Code propre** : Commentaires, docstrings, noms explicites  
✅ **Robustesse** : Gestion d'erreurs complète  
✅ **Documentation** : Technique et utilisateur

---

**Document rédigé par :** Étudiant FC Data Science 2025-2026  
**Institution :** Université de Lorraine - IDMC  
**Date :** Février 2026
