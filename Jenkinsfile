pipeline {
    agent any

    environment {
        APP_NAME     = "flask-app"
        IMAGE_NAME   = "dhivagar/flask-app"
        IMAGE_TAG    = "${BUILD_NUMBER}"
        DOCKER_CREDS = "dockerhub-creds"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // Run lint & sanity inside a Python container
        stage('Lint & Sanity Check') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root:root' // run as root inside container
                }
            }
            steps {
                sh '''
                    python3 --version
                    python3 -m py_compile app.py
                '''
            }
        }

        // Build Docker image on the main agent
        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: DOCKER_CREDS,
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Smoke Test Container') {
            steps {
                sh '''
                    docker run -d --name test-flask -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 5
                    curl -f http://localhost:5000/health
                    docker rm -f test-flask
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Flask app image built & validated successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
        always {
            sh 'docker system prune -f'
        }
    }
}
