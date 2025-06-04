pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        PYTHON = "${VENV_DIR}/bin/python"
        PIP = "${VENV_DIR}/bin/pip"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Checkout your Git repo here - update URL & branch as needed
                git branch: 'main', url: 'git@github.com:yourusername/ec2_backup_project.git'
            }
        }

        stage('Debug Workspace') {
            steps {
                echo "Workspace is: ${WORKSPACE}"
                sh 'pwd'
                sh 'ls -l'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    if (!fileExists("${VENV_DIR}/bin/activate")) {
                        echo "Virtual environment not found! Creating it now..."
                        sh "python3 -m venv ${VENV_DIR}"
                    } else {
                        echo "Virtual environment already exists."
                    }
                }
            }
        }

        stage('Install Requirements') {
            steps {
                // If you have requirements.txt, install here, else skip or modify
                sh """
                   ${PIP} install --upgrade pip
                   ${PIP} install -r requirements.txt || echo "No requirements.txt found, skipping."
                """
            }
        }

        stage('Run Backup Script') {
            steps {
                // Activate venv & run your python script from workspace
                sh """
                   source ${VENV_DIR}/bin/activate
                   cd ${WORKSPACE}
                   ${PYTHON} backup_test.py
                """
            }
        }
    }

    post {
        success {
            echo "✅ Backup script ran successfully!"
        }
        failure {
            echo "❌ Backup job failed."
        }
    }
}
