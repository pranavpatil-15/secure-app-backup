pipeline {
    agent { label 'ec2-agent' }

    environment {
        VENV_DIR = '/home/ubuntu/ec2_backup_project/venv'
        PROJECT_DIR = '/home/ubuntu/ec2_backup_project'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Uncomment this if you want Jenkins to fetch code fresh
                // git branch: 'main', url: 'git@github.com:yourusername/yourrepo.git'
                
                echo "📦 Skipping Git checkout since code assumed present"
            }
        }
        stage('Debug: List files') {
            steps {
                sh '''
                echo "📁 Listing files in project dir:"
                ls -l ${PROJECT_DIR}
                '''
            }
        }
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
