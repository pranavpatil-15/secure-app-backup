pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/pranavpatil-15/secure-app-backup.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                . venv/bin/activate
                nohup python3 app_test.py > flask.log 2>&1 &
                '''
            }
        }
    }

    post {
        always {
            sh 'tail -20 flask.log || echo "No logs found"'
        }
    }
}

