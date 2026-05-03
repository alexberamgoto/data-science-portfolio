from ETL import ETL
from Feature import FeatureEngineering   # <- si ta classe est dans Feature.py

def main():
    etl = ETL(
        logs_path="logs_info_25_pseudo.csv",
        notes_path="notes_info_25_pseudo.csv",
        base_dir="."   # ou Path(__file__).resolve().parent
    )
    logs, notes = etl.load_data()
    merged = etl.merge_data(logs, notes)  # Assure-toi que ETL.merge_data() retourne bien un DataFrame

    # Donne le nom exact de ta cible si tu en as une (sinon, laisse None)
    feat = FeatureEngineering(merged, target_col="label")   # <--- adapte "label"
    X, y = feat.build_features()

    print("OK -> X shape:", X.shape, "| y is None ?", y is None)

if __name__ == "__main__":
    main()