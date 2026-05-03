import os
import logging
import streamlit as st

from modele import Modele
from controleur import Controleur
from vue import Vue



# Utiliser toute la largeur de la fenêtre
st.set_page_config(layout="wide")

logging.basicConfig(level=logging.INFO)

st.title("Application de visualisation des décès COVID-19")

# ==========================
# Colonnes : gauche = visualisation / droite = paramètres
# ==========================
col1, col2 = st.columns([4, 1])   # <-- colonne gauche 4x plus large

# ==========================
# Colonne de droite : paramètres
# ==========================
with col2:
    st.subheader("Paramètres")

    # Paramètre 0 : fichier CSV
    fichier = st.file_uploader(
        "Choisir un fichier CSV",
        type=["csv"],
        help="Sélectionnez le fichier CSV contenant les données."
    )

    # Code du département
    departement = st.number_input(
        "Code département",
        min_value=0,
        step=1,
        help="Ex : 1 = Ain, 57 = Moselle (0 = France entière)"
    )

    # Dates
    date_de = st.date_input("Date de début")
    date_a = st.date_input("Date de fin")

    # Bouton d'affichage
    afficher = st.button("Afficher")

    # deconnexion
    if st.button("❌ Quitter l'application"):
        os.kill(os.getpid(), 9)


# ==========================
# Colonne de gauche : visualisation (grande zone)
# ==========================
with col1:
    st.subheader("Visualisation")

    if afficher:
        if date_de > date_a:
            st.error("La date de début doit être inférieure ou égale à la date de fin.")
        else:
            if fichier is not None:
                logging.info(f"Fichier sélectionné : {fichier.name}")

                # Charger le modèle
                m = Modele(fichier)

                # Filtrer
                serie = Controleur.select_data(
                    m,
                    departement=departement,
                    date_de=date_de,
                    date_a=date_a,
                )

                if serie.empty:
                    st.warning("Aucune donnée à afficher pour ces paramètres.")
                else:
                    fig = Vue.get_fig_deces(serie)

                    # Affichage grande largeur
                    st.pyplot(fig, use_container_width=True)

            else:
                st.error("Veuillez sélectionner un fichier CSV.")
    else:
        st.info("Choisissez vos paramètres à droite puis cliquez sur **Afficher**.")
