pipeline {
    agent any

    environment {
        APP_NAME     = "flask-app"
        IMAGE_NAME   = "dhivagargopal/flask-app"
        IMAGE_TAG    = "${BUILD_NUMBER}"
        DOCKER_CREDS = "dockerhub-creds"
        K8S_DIR      = "k8s"  // path to your YAML files in repo
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

        stage('Lint & Sanity Check') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root:root'
                }
            }
            steps {
                sh '''
                    python3 --version
                    python3 -m compileall .
                '''
            }
        }

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

        stage('Deploy to Minikube') {
            steps {
                sh """
                    # Ensure Minikube uses the correct Docker environment if needed
                    # eval \$(minikube docker-env)

                    # Apply all Kubernetes manifests
                    kubectl apply -f ${K8S_DIR}/deployment.yaml
                    kubectl apply -f ${K8S_DIR}/service.yaml
                    kubectl apply -f ${K8S_DIR}/hpa.yaml
                    kubectl apply -f ${K8S_DIR}/ingress.yml

                    # Wait for deployment rollout
                    kubectl rollout status deployment/${APP_NAME} -n default

                    # List pods
                    kubectl get pods -n default
                """
            }
        }

    } // end of stages

    post {
        success {
            echo "✅ Flask app image built, pushed, and deployed successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
        always {
            sh 'docker system prune -f'
        }
    }

} // end of pipeline
