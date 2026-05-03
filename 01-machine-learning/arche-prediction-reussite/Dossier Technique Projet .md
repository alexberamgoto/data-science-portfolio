 # DOSSIER TECHNIQUE

### Système de Prédiction de réussite / l'échec d'Apprenant via traces numerique l'espace ARCHE

Projet réalisé par : Djekounmian Beramgoto Alexis    

---

##  Table des Matières

1. Conception du Logiciel
2. Conception de l'Interface Utilisateur
3. Principaux Algorithmes
5. Documentation du Code

---

## Conception du Logiciel


Elle est composée de **deux parties principales** :

```
┌────────────────────────────────────────────────────────────----──┐
│                    Partie 1 : Main.ipynb                         │
│              (Notebook d'Entraînement des Modèles)               |
├───────────────────────────────────────────────────────────----───┤
│                                                                  │
│  Input                    Processing               Output        │
│  ┌─────────────---┐         ┌──────────────┐        ┌────────┐   │
│  logs_infos_25.csv     │───▶│ ETL          │───────▶│Features│   │
│  notes_infos_25.csv    │         │ Feature Eng. │   │Dataset │
│  └────────────---─┘         └──────────────┘        └────────┘   │
│                                 │                      │         │
│                                 ▼                      ▼         │
│                          ┌──────────────┐      ┌──────────┐│
│                          │ Train/Test   │      │ Models   ││
│                          │ Split        │      │ Trained  ││
│                          └──────────────┘      └──────────┘│
│                                 │                      │     │
│                                 ▼                      ▼     │
│                          ┌──────────────┐      ┌──────────┐│
│                          │ Régression   │      │.pkl files││
│                          │ Random Forest│      │          ││
│                          └──────────────┘      └──────────┘│
└──────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────┐
│                Partie 2: Application.py                     │
│            (Application Streamlit Interactive)               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Page 1    │  │   Page 2    │  │   Page 3    │        │
│  │  Accueil    │  │     ETL     │  │  Features   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │   Page 4    │  │   Page 5    │                          │
│  │ Modélisation│  │ Prédiction  │                          │
│  └─────────────┘  └─────────────┘                          │
│                                                             │
│  Backend: Session State Management                          │
│  ├─ logs (DataFrame)                                        │
│  ├─ notes (DataFrame)                                       │
│  ├─ features (DataFrame)                                    │
│  ├─ reg_model (LinearRegression)                            │
│  └─ rf_model (RandomForestClassifier)                       │
└──────────────────────────────────────────────────────────────┘
```

###   Programmation


1. Programmation Normale (Main.ipynb)
   - Structure linéaire séquentielle
   - Chaque cellule = une étape du pipeline
   - Facilite la compréhension pour débutants
   - Permet l'exécution pas à pas

2. **Programmation OO** (Application.py)
   - Fonctions pures avec décorateurs Streamlit
   - `@st.cache_data` pour optimisation
   - Chaque fonction a une responsabilité unique
-Les fonctions sont réutilisables,le code est modulaire

Exemple de structure  dans Application.py :

```python
@st.cache_data
def load_data(logs_file, notes_file):
    """Fonction pure de chargement"""
    logs = pd.read_csv(logs_file)
    notes = pd.read_csv(notes_file)
    return logs, notes

def clean_data(logs, notes):
    """Fonction de transformation"""
    # Détection automatique colonne date
    if 'heure' in logs.columns:
        logs['heure'] = pd.to_datetime(logs['heure'], errors='coerce')
    elif 'date' in logs.columns:
        logs['date'] = pd.to_datetime(logs['date'], errors='coerce')
    
    logs = logs.dropna()
    notes = notes.dropna()
    return logs, notes

def create_features(logs):
    """Fonction d'extraction de features"""
    features = logs.groupby("pseudo").agg(
        nb_actions=("evenement", "count"),
        nb_connexions=("composant", lambda x: (x == "login").sum()),
        nb_ressources=("contexte", "nunique")
    ).reset_index()
    return features
```

###  Gestion de l'État (State Management)

Problème : Streamlit recharge la page à chaque interaction.

