pipeline {
    agent { label 'agent-vinod' }

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
                    ./venv/bin/pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Run Backup Script') {
            steps {
                echo '🛠️ Running backup script...'
                sh '''
                    ./venv/bin/python3 backup_test.py
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
