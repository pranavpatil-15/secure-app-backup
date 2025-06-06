pipeline {
    agent any

    environment {
        // Set the path to your secret key if you use Jenkins credentials, else leave as is
        ENCRYPTION_KEY_FILE = '/home/ubuntu/workspace/ec2-cloud-backup/secret.key'
        AWS_DEFAULT_REGION = 'ap-south-1' // Change if your AWS region is different
        // If you use Jenkins credentials for AWS, uncomment below and set up in Jenkins
        // AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        // AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/pranavpatil-15/secure-app-backup.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                cd /home/ubuntu/workspace/ec2-cloud-backup
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                cd /home/ubuntu/workspace/ec2-cloud-backup
                . venv/bin/activate
                nohup venv/bin/python app.py > flask_app.log 2>&1 &
                sleep 5  # Give the server a moment to start
                '''
            }
        }

        stage('Automated Backup') {
            steps {
                sh '''
                curl -X POST http://localhost:5000/create_backup
                '''
            }
        }

        stage('Cleanup Old Backups') {
            steps {
                sh '''
                curl -X POST "http://localhost:5000/cleanup_old_backups?days=30"
                '''
            }
        }
    }

    post {
        always {
            sh '''
            cd /home/ubuntu/workspace/ec2-cloud-backup
            tail -20 flask_app.log || echo "No logs found"
            '''
        }
    }
}

