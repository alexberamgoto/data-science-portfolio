"""
Machine Learning model for breast cancer risk prediction.
Trains a RandomForestClassifier on the Hugging Face dataset
'tarekmasryo/cancer-risk-factors-data'.
Falls back to synthetic data if Hugging Face is unavailable (e.g. no network).
"""
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import asyncio
from concurrent.futures import ThreadPoolExecutor

MODEL_PATH = "/app/app/model/cancer_risk_model.pkl"
ENCODER_PATH = "/app/app/model/label_encoder.pkl"

_model = None
_encoder = None
_executor = ThreadPoolExecutor(max_workers=2)

# Order of features expected by the model
FEATURE_COLUMNS = [
    "Age", "Gender", "Smoking", "Alcohol_Use", "Obesity",
    "Family_History", "Diet_Red_Meat", "Diet_Salted_Processed",
    "Fruit_Veg_Intake", "Physical_Activity", "Air_Pollution",
    "Occupational_Hazards", "BRCA_Mutation", "H_Pylori_Infection",
    "Calcium_Intake", "BMI", "Physical_Activity_Level",
]


def _generate_synthetic_data(n: int = 5000) -> pd.DataFrame:
    """Generate synthetic training data when HuggingFace is unavailable."""
    np.random.seed(42)

    # Create risk scores to make labels more realistic
    age = np.random.randint(20, 80, n)
    smoking = np.random.randint(0, 11, n)
    alcohol = np.random.randint(0, 11, n)
    obesity = np.random.randint(0, 11, n)
    family_hist = np.random.randint(0, 2, n)
    brca = np.random.randint(0, 2, n)
    fruit_veg = np.random.randint(0, 11, n)
    activity = np.random.randint(0, 11, n)

    # Composite risk score for more realistic labels
    risk_score = (
        (age / 80) * 2
        + smoking * 0.3
        + alcohol * 0.2
        + obesity * 0.25
        + family_hist * 1.5
        + brca * 2.0
        - fruit_veg * 0.15
        - activity * 0.15
        + np.random.normal(0, 1, n)
    )

    # Assign labels based on risk score percentiles
    labels = np.where(
        risk_score < np.percentile(risk_score, 40), "Low",
        np.where(risk_score < np.percentile(risk_score, 75), "Medium", "High")
    )

    return pd.DataFrame({
        "Age": age,
        "Gender": np.random.randint(0, 2, n),
        "Smoking": smoking,
        "Alcohol_Use": alcohol,
        "Obesity": obesity,
        "Family_History": family_hist.astype(bool),
        "Diet_Red_Meat": np.random.randint(0, 11, n),
        "Diet_Salted_Processed": np.random.randint(0, 11, n),
        "Fruit_Veg_Intake": fruit_veg,
        "Physical_Activity": activity,
        "Air_Pollution": np.random.randint(0, 11, n),
        "Occupational_Hazards": np.random.randint(0, 11, n),
        "BRCA_Mutation": brca.astype(bool),
        "H_Pylori_Infection": np.random.randint(0, 2, n).astype(bool),
        "Calcium_Intake": np.random.randint(0, 11, n),
        "BMI": np.round(np.random.uniform(15.0, 45.0, n), 1),
        "Physical_Activity_Level": np.random.randint(0, 11, n),
        "Risk_Level": labels,
    })


def _train_model():
    """Train the model from Hugging Face dataset or synthetic data."""
    print("🧠 Training ML model...")

    try:
        from datasets import load_dataset
        dataset = load_dataset("tarekmasryo/cancer-risk-factors-data")
        df = pd.DataFrame(dataset["train"])
        print("✅ Dataset loaded from Hugging Face")
    except Exception as e:
        print(f"⚠️ HuggingFace unavailable ({e})")
        print("🔄 Using synthetic training data...")
        df = _generate_synthetic_data()

    # Encode target variable
    encoder = LabelEncoder()
    df["Risk_Encoded"] = encoder.fit_transform(df["Risk_Level"])

    # Convert booleans to int for sklearn
    for col in ["Family_History", "BRCA_Mutation", "H_Pylori_Infection"]:
        if col in df.columns:
            df[col] = df[col].astype(int)

    X = df[FEATURE_COLUMNS].values
    y = df["Risk_Encoded"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    print("📊 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=encoder.classes_))

    # Feature importances
    importances = dict(zip(FEATURE_COLUMNS, model.feature_importances_))
    top_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:5]
    print("🔑 Top 5 features:")
    for feat, imp in top_features:
        print(f"   {feat}: {imp:.4f}")

    # Save model and encoder
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")

    return model, encoder


def load_model():
    """Load model from disk or train a new one."""
    global _model, _encoder
    if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
        _model = joblib.load(MODEL_PATH)
        _encoder = joblib.load(ENCODER_PATH)
        print("✅ ML Model loaded from disk")
    else:
        _model, _encoder = _train_model()


def _predict_sync(health_data: dict) -> dict:
    """Synchronous prediction — runs in thread pool."""
    global _model, _encoder

    if _model is None or _encoder is None:
        load_model()

    # Build feature vector in the EXACT order expected by the model
    features = np.array([[
        health_data.get("age", 0),
        health_data.get("gender", 0),
        health_data.get("smoking", 0),
        health_data.get("alcohol_use", 0),
        health_data.get("obesity", 0),
        int(health_data.get("family_history", False)),
        health_data.get("diet_red_meat", 0),
        health_data.get("diet_salted_processed", 0),
        health_data.get("fruit_veg_intake", 0),
        health_data.get("physical_activity", 0),
        health_data.get("air_pollution", 0),
        health_data.get("occupational_hazards", 0),
        int(health_data.get("brca_mutation", False)),
        int(health_data.get("h_pylori_infection", False)),
        health_data.get("calcium_intake", 0),
        health_data.get("bmi", 25.0),
        health_data.get("physical_activity_level", 0),
    ]])

    prediction = _model.predict(features)[0]
    probabilities = _model.predict_proba(features)[0]
    confidence = float(max(probabilities))
    risk_level = _encoder.inverse_transform([prediction])[0]

    return {
        "risk_level": risk_level,
        "confidence": round(confidence, 4),
        "probabilities": {
            label: round(float(prob), 4)
            for label, prob in zip(_encoder.classes_, probabilities)
        },
    }


async def predict_risk(health_data: dict) -> dict:
    """
    Async prediction wrapper.
    Runs the model inference in a thread pool to avoid blocking
    the FastAPI event loop (simulates a potentially slow computation).
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, _predict_sync, health_data)
