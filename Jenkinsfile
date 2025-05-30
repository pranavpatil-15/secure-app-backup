pipeline {
    agent { label 'ec2-agent' }  // use the name you gave your agent node
    stages {
        stage('Pull from GitHub') {
            steps {
                git 'https://github.com/pranavpatil-15/secure-app-backup'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Run Flask App') {
            steps {
                sh '''
                    pkill -f app_test.py || true
                    nohup python3 app_test.py &
                '''
            }
        }
    }
}

