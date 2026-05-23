pipeline {
    agent any

    stages {
        stage('Data Ingest') {
            steps {
                echo 'Ingesting data...'
                sh "./venv/bin/python src/stage_01_data_ingest.py"
            }
        }

        stage('Model Train') {
            steps {
                echo 'Training model...'
                sh "./venv/bin/python src/stage_02_model_train.py"
            }
        }

        stage('Model Deploy') {
            steps {
                echo 'Deploying model...'
                sh "./venv/bin/python src/stage_03_model_deploy.py"
            }
        }
    }
}