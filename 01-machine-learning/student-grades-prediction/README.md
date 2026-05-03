# Student Grades Prediction — Application Tkinter + Notebook

Application desktop **Tkinter** d'analyse et de prédiction des notes étudiantes à partir des traces d'activité, accompagnée du notebook d'analyse exploratoire.

## Objectif
Prédire la **note** ou la **réussite** d'un apprenant à partir de ses logs d'activité (plateforme ARCHE).

## Stack
Python 3.11 · pandas · scikit-learn · Tkinter · matplotlib

## Structure
```
Application.py                # GUI Tkinter (chargement CSV, entraînement, prédiction)
Main.ipynb                    # EDA + comparaison de modèles
Dossier d'analyse projet.md   # Cahier des charges & démarche
Dossier Technique Projet.md   # Architecture technique et choix algorithmiques
logs_info_25_pseudo.csv       # Logs d'activité anonymisés
notes_info_25_pseudo.csv      # Notes anonymisées
```

## Lancer

```bash
pip install pandas scikit-learn matplotlib
python Application.py
```

## Modèles comparés
- Régression linéaire / logistique
- Random Forest
- Métriques : RMSE, accuracy, F1, matrice de confusion
