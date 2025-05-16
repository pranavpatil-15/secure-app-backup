pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/strangepranav/secure-app-backup.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Backup Script') {
            steps {
                sh 'python3 backup_test.py'
            }
        }

        stage('Restart Flask App') {
            steps {
                sh 'sudo systemctl restart flask-app' // or your app restart command
            }
        }
    }

    post {
        success {
            echo '✅ Backup and deploy successful!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}
