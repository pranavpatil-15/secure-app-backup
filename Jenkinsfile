pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Checking out repo...'
                checkout scm
            }
        }

        stage('Run Flask App') {
            steps {
                echo '🚀 Starting Flask app (app_test.py)...'
                sh '''
                #!/bin/bash
                cd $WORKSPACE/ec2_backup_project
                source venv/bin/activate
                nohup python app_test.py > flask_app.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Flask app started successfully!'
        }
        failure {
            echo '❌ Failed to start Flask app.'
            sh 'cat ec2_backup_project/flask_app.log || true'
        }
    }
}
