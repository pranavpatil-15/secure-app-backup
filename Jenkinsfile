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
                echo "📦 Running Flask app..."
                sh '''
                    nohup python3 app_test.py > flask_app.log 2>&1 &
                    sleep 5  # Give it time to start
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
