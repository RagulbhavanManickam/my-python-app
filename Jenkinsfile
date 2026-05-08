pipeline {
    agent any

    environment {
        IMAGE_NAME  = "my-python-app"
        REGISTRY    = "ragulbhavanmanickam"
        VERSION_TAG = "${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"
        LATEST_TAG  = "${REGISTRY}/${IMAGE_NAME}:latest"
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds1',
                    url: 'https://github.com/RagulbhavanManickam/my-python-app.git'
                echo "✅ Code cloned — Build #${BUILD_NUMBER}"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build \
                        -t ${VERSION_TAG} \
                        -t ${LATEST_TAG} \
                        .
                """
                echo "✅ Docker image built"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | \
                          docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${VERSION_TAG}
                        docker push ${LATEST_TAG}
                        docker logout
                    '''
                }
                echo "✅ Image pushed to Docker Hub"
            }
        }

        stage('Deploy with Ansible') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'ansible-ssh-key',
                        keyFileVariable: 'SSH_KEY'
                    ),
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh """
                        ansible-playbook -i inventory.ini deploy.yml \
                            --private-key=\$SSH_KEY \
                            --extra-vars "image_tag=${BUILD_NUMBER} \
                                          docker_user=\$DOCKER_USER \
                                          docker_pass=\$DOCKER_PASS"
                    """
                }
                echo "✅ Deployed via Ansible"
            }
        }
    }

    post {
        success {
            echo "🎉 Build #${BUILD_NUMBER} deployed successfully!"
        }
        failure {
            echo "❌ Build #${BUILD_NUMBER} failed. Check logs above."
        }
        always {
            sh "docker rmi ${VERSION_TAG} || true"
            sh "docker rmi ${LATEST_TAG}  || true"
            sh "docker image prune -f     || true"
        }
    }
}
