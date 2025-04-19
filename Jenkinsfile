pipeline {
    agent any
    stages {
        stage('Clonar repositorio') {
            steps {
                git 'https://github.com/EstebanCP2003/Proyecto-Python_Parqueadero.git'
            }
        }
        stage('Instalar dependencias') {
            steps {
                sh 'pip install -r requirements.txt || true'
            }
        }
        stage('Ejecutar pruebas') {
            steps {
                sh 'python -m unittest discover tests'
            }
        }
    }
    post {
        always {
            junit 'tests/*.xml' // si generas reporte JUnit
        }
    }
}
