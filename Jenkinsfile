pipeline {
    agent any

    stages {
        stage('Setup Environment') {
            steps {
                echo 'Creating Jenkins virtual environment and installing libraries...'
                sh '''
                python3 -m venv venv
                ./venv/bin/pip install mlflow scikit-learn pandas numpy
                '''
            }
        }
        
        stage('Data Ingest') {
            steps {
                echo 'Starting Data Ingestion...'
                sh "./venv/bin/python src/data_ingest.py"
            }
        }
        
        stage('Model Train') {
            steps {
                echo 'Starting Model Training...'
                sh "./venv/bin/python src/train.py"
            }
        }
        
        stage('Model Deploy - MLflow') {
            steps {
                echo 'Logging to MLflow...'
                sh "./venv/bin/python src/deploy.py"
            }
        }
        
        stage('Model Test') {
            steps {
                echo 'Testing Model...'
                sh "./venv/bin/python src/test_model.py"
            }
        }
    }

    post {
        always {
            echo "Pipeline run complete! (Email notifications disabled for local run)"
        }
        success {
            echo "Build Successful! Ready for Pre-Prod."
        }
        failure {
            echo "Build Failed. Check the logs."
        }
    }
}
