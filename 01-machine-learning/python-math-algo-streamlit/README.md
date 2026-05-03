
# Projet ARCHE – Prédiction de la réussite

## Objectif
Modéliser la réussite (ou la **note**) d’un apprenant à partir des **logs ARCHE** et des **notes**, comparer une **régression multiple** avec une approche **IA/ML** (RandomForest), et **évaluer** les modèles.

## Jeux de données fournis
- `logs_info_25_pseudo.csv` — traces d’activité (colonnes: `heure, pseudo, contexte, composant, evenement`).
- `notes_info_25_pseudo.csv` — notes (colonnes: `pseudo, note`).

> Schémas et livrables tels que précisés dans le cahier des charges (ETL, features, modélisation, évaluation, livrables, **deadline 01/02/2026**).

## Installation
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Exécution (pipeline batch)
```bash
python pipeline.py --logs logs_info_25_pseudo.csv --notes notes_info_25_pseudo.csv   --sep ',' --success-threshold 10 --outdir outputs
```

## Interface Streamlit
```bash
streamlit run app_streamlit.py
```

## Sorties
- `features.csv` — indicateurs par apprenant
- `metrics_regression.json`, `metrics_classification.json` — métriques
- `figures/` — importances, prédictions vs réel, résidus, matrices de confusion
- `Dossier_technique_ARCHE_final.docx`, `Dossier_analyse_ARCHE_final.docx` — documents prêts à déposer
- `Soutenance_ARCHE.pptx` — diaporama de soutenance

## Reproductibilité & confidentialité
- Random state fixé, transformations standardisées.
- Données **anonymisées**, aucun identifiant nominatif dans les livrables.
