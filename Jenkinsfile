pipeline {
    agent { label 'ec2-agent' }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Checking out repository...'
                checkout scm
            }
        }

        stage('Run app_test.py') {
            steps {
                echo '🚀 Running app_test.py (Flask App for Dashboard)...'
                sh '''
                    #!/bin/bash
                    cd ec2_backup_project
                    echo "📁 In project directory: $(pwd)"

                    # Activate the virtual environment
                    source venv/bin/activate

                    # Kill any existing Flask app running on port 5000
                    fuser -k 5000/tcp || true

                    # Run the app in background and log output
                    nohup python app_test.py > flask_app.log 2>&1 &

                    # Wait for Flask app to boot up
                    sleep 3
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Flask app started successfully! Check flask_app.log for output.'
        }
        failure {
            echo '❌ Failed to start Flask app. Printing logs...'
            sh 'cat ec2_backup_project/flask_app.log || true'
        }
    }
}
