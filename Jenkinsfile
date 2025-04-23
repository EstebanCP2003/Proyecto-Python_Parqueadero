pipeline {
    agent {
        label 'agent1'
    }

    stages {
        stage('Preparar entorno') {
            steps {
                script {
                    // Crear un entorno virtual de Python
                    sh 'python3 -m venv venv'
                    // Activar el entorno virtual y luego instalar las dependencias
                    sh '''
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install unittest2
                        pip install pytest
                        pip install customtkinter
                        pip install unittest-xml-reporting
                    '''
                }
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                script {
                    // Ejecutar las pruebas dentro del entorno virtual
                    sh '''
                        . venv/bin/activate
                        python -m unittest discover -s tests -p "test_*.py"
                    '''
                }
            }
        }

        stage('Generar reportes') {
            steps {
                script {
                    // Crear directorio de reportes y generar los reportes XML
                    sh '''
                        . venv/bin/activate
                        mkdir -p tests/reports
                        python -m xmlrunner discover -s tests -p "test_*.py" -o tests/reports
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizado"
            // Archivar los reportes de pruebas
            junit 'tests/reports/*.xml'
        }
    }
}