Solution :Utilisation de `st.session_state` comme store persistant.

```python
# Sauvegarde dans le state
st.session_state['logs'] = logs_clean
st.session_state['notes'] = notes_clean
st.session_state['features'] = features
st.session_state['reg_model'] = reg
st.session_state['rf_model'] = rf

# Récupération depuis le state
if 'logs' in st.session_state:
    logs = st.session_state['logs']
```

Architecture du State :

```
st.session_state
├── logs: DataFrame (16,229 lignes × 5 colonnes)
├── notes: DataFrame (100 lignes × 2 colonnes)
├── features: DataFrame (95 lignes × 4 colonnes)
├── reg_model: LinearRegression instance
├── rf_model: RandomForestClassifier instance
├── X_train: DataFrame (76 lignes × 3 colonnes)
├── X_test: DataFrame (19 lignes × 3 colonnes)
├── y_train: Series (76 valeurs)
├── y_test: Series (19 valeurs)
├── rmse: float
└── accuracy: float
```

###  Pipeline de Traitement des Données

Flow complet du Main.ipynb :

```python
# ÉTAPE 1: Chargement
logs = pd.read_csv("logs_info_25_pseudo.csv")      # 16,229 lignes
notes = pd.read_csv("notes_info_25_pseudo.csv")    # 100 lignes

# ÉTAPE 2: Nettoyage
# Détection automatique de la colonne date
if 'date' in logs.columns:
    logs['date'] = pd.to_datetime(logs['date'])
logs = logs.dropna()                                # Aucune perte
notes = notes.dropna()                              # Aucune perte

# ÉTAPE 3: Feature Engineering
features = logs.groupby("pseudo").agg(
    nb_actions=("evenement", "count"),              # Agrégation COUNT
    nb_connexions=("composant", lambda x: (x == "login").sum()),  # Filtre + COUNT
    nb_ressources=("contexte", "nunique")           # Comptage valeurs uniques
).reset_index()

# ÉTAPE 4: Fusion
data = features.merge(notes, on="pseudo")           # Inner join
# Résultat: 95 étudiants (5 perdus car pas de notes)

# ÉTAPE 5: Préparation ML
X = data[["nb_actions", "nb_connexions", "nb_ressources"]]  # (95, 3)
y = data["note"]                                             # (95,)

# ÉTAPE 6: Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# Train: 76 étudiants | Test: 19 étudiants

# ÉTAPE 7: Modélisation
reg = LinearRegression()
reg.fit(X_train, y_train)



rf = RandomForestClassifier(random_state=42, n_estimators=100)
y_class = (data["note"] >= 10).astype(int)
rf.fit(X_train, y_class.iloc[X_train.index])

# ÉTAPE 8: Sauvegarde
import joblib
joblib.dump(reg, "model_regression.pkl")
joblib.dump(rf, "model_random_forest.pkl")
```

###  Gestion des Erreurs et Robustesse

**1. Détection Automatique de Colonnes**

```python
# Flexible: supporte plusieurs noms de colonnes de date
date_columns = ['heure', 'date', 'time', 'timestamp']
for col in date_columns:
    if col in logs.columns:
        logs[col] = pd.to_datetime(logs[col], errors='coerce')
        break
else:
    print(" Colonne de date introuvable")
    print("Colonnes disponibles:", logs.columns.tolist())
```

**2. Validation des Données**

```python
# Vérification de la présence des colonnes essentielles
required_cols_logs = ['pseudo', 'evenement', 'composant', 'contexte']
required_cols_notes = ['pseudo', 'note']

assert all(col in logs.columns for col in required_cols_logs), \
    "Colonnes manquantes dans logs"
assert all(col in notes.columns for col in required_cols_notes), \
    "Colonnes manquantes dans notes"
```

**3. Gestion des valeurs manquantes NaN**

```python
# Stratégie: Suppression stricte
logs = logs.dropna()    # Supprime lignes avec ANY NaN
notes = notes.dropna()  # Supprime lignes avec ANY NaN

# Vérification post-traitement
assert not data.isnull().any().any(), "Des NaN persistent!"
```

**4. Traçabilité**

