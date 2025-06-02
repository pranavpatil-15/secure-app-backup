pipeline {
    agent { label 'agent-vinod' }

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                echo "🧹 Cleaning old virtual environment if exists..."
                sh "rm -rf ${env.VENV_DIR}"
            }
        }

        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Install System Dependencies') {
            steps {
                echo "🔧 Installing system-level dependencies..."
                sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3-venv python3-pip wget
                '''
            }
        }

        stage('Set Up Python Virtual Environment') {
            steps {
                echo "📦 Setting up Python virtual environment and upgrading pip..."
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip setuptools wheel
                '''
            }
        }

        stage('Install Project Dependencies') {
            steps {
                echo "📥 Installing project Python dependencies..."
                sh '''
                    ${VENV_DIR}/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Backup Script') {
            steps {
                echo "🚀 Running backup script..."
                sh '''
                    ${VENV_DIR}/bin/python your_backup_script.py
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
