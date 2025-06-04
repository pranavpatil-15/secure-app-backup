pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Cloning repo from GitHub...'
                // Replace with your GitHub HTTPS link to ensure Jenkins pulls code
                git branch: 'main', url: 'https://github.com/pranavpatil-15/secure-app-backup.git'
            }
        }

        stage('Start Flask App') {
            steps {
                echo '🚀 Running app_test.py from virtual environment...'
                sh '''
                    cd ec2_backup_project
                    source venv/bin/activate
                    nohup python app_test.py > flask_app.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Flask app launched successfully and running in background!'
        }
        failure {
            echo '❌ Failed to start Flask app. Check logs:'
            sh 'cat ec2_backup_project/flask_app.log || true'
        }
    }
}
