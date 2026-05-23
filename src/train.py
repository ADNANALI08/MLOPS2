import mlflow
import os
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd


MLFLOW_URI = "http://localhost:5000"
EXPERIMENT_NAME = "iris-random-forest"


# Now your existing code will work without needing port 5000
mlflow.set_experiment("iris-random-forest")

# Create a local directory for tracking if it doesn't exist
tracking_uri = "file://" + os.path.join(os.getcwd(), "mlruns")
mlflow.set_tracking_uri(tracking_uri)


def train_model():
 tracking_uri = "file://" + os.path.join(os.getcwd(), "mlruns")
    mlflow.set_tracking_uri(tracking_uri)
    EXPERIMENT_NAME = "iris-random-forest"
    mlflow.set_experiment(EXPERIMENT_NAME)




    df = pd.read_csv('data/iris.csv')
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with mlflow.start_run() as run:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, model.predict(X_test))

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)
        mlflow.log_param("test_size", 0.2)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")

        print(f"[TRAIN] Accuracy: {accuracy}")
        print(f"[TRAIN] Run ID: {run.info.run_id}")

        with open("run_id.txt", "w") as f:
            f.write(run.info.run_id)

if __name__ == "__main__":
    train_model()
