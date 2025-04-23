pipeline {
    agent {
        label 'agent1'
    }

    stages {
        stage('Preparar entorno') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install unittest2 pytest customtkinter unittest-xml-reporting
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m unittest discover -s tests -p '*.py'
                '''
            }
        }

        stage('Generar reportes') {
            steps {
                sh '''
                    . venv/bin/activate
                    mkdir -p tests/reports
                    python -m xmlrunner discover -s tests -p "*.py" -o tests/reports
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
