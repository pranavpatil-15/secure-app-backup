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
                    chmod +x venv/bin/activate
                    . venv/bin/activate || source venv/bin/activate

                    # Kill if already running
                    pkill -f app_test.py || true

                    # Start Flask app in background
                    nohup python3 app_test.py > flask_app.log 2>&1 &
                    sleep 5
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
