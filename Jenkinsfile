pipeline {
    agent { label 'ec2-agent' }

    environment {
        VENV_DIR = '/home/ubuntu/ec2_backup_project/venv'
        PROJECT_DIR = '/home/ubuntu/ec2_backup_project'
        PYTHON = "${VENV_DIR}/bin/python"
    }

    stages {
        stage('Run Flask App') {
            steps {
                echo "🚀 Starting Flask app (app_test.py)..."
                sh """
                   cd ${PROJECT_DIR}
                   source ${VENV_DIR}/bin/activate
                   nohup ${PYTHON} app_test.py > flask_app.log 2>&1 &
                """
            }
        }
    }

    post {
        success {
            echo "✅ Flask app started successfully!"
        }
        failure {
            echo "❌ Failed to start Flask app."
        }
    }
}
