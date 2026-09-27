import joblib
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_FOLDER = BASE_DIR / "models"

# -----------------------------
# Load model scores
# -----------------------------
model_scores = joblib.load(MODELS_FOLDER / "model_scores.pkl")

# -----------------------------
# Find best model
# -----------------------------
best_model_name = max(model_scores, key=model_scores.get)

# -----------------------------
# Model file mapping
# -----------------------------
model_files = {
    "Random Forest": "random_forest.pkl",
    "Decision Tree": "decision_tree.pkl",
    "XGBoost": "xgboost.pkl"
}

# -----------------------------
# Load best model
# -----------------------------
model = joblib.load(
    MODELS_FOLDER / model_files[best_model_name]
)

# -----------------------------
# Load feature names
# -----------------------------
features = joblib.load(
    MODELS_FOLDER / "features.pkl"
)

# -----------------------------
# Load label encoders
# -----------------------------
label_encoders = joblib.load(
    MODELS_FOLDER / "label_encoders.pkl"
)

# -----------------------------
# Helper Functions
# -----------------------------
def get_model():
    return model


def get_model_name():
    return best_model_name


def get_accuracy():
    return model_scores[best_model_name]


def get_features():
    return features


def get_label_encoders():
    return label_encoders