```python
# Logs de transformation
print(f"Logs avant nettoyage: {len(logs_brut)} lignes")
print(f"Logs après nettoyage: {len(logs)} lignes")
print(f"Perte: {len(logs_brut) - len(logs)} lignes ({...}%)")

print(f"Features extraites: {len(features)} étudiants")
print(f"Après merge: {len(data)} étudiants")
print(f"Perdus (pas de notes): {len(features) - len(data)}")
```

---

##  Conception de l'Interface Utilisateur

### A Navigation

**Pattern : Multi-Page Application**

```python
# Sidebar pour navigation
st.sidebar.header("📊 Navigation")
page = st.sidebar.radio(
    "Choisissez une étape :",
    ["🏠 Accueil", 
     "📁 1. ETL - Chargement des données", 
     "🔧 2. Feature Engineering", 
     "🤖 3. Modélisation", 
     "📈 4. Évaluation", 
     "🔮 5. Prédiction"]
)

# Routing conditionnel
if page == "🏠 Accueil":
    afficher_accueil()
elif page == "📁 1. ETL - Chargement des données":
    afficher_etl()
# ... etc
```

```

###  Composants UI Utilisés

####  Upload de Fichiers**

```python
col1, col2 = st.columns(2)

with col1:
    logs_file = st.file_uploader(
        "📊 Charger le fichier logs.csv", 
        type=["csv"]
    )

with col2:
    notes_file = st.file_uploader(
        "📝 Charger le fichier notes.csv", 
        type=["csv"]
    )
```

Workflow :
1. Utilisateur clique sur "Browse files"
2. Sélection d'un fichier .csv local
3. Upload automatique en mémoire
4. Accessible via `pd.read_csv(logs_file)`

####  Affichage de DataFrames

```python
st.subheader("📊 Aperçu des Logs")
st.write(f"**Dimensions :** {logs.shape[0]} lignes × {logs.shape[1]} colonnes")
st.dataframe(logs.head(10))
```

Rendu :Tableau interactif avec scrolling horizontal/vertical.

####  Boutons d'Action

```python
if st.button("🧹 Nettoyer les données"):
    logs_clean, notes_clean = clean_data(logs, notes)
    st.success("✅ Données nettoyées !")
    st.session_state['logs'] = logs_clean
    st.session_state['notes'] = notes_clean
```

Comportement : Clic → Exécution → Rechargement page → État préservé via session_state.

####  Métriques

```python
col1, col2 = st.columns(2)

with col1:
    st.metric("Note Prédite", f"{note_pred:.2f}/20")

with col2:
    resultat = " RÉUSSITE" if reussite_pred == 1 else " ÉCHEC"
    st.metric("Prédiction", resultat)
```

Affichage :Cartes avec valeur principale et label.

####  Inputs Numériques

```python
col1, col2, col3 = st.columns(3)

with col1:
    nb_actions = st.number_input(
        "📊 Nombre d'actions",
        min_value=0,
        max_value=10000,
        value=100,
        step=10,
        help="Nombre total d'événements enregistrés"
    )
```

Features :
- Validation automatique (min/max)
- Boutons +/- ou saisie directe
- Tooltip au survol

#### Graphiques

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(y_test, y_pred_reg, alpha=0.6, edgecolors='k')
ax.plot([y_test.min(), y_test.max()], 
        [y_test.min(), y_test.max()], 
        'r--', lw=2, label='Prédiction parfaite')
ax.set_xlabel('Notes réelles')
ax.set_ylabel('Notes prédites')
ax.set_title('Régression Linéaire : Prédictions vs Réalité')
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)
```

Intégration : Matplotlib → Streamlit via `st.pyplot()`.

### Flow Utilisateur Complet

