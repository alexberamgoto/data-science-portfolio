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

# Configuration de la page
st.set_page_config(
    page_title="Prédiction de Réussite / Echec Apprenant via ses traces numériques sur plateforme -ARCHE",
    page_icon="🎓",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown('<div class="main-header">Prédiction de Réussite / Echec Apprenant via ses traces numériques sur plateforme -ARCHE</div>',
            unsafe_allow_html=True)
st.markdown("**Builded by AlexDB26**")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Choisissez une étape :",
    ["Accueil", "1. ETL - Chargement des données", "2. Feature Engineering",
     "3. Modélisation", "4. Évaluation", "5. Prédiction"]
)


# Fonction pour charger les données
@st.cache_data
def load_data(logs_file, notes_file):
    logs = pd.read_csv(logs_file)
    notes = pd.read_csv(notes_file)
    return logs, notes


# Fonction pour nettoyer les données
def clean_data(logs, notes):
    # Détection automatique de la colonne de date/heure
    if 'heure' in logs.columns:
        logs['heure'] = pd.to_datetime(logs['heure'], errors='coerce')
    elif 'date' in logs.columns:
        logs['date'] = pd.to_datetime(logs['date'], errors='coerce')
    elif 'time' in logs.columns:
        logs['time'] = pd.to_datetime(logs['time'], errors='coerce')

    logs = logs.dropna()
    notes = notes.dropna()
    return logs, notes


# Fonction pour créer les features
def create_features(logs):
    features = logs.groupby("pseudo").agg(
        nb_actions=("evenement", "count"),
        nb_connexions=("composant", lambda x: (x == "login").sum()),
        nb_ressources=("contexte", "nunique")
    ).reset_index()
    return features


# PAGE 1: ACCUEIL
if page == "Accueil":
    st.header("Bienvenue dans l'application de prédiction")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Problématique

        **Est-il possible de prédire la réussite d'un apprenant en analysant ses 
        traces numériques au sein de la plateforme ARCHE ?**

        Cette application permet de :
        - Analyser les logs d'activité des étudiants
        - Extraire des indicateurs pertinents
        - Comparer deux modèles de Machine Learning
        - Prédire la réussite ou l'échec des étudiants
        """)

    with col2:
        st.markdown("""
        ### Objectifs du Projet

        1. **ETL** : Extraire, nettoyer et transformer les données
        2. **Feature Engineering** : Calculer les meilleurs indicateurs
        3. **Modélisation** : 
           - Régression Linéaire Multiple
           - Random Forest Classifier
        4. **Évaluation** : Comparer les performances
        5. **Prédiction** : Utiliser le meilleur modèle
        """)

    st.markdown("---")

    st.info("**Utilisez le menu à gauche pour naviguer entre les différentes étapes du projet**")

    # Informations sur les données attendues
    st.header("Structure des Données Attendues")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Fichier logs.csv :**
        - `heure` : Horodatage de l'activité
        - `pseudo` : ID de l'apprenant
        - `contexte` : Ressource objet de l'activité
        - `composant` : Type d'activité
        - `evenement` : Précisions sur l'activité
        """)

    with col2:
        st.markdown("""
        **Fichier notes.csv :**
        - `pseudo` : ID de l'apprenant
        - `note` : Note obtenue
        """)

