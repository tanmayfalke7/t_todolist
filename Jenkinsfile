pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/tanmayfalke7/t_todolist'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t todolist-streamlit .'
                }
            }
        }

        stage('Stop Old Containers') {
            steps {
                script {
                    sh 'docker compose down || true'
                }
            }
        }

        stage('Start Containers') {
            steps {
                script {
                    sh 'docker compose up -d --build'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Deployment failed!'
        }
    }
}
