pipeline {
  agent any

  environment {
    BASE_URL            = "https://makeupstore.com"
    TEST_LOGIN_EMAIL    = credentials('TEST_LOGIN_EMAIL')
    TEST_LOGIN_PASSWORD = credentials('TEST_LOGIN_PASSWORD')
    HEADLESS            = "true"
    PYTHONWARNINGS      = "ignore"
  }

  triggers { cron('H 4 * * 1') }

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '30'))
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Preflight (versions)') {
      steps {
        sh '''
          echo "Python:"; python3 --version || true
          echo "Chrome:"; (google-chrome --version || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version || true)
        '''
      }
    }

    stage('Setup venv') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run smoke tests') {
      steps {
        sh '''
          . .venv/bin/activate
          pytest -m "smoke" \
            --junitxml=reports/junit-smoke.xml \
            --alluredir=reports/allure
        '''
      }
      post {
        always {
          junit 'reports/junit-smoke.xml'
          archiveArtifacts artifacts: 'reports/**', fingerprint: true
        }
      }
    }

    stage('Publish Allure') {
      when { expression { return fileExists('reports/allure') } }
      steps {
        // Сработает, только если установлен Allure Jenkins Plugin и настроен tool
        script {
          try {
            allure includeProperties: false, jdk: '', results: [[path: 'reports/allure']]
          } catch (err) {
            echo "Allure plugin not configured, skipping. ${err}"
          }
        }
      }
    }
  }

  post {
    success { echo "✅ Smoke passed: ${env.JOB_NAME} #${env.BUILD_NUMBER}" }
    failure { echo "❌ Smoke failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}" }
  }
}
