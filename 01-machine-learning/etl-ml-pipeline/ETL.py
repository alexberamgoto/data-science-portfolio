# ETL.py
import pandas as pd
from pathlib import Path

class ETL:
    def __init__(self, logs_path, notes_path, base_dir=None):
        # Détermine le dossier où chercher les fichiers
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent

        self.logs_path = Path(base_dir) / logs_path
        self.notes_path = Path(base_dir) / notes_path

    def load_data(self):
        print(f"[ETL] Lecture logs : {self.logs_path}")
        print(f"[ETL] Lecture notes: {self.notes_path}")

        if not self.logs_path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {self.logs_path}")

        if not self.notes_path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {self.notes_path}")

        logs = pd.read_csv(self.logs_path)
        notes = pd.read_csv(self.notes_path)

        return logs, notes

    def merge_data(self, logs, notes):
        merged = logs.merge(notes, how="left")
        return merged