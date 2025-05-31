pipeline {
    agent { label 'ec2-Agent' }

    environment {
        FLASK_ENV = 'production'
        APP_FILE = 'app_test.py'
        BACKUP_DIR = '/home/ubuntu/secure-app-backup'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo '📦 Installing dependencies...'
                sh '''
                    sudo apt update
                    sudo apt install -y python3-pip
                    pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                echo '🚀 Starting Flask app...'
                sh '''
                    # Kill any running Flask app on port 5000
                    fuser -k 5000/tcp || true

                    # Run the Flask app in background using nohup
                    nohup python3 ${APP_FILE} > flask_output.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Deployment failed.'
        }
    }
}

