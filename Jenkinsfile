pipeline {
    agent any

    environment {
        VENV_PATH = "${WORKSPACE}/venv"
        MLFLOW_PORT = "5000"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Creating Jenkins virtual environment and installing libraries...'
                sh """
                python3 -m venv ${VENV_PATH}
                ${VENV_PATH}/bin/pip install --upgrade pip
                ${VENV_PATH}/bin/pip install mlflow scikit-learn pandas numpy
                """
            }
        }

        stage('Start MLflow Server') {
            steps {
                echo 'Starting MLflow Tracking Server with SQLite backend...'
                // Running it in the background using 'BUILD_ID=dontKillMe' so Jenkins doesn't kill it immediately
                sh """
                BUILD_ID=dontKillMe ${VENV_PATH}/bin/mlflow server \
                    --backend-store-uri sqlite:///mlflow.db \
                    --default-artifact-root ./mlruns \
                    --host 127.0.0.1 \
                    --port ${MLFLOW_PORT} > mlflow_server.log 2>&1 &
                sleep 5
                """
            }
        }

        stage('Data Ingest') {
            steps {
                echo 'Starting Data Ingestion...'
                sh "${VENV_PATH}/bin/python src/data_ingest.py"
            }
        }

        stage('Model Train') {
            steps {
                echo 'Starting Model Training...'
                sh "${VENV_PATH}/bin/python src/train.py"
            }
        }

        stage('Model Deploy') {
            steps {
                echo 'Deploying Latest Model...'
                sh "${VENV_PATH}/bin/python src/deploy.py"
            }
        }
    }

    post {
        always {
            echo 'Cleaning up any lingering MLflow server processes...'
            sh "pkill -f 'mlflow server' || true"
        }
    }
}
