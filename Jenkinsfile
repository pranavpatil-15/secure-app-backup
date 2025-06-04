pipeline {
    agent { label 'ec2-agent' }

    environment {
        APP_PORT = '5000'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/pranavpatil-15/secure-app-backup.git'
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                    echo "🔄 Running app_test.py (Flask App for Dashboard)..."
                    nohup python3 app_test.py > flask_app.log 2>&1 &
                '''
            }
        }
    }

    post {
        failure {
            echo "❌ Failed to start Flask app. Printing logs..."
            sh 'cat flask_app.log || true'
        }
    }
}
