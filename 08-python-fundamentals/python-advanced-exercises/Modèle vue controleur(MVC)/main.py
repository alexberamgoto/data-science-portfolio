import logging

import streamlit as st
import os

import controleur

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
        os.kill(os.getpid(), 9)
with col1:
    st.subheader("Visualisation")
    if afficher:
        logging.info(f'Fichier selcetionné: {fichier.name}')
        #Recuperation d'un fichier via la methode  vue.get_fig_deces
        m=Modele(fichier)
        serie =controleur.select_data_deces(m.data,departement,date_de,date_a)
        logging.info(f'serie extraite:{serie}')
        fig=Vue.get_fig_deces(serie)
        st.plotly_chart(fig)
    else:
        st.error("Veuillez selectionner un fichier csv")
    else:
    st.info("Cliquez sur 'Afficher' pour visualiser la figure")