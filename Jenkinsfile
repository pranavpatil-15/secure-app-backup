pipeline {
    agent { label 'ec2-agent' }

    environment {
        VENV_DIR = 'venv'
        PYTHON = "${env.WORKSPACE}/${env.VENV_DIR}/bin/python"
        PIP = "${env.WORKSPACE}/${env.VENV_DIR}/bin/pip"
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
                echo "🔄 Checking out source code from SCM..."
                checkout scm
            }
        }

        stage('Install System Dependencies') {
            steps {
                echo "🔧 Installing system-level dependencies (python3-venv, python3-pip, wget)..."
                sh '''
                    sudo apt-get update -y
                    sudo apt-get install -y python3-venv python3-pip wget
                '''
            }
        }

        stage('Set Up Python Virtual Environment') {
            steps {
                echo "📦 Setting up Python virtual environment and upgrading pip, setuptools, wheel..."
                sh """
                    python3 -m venv ${env.VENV_DIR}
                    ${env.PIP} install --upgrade pip setuptools wheel
                """
            }
        }

        stage('Install Project Dependencies') {
            steps {
                echo "📥 Installing Python dependencies from requirements.txt..."
                sh """
                    ${env.PIP} install -r requirements.txt
                """
            }
        }

        stage('Run Backup Script') {
            steps {
                echo "🚀 Running backup script..."
                sh """
                    ${env.PYTHON} your_backup_script.py
                """
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
        always {
            echo "🧹 Cleaning up workspace after job..."
            cleanWs()
        }
    }
}

