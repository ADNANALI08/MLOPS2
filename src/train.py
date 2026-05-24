import mlflow
import os

def train_model():
    # Set the tracking URI to your MLflow server
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    
    # Set the experiment
    EXPERIMENT_NAME = "iris-random-forest"
    mlflow.set_experiment(EXPERIMENT_NAME)
    
    print("Training successfully started and connected to MLflow server.")
    # Your training code goes here

if __name__ == "__main__":
    train_model()