```
┌─────────────────────────────────────────────────────────┐
│  1. ACCUEIL                                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │ - Présentation problématique                    │   │
│  │ - Objectifs du projet                           │   │
│  │ - Structure des données attendues              │   │
│  └─────────────────────────────────────────────────┘   │
│                        │                                │
│                        ▼                                │
│  2. ETL                                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Upload logs.csv] [Upload notes.csv]           │   │
│  │ → Affichage aperçu                              │   │
│  │ [Bouton: Nettoyer]                              │   │
│  │ → Sauvegarde dans session_state                │   │
│  └─────────────────────────────────────────────────┘   │
│                        │                                │
│                        ▼                                │
│  3. FEATURE ENGINEERING                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Affichage des 3 métriques calculées            │   │
│  │ - nb_actions                                    │   │
│  │ - nb_connexions                                 │   │
│  │ - nb_ressources                                 │   │
│  │ [Bouton: Fusionner avec notes]                 │   │
│  │ → Sauvegarde features dans session_state       │   │
│  └─────────────────────────────────────────────────┘   │
│                        │                                │
│                        ▼                                │
│  4. MODÉLISATION                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Sélection: Train size, Random state]          │   │
│  │ [Bouton: Entraîner les modèles]               │   │
│  │ → Affichage résultats:                         │   │
│  │   - RMSE Régression                            │   │
│  │   - Accuracy Random Forest                     │   │
│  │   - Graphiques                                 │   │
│  │ → Sauvegarde modèles dans session_state       │   │
│  └─────────────────────────────────────────────────┘   │
│                        │                                │
│                        ▼                                │
│  5. PRÉDICTION                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Input: nb_actions]                             │   │
│  │ [Input: nb_connexions]                          │   │
│  │ [Input: nb_ressources]                          │   │
│  │ [Bouton: Prédire]                              │   │
│  │ → Affichage:                                    │   │
│  │   - Note prédite (Régression)                  │   │
│  │   - Réussite/Échec (Random Forest)            │   │
│  │   - Probabilités                               │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```
---

##  Principaux Algorithmes

###  Algorithme de Feature Engineering

Code implémenté :

```python
features = logs.groupby("pseudo").agg(
    nb_actions=("evenement", "count"),
    nb_connexions=("composant", lambda x: (x == "login").sum()),
    nb_ressources=("contexte", "nunique")
).reset_index()
```

Décomposition algorithmique :

```
ALGORITHME: extract_features(logs)
ENTRÉE: logs DataFrame (16,229 lignes × 5 colonnes)
SORTIE: features DataFrame (95 lignes × 4 colonnes)

DÉBUT
    # Étape 1: Groupement par étudiant
    grouped ← logs.groupby("pseudo")
    # Résultat: GroupBy object avec 95 groupes (1 par étudiant)
    
    # Étape 2: Agrégations multiples
    features ← DataFrame vide
    
    POUR CHAQUE groupe g DANS grouped:
        pseudo ← g.name
        
        # Feature 1: Compter tous les événements
        nb_actions ← COUNT(g["evenement"])
        
        # Feature 2: Compter les login
        nb_connexions ← 0
        POUR CHAQUE ligne IN g:
            SI ligne["composant"] == "login" ALORS
                nb_connexions ← nb_connexions + 1
            FIN SI
        FIN POUR
        
        # Feature 3: Compter contextes uniques
        contextes_uniques ← ENSEMBLE_VIDE
        POUR CHAQUE ligne IN g:
            AJOUTER ligne["contexte"] DANS contextes_uniques
        FIN POUR
        nb_ressources ← TAILLE(contextes_uniques)
        
        # Stocker
        AJOUTER_LIGNE(features, {
            'pseudo': pseudo,
            'nb_actions': nb_actions,
            'nb_connexions': nb_connexions,
            'nb_ressources': nb_ressources
        })
    FIN POUR
    
    RETOURNER features
FIN
```

Complexité :
- Groupby : O(n log n) avec n = 16,229
- Agrégations : O(n) car parcours unique
- Total : O(n log n)

Optimisation Pandas :
Pandas utilise des opérations vectorisées (NumPy) donc beaucoup plus rapide qu'une boucle Python pure.

### Algorithme de Régression Linéaire

Équation mathématique :

```
y = β₀ + β₁·x₁ + β₂·x₂ + β₃·x₃ + ε

Où:
- y = note (variable dépendante)
- x₁ = nb_actions
- x₂ = nb_connexions
- x₃ = nb_ressources
- β₀, β₁, β₂, β₃ = coefficients
- ε = erreur résiduelle
```

