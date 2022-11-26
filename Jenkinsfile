node {
    agents any
    stages {
        def app
        stage('Clone') {
            checkout scm 
        }
        stage('Backup'){
            sh 'docker rmi myapi-stories:backup || true'
            sh 'docker image tag myapi-stories myapi-stories:backup || true'
            sh 'docker rmi myapi-stories:latest || true'
        }
        stage('Build') {
            app = docker.build("myapi-stories:latest")
        }
        stage('Test') {
            app.inside {
                sh 'pip list'
            }
        }
        stage('Deploy') {
            sh 'set'
            sh 'docker stop myapi-stories || true && docker rm myapi-stories || true'
            sh 'docker run -p 5001:5000 -d --rm --name myapi-stories -e MYSQL_IP="$MYSQL_IP" -e MYSQL_PORT="3306" -e MYSQL_USER="$MYSQL_USER" -e MYSQL_PASSWORD="$MYSQL_PASSWORD" myapi-stories:latest'
            sh 'docker exec myapi-stories python init-db.py'
        }
    }
    post{
        failure{
            sh 'docker image myapi-stories:backup tag myapi-stories:latest || true'
            sh 'docker run -p 5001:5000 -d --rm --name myapi-stories -e MYSQL_IP="$MYSQL_IP" -e MYSQL_PORT="3306" -e MYSQL_USER="$MYSQL_USER" -e MYSQL_PASSWORD="$MYSQL_PASSWORD" myapi-stories:latest'
        }
    }
}