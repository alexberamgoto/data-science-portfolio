#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(logs_path, notes_path, sep=','):
    logs = pd.read_csv(logs_path, sep=sep, dtype=str)
    notes = pd.read_csv(notes_path, sep=sep, dtype=str)
    logs.columns  = [c.replace('’', "'").strip().lower() for c in logs.columns]
    notes.columns = [c.replace('’', "'").strip().lower() for c in notes.columns]
    logs = logs.rename(columns={"nom de l'événement": 'evenement'})
    logs['heure'] = pd.to_datetime(logs.get('heure'), errors='coerce')
    notes['note'] = pd.to_numeric(notes.get('note'), errors='coerce')
    logs['pseudo'] = logs['pseudo'].astype(str).str.strip()
    notes['pseudo'] = notes['pseudo'].astype(str).str.strip()
    return logs, notes

def build_features(logs: pd.DataFrame) -> pd.DataFrame:
    logs['jour'] = logs['heure'].dt.date
    def _cumul_temps(series_datetime: pd.Series) -> int:
        x = pd.to_datetime(series_datetime, errors='coerce').dropna().sort_values()
        if x.size < 2: return 0
        diffs = x.diff().dt.total_seconds().iloc[1:]
        return int(diffs[(diffs > 0) & (diffs < 300)].sum())
    grp = logs.groupby('pseudo')
    feats = pd.DataFrame({'pseudo': grp.size().index})
    feats['events_total'] = grp.size().values
    feats['jours_actifs'] = grp['jour'].nunique().values
    feats['contexts_unique'] = grp['contexte'].nunique().values if 'contexte' in logs.columns else 0
    if 'composant' in logs.columns:
        comp_counts = logs.pivot_table(index='pseudo', columns='composant', values='evenement', aggfunc='count', fill_value=0)
        comp_counts.columns = [f"comp_{str(c).strip().lower()}" for c in comp_counts.columns]
        feats = feats.merge(comp_counts, left_on='pseudo', right_index=True, how='left')
    feats['temps_actif_s'] = feats['pseudo'].map(grp['heure'].apply(_cumul_temps))
    last_activity = grp['heure'].max(); max_date = logs['heure'].max()
    def _recence(p):
        la = last_activity.get(p)
        if pd.notnull(la) and pd.notnull(max_date):
            return (max_date - la).days
        return 0
    feats['recence_jours'] = feats['pseudo'].map(_recence)
    return feats.fillna(0)


def main():
    ap = argparse.ArgumentParser(description='ARCH E pipeline CLI')
    ap.add_argument('--logs', required=True)
    ap.add_argument('--notes', required=True)
    ap.add_argument('--sep', default=',')
    ap.add_argument('--success-threshold', type=float, default=10.0)
    ap.add_argument('--outdir', default='outputs')
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    os.makedirs(os.path.join(args.outdir,'figures'), exist_ok=True)

    logs, notes = load_data(args.logs, args.notes, sep=args.sep)
    feats = build_features(logs)
    feats.to_csv(os.path.join(args.outdir,'features.csv'), index=False)

    data = feats.merge(notes[['pseudo','note']], on='pseudo', how='inner')
    X = data.drop(columns=['pseudo','note']); y = data['note']

    # Regression
    num_cols = X.columns.tolist()
    preproc  = ColumnTransformer([('scale', StandardScaler(), num_cols)], remainder='drop')
    lin_pipe = Pipeline([('preproc', preproc), ('model', LinearRegression())])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    lin_pipe.fit(X_train, y_train)
    y_pred_lin = lin_pipe.predict(X_test)
    metrics_lin = {
        'MAE': float(mean_absolute_error(y_test, y_pred_lin)),
        'RMSE': float(np.sqrt(mean_squared_error(y_test, y_pred_lin))),
        'R2': float(r2_score(y_test, y_pred_lin))
    }

    rf_pipe = Pipeline([('preproc', preproc), ('model', RandomForestRegressor(random_state=42))])
    rf_pipe.fit(X_train, y_train)
    y_pred_rf = rf_pipe.predict(X_test)
    metrics_rf = {
        'MAE': float(mean_absolute_error(y_test, y_pred_rf)),
        'RMSE': float(np.sqrt(mean_squared_error(y_test, y_pred_rf))),
        'R2': float(r2_score(y_test, y_pred_rf))
    }

    with open(os.path.join(args.outdir,'metrics_regression.json'),'w') as f:
        json.dump({'linear_regression': metrics_lin, 'random_forest': metrics_rf}, f, indent=2)

    # Feature importances
    try:
        rf = rf_pipe.named_steps['model']
        importances = rf.feature_importances_
        order = importances.argsort()[::-1]
        plt.figure(figsize=(8, max(4, len(num_cols)*0.25)))
        plt.barh(np.array(num_cols)[order][::-1], np.array(importances)[order][::-1])
        plt.title('Importance des variables (RF)')
        plt.xlabel('Importance')
        plt.tight_layout()
        plt.savefig(os.path.join(args.outdir,'figures','feature_importances_rf.png'), dpi=150)
        plt.close()
    except Exception:
        pass

    # Classification
    success = (y >= args.success_threshold).astype(int)
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(X, success, test_size=0.25, random_state=42, stratify=success)

    log_pipe = Pipeline([('preproc', preproc), ('model', LogisticRegression(max_iter=1000))])
    log_pipe.fit(Xc_train, yc_train)
    y_proba_log = log_pipe.predict_proba(Xc_test)[:,1]
    yc_pred_log = (y_proba_log >= 0.5).astype(int)
    metrics_log = {
        'accuracy': float(accuracy_score(yc_test, yc_pred_log)),
        'precision': float(precision_score(yc_test, yc_pred_log, zero_division=0)),
        'recall': float(recall_score(yc_test, yc_pred_log, zero_division=0)),
        'f1': float(f1_score(yc_test, yc_pred_log, zero_division=0)),
        'roc_auc': float(roc_auc_score(yc_test, y_proba_log))
    }

    rfc_pipe = Pipeline([('preproc', preproc), ('model', RandomForestClassifier(random_state=42))])
    rfc_pipe.fit(Xc_train, yc_train)
    y_proba_rfc = rfc_pipe.predict_proba(Xc_test)[:,1]
    yc_pred_rfc = (y_proba_rfc >= 0.5).astype(int)
    metrics_rfc = {
        'accuracy': float(accuracy_score(yc_test, yc_pred_rfc)),
        'precision': float(precision_score(yc_test, yc_pred_rfc, zero_division=0)),
        'recall': float(recall_score(yc_test, yc_pred_rfc, zero_division=0)),
        'f1': float(f1_score(yc_test, yc_pred_rfc, zero_division=0)),
        'roc_auc': float(roc_auc_score(yc_test, y_proba_rfc))
    }

    with open(os.path.join(args.outdir,'metrics_classification.json'),'w') as f:
        json.dump({'logistic_regression': metrics_log, 'random_forest_classifier': metrics_rfc}, f, indent=2)

    print('Done. Outputs saved to', args.outdir)