Méthode des Moindres Carrés Ordinaires :

```
ALGORITHME: fit_linear_regression(X, y)
ENTRÉE: 
    X: matrice (76, 3) des features d'entraînement
    y: vecteur (76,) des notes d'entraînement
SORTIE: 
    β: vecteur (4,) des coefficients [β₀, β₁, β₂, β₃]

DÉBUT
    # Étape 1: Ajouter colonne de 1 pour intercept
    X_augmented ← AJOUTER_COLONNE(X, ONES(76))
    # Résultat: matrice (76, 4)
    
    # Étape 2: Calcul matriciel
    # Formule: β = (X^T X)^(-1) X^T y
    
    X_transpose ← TRANSPOSER(X_augmented)
    # Shape: (4, 76)
    
    XtX ← MULTIPLIER(X_transpose, X_augmented)
    # Shape: (4, 4) - matrice carrée
    
    XtX_inverse ← INVERSER(XtX)
    # Shape: (4, 4)
    
    Xty ← MULTIPLIER(X_transpose, y)
    # Shape: (4,)
    
    β ← MULTIPLIER(XtX_inverse, Xty)
    # Shape: (4,)
    
    RETOURNER β
FIN
```

Implémentation NumPy équivalente :

```python
import numpy as np

def fit_ols(X, y):
    # Ajouter intercept
    X_aug = np.c_[np.ones(len(X)), X]
    
    # Calcul matriciel
    XtX = X_aug.T @ X_aug
    Xty = X_aug.T @ y
    beta = np.linalg.inv(XtX) @ Xty
    
    return beta

# Résultats obtenus
beta = fit_ols(X_train, y_train)
# beta[0] = β₀ (intercept)
# beta[1] = β₁ (coef nb_actions)
# beta[2] = β₂ (coef nb_connexions)
# beta[3] = β₃ (coef nb_ressources)
```

Complexité :
- Multiplication matricielle : O(n × p²) avec n=76, p=3 → O(76 × 9) = O(684)
- Inversion matrice : O(p³) → O(27)
- Total : O(n × p² + p³) → Très rapide pour nos dimensions

### Algorithme Random Forest

Principe :

```
ALGORITHME: random_forest_classifier(X, y, n_estimators=100)
ENTRÉE: 
    X: features (76, 3)
    y: classes binaires {0, 1} (76,)
    n_estimators: nombre d'arbres
SORTIE: 
    forest: ensemble de 100 arbres de décision

DÉBUT
    forest ← LISTE_VIDE
    
    POUR i DE 1 À 100:
        # Étape 1: Bootstrap sampling (avec remplacement)
        indices ← SAMPLE_AVEC_REMPLACEMENT(0..75, taille=76)
        X_boot ← X[indices]
        y_boot ← y[indices]
        
        # Étape 2: Construire un arbre de décision
        arbre ← CONSTRUIRE_ARBRE(X_boot, y_boot)
        
        # Ajouter à la forêt
        AJOUTER(forest, arbre)
    FIN POUR
    
    RETOURNER forest
FIN

FONCTION: CONSTRUIRE_ARBRE(X, y, profondeur=0, max_profondeur=10)
DÉBUT
    # Condition d'arrêt
    SI profondeur >= max_profondeur OU TOUS_MEME_CLASSE(y):
        RETOURNER FEUILLE(classe_majoritaire(y))
    FIN SI
    
    # Trouver meilleure division
    meilleure_feature ← None
    meilleure_seuil ← None
    meilleur_gain ← -∞
    
    # Random feature subset (√p features)
    features_candidates ← SAMPLE_SANS_REMPLACEMENT(0..2, taille=√3≈2)
    
    POUR CHAQUE feature f DANS features_candidates:
        POUR CHAQUE seuil s DANS VALEURS_UNIQUES(X[:, f]):
            gauche ← X[X[:, f] <= s]
            droite ← X[X[:, f] > s]
            
            gain ← CALCUL_GINI_GAIN(y, gauche, droite)
            
            SI gain > meilleur_gain:
                meilleur_gain ← gain
                meilleure_feature ← f
                meilleure_seuil ← s
            FIN SI
        FIN POUR
    FIN POUR
    
    # Créer nœud
    noeud ← NOEUD(feature=meilleure_feature, seuil=meilleure_seuil)
    
    # Récursion
    X_gauche, y_gauche ← FILTRER(X, y, X[:, meilleure_feature] <= meilleure_seuil)
    X_droite, y_droite ← FILTRER(X, y, X[:, meilleure_feature] > meilleure_seuil)
    
    noeud.gauche ← CONSTRUIRE_ARBRE(X_gauche, y_gauche, profondeur+1, max_profondeur)
    noeud.droite ← CONSTRUIRE_ARBRE(X_droite, y_droite, profondeur+1, max_profondeur)
    
    RETOURNER noeud
FIN

FONCTION: predict_random_forest(forest, X_new)
DÉBUT
    votes ← LISTE_VIDE
    
    POUR CHAQUE arbre DANS forest:
        prediction ← arbre.predict(X_new)
        AJOUTER(votes, prediction)
    FIN POUR
    
    # Vote majoritaire
    prediction_finale ← MODE(votes)
    
    # Calcul probabilités
    proba_classe_1 ← COUNT(votes == 1) / TAILLE(votes)
    proba_classe_0 ← 1 - proba_classe_1
    
    RETOURNER prediction_finale, [proba_classe_0, proba_classe_1]
FIN
```

