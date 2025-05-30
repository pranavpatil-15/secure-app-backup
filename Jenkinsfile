pipeline {
    agent any

    environment {
        // Optional: Set environment variables if needed
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/pranav-patil-dev/secure-app-backup.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run App') {
            steps {
                sh 'nohup python3 app_test.py &'
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Build failed.'
        }
    }
}
