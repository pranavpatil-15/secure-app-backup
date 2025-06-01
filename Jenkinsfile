pipeline {
    agent any

    environment {
        // Activate virtual environment path
        VENV_PATH = 'venv/bin/activate'
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo '✅ Cloning repository...'
                sh 'ls -la'
            }
        }

        stage('Set Up Environment') {
            steps {
                echo '📦 Setting up Python environment...'
                sh '''#!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Run Backup Script') {
            steps {
                echo '🛠️ Running backup script...'
                sh '''#!/bin/bash
                    source venv/bin/activate
                    python3 backup_test.py
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Backup job completed successfully.'
        }
        failure {
            echo '❌ Backup job failed.'
        }
    }
}

