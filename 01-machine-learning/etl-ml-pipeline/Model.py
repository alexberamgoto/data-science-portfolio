from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

class ModelTrainer:
    def __init__(self, features):
        self.features = features
        self.models = {}
        self.results = {}

    def split_data(self):
        X = self.features[['nb_activites', 'nb_contextes_uniques', 'nb_composants_uniques', 'temps_total']]
        y = self.features['reussite']
        return train_test_split(X, y, test_size=0.3, random_state=42)

    def train_models(self):
        X_train, X_test, y_train, y_test = self.split_data()

        # Mise à l’échelle
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Régression Logistique
        log_reg = LogisticRegression()
        log_reg.fit(X_train_scaled, y_train)
        self.models["logistic_regression"] = (log_reg, X_test_scaled, y_test)

        # Random Forest
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        self.models["random_forest"] = (rf, X_test, y_test)
