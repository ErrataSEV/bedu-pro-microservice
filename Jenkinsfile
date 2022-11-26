node {
    def app
    stage('Clone') {
        checkout scm 
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