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
                    cd $WORKSPACE/ec2-cloud-backup

                    # Create virtual environment if not exists
                    if [ ! -d "venv" ]; then
                        python3 -m venv venv
                    fi

                    # Activate venv
                    . venv/bin/activate

                    # Install dependencies
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    # Kill old Flask app if running
                    pkill -f app_test.py || true

                    # Run Flask app with correct syntax (no --host here)
                    nohup python3 app_test.py > flask_app.log 2>&1 &

                    # Wait for app to start
                    sleep 5

                    # Optional: check if app is reachable
                    curl -I http://localhost:5000 || echo "⚠️ Flask app not responding."
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Flask app launched successfully!'
        }
        failure {
            echo '❌ Build failed. Showing Flask log:'
            sh 'cat $WORKSPACE/ec2-cloud-backup/flask_app.log || true'
        }
    }
}

