pipeline {
    agent { label 'ec2-agent' }

    environment {
        VENV_DIR = '/home/ubuntu/ec2_backup_project/venv'
        PROJECT_DIR = '/home/ubuntu/ec2_backup_project'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo "📦 Skipping Git checkout since code already exists on EC2"
            }
        }

        stage('Activate Virtual Environment') {
            steps {
                echo "✅ Using existing virtual environment"
                sh '''
                    ${VENV_DIR}/bin/pip --version
                '''
            }
        }

        stage('Run Backup Script') {
            steps {
                echo "🚀 Running backup script from existing project dir..."
                sh '''
                    cd ${PROJECT_DIR}
                    ${VENV_DIR}/bin/python backup_test.py
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Backup job succeeded."
        }
        failure {
            echo "❌ Backup job failed."
        }
    }
}
