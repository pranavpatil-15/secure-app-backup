pipeline {
    agent any

    stages {
        stage('Pull from GitHub') {
            steps {
                git credentialsId: 'github-creds', url: 'https://github.com/pranavpatil-15/secure-app-backup.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip zip
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                pkill -f app_test.py || true
                nohup python3 app_test.py > flask.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Deployment failed!'
        }
    }
}

