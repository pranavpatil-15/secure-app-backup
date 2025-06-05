pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Cloning repository...'
                git branch: 'main', url: 'https://github.com/pranavpatil-15/secure-app-backup.git'
            }
        }

        stage('Run Flask App') {
            steps {
                echo '🚀 Starting Flask App...'
                sh '''
                    . venv/bin/activate
                    nohup python3 app_test.py > flask_app.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Flask app launched successfully!'
        }
        failure {
            echo '❌ Build failed. Here is the log:'
            sh 'cat flask_app.log || true'
        }
    }
}
