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
                    # Activate virtual environment (use . instead of source for /bin/sh)
                    . /home/ubuntu/myenv/bin/activate

                    # Navigate to Jenkins workspace directory
                    cd /home/ubuntu/workspace/ec2-cloud-backup

                    # Kill any existing Flask app
                    pkill -f app_test.py || true

                    # Start Flask app in background using nohup
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
            echo '❌ Build failed. Here is the log:'
            sh 'cat flask_app.log || true'
        }
    }
}
