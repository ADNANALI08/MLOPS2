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
    # Check if an argument was passed via CLI; if not, pull the latest active run from MLflow
    if len(sys.argv) > 1:
        model_uri = sys.argv[1]
    else:
        print("[DEPLOY] No model URI passed as argument. Fetching latest run from MLflow tracking server...")
        try:
            mlflow.set_tracking_uri(MLFLOW_URI)
            client = MlflowClient()
            
            # Find the experiment ID for your model
            experiment = client.get_experiment_by_name(MODEL_NAME)
            if experiment is None:
                # If experiment name doesn't match iris-classifier, fall back to Default experiment (ID: '0')
                experiment_id = "0"
            else:
                experiment_id = experiment.experiment_id

            # Search for the latest successful run in that experiment
            runs = client.search_runs(
                experiment_ids=[experiment_id],
                max_results=1,
                order_by=["attributes.start_time DESC"]
            )

            if not runs:
                raise ValueError(f"No runs found in MLflow experiment ID: {experiment_id}")

            latest_run_id = runs[0].info.run_id
            model_uri = f"runs:/{latest_run_id}/model"
            print(f"[DEPLOY] Found latest run ID: {latest_run_id}. Using URI: {model_uri}")

        except Exception as e:
            print(f"[DEPLOY ERROR] Failed to auto-detect latest MLflow run: {e}")
            print("[DEPLOY] Ensure your MLflow tracking server is running at http://localhost:5000")
            sys.exit(1)

    deploy_model(model_uri)