# PAGE 2: ETL
elif page == "1. ETL - Chargement des données":
    st.header("Étape 1 : ETL - Extract, Transform, Load")

    st.markdown("""
    Cette étape permet de charger les fichiers CSV contenant :
    1. Les **logs d'activité** des étudiants sur la plateforme ARCHE
    2. Les **notes** obtenues par les étudiants
    """)

    col1, col2 = st.columns(2)

    with col1:
        logs_file = st.file_uploader("Charger le fichier logs.csv", type=["csv"])

    with col2:
        notes_file = st.file_uploader("Charger le fichier notes.csv", type=["csv"])

    if logs_file and notes_file:
        # Chargement
        logs, notes = load_data(logs_file, notes_file)

        st.success("Fichiers chargés avec succès !")

        # Affichage des données brutes
        st.subheader("Aperçu des Logs")
        st.write(f"**Dimensions :** {logs.shape[0]} lignes × {logs.shape[1]} colonnes")
        st.dataframe(logs.head(10))

        st.subheader("Aperçu des Notes")
        st.write(f"**Dimensions :** {notes.shape[0]} lignes × {notes.shape[1]} colonnes")
        st.dataframe(notes.head(10))

        # Nettoyage
        if st.button("Nettoyer les données"):
            logs_clean, notes_clean = clean_data(logs, notes)

            st.success("Données nettoyées !")
            st.write(f"Logs après nettoyage : {len(logs_clean)} lignes")
            st.write(f"Notes après nettoyage : {len(notes_clean)} lignes")

            # Sauvegarder dans la session
            st.session_state['logs'] = logs_clean
            st.session_state['notes'] = notes_clean

            st.info("Passez à l'étape suivante : **Feature Engineering**")
    else:
        st.warning("Veuillez charger les deux fichiers CSV pour continuer")

# PAGE 3: FEATURE ENGINEERING
elif page == "2. Feature Engineering":
    st.header("Étape 2 : Feature Engineering")

    if 'logs' not in st.session_state or 'notes' not in st.session_state:
        st.warning("Veuillez d'abord charger les données dans l'étape 1")
    else:
        logs = st.session_state['logs']
        notes = st.session_state['notes']

        st.markdown("""
        ### Extraction des Indicateurs

        À partir des logs, nous calculons pour chaque étudiant :
        """)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("nb_actions", "Nombre total d'actions")
        with col2:
            st.metric("nb_connexions", "Nombre de connexions")
        with col3:
            st.metric("nb_ressources", "Nombre de ressources uniques")

        if st.button("Générer les Features"):
            features = create_features(logs)

            st.success("Features générées avec succès !")
            st.dataframe(features.head(10))

            # Fusion avec les notes
            data = features.merge(notes, on="pseudo")

            st.subheader("Statistiques Descriptives")
            st.write(data.describe())

            # Visualisations
            st.subheader("Visualisations")

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots(figsize=(8, 6))
                data[['nb_actions', 'nb_connexions', 'nb_ressources']].boxplot(ax=ax)
                ax.set_title("Distribution des Features")
                ax.set_ylabel("Valeur")
                st.pyplot(fig)

            with col2:
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.hist(data['note'], bins=20, edgecolor='black')
                ax.set_title("Distribution des Notes")
                ax.set_xlabel("Note")
                ax.set_ylabel("Fréquence")
                st.pyplot(fig)

            # Matrice de corrélation
            st.subheader("Matrice de Corrélation")
            fig, ax = plt.subplots(figsize=(10, 8))
            corr = data[['nb_actions', 'nb_connexions', 'nb_ressources', 'note']].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, fmt='.2f')
            st.pyplot(fig)

            # Sauvegarder
            st.session_state['data'] = data
            st.info("Passez à l'étape suivante : **Modélisation**")

