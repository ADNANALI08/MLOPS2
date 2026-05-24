import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import mlflow.sklearn

def train_model():
    # 1. Connect to the running pipeline server
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    
    EXPERIMENT_NAME = "iris-random-forest"
    mlflow.set_experiment(EXPERIMENT_NAME)
    
    print("Training successfully started and connected to MLflow server.")
    
    # 2. YOU NEED THIS: Start an official MLflow tracking run
    with mlflow.start_run():
        # Load your data (adjust the path to match your data ingest location)
        df = pd.read_csv("data/iris.csv") # or wherever data_ingest.py saves it
        X = df.drop(columns=['target'])
        y = df['target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Log metrics/parameters so the run is valid
        accuracy = model.score(X_test, y_test)
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", accuracy)
        
        # 3. Log the model artifact so deploy.py can find it!
        mlflow.sklearn.log_model(model, "model")
        print(f"Training finished! Model logged with accuracy: {accuracy}")

if __name__ == "__main__":
    train_model()
