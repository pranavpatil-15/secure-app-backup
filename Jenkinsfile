pipeline {
    agent { label 'ec2-agent' }

    environment {
        VENV_DIR = '/home/ubuntu/ec2_backup_project/venv'
        PROJECT_DIR = '/home/ubuntu/ec2_backup_project'
    }

    stages {
        stage('Validate Virtual Environment') {
            steps {
                echo "🔍 Checking virtual environment and pip version"
                sh '''
                    if [ ! -d "${VENV_DIR}" ]; then
                        echo "Virtual environment not found! Creating it now..."
                        python3 -m venv ${VENV_DIR}
                    fi

                    # Activate venv and install pip if missing
                    source ${VENV_DIR}/bin/activate

                    # Ensure pip is installed/upgraded inside venv
                    if ! command -v pip > /dev/null; then
                        echo "pip not found, installing pip..."
                        python get-pip.py
                    else
                        echo "pip found, upgrading pip..."
                        pip install --upgrade pip
                    fi

                    pip --version
                '''
            }
        }

        stage('Install Requirements') {
            steps {
                echo "📦 Installing Python dependencies from requirements.txt"
                sh '''
                    source ${VENV_DIR}/bin/activate
                    cd ${PROJECT_DIR}
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    else
                        echo "No requirements.txt found, skipping pip install."
                    fi
                '''
            }
        }

        stage('Run Backup Script') {
            steps {
                echo "🚀 Running backup script..."
                sh '''
                    source ${VENV_DIR}/bin/activate
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