# PAGE 4: MODÉLISATION
elif page == "3. Modélisation":
    st.header("Étape 3 : Modélisation")

    if 'data' not in st.session_state:
        st.warning("Veuillez d'abord générer les features dans l'étape 2")
    else:
        data = st.session_state['data']

        st.markdown("""
        ### Comparaison de Deux Approches

        1. **Régression Linéaire Multiple** : Prédit la note exacte (0-20)
        2. **Random Forest Classifier** : Prédit Réussite (≥10) ou Échec (<10)
        """)

        # Paramètres
        st.sidebar.subheader("Paramètres")
        test_size = st.sidebar.slider("Taille de l'ensemble de test", 0.1, 0.4, 0.2, 0.05)
        random_state = st.sidebar.number_input("Random State", value=42)

        # Préparation des données
        X = data[["nb_actions", "nb_connexions", "nb_ressources"]]
        y = data["note"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Taille ensemble d'entraînement", len(X_train))
        with col2:
            st.metric("Taille ensemble de test", len(X_test))

        if st.button("Entraîner les Modèles"):
            with st.spinner("Entraînement en cours..."):
                # RÉGRESSION LINÉAIRE
                st.subheader("1. Régression Linéaire Multiple")

                reg = LinearRegression()
                reg.fit(X_train, y_train)
                y_pred_reg = reg.predict(X_test)
                rmse = mean_squared_error(y_test, y_pred_reg) ** 0.5

                st.write(f"**RMSE :** {rmse:.4f}")

                # Coefficients
                coefficients = pd.DataFrame({
                    "Feature": X.columns,
                    "Coefficient": reg.coef_
                }).sort_values("Coefficient", ascending=False)

                st.write("**Coefficients :**")
                st.dataframe(coefficients)
                st.write(f"**Intercept :** {reg.intercept_:.4f}")

                # Visualisation prédictions vs réalité
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.scatter(y_test, y_pred_reg, alpha=0.6, edgecolors='k')
                ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                        'r--', lw=2, label='Prédiction parfaite')
                ax.set_xlabel('Notes réelles')
                ax.set_ylabel('Notes prédites')
                ax.set_title('Régression Linéaire : Prédictions vs Réalité')
                ax.legend()
                ax.grid(alpha=0.3)
                st.pyplot(fig)

                # RANDOM FOREST
                st.subheader("2. Random Forest Classifier")

                # Créer la cible binaire
                data["reussite"] = (data["note"] >= 10).astype(int)
                y_class = data["reussite"]

                rf = RandomForestClassifier(random_state=random_state, n_estimators=100)
                rf.fit(X_train, y_class.iloc[X_train.index])
                y_pred_class = rf.predict(X_test)

                acc = accuracy_score(y_class.iloc[X_test.index], y_pred_class)

                st.write(f"**Accuracy :** {acc:.4f} ({acc * 100:.2f}%)")

                # Importance des features
                importance = pd.DataFrame({
                    "Feature": X.columns,
                    "Importance": rf.feature_importances_
                }).sort_values("Importance", ascending=False)

                st.write("**Importance des Features :**")
                st.dataframe(importance)

                # Matrice de confusion
                cm = confusion_matrix(y_class.iloc[X_test.index], y_pred_class)

                fig, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                            xticklabels=['Échec', 'Réussite'],
                            yticklabels=['Échec', 'Réussite'])
                ax.set_title('Matrice de Confusion')
                ax.set_ylabel('Classe réelle')
                ax.set_xlabel('Classe prédite')
                st.pyplot(fig)

                # Classification report
                st.write("**Rapport de Classification :**")
                report = classification_report(y_class.iloc[X_test.index], y_pred_class,
                                               target_names=['Échec', 'Réussite'], output_dict=True)
                st.dataframe(pd.DataFrame(report).transpose())

                # Sauvegarde des modèles
                st.session_state['reg_model'] = reg
                st.session_state['rf_model'] = rf
                st.session_state['rmse'] = rmse
                st.session_state['accuracy'] = acc
                st.session_state['X_test'] = X_test
                st.session_state['y_test'] = y_test
                st.session_state['y_class_test'] = y_class.iloc[X_test.index]

                st.success("Modèles entraînés avec succès !")
                st.info("Passez à l'étape suivante : **Évaluation**")

