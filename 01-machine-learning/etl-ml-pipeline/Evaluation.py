from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

class Evaluation:
    def __init__(self, models):
        self.models = models

    def evaluate(self):
        metrics = {}
        for name, (model, X_test, y_test) in self.models.items():
            y_pred = model.predict(X_test)
            metrics[name] = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred),
                "recall": recall_score(y_test, y_pred),
                "f1_score": f1_score(y_test, y_pred),
                "confusion_matrix": confusion_matrix(y_test, y_pred)
            }
        return metrics
