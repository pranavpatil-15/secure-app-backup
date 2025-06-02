pipeline {
    agent { label 'agent-vinod' }

    environment {
        VENV_DIR = "venv"
        PIP = "./${VENV_DIR}/bin/pip"
        PYTHON = "./${VENV_DIR}/bin/python"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install System Dependencies') {
            steps {
                echo '🔧 Installing system-level dependencies...'
                sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3-venv python3-pip wget
                '''
            }
        }

        stage('Set Up Python Virtual Environment') {
            steps {
                echo '📦 Setting up Python virtual environment...'
                sh '''
                    python3 -m venv ${VENV_DIR} || true
                    
                    if [ ! -f "${PIP}" ]; then
                        echo '⚠️ pip not found, installing manually...'
                        wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
                        ${PYTHON} get-pip.py
                    fi
                    
                    ${PIP} install --upgrade pip
                '''
            }
        }

        stage('Install Project Dependencies') {
            steps {
                echo '📥 Installing project dependencies...'
                sh '''
                    if [ -f requirements.txt ]; then
                        ${PIP} install --break-system-packages -r requirements.txt
                    else
                        ${PIP} install flask boto3 cryptography
                    fi
                '''
            }
        }

        stage('Run Backup Script') {
            steps {
                echo '🚀 Running backup script...'
                sh '''
                    ${PYTHON} backup_test.py
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ Backup job failed.'
        }
        success {
            echo '✅ Backup job completed successfully.'
        }
    }
}