# PAGE 5: ÉVALUATION
elif page == "4. Évaluation":
    st.header("Étape 4 : Évaluation des Modèles")

    if 'reg_model' not in st.session_state or 'rf_model' not in st.session_state:
        st.warning("Veuillez d'abord entraîner les modèles dans l'étape 3")
    else:
        st.markdown("### Comparaison des Performances")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Régression Linéaire</h3>
                <h2 style="color: #1f77b4;">RMSE : {:.4f}</h2>
                <p>Erreur moyenne de prédiction sur les notes</p>
            </div>
            """.format(st.session_state['rmse']), unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>Random Forest</h3>
                <h2 style="color: #2ca02c;">Accuracy : {:.2f}%</h2>
                <p>Taux de prédiction correcte Réussite/Échec</p>
            </div>
            """.format(st.session_state['accuracy'] * 100), unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        ### Conclusion

        **Quel modèle choisir ?**

        - **Régression Linéaire** : Utile pour prédire une note exacte, mais peut être imprécis
        - **Random Forest** : Meilleur pour la classification binaire (Réussite/Échec)

        Pour ce projet, le **Random Forest** est recommandé car :
        1. Meilleure interprétabilité (Réussite vs Échec)
        2. Plus robuste aux valeurs aberrantes
        3. Permet d'identifier les étudiants à risque
        """)

        # Sauvegarde des modèles
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Sauvegarder Régression Linéaire"):
                joblib.dump(st.session_state['reg_model'], "model_regression.pkl")
                st.success("Modèle sauvegardé : model_regression.pkl")

        with col2:
            if st.button("Sauvegarder Random Forest"):
                joblib.dump(st.session_state['rf_model'], "model_random_forest.pkl")
                st.success("Modèle sauvegardé : model_random_forest.pkl")

# PAGE 6: PRÉDICTION
elif page == "5. Prédiction":
    st.header("Étape 5 : Prédiction sur Nouveaux Étudiants")

    if 'rf_model' not in st.session_state:
        st.warning("Veuillez d'abord entraîner les modèles")
    else:
        st.markdown("""
        ### Prédire la réussite d'un nouvel étudiant

        Entrez les caractéristiques d'activité d'un étudiant :
        """)

        col1, col2, col3 = st.columns(3)

        with col1:
            nb_actions = st.number_input("Nombre d'actions", min_value=0, value=100, step=10)

        with col2:
            nb_connexions = st.number_input("Nombre de connexions", min_value=0, value=10, step=1)

        with col3:
            nb_ressources = st.number_input("Nombre de ressources", min_value=0, value=5, step=1)

        if st.button("Prédire"):
            # Préparer les données
            X_new = pd.DataFrame({
                'nb_actions': [nb_actions],
                'nb_connexions': [nb_connexions],
                'nb_ressources': [nb_ressources]
            })

            # Prédiction avec Régression
            reg = st.session_state['reg_model']
            note_pred = reg.predict(X_new)[0]

            # Prédiction avec Random Forest
            rf = st.session_state['rf_model']
            reussite_pred = rf.predict(X_new)[0]
            proba = rf.predict_proba(X_new)[0]

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Régression Linéaire")
                st.metric("Note prédite", f"{note_pred:.2f}/20")

            with col2:
                st.subheader("Random Forest")
                resultat = "RÉUSSITE" if reussite_pred == 1 else "ÉCHEC"
                st.metric("Prédiction", resultat)
                st.write(f"**Probabilité de réussite :** {proba[1] * 100:.1f}%")
                st.write(f"**Probabilité d'échec :** {proba[0] * 100:.1f}%")

            # Visualisation des probabilités
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(['Échec', 'Réussite'], [proba[0], proba[1]],
                    color=['#e74c3c', '#2ecc71'], edgecolor='black')
            ax.set_xlabel('Probabilité')
            ax.set_title('Probabilités de Prédiction')
            ax.set_xlim([0, 1])
            for i, v in enumerate([proba[0], proba[1]]):
                ax.text(v + 0.02, i, f'{v * 100:.1f}%', va='center')
            st.pyplot(fig)



# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px; border-radius: 10px; margin-top: 30px;'>
        <p style='color: white; margin: 0; font-size: 0.9em;'>
            <b>Université de Lorraine - Institut des Sciences du Digital</b><br>
        
    </div>
""", unsafe_allow_html=True)