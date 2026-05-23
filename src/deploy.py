import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import subprocess, sys, time, os, signal

MLFLOW_URI = "http://localhost:5000"
MODEL_NAME = "iris-classifier"

def deploy_model(model_uri, port=6000):
    mlflow.set_tracking_uri(MLFLOW_URI)
    print(f"[DEPLOY] Deploying model from: {model_uri}")
    print(f"[DEPLOY] Starting MLflow model server on port {port}...")

    os.system(f"fuser -k {port}/tcp 2>/dev/null || true")
    time.sleep(2)

    process = subprocess.Popen(
        ["mlflow", "models", "serve",
         "-m", model_uri,
         "-p", str(port),
         "--no-conda"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(8)

    if process.poll() is None:
        print(f"[DEPLOY] Model successfully deployed at http://localhost:{port}")
        with open("deploy_pid.txt", "w") as f:
            f.write(str(process.pid))
    else:
        stdout, stderr = process.communicate()
        print(f"[DEPLOY ERROR] {stderr.decode()}")
        sys.exit(1)

if __name__ == "__main__":
    model_uri = sys.argv[1]
    deploy_model(model_uri)
