pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                // Pull your latest code from GitHub
                git branch: 'main', url: 'https://github.com/pranavpatil-15/secure-app-backup.git'
            }
        }

        stage('Install dependencies') {
            steps {
                // Assuming you have Python 3 and virtualenv installed on your EC2
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                // Kill any existing Flask processes on port 5000
                sh '''
                lsof -ti tcp:5000 | xargs -r kill -9
                '''

                // Run Flask app in background using nohup so it keeps running after Jenkins finishes
                sh '''
                source venv/bin/activate
                nohup python3 app_test.py > flask.log 2>&1 &
                '''
            }
        }
    }

    post {
        always {
            // Show last 20 lines of logs so you can debug if needed
            sh 'tail -20 flask.log || echo "No logs yet"'
        }
    }
}

