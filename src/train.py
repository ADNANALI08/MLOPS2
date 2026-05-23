import mlflow
import os

def train_model():
    tracking_uri = "file://" + os.path.join(os.getcwd(), "mlruns")
    mlflow.set_tracking_uri(tracking_uri)
    
    EXPERIMENT_NAME = "iris-random-forest"
    mlflow.set_experiment(EXPERIMENT_NAME)
    
    print("Training successfully started...")

if __name__ == "__main__":
    train_model()
