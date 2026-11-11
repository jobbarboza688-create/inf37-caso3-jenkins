pipeline {
  agent any
  options { timestamps(); disableConcurrentBuilds(); skipDefaultCheckout(true) }
  triggers { pollSCM('H/5 * * * *') }
  stages {
    stage('GitHub') {
      steps { deleteDir(); checkout scm; sh 'git rev-parse HEAD' }
    }
    stage('Entorno y dependencias') {
      steps {
        sh '''
          python3 -m venv .venv
          .venv/bin/python -m pip install -r requirements-dev.txt
          .venv/bin/python -m pip install --no-build-isolation -e .
          mkdir -p reports
          touch reports/flake8.txt
          .venv/bin/python -m pip freeze > reports/dependencies.txt
        '''
      }
    }
    stage('Calidad y pruebas') {
      steps {
        script {
          def lint = sh(returnStatus: true, script: '.venv/bin/python -m flake8 src tests scripts --output-file=reports/flake8.txt')
          def tests = sh(returnStatus: true, script: '.venv/bin/python -m pytest -v --junitxml=reports/pytest.xml > reports/pytest.txt 2>&1')
          def security = sh(returnStatus: true, script: '.venv/bin/python -m bandit -r src scripts -f json -o reports/bandit.json > reports/bandit-console.txt 2>&1')
          if (lint != 0 || tests != 0 || security != 0) {
            error('Calidad rechazada: consultar reportes archivados')
          }
        }
      }
    }
    stage('Empaquetar') {
      steps {
        sh '.venv/bin/python -m build --no-isolation'
        sh 'sha256sum dist/* > reports/SHA256SUMS'
      }
    }
    stage('Desplegar a pruebas') {
      steps { sh '.venv/bin/python scripts/deploy.py dist/*.whl > reports/deploy.json' }
    }
  }
  post {
    always {
      junit allowEmptyResults: true, testResults: 'reports/pytest.xml'
      archiveArtifacts artifacts: 'reports/**,dist/**', allowEmptyArchive: true, fingerprint: true
    }
  }
}
