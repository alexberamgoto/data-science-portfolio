import streamlit as st
import pandas as pd
from pathlib import Path

# Importation de pipeline
from ETL import ETL
from Feature import FeatureEngineering
from Evaluation import Evaluation


# ------------------------------
# CONFIGURATION DE LA PAGE
# ------------------------------
st.set_page_config(
    page_title="Analyse Logs & Notes",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Plateforme d’Analyse : Logs, Notes & Modélisation")
st.markdown("---")


# ------------------------------
# FONCTION : Pipeline complet
# ------------------------------
@st.cache_data(show_spinner=True)
def run_pipeline(log_file, notes_file):
    base_dir = Path(".")

    # 1. ETL
    etl = ETL(
        logs_path=log_file,
        notes_path=notes_file,
        base_dir=base_dir
    )
    logs, notes = etl.load_data()
    merged = etl.merge_data(logs, notes)

    # 2. Features
    feat = FeatureEngineering(merged)
    X, y = feat.build_features()

    return logs, notes, merged, X, y


# ------------------------------
# Upload des fichiers CSV
# ------------------------------
st.sidebar.header("📂 Fichiers d'entrée")

log_file = st.sidebar.file_uploader(
    "Importer le fichier logs",
    type=["csv"],
    key="logs"
)

notes_file = st.sidebar.file_uploader(
    "Importer le fichier notes",
    type=["csv"],
    key="notes"
)


run_button = st.sidebar.button("🚀 Lancer l’analyse")


# ---------------------------------------------------------------------------------------------------
# EXECUTION DU PIPELINE
# ---------------------------------------------------------------------------------------------------
if run_button:

    if not log_file or not notes_file:
        st.error("Veuillez importer **les deux fichiers CSV** avant de lancer l’analyse.")
        st.stop()

    try:
        # Sauvegarde temporaire des fichiers uploadés
        logs_path = "uploaded_logs.csv"
        notes_path = "uploaded_notes.csv"

        with open(logs_path, "wb") as f:
            f.write(log_file.getbuffer())

        with open(notes_path, "wb") as f:
            f.write(notes_file.getbuffer())

        logs, notes, merged, X, y = run_pipeline(
            logs_path,
            notes_path
        )

        st.success("Pipeline exécuté avec succès 🎉")

        # ------------------------------------------------------
        # AFFICHAGE DES DONNÉES
        # ------------------------------------------------------
        st.subheader("📘 Aperçu des données Logs")
        st.dataframe(logs.head(20))

        st.subheader("📝 Aperçu des données Notes")
        st.dataframe(notes.head(20))

        st.subheader("🔗 Données fusionnées (Merged)")
        st.dataframe(merged.head(20))

        # ------------------------------------------------------
        # AFFICHAGE FEATURES
        # ------------------------------------------------------
        st.subheader("🧬 Features générées")
        st.write("Dimensions : ", X.shape)
        st.dataframe(X.head())

        # ------------------------------------------------------
        # MODELISATION
        # ------------------------------------------------------
        st.header("🤖 Modèle : Entraînement et Évaluation")

        if y is None:
            st.warning("⚠️ Aucune colonne cible détectée : Impossible d’entraîner un modèle.")
        else:
            evaluator = Evaluation()
            model, score, y_pred = evaluator.train(X, y)

            st.success("Modèle entraîné avec succès !")

            st.metric("Score du modèle", f"{score:.4f}")

            st.subheader("📉 Prédictions (échantillon)")
            preview = pd.DataFrame({
                "Réel": y[:20],
                "Prédit": y_pred[:20]
            })
            st.dataframe(preview)

            st.subheader("📈 Visualisation des erreurs")
            st.line_chart(y[:200] - y_pred[:200])

    except Exception as e:
        st.error(f"❌ Une erreur est survenue : {e}")

else:
    st.info("👉 Importez vos CSV puis cliquez sur **Lancer l’analyse**.")


st.markdown("---")
st.caption("Application Streamlit générée automatiquement – Projet Analyse Logs & Notes")