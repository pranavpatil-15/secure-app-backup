pipeline {
    agent any

    environment {
        FLASK_APP = 'app_test.py'
        FLASK_ENV = 'production'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/pranavpatil-15/secure-app-backup.git'
            }
        }

        stage('Set Up Python Env') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt || pip install flask boto3
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                source venv/bin/activate
                nohup flask run --host=0.0.0.0 --port=5000 > flask_app.log 2>&1 &
                sleep 5
                '''
            }
        }

        stage('Show Flask Logs') {
            steps {
                script {
                    echo "✅ Flask app started. Printing recent logs:"
                }
                sh '''
                if [ -f flask_app.log ]; then
                    tail -n 20 flask_app.log
                else
                    echo "⚠️ flask_app.log not found."
                fi
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ Build failed. Please check above logs for details.'
            sh 'cat flask_app.log || echo "No log file found."'
        }
        success {
            echo '✅ Build succeeded. Flask app should be running.'
        }
    }
}
