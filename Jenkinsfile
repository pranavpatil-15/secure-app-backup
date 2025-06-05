pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Cloning repository...'
                git branch: 'main', url: 'https://github.com/pranavpatil-15/secure-app-backup.git'
            }
        }

        stage('Setup and Run Flask App') {
            steps {
                echo '🚀 Setting up environment and starting Flask app...'
                sh '''
                    # Create virtual environment if not exists
                    if [ ! -d "venv" ]; then
                        python3 -m venv venv
                    fi

                    # Activate venv and install requirements
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install flask

                    # Kill running Flask app if any
                    pkill -f app_test.py || true

                    # Run Flask app in background binding to 0.0.0.0
                    nohup python3 app_test.py --host=0.0.0.0 --port=5000 > flask_app.log 2>&1 &

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
            echo '❌ Build failed. Logs:'
            sh 'cat flask_app.log || true'
        }
    }
}
