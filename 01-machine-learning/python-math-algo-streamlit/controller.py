# controllers/pipeline_controller.py
import os
from models.data_loader import DataLoader
from models.feature_builder import FeatureBuilder
from models.ml_models import MLModels

class PipelineController:
    def __init__(self, logs_path: str, notes_path: str,
                 sep: str = ',', success_threshold: float = 10.0,
                 outdir: str = 'outputs'):
        self.logs_path = logs_path
        self.notes_path = notes_path
        self.sep = sep
        self.success_threshold = success_threshold
        self.outdir = outdir

        self.data_loader = DataLoader(sep=self.sep)
        self.feature_builder = FeatureBuilder()
        self.ml_models = MLModels(success_threshold=self.success_threshold, outdir=self.outdir)

    def run(self):
        logs, notes = self.data_loader.load_data(self.logs_path, self.notes_path)
        feats = self.feature_builder.build_features(logs)

        os.makedirs(self.outdir, exist_ok=True)
        feats.to_csv(os.path.join(self.outdir, 'features.csv'), index=False)

        X, y = self.ml_models.prepare_data(feats, notes)
        metrics_lin, metrics_rf = self.ml_models.train_regressions(X, y)
        metrics_log, metrics_rfc = self.ml_models.train_classifiers(X, y)
        self.ml_models.save_best_model()

        return {
            "reg_lin": metrics_lin,
            "reg_rf": metrics_rf,
            "clf_log": metrics_log,
            "clf_rf": metrics_rfc
        }