Implémentation Scikit-learn :

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=100,       # Nombre d'arbres
    random_state=42,        # Reproductibilité
    max_depth=None,         # Profondeur illimitée (défaut)
    min_samples_split=2,    # Min échantillons pour diviser
    min_samples_leaf=1,     # Min échantillons par feuille
    max_features='sqrt'     # √p features par arbre
)

rf.fit(X_train, y_class_train)
```

Complexité :
- Construction 1 arbre : O(n × p × log n) avec n=76, p=3
- 100 arbres : O(100 × 76 × 3 × log 76) ≈ O(100 × 76 × 3 × 6.25) ≈ O(142,500)
- Prédiction : O(100 × log 76) ≈ O(625) → Très rapide

### Métriques d'Évaluation

####  RMSE (Root Mean Squared Error)

```python
ALGORITHME: calcul_rmse(y_true, y_pred)
ENTRÉE: 
    y_true: notes réelles (19,)
    y_pred: notes prédites (19,)
SORTIE: 
    rmse: float

DÉBUT
    n ← TAILLE(y_true)
    somme_carres_erreurs ← 0
    
    POUR i DE 0 À n-1:
        erreur ← y_true[i] - y_pred[i]
        somme_carres_erreurs ← somme_carres_erreurs + erreur²
    FIN POUR
    
    mse ← somme_carres_erreurs / n
    rmse ← RACINE_CARREE(mse)
    
    RETOURNER rmse
FIN
```

Formule mathématique :

```
RMSE = √(1/n × Σ(yᵢ - ŷᵢ)²)

Où:
- n = nombre d'échantillons de test (19)
- yᵢ = note réelle de l'étudiant i
- ŷᵢ = note prédite de l'étudiant i
```

Implémentation Scikit-learn :

```python
from sklearn.metrics import mean_squared_error

rmse = mean_squared_error(y_test, y_pred_reg) ** 0.5
# Ou avec squared=False (si version récente)
rmse = mean_squared_error(y_test, y_pred_reg, squared=False)
```

####  Accuracy

```python
ALGORITHME: calcul_accuracy(y_true, y_pred)
ENTRÉE: 
    y_true: classes réelles {0, 1} (19,)
    y_pred: classes prédites {0, 1} (19,)
SORTIE: 
    accuracy: float [0, 1]

DÉBUT
    n ← TAILLE(y_true)
    correct ← 0
    
    POUR i DE 0 À n-1:
        SI y_true[i] == y_pred[i]:
            correct ← correct + 1
        FIN SI
    FIN POUR
    
    accuracy ← correct / n
    
    RETOURNER accuracy
