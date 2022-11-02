pipeline {
  agent {
    node {
      label 'S3'
    }

  }
  stages {
    stage('S3 Upload') {
      steps {
        listAWSAccounts(parent: 'test')
      }
    }

  }
  environment {
    S3_Upload = 'Upload'
  }
}