import mlflow
import sys

def deploy():
    # 1. Connect to the same server
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    
    # 2. Look for the specific experiment
    experiment_name = "iris-random-forest"
    experiment = mlflow.get_experiment_by_name(experiment_name)
    
    if not experiment:
        print(f"Error: Experiment '{experiment_name}' not found.")
        sys.exit(1)
        
    # 3. Search for the latest run in that experiment
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=1
    )
    
    if runs.empty:
        print("No runs found in experiment.")
        sys.exit(1)
        
    run_id = runs.iloc[0].run_id
    print(f"Success! Latest run found: {run_id}")

if __name__ == "__main__":
    deploy()