FIN
```

Formule mathématique :

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)

Où:
- TP = True Positives (réussites bien prédites)
- TN = True Negatives (échecs bien prédits)
- FP = False Positives (échecs prédits comme réussite)
- FN = False Negatives (réussites prédites comme échec)
```

Implémentation Scikit-learn :

```python
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_class_test, y_pred_class)
```

---

## Architecture Technique Détaillée

### Stack Technologique Complète

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                       │
├─────────────────────────────────────────────────────────┤
│  Streamlit 1.20.0                                       │
│  ├─ st.sidebar (Navigation)                             │
│  ├─ st.file_uploader (Upload CSV)                       │
│  ├─ st.dataframe (Affichage données)                    │
│  ├─ st.pyplot (Graphiques)                              │
│  └─ st.session_state (State management)                 │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC                        │
├─────────────────────────────────────────────────────────┤
│  Python 3.10+                                           │
│  ├─ Fonctions de traitement                            │
│  ├─ Pipeline ETL                                        │
│  ├─ Feature engineering                                 │
│  └─ Gestion du flow applicatif                         │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER                           │
├─────────────────────────────────────────────────────────┤
│  Pandas 1.5.0                                           │
│  ├─ DataFrame (structure principale)                    │
│  ├─ Series (vecteurs)                                   │
│  ├─ GroupBy (agrégations)                              │
│  └─ Merge (jointures)                                   │
│                                                         │
│  NumPy 1.23.0                                           │
│  └─ Arrays sous-jacents (optimisation)                  │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                 MACHINE LEARNING LAYER                  │
├─────────────────────────────────────────────────────────┤
│  Scikit-learn 1.2.0                                     │
│  ├─ LinearRegression                                    │
│  ├─ RandomForestClassifier                             │
│  ├─ train_test_split                                    │
│  ├─ mean_squared_error                                  │
│  └─ accuracy_score                                      │
│                                                         │
│  Joblib 1.2.0                                           │
│  └─ Serialization modèles (.pkl)                        │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                VISUALIZATION LAYER                      │
├─────────────────────────────────────────────────────────┤
│  Matplotlib 3.6.0                                       │
│  ├─ pyplot (API haut niveau)                           │
│  └─ Axes (contrôle bas niveau)                         │
│                                                         │
│  Seaborn 0.12.0                                         │
│  └─ Heatmap, histogrammes stylisés                     │
└─────────────────────────────────────────────────────────┘
```

### Diagramme de Flux de Données

```
[logs.csv] [notes.csv]
      │         │
      ▼         ▼
 pd.read_csv() pd.read_csv()
      │         │
      ▼         ▼
[DataFrame]  [DataFrame]
 16,229×5     100×2
      │         │
      ▼         │
 clean_data()   │
      │         │
      ▼         │
[logs_clean]    │
 16,227×5       │
      │         │
      ▼         │
create_features()
      │         │
      ▼         │
  [features]    │
    95×4        │
      │         │
      └────┬────┘
           │
           ▼
     pd.merge()
           │
           ▼
       [data]
        95×5
           │
       ┌───┴───┐
       ▼       ▼
      [X]     [y]
     95×3     95×1
       │       │
       ▼       ▼
 train_test_split()
       │
   ┌───┴───┬───────────┐
   ▼       ▼           ▼
[X_train][y_train][X_test][y_test]
  76×3    76×1     19×3   19×1
   │       │
   └───┬───┘
       │
   ┌───┴───────┐
   ▼           ▼
[Regression][RandomForest]
   │           │
   ▼           ▼
