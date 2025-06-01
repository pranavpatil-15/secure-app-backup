pipeline {
    agent any

    environment {
        PROJECT_DIR = "ec2_backup_project"
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo '✅ Cloning repository...'
                // This step is implicit if using pipeline from SCM
                sh 'ls -la'
            }
        }

        stage('Set Up Environment') {
            steps {
                echo '📦 Setting up Python environment...'
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r ${PROJECT_DIR}/requirements.txt
                '''
            }
        }

        stage('Run Backup Script') {
            steps {
                echo '💾 Running backup script...'
                sh '''
                    source venv/bin/activate
                    python3 ${PROJECT_DIR}/backup_script.py
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Backup job completed successfully!'
        }
        failure {
            echo '❌ Backup job failed.'
        }
    }
}

