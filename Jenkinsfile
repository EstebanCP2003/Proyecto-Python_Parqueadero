
pipeline {

    agent{
        label 'agent1'
    }

    stages {
        stage('Preparar entorno') {

            steps {
                sh '''
                    pip install --upgrade pip
                    pip install unittest2
                    pip install pytest
                    pip install customtkinter
                    pip install unittest-xml-reporting
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                sh '''
                    python -m unittest discover -s tests -p "test_*.py" 
                '''
            }
        }

        stage('Generar reportes') {
            steps {
                sh '''
                    mkdir -p tests/reports
                    python -m xmlrunner discover -s tests -p "test_*.py" -o tests/reports
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizado"
            junit 'tests/reports/*.xml'
        }
    }
}