[.pkl]      [.pkl]
```

### Structure des Fichiers

```
projet-arche/
│
├── Main.ipynb                          # Notebook d'entraînement
│   ├─ Cellule 1: Imports
│   ├─ Cellule 2: Chargement données
│   ├─ Cellule 3: Nettoyage
│   ├─ Cellule 4: Feature engineering
│   ├─ Cellule 5: Train/test split
│   ├─ Cellule 6: Régression linéaire
│   ├─ Cellule 7: Random Forest
│   ├─ Cellule 8: Évaluation
│   └─ Cellule 9: Sauvegarde modèles
│
├── Application.py                      # Application Streamlit
│   ├─ Configuration page (ligne 14-18)
│   ├─ CSS personnalisé (ligne 21-42)
│   ├─ Sidebar navigation (ligne 49-54)
│   ├─ Fonctions utilitaires:
│   │   ├─ load_data() (ligne 57-61)
│   │   ├─ clean_data() (ligne 64-75)
│   │   └─ create_features() (ligne 78-84)
│   ├─ Page Accueil (ligne 87-143)
│   ├─ Page ETL (ligne 146-192)
│   ├─ Page Features (ligne 195-259)
│   ├─ Page Modélisation (ligne 262-384)
│   ├─ Page Évaluation (ligne 387-442)
│   ├─ Page Prédiction (ligne 445-509)
│   └─ Footer (ligne 512-519)
│
├── logs_info_25_pseudo.csv             # Données logs
│   ├─ 16,229 lignes
│   └─ 5 colonnes: date, pseudo, contexte, composant, evenement
│
├── notes_info_25_pseudo.csv            # Données notes
│   ├─ 100 lignes
│   └─ 2 colonnes: pseudo, note
│
├── model_regression.pkl                # Modèle sauvegardé (généré)
│   └─ LinearRegression instance sérialisée
│
├── model_random_forest.pkl             # Modèle sauvegardé (généré)
│   └─ RandomForestClassifier instance sérialisée
│
└── requirements.txt                    # Dépendances
    ├─ pandas==1.5.0
    ├─ scikit-learn==1.2.0
    ├─ streamlit==1.20.0
    ├─ matplotlib==3.6.0
    ├─ seaborn==0.12.0
    ├─ joblib==1.2.0
    └─ numpy==1.23.0
```

---

## Documentation du Code

###  Code du Notebook (Main.ipynb)

Imports :
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
```

Chargement :
```python
logs = pd.read_csv("logs_info_25_pseudo.csv")
notes = pd.read_csv("notes_info_25_pseudo.csv")
```

Nettoyage :
```python
if 'date' in logs.columns:
    logs['date'] = pd.to_datetime(logs['date'])
logs = logs.dropna()
notes = notes.dropna()
```

Feature Engineering :
```python
features = logs.groupby("pseudo").agg(
    nb_actions=("evenement", "count"),
    nb_connexions=("composant", lambda x: (x == "login").sum()),
    nb_ressources=("contexte", "nunique")
).reset_index()

data = features.merge(notes, on="pseudo")
```

Préparation ML :
```python
X = data[["nb_actions", "nb_connexions", "nb_ressources"]]
y = data["note"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

Régression :
```python
reg = LinearRegression()
reg.fit(X_train, y_train)
y_pred_reg = reg.predict(X_test)
rmse = mean_squared_error(y_test, y_pred_reg) ** 0.5
```

Random Forest :
```python
data["reussite"] = (data["note"] >= 10).astype(int)
y_class = data["reussite"]
rf = RandomForestClassifier(random_state=42, n_estimators=100)
rf.fit(X_train, y_class.iloc[X_train.index])
y_pred_class = rf.predict(X_test)
acc = accuracy_score(y_class.iloc[X_test.index], y_pred_class)
```

Sauvegarde :
```python
import joblib
joblib.dump(reg, "model_regression.pkl")
joblib.dump(rf, "model_random_forest.pkl")
```

### Code de l'Application (Application.py)

Structure condensée avec annotations :

```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix, classification_report
import joblib
import os

# Configuration
st.set_page_config(page_title="...", page_icon="🎓", layout="wide")

# CSS
st.markdown("""<style>...</style>""", unsafe_allow_html=True)

# Navigation
page = st.sidebar.radio("Choisissez une étape :", [...])

# Fonctions
@st.cache_data
def load_data(logs_file, notes_file):
    # ...

def clean_data(logs, notes):
    # ...

def create_features(logs):
    # ...

# Pages
if page == "🏠 Accueil":
    # ...
elif page == "📁 1. ETL":
    # ...
elif page == "🔧 2. Feature Engineering":
    # ...
# ... etc 
```

---



les references neccessaires à rappeler dans le cadre de la presentation 



