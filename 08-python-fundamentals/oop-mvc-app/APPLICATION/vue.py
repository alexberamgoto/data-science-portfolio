"""
vue.py
Classe Vue - Interface utilisateur avec Streamlit
Architecture MVC pour l'application Streamlit
Projet : Prédiction de Réussite Étudiante
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Vue:
    """
    Classe pour gérer l'affichage de l'interface utilisateur
    
    Cette classe gère :
    - L'affichage des composants Streamlit
    - Les inputs utilisateur
    - Les résultats de prédiction
    """
    
    def __init__(self):
        """Initialise la Vue"""
        self.configurer_page()
        self.appliquer_style()
    
    def configurer_page(self):
        """Configure la page Streamlit"""
        st.set_page_config(
            page_title="Prédiction Réussite ARCHE",
            page_icon="🎓",
            layout="wide"
        )
    
    def appliquer_style(self):
        """Applique le CSS personnalisé"""
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
            .metric-card {
                background-color: #f0f9ff;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #3b82f6;
                margin: 10px 0;
            }
            </style>
        """, unsafe_allow_html=True)
    
    def afficher_entete(self):
        """Affiche l'en-tête de l'application"""
        st.markdown('<div class="main-header">🎓 Prédiction de Réussite Étudiante</div>', 
                    unsafe_allow_html=True)
        st.markdown("**Plateforme ARCHE - Université de Lorraine**")
        st.markdown("---")
    
    def afficher_description(self):
        """Affiche la description du projet"""
        st.markdown("""
        ### 📋 À propos
        
        Cette application utilise le **Machine Learning** pour prédire la réussite 
        des étudiants en analysant leurs traces numériques sur la plateforme ARCHE.
        
        **Modèle utilisé :** Régression Linéaire Multiple
        
        **Problématique :** Est-il possible de prédire la réussite d'un apprenant 
        en analysant ses traces numériques au sein de la plateforme ARCHE ?
        """)
    
    def afficher_formulaire(self):
        """
        Affiche le formulaire de saisie des données
        
        Returns:
            tuple: (nb_actions, nb_connexions, nb_ressources)
        """
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
                help="Nombre total d'événements enregistrés sur ARCHE"
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
        
        return nb_actions, nb_connexions, nb_ressources
    
    def afficher_bouton_prediction(self):
        """
        Affiche le bouton de prédiction
        
        Returns:
            bool: True si le bouton est cliqué
        """
        return st.button("🔮 Prédire la Réussite", type="primary", use_container_width=True)
    
    def afficher_resultats(self, note_predite):
        """
        Affiche les résultats de la prédiction
        
        Args:
            note_predite (float): Note prédite par le modèle
        """
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
                confiance = min(((note_predite-10)/10*100), 100)
                st.markdown(f"**Confiance :** {confiance:.0f}%")
            else:
                st.error("❌ ÉCHEC PROBABLE")
                st.markdown(f"**Écart au seuil :** {10-note_predite:.2f} points")
        
        # Barre de progression
        st.markdown("#### 📈 Visualisation de la Note")
        progress = note_predite / 20
        st.progress(progress)
        
        # Graphique jauge
        self.afficher_jauge(note_predite)
        
        # Interprétation
        self.afficher_interpretation(note_predite)
    
    def afficher_jauge(self, note_predite):
        """
        Affiche une jauge visuelle de la note
        
        Args:
            note_predite (float): Note prédite
        """
        fig, ax = plt.subplots(figsize=(8, 2))
        
        # Créer la jauge
        colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71']
        positions = [0, 10, 12, 20]
        
        for i in range(len(colors)):
            if i < len(positions) - 1:
                ax.barh(0, positions[i+1] - positions[i], left=positions[i], 
                       height=0.5, color=colors[i], alpha=0.3, edgecolor='black')
        
        # Ajouter la position de la note
        ax.scatter([note_predite], [0], s=500, c='red', marker='v', 
                  edgecolors='black', linewidths=2, zorder=5)
        ax.text(note_predite, -0.15, f'{note_predite:.1f}', 
               ha='center', fontsize=14, fontweight='bold')
        
        # Ligne de seuil
        ax.axvline(10, color='black', linestyle='--', linewidth=2, label='Seuil (10/20)')
        
        ax.set_xlim(0, 20)
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([])
        ax.set_xlabel('Note', fontsize=12)
        ax.legend(loc='upper right')
        ax.grid(axis='x', alpha=0.3)
        
        st.pyplot(fig)
        plt.close()
    
    def afficher_interpretation(self, note_predite):
        """
        Affiche l'interprétation de la note
        
        Args:
            note_predite (float): Note prédite
        """
        st.markdown("#### 💡 Interprétation et Recommandations")
        
        if note_predite >= 16:
            st.info("""
            **Excellent profil** 🌟  
            
            L'étudiant montre une activité très élevée et devrait réussir 
            brillamment. 
            
            **Recommandations :**
            - Encourager à maintenir ce niveau d'engagement
            - Proposer des ressources supplémentaires pour approfondir
            - Potentiel pour devenir tuteur pour d'autres étudiants
            """)
        elif note_predite >= 12:
            st.info("""
            **Bon profil** ✅  
            
            L'étudiant a une activité satisfaisante et devrait réussir 
            sans difficulté majeure.
            
            **Recommandations :**
            - Continue sur cette lancée
            - Participer activement aux sessions de TD
            - Explorer des ressources complémentaires
            """)
        elif note_predite >= 10:
            st.warning("""
            **Profil limite** ⚠️  
            
            L'étudiant est proche du seuil de réussite. Un accompagnement 
            pourrait être bénéfique pour consolider ses acquis.
            
            **Recommandations :**
            - Augmenter le temps consacré à la plateforme
            - Consulter plus de ressources variées
            - Participer aux séances de tutorat
            - Contacter l'enseignant en cas de difficulté
            """)
        else:
            st.error("""
            **Profil à risque** 🚨  
            
            L'activité de l'étudiant est faible. Un accompagnement urgent 
            est recommandé pour éviter l'échec.
            
            **Actions urgentes :**
            - **Contact immédiat** avec l'étudiant
            - Mise en place d'un suivi personnalisé
            - Augmentation significative de l'activité sur ARCHE
            - Participation obligatoire aux séances de soutien
            - Évaluation des difficultés rencontrées
            """)
    
    def afficher_coefficients(self, coefficients):
        """
        Affiche les coefficients du modèle
        
        Args:
            coefficients (dict): Dictionnaire des coefficients
        """
        with st.expander("📊 Détails du Modèle - Coefficients de Régression"):
            st.markdown("**Équation de régression linéaire multiple :**")
            st.latex(r"""
            \text{Note} = \beta_0 + \beta_1 \times \text{nb\_actions} + 
            \beta_2 \times \text{nb\_connexions} + \beta_3 \times \text{nb\_ressources}
            """)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("β₀ (Intercept)", f"{coefficients['intercept']:.4f}")
            with col2:
                st.metric("β₁ (Actions)", f"{coefficients['nb_actions']:.6f}")
            with col3:
                st.metric("β₂ (Connexions)", f"{coefficients['nb_connexions']:.6f}")
            with col4:
                st.metric("β₃ (Ressources)", f"{coefficients['nb_ressources']:.6f}")
            
            st.markdown("""
            **Interprétation des coefficients :**
            
            - **β₀ (Intercept)** : Note de base (quand toutes les features = 0)
            - **β₁ (Actions)** : Impact d'une action supplémentaire sur la note
            - **β₂ (Connexions)** : Impact d'une connexion supplémentaire
            - **β₃ (Ressources)** : Impact d'une ressource supplémentaire consultée
            
            **Note :** Un coefficient **positif** indique que l'augmentation 
            de cette feature entraîne une augmentation de la note prédite.
            """)
            
            # Graphique des coefficients
            self.afficher_graphique_coefficients(coefficients)
    
    def afficher_graphique_coefficients(self, coefficients):
        """
        Affiche un graphique des coefficients
        
        Args:
            coefficients (dict): Coefficients du modèle
        """
        fig, ax = plt.subplots(figsize=(10, 4))
        
        features = ['nb_actions', 'nb_connexions', 'nb_ressources']
        valeurs = [coefficients[f] for f in features]
        colors = ['#3b82f6' if v > 0 else '#ef4444' for v in valeurs]
        
        ax.barh(features, valeurs, color=colors, edgecolor='black', alpha=0.7)
        ax.set_xlabel('Coefficient', fontsize=12)
        ax.set_title('Importance des Features', fontsize=14, fontweight='bold')
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(axis='x', alpha=0.3)
        
        # Ajouter les valeurs
        for i, v in enumerate(valeurs):
            ax.text(v, i, f' {v:.6f}', va='center', fontsize=10)
        
        st.pyplot(fig)
        plt.close()
    
    def afficher_erreur(self, message):
        """
        Affiche un message d'erreur
        
        Args:
            message (str): Message d'erreur
        """
        st.error(f"❌ {message}")
    
    def afficher_avertissement(self, message):
        """
        Affiche un message d'avertissement
        
        Args:
            message (str): Message d'avertissement
        """
        st.warning(f"⚠️ {message}")
    
    def afficher_succes(self, message):
        """
        Affiche un message de succès
        
        Args:
            message (str): Message de succès
        """
        st.success(f"✅ {message}")
    
    def afficher_sidebar(self):
        """Affiche la barre latérale avec des informations"""
        st.sidebar.header("ℹ️ Informations")
        
        st.sidebar.markdown("""
        ### 📚 Features Utilisées
        
        **nb_actions**  
        Nombre total d'événements enregistrés pour l'étudiant sur la plateforme ARCHE.
        
        **nb_connexions**  
        Nombre de fois que l'étudiant s'est connecté à la plateforme.
        
        **nb_ressources**  
        Nombre de ressources pédagogiques différentes consultées par l'étudiant.
        
        ---
        
        ### 🎯 Seuil de Réussite
        
        Une note **≥ 10/20** indique une réussite probable.
        
        - **16-20** : Excellent
        - **12-16** : Bien
        - **10-12** : Limite
        - **0-10** : À risque
        
        ---
        
        ### 📊 À propos du Modèle
        
        **Type :** Régression Linéaire Multiple  
        **Algorithme :** Moindres Carrés Ordinaires (OLS)  
        **Entraînement :** Données ARCHE 2024-2025  
        **Features :** 3 indicateurs d'activité
        
        ---
        
        ### 🔧 Méthodologie
        
        1. **ETL** : Extraction et nettoyage des données
        2. **Feature Engineering** : Calcul des indicateurs
        3. **Modélisation** : Régression linéaire
        4. **Évaluation** : RMSE, R², MAE
        5. **Déploiement** : Application Streamlit
        
        ---
        
        ### 👨‍🎓 Projet Académique
        
        **Formation :** FC Data Scientist 2025-2026  
        **Institution :** Université de Lorraine - IDMC  
        **Encadrant :** azim.roussanaly@univ-lorraine.fr  
        **Date limite :** 01/02/2026
        """)
    
    def afficher_footer(self):
        """Affiche le pied de page"""
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <small>
            🎓 <b>Université de Lorraine - IDMC</b><br>
            Formation Continue Data Scientist 2025-2026<br>
            Projet : Prédiction de Réussite via Traces Numériques ARCHE<br><br>
            <i>Problématique : Est-il possible de prédire la réussite d'un apprenant 
            en analysant ses traces numériques au sein de la plateforme ARCHE ?</i>
            </small>
        </div>
        """, unsafe_allow_html=True)
    
    def afficher_statistiques_modele(self, stats):
        """
        Affiche les statistiques du modèle
        
        Args:
            stats (dict): Dictionnaire avec les statistiques
        """
        with st.expander("📈 Statistiques du Modèle"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'rmse' in stats:
                    st.metric("RMSE", f"{stats['rmse']:.4f}")
            
            with col2:
                if 'r2' in stats:
                    st.metric("R² Score", f"{stats['r2']:.4f}")
            
            with col3:
                if 'mae' in stats:
                    st.metric("MAE", f"{stats['mae']:.4f}")
            
            st.markdown("""
            **Interprétation des métriques :**
            
            - **RMSE** (Root Mean Squared Error) : Erreur moyenne en points
            - **R²** : Qualité de l'ajustement (0-1, plus proche de 1 = meilleur)
            - **MAE** (Mean Absolute Error) : Erreur absolue moyenne
            """)
