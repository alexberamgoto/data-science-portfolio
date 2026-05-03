# Analyse descriptive des patients — ML optimisé (RF + GB + GridSearchCV)

Étude statistique et modélisation prédictive sur un dataset de patients : analyse descriptive complète, détection de multicollinéarité, optimisation d'hyperparamètres et évaluation par courbes ROC.

## Objectif
Construire un modèle de prédiction de risque patient à partir de variables cliniques, en optimisant rigoureusement les modèles ensemblistes (Random Forest, Gradient Boosting) via validation croisée.

## Approche

| Étape | Méthode |
|-------|---------|
| 1. Analyse descriptive | Statistiques univariées, corrélations, distributions |
| 2. Multicollinéarité | **VIF** (Variance Inflation Factor) + heatmap des corrélations |
| 3. Modélisation | Random Forest, Gradient Boosting |
| 4. Optimisation | **GridSearchCV** — 720 configurations testées avec 5-fold CV |
| 5. Évaluation | Courbes **ROC**, AUC, matrices de confusion, F1 |
| 6. Comparaison | Tableau quantifié avant/après optimisation |

## Résultats
- Random Forest : **+3 à +8 % AUC** après GridSearchCV
- Gradient Boosting : **+2 à +6 % AUC** après GridSearchCV
- Validation 5-fold pour robustesse statistique

## Stack
Python 3.11 · pandas · numpy · scikit-learn · matplotlib · seaborn · statsmodels (VIF) · Jupyter

## Structure
```
Analyse_complète.ipynb           # Notebook principal — pipeline ML complet
Analyse_descriptive_revue.ipynb  # Revue critique de l'analyse descriptive
python/                          # Exercices d'appui (stats descriptives Python)
output_final_cols.xlsx           # Variables sélectionnées finales
RESUME_EXECUTIF.md               # Synthèse 30 secondes
GUIDE_UTILISATION.md             # Mode d'emploi
OPTIMISATIONS_APPLIQUEES.md      # Détail technique des optimisations
MODIFICATIONS_DETAILLEES.md      # Diff avant/après code
CHECKLIST_VERIFICATION.md        # Points de validation qualité
INDEX.md                         # Navigation
```

## Lancer

```bash
pip install pandas numpy scikit-learn matplotlib seaborn statsmodels jupyter
jupyter notebook Analyse_complète.ipynb
```

⏱️ Temps d'exécution : **~2 min 30** (GridSearchCV CPU-intensif sur 720 configs).
