# models/ml_models.py
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import matplotlib.pyplot as plt
import os
import joblib

class MLModels:
    def __init__(self, success_threshold: float = 10.0, outdir: str = "outputs"):
        self.success_threshold = success_threshold
        self.outdir = outdir
        os.makedirs(self.outdir, exist_ok=True)
        os.makedirs(os.path.join(self.outdir, "figures"), exist_ok=True)

        self.reg_lin_pipe = None
        self.reg_rf_pipe = None
        self.clf_log_pipe = None
        self.clf_rf_pipe = None
        self.num_cols = None

    def prepare_data(self, feats: pd.DataFrame, notes: pd.DataFrame):
        data = feats.merge(notes[['pseudo', 'note']], on='pseudo', how='inner')
        X = data.drop(columns=['pseudo', 'note'])
        y = data['note']
        self.num_cols = X.columns.tolist()
        return X, y

    def _build_preproc(self):
        return ColumnTransformer(
            [('scale', StandardScaler(), self.num_cols)],
            remainder='drop'
        )

    def train_regressions(self, X: pd.DataFrame, y: pd.Series):
        preproc = self._build_preproc()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42
        )

        # Linéaire
        self.reg_lin_pipe = Pipeline([
            ('preproc', preproc),
            ('model', LinearRegression())
        ])
        self.reg_lin_pipe.fit(X_train, y_train)
        y_pred_lin = self.reg_lin_pipe.predict(X_test)
        metrics_lin = {
            'MAE': float(mean_absolute_error(y_test, y_pred_lin)),
            'RMSE': float(np.sqrt(mean_squared_error(y_test, y_pred_lin))),
            'R2': float(r2_score(y_test, y_pred_lin))
        }

        # Random forest
        self.reg_rf_pipe = Pipeline([
            ('preproc', preproc),
            ('model', RandomForestRegressor(random_state=42))
        ])
        self.reg_rf_pipe.fit(X_train, y_train)
        y_pred_rf = self.reg_rf_pipe.predict(X_test)
        metrics_rf = {
            'MAE': float(mean_absolute_error(y_test, y_pred_rf)),
            'RMSE': float(np.sqrt(mean_squared_error(y_test, y_pred_rf))),
            'R2': float(r2_score(y_test, y_pred_rf))
        }

        with open(os.path.join(self.outdir, 'metrics_regression.json'), 'w') as f:
            json.dump({
                'linear_regression': metrics_lin,
                'random_forest': metrics_rf
            }, f, indent=2)

        self._plot_feature_importances()

        return metrics_lin, metrics_rf

    def _plot_feature_importances(self):
        if self.reg_rf_pipe is None:
            return
        try:
            rf = self.reg_rf_pipe.named_steps['model']
            importances = rf.feature_importances_
            order = importances.argsort()[::-1]

            plt.figure(figsize=(8, max(4, len(self.num_cols) * 0.25)))
            plt.barh(
                np.array(self.num_cols)[order][::-1],
                np.array(importances)[order][::-1]
            )
            plt.title('Importance des variables (RF)')
            plt.xlabel('Importance')
            plt.tight_layout()
            plt.savefig(os.path.join(self.outdir, 'figures', 'feature_importances_rf.png'), dpi=150)
            plt.close()
        except Exception:
            pass

    def train_classifiers(self, X: pd.DataFrame, y: pd.Series):
        preproc = self._build_preproc()

        success = (y >= self.success_threshold).astype(int)
        Xc_train, Xc_test, yc_train, yc_test = train_test_split(
            X, success, test_size=0.25, random_state=42, stratify=success
        )

        # Logistique
        self.clf_log_pipe = Pipeline([
            ('preproc', preproc),
            ('model', LogisticRegression(max_iter=1000))
        ])
        self.clf_log_pipe.fit(Xc_train, yc_train)
        y_proba_log = self.clf_log_pipe.predict_proba(Xc_test)[:, 1]
        yc_pred_log = (y_proba_log >= 0.5).astype(int)
        metrics_log = {
            'accuracy': float(accuracy_score(yc_test, yc_pred_log)),
            'precision': float(precision_score(yc_test, yc_pred_log, zero_division=0)),
            'recall': float(recall_score(yc_test, yc_pred_log, zero_division=0)),
            'f1': float(f1_score(yc_test, yc_pred_log, zero_division=0)),
            'roc_auc': float(roc_auc_score(yc_test, y_proba_log))
        }

        # RF classifier
        self.clf_rf_pipe = Pipeline([
            ('preproc', preproc),
            ('model', RandomForestClassifier(random_state=42))
        ])
        self.clf_rf_pipe.fit(Xc_train, yc_train)
        y_proba_rfc = self.clf_rf_pipe.predict_proba(Xc_test)[:, 1]
        yc_pred_rfc = (y_proba_rfc >= 0.5).astype(int)
        metrics_rfc = {
            'accuracy': float(accuracy_score(yc_test, yc_pred_rfc)),
            'precision': float(precision_score(yc_test, yc_pred_rfc, zero_division=0)),
            'recall': float(recall_score(yc_test, yc_pred_rfc, zero_division=0)),
            'f1': float(f1_score(yc_test, yc_pred_rfc, zero_division=0)),
            'roc_auc': float(roc_auc_score(yc_test, y_proba_rfc))
        }

        with open(os.path.join(self.outdir, 'metrics_classification.json'), 'w') as f:
            json.dump({
                'logistic_regression': metrics_log,
                'random_forest_classifier': metrics_rfc
            }, f, indent=2)

        return metrics_log, metrics_rfc

    def save_best_model(self):
        # Exemple : on décide que le meilleur modèle est le RF régression
        if self.reg_rf_pipe is None:
            return
        joblib.dump(self.reg_rf_pipe, os.path.join(self.outdir, 'best_model_rf.joblib'))
