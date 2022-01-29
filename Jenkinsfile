pipeline {

  agent { label 'ubuntu' }

  stages {

    stage('Checkout') {
      steps {
          checkout scm
      }  
    }

    stage('Checkout app code to deploy') {
        steps {
            script {
                    sh """
                       [[ -d "/var/tmp/stockfi" ]] && sudo rm -rf /var/tmp/stockfi
                       sudo git clone https://github.com/woodez/stockfi.git /var/tmp/stockfi
                    """    
             
            }
        }
    }

    stage('Deploy stockfi app'){
        steps {
               sh """
                  sudo systemctl stop nginx
                  sudo systemctl stop django
                  [[ -d "/opt/stockfi" ]] && sudo rm -rf /opt/stockfi
                  sudo mv /var/tmp/stockfi/src/stockfi /opt/.
                  sudo chown -R nginx:nginx /opt/stockfi
                  sudo systemctl start django
                  sudo systemctl start nginx
               """
        }
    }
  
  } 
}