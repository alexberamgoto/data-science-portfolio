# views/app_streamlit.py
import streamlit as st
import pandas as pd
import joblib
from models.feature_builder import FeatureBuilder

st.set_page_config(page_title="ARCH E - Prédiction", layout="wide")

st.title("Application ARCHE (MVC + Streamlit)")

st.sidebar.header("Configuration")

uploaded_logs = st.sidebar.file_uploader("Fichier logs CSV", type=["csv"])
uploaded_notes = st.sidebar.file_uploader("Fichier notes CSV (optionnel, pour métriques)", type=["csv"])

threshold = st.sidebar.number_input("Seuil de réussite (note)", value=10.0)
model_path = st.sidebar.text_input("Chemin du modèle RF", "outputs/best_model_rf.joblib")

if st.sidebar.button("Lancer la prédiction"):
    if uploaded_logs is None:
        st.error("Veuillez charger au moins le fichier de logs.")
    else:
        logs = pd.read_csv(uploaded_logs, dtype=str)
        logs.columns = [c.replace('’', "'").strip().lower() for c in logs.columns]
        logs = logs.rename(columns={"nom de l'événement": 'evenement'})
        logs['heure'] = pd.to_datetime(logs.get('heure'), errors='coerce')
        logs['pseudo'] = logs['pseudo'].astype(str).str.strip()

        fb = FeatureBuilder()
        feats = fb.build_features(logs)

        st.subheader("Features extraites")
        st.dataframe(feats.head())

        try:
            model = joblib.load(model_path)
        except Exception as e:
            st.error(f"Impossible de charger le modèle : {e}")
        else:
            X = feats.drop(columns=['pseudo'])
            y_pred = model.predict(X)

            st.subheader("Prédictions de note")
            result_df = feats[['pseudo']].copy()
            result_df['note_predite'] = y_pred
            result_df['reussi'] = (result_df['note_predite'] >= threshold).astype(int)

            st.dataframe(result_df.head())

            nb_reussite = int(result_df['reussi'].sum())
            nb_total = int(len(result_df))
            nb_echec = nb_total - nb_reussite

            st.metric("Nombre d'admis (prédits)", nb_reussite)
            st.metric("Nombre d'échecs (prédits)", nb_echec)

            st.bar_chart(result_df['reussi'].value_counts())
