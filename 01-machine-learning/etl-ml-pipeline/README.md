# ETL & ML Pipeline — Prédiction de la réussite étudiante

Pipeline objet en Python séparant **ETL**, **feature engineering**, **entraînement** et **évaluation**, avec une UI **Streamlit**.

## Objectif
À partir des logs d'activité d'apprenants (LMS) et de leurs notes, construire un score de réussite et comparer plusieurs modèles (Régression Logistique vs Random Forest).

## Stack
Python 3.11 · pandas · scikit-learn · Streamlit

## Structure
```
ETL.py          # Chargement et fusion logs ↔ notes
Feature.py      # Feature engineering (nb activités, contextes, temps)
Model.py        # Entraînement LogReg + RandomForest
Evaluation.py   # Métriques & scoring
App.py          # Interface Streamlit (upload CSV, exécution pipeline)
main.py         # Pipeline batch en CLI
```

## Lancer

```bash
pip install pandas scikit-learn streamlit
streamlit run App.py        # UI
python main.py              # batch
```

Données fournies (anonymisées) : `logs_info_25_pseudo.csv`, `notes_info_25_pseudo.csv`.
