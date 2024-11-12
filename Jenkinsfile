pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        PYTHON = "${VENV_DIR}/Scripts/python" // For Windows
        PIP = "${VENV_DIR}/Scripts/pip"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/username/your-django-repo.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Create virtual environment
                    bat "python -m venv ${VENV_DIR}"
                    bat "${PIP} install --upgrade pip"
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "${PIP} install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                bat "${PYTHON} manage.py test"
            }
        }

        stage('Run Server') {
            steps {
                bat "${PYTHON} manage.py runserver"
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
