
import os
import io
import sys
import pandas as pd
import streamlit as st
import altair as alt

try:
    from Controleur import Controleur
except ModuleNotFoundError:
    try:
        from controleur import Controleur
    except ModuleNotFoundError:
        app_dir = os.path.dirname(os.path.abspath(__file__))
        if app_dir not in sys.path:
            sys.path.insert(0, app_dir)
        try:
            from Controleur import Controleur
        except ModuleNotFoundError:
            from controleur import Controleur

st.set_page_config(page_title="Prédiction Réussite/Échec", layout="wide")
st.title("🎯 Prédiction Réussite / Échec")

with st.sidebar:
    st.header("Paramètres")
    seuil = st.slider("Seuil de réussite (note)", min_value=0.0, max_value=20.0, step=0.5, value=10.0, key="seuil_slider")
    model_path = st.text_input("Chemin du modèle (joblib)", value="model_lr.pkl", key="model_path_input")
    fichier = st.file_uploader("Choisir un fichier logs CSV", type=["csv"], help="Fichier de logs au format train_x/test_x", key="uploader")
    run = st.button("▶️ Analyser", key="analyser_btn")
    st.markdown("---")
    if st.button("❌ Quitter l'application", key="quit_btn"):
        os.kill(os.getpid(), 9)

preds_df = None
counts = None
info = None

if run:
    if fichier is None:
        st.error("Veuillez sélectionner un fichier CSV de logs.")
    else:
        try:
            out = Controleur.methodeA(fichier, seuil=seuil, model_path=model_path)
            if isinstance(out, tuple) and len(out) == 3:
                preds_df, counts, info = out
            else:
                preds_df, counts = out
                info = {"renamed_cols": {}, "synthetic_date": False}
        except Exception as e:
            st.error(f"Erreur pendant la prédiction : {e}")

# Messages d'avertissement (si dispo)
if info is not None:
    msgs = []
    renamed = info.get("renamed_cols", {}) or {}
    if renamed:
        renamed_pairs = ", ".join([f"{k} → {v}" for k, v in renamed.items()])
        msgs.append(f"Certaines colonnes ont été renommées automatiquement : {renamed_pairs}.")
    if info.get("synthetic_date", False):
        msgs.append("La colonne 'date' étant absente, une chronologie synthétique a été générée. Les features temporelles peuvent être moins informatives.")
    if msgs:
        msg_text = "".join(msgs)
        st.warning(msg_text)

col_main, col_side = st.columns([5, 2])

with col_main:
    st.subheader("Visualisation")
    if run and (preds_df is not None) and (counts is not None):
        total = int(counts.sum())
        chart_df = counts.reset_index()
        chart_df.columns = ["Résultat", "Nombre"]
        chart = (
            alt.Chart(chart_df)
            .mark_bar(size=50, cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Résultat:N", sort=["Réussite", "Échec"]),
                y=alt.Y("Nombre:Q"),
                color=alt.Color("Résultat:N", scale=alt.Scale(range=["#4CAF50", "#F44336"]))
            )
        )
        st.altair_chart(chart, use_container_width=True, theme=None)

        st.markdown("### Détail des prédictions")
        st.dataframe(preds_df.sort_values("prediction", ascending=False), use_container_width=True)

        csv_buffer = io.StringIO()
        preds_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="💾 Télécharger les prédictions (CSV)",
            data=csv_buffer.getvalue(),
            file_name="predictions.csv",
            mime="text/csv",
            key="download_preds_btn"
        )
    else:
        st.info("Chargez un CSV de logs dans la barre latérale, réglez le seuil puis cliquez sur **Analyser**.")

with col_side:
    st.subheader("KPI")
    if run and (preds_df is not None) and (counts is not None):
        total = int(counts.sum())
        success = int(counts.get("Réussite", 0))
        failure = int(counts.get("Échec", 0))
        st.metric("Réussites", success, delta=f"{(success/total*100 if total else 0):.1f}%", help="Part des prédictions >= seuil")
        st.metric("Échecs", failure, delta=f"{(failure/total*100 if total else 0):.1f}%", help="Part des prédictions < seuil")
    else:
        st.write("Aucune analyse en cours.")
