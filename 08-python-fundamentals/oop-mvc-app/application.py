"""
application.py
Application Streamlit complète pour la prédiction de réussite
Projet : Prédiction de Réussite Étudiante - ARCHE
Formation : FC Data Scientist 2025-2026
"""

import streamlit as st
import pandas as pd
import joblib

# Configuration de la page
st.set_page_config(
    page_title="Prédiction Réussite ARCHE",
    page_icon="🎓",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown('<div class="main-header">🎓 Prédiction de Réussite Étudiante</div>', 
            unsafe_allow_html=True)
st.markdown("**Plateforme ARCHE - Université de Lorraine**")

# Charger le modèle
@st.cache_resource
def charger_modele():
    """Charge le modèle de régression linéaire"""
    try:
        modele = joblib.load('model_lr.pkl')
        return modele
    except:
        return None

modele = charger_modele()

if modele is None:
    st.error("""
    ❌ **Modèle non trouvé !**
    
    Veuillez d'abord exécuter le notebook `main.ipynb` pour entraîner et sauvegarder le modèle.
    """)
    st.stop()

# Sidebar
st.sidebar.header("ℹ️ Informations")
st.sidebar.markdown("""
### 📚 Features Utilisées

**nb_actions**  
Nombre total d'événements enregistrés pour l'étudiant.

**nb_connexions**  
Nombre de fois que l'étudiant s'est connecté à la plateforme.

**nb_ressources**  
Nombre de ressources différentes consultées par l'étudiant.

---

### 🎯 Seuil de Réussite

Une note **≥ 10/20** indique une réussite probable.

---

### 📊 À propos du Modèle

**Type :** Régression Linéaire Multiple  
**Algorithme :** Moindres Carrés Ordinaires  
**Entraînement :** Données ARCHE 2024-2025

---

### 👨‍🎓 Projet

**Formation :** FC Data Scientist 2025-2026  
**Institution :** Université de Lorraine - IDMC  
**Contact :** azim.roussanaly@univ-lorraine.fr
""")

# Description
st.markdown("""
### 📋 À propos

Cette application utilise le **Machine Learning** pour prédire la réussite 
des étudiants en analysant leurs traces numériques sur la plateforme ARCHE.

**Modèle utilisé :** Régression Linéaire Multiple
""")

st.markdown("---")

# Formulaire de saisie
st.markdown("### 📝 Profil de l'Étudiant")
st.markdown("Entrez les caractéristiques d'activité de l'étudiant :")

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

with col2:
    nb_connexions = st.number_input(
        "🔑 Nombre de connexions",
        min_value=0,
        max_value=1000,
        value=10,
        step=1,
        help="Nombre de fois que l'étudiant s'est connecté"
    )

with col3:
    nb_ressources = st.number_input(
        "📚 Nombre de ressources",
        min_value=0,
        max_value=500,
        value=5,
        step=1,
        help="Nombre de ressources différentes consultées"
    )

# Validation des inputs
valide = True
if nb_connexions > nb_actions:
    st.warning("⚠️ Le nombre de connexions ne peut pas dépasser le nombre d'actions")
    valide = False

if nb_ressources > nb_actions:
    st.warning("⚠️ Le nombre de ressources ne peut pas dépasser le nombre d'actions")
    valide = False

# Bouton de prédiction
if st.button("🔮 Prédire la Réussite", type="primary", use_container_width=True) and valide:
    
    # Créer le DataFrame pour la prédiction
    X = pd.DataFrame({
        'nb_actions': [nb_actions],
        'nb_connexions': [nb_connexions],
        'nb_ressources': [nb_ressources]
    })
    
    # Prédire
    note_predite = modele.predict(X)[0]
    
    # S'assurer que la note est entre 0 et 20
    note_predite = max(0, min(20, note_predite))
    
    # Afficher les résultats
    st.markdown("---")
    st.markdown("### 📊 Résultats de la Prédiction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Note Prédite",
            value=f"{note_predite:.2f} / 20"
        )
    
    with col2:
        if note_predite >= 10:
            st.success("✅ RÉUSSITE PROBABLE")
            st.markdown(f"**Confiance :** {((note_predite-10)/10*100):.0f}%")
        else:
            st.error("❌ ÉCHEC PROBABLE")
            st.markdown(f"**Écart au seuil :** {10-note_predite:.2f} points")
    
    # Barre de progression
    st.markdown("#### 📈 Visualisation")
    progress = note_predite / 20
    st.progress(progress)
    
    # Interprétation
    st.markdown("#### 💡 Interprétation")
    
    if note_predite >= 16:
        st.info("""
        **Excellent profil** 🌟  
        L'étudiant montre une activité très élevée et devrait réussir 
        brillamment. Continue comme ça !
        """)
    elif note_predite >= 12:
        st.info("""
        **Bon profil** ✅  
        L'étudiant a une activité satisfaisante et devrait réussir 
        sans difficulté majeure.
        """)
    elif note_predite >= 10:
        st.warning("""
        **Profil limite** ⚠️  
        L'étudiant est proche du seuil de réussite. Un accompagnement 
        pourrait être bénéfique pour consolider ses acquis.
        """)
    else:
        st.error("""
        **Profil à risque** 🚨  
        L'activité de l'étudiant est faible. Un accompagnement urgent 
        est recommandé pour éviter l'échec.
        """)
    
    # Coefficients du modèle
    with st.expander("📊 Coefficients du Modèle (Avancé)"):
        st.markdown("**Équation de régression :**")
        st.latex(r"""
        \text{Note} = \beta_0 + \beta_1 \times \text{actions} + 
        \beta_2 \times \text{connexions} + \beta_3 \times \text{ressources}
        """)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("β₀ (Intercept)", f"{modele.intercept_:.4f}")
        with col2:
            st.metric("β₁ (Actions)", f"{modele.coef_[0]:.6f}")
        with col3:
            st.metric("β₂ (Connexions)", f"{modele.coef_[1]:.6f}")
        with col4:
            st.metric("β₃ (Ressources)", f"{modele.coef_[2]:.6f}")
        
        st.markdown("""
        **Interprétation :**
        - Un coefficient **positif** signifie qu'une augmentation de cette feature 
          entraîne une augmentation de la note.
        - Plus le coefficient est **élevé**, plus la feature est importante.
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <small>
    🎓 Université de Lorraine - IDMC | FC Data Scientist 2025-2026<br>
    Projet : Prédiction de Réussite via Traces Numériques ARCHE
    </small>
</div>
""", unsafe_allow_html=True)
