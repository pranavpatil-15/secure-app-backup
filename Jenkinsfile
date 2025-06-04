pipeline {
    agent { label 'ec2-agent' }

    environment {
        VENV_DIR = '/home/ubuntu/ec2_backup_project/venv'
        PROJECT_DIR = '/home/ubuntu/ec2_backup_project'
    }

    stages {
        stage('Run Backup Script') {
            steps {
                echo "🚀 Running backup script..."
                sh '''
                    . ${VENV_DIR}/bin/activate
                    cd ${PROJECT_DIR}
                    python backup_test.py
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
