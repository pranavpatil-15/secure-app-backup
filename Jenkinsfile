pipeline {
    agent any
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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Backup Script') {
            steps {
                echo '📁 Running backup script...'
                sh '''
                    . venv/bin/activate
                    python3 backup_test.py
                '''
            }
        }
    }
    post {
        failure {
            echo '❌ Backup job failed.'
        }
        success {
            echo '✅ Backup job succeeded.'
        }
    }
}

