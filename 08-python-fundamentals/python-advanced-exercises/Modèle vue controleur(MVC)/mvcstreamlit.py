import streamlit as st
import os

# Mise en page avec deux colonnes
col1, col2 = st.columns(2)

with col2:

    st.subheader("Paramètres")

    # Paramètre 0 : Chargement du fichier CSV
    fichier = st.file_uploader(
        "Choisir un fichier CSV",
        type=["csv"],
        help="Sélectionnez le fichier CSV contenant les données."
    )

    # Paramètre 1 : Valeur numérique
    departement = st.number_input(
        "Paramètre 1",
        min_value=0,
        help="Entrez une valeur numérique."
    )

    # Paramètre 2 : Date de début
    date_de = st.date_input(
        "Date de début",
        value=None,
        help="Choisissez la date de début."
    )

    # Paramètre 3 : Date de fin
    date_a = st.date_input(
        "Date de fin",
        value=None,
        help="Choisissez la date de fin."
    )

    # Bouton Afficher
    afficher = st.button("Afficher")

    # Bouton pour quitter l'application
    if st.button("❌ Quitter l'application"):
        os.kill(os.getpid(),9)