if __name__ == '__main__':
    logs, notes = load_data("logs_info_25_pseudo.csv", "notes_info_25_pseudo.csv")

    #print(logs.head())
    feats = build_features(logs)
    #print(feats.head())
    #feats.to_csv(os.path.join(args.outdir, 'features.csv'), index=False)

    data = feats.merge(notes[['pseudo', 'note']], on='pseudo', how='inner')

    print(data.head())
    X = data.drop(columns=['pseudo', 'note']);
    y = data['note']

    # Regression
    num_cols = X.columns.tolist()
    preproc = ColumnTransformer([('scale', StandardScaler(), num_cols)], remainder='drop')
    lin_pipe = Pipeline([('preproc', preproc), ('model', LinearRegression())])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    print(len(X_train),len(X_test),len(y_train),len(y_test))
    lin_pipe.fit(X_train, y_train)

    # Accès direct au modèle linéaire dans le pipeline
    reg = lin_pipe.named_steps['model']

    pentes = reg.coef_  # array des coefficients (pentes)
    intercept = reg.intercept_  # ordonnée à l’origine

    print("b",intercept)
    print("a",pentes)

    y_pred_lin = lin_pipe.predict(X_test)
    metrics_lin = {
        'MAE': float(mean_absolute_error(y_test, y_pred_lin)),
        'RMSE': float(np.sqrt(mean_squared_error(y_test, y_pred_lin))),
        'R2': float(r2_score(y_test, y_pred_lin))
    }

    print(metrics_lin)

    print("*"*20)

    rf_pipe = Pipeline([('preproc', preproc), ('model', RandomForestRegressor(random_state=42))])
    rf_pipe.fit(X_train, y_train)
    y_pred_rf = rf_pipe.predict(X_test)
    metrics_rf = {
        'MAE': float(mean_absolute_error(y_test, y_pred_rf)),
        'RMSE': float(np.sqrt(mean_squared_error(y_test, y_pred_rf))),
        'R2': float(r2_score(y_test, y_pred_rf))
    }
    print(metrics_rf)

    # Récupérer le modèle RF dans le pipeline
    rf = rf_pipe.named_steps['model']

    importances = rf.feature_importances_
    order = importances.argsort()[::-1]  # indices triés décroissants

    plt.figure(figsize=(8, max(4, len(num_cols) * 0.25)))
    plt.barh(
        np.array(num_cols)[order][::-1],  # noms de variables triés
        np.array(importances)[order][::-1]  # importances triées
    )
    plt.title('Importance des variables (Random Forest)')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.savefig("feature_importances_rf.png", dpi=150)


    # To Do streamlit
    #Enregistrer le meilleur modèle pour l'application MVC streamlit
    # l'app charge un fichier csv, et aussi ton meilleur modèle (dons ton cas RF)
    # créer les features à partir des logs
    # après le chargement, on applique le best model sur les données traitées lors de l'application du feature enginering
    #afficher le  nombre des admis et échouer

