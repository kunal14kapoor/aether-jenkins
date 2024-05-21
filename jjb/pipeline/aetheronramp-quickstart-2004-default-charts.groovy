// SPDX-FileCopyrightText: 2021 Open Networking Foundation <info@opennetworking.org>
// SPDX-License-Identifier: LicenseRef-ONF-Member-Only-1.0
pipeline {

  agent {
        label 'Mumbai-A1'
    }
  
  stages{
      
      stage("Cleanup"){
      steps {
        sh """
        cd $WORKSPACE
        sudo rm -rf *
        """
      }
    }

      stage('Install aether-onramp') {
       steps {
           sh """
            cd $WORKSPACE
            git clone --recursive https://github.com/opennetworkinglab/aether-onramp.git 
            cd aether-onramp
            # determine local IP
            MYIP=\$(hostname -I | awk '{print \$1}')
            # determine local NET_INTERFACE (Well, someday...)  
            # We just know the current Aether-Onramp-Ready AMI is using ens5
            NET_INTERFACE="eth0"
            sudo cp -r /home/ubuntu/hosts.ini hosts.ini
            sudo cp  vars/main-gnbsim.yml  vars/main.yml
            sudo sed -i "s/10.76.28.113/\$(hostname -I | awk '{ print \$1 }')/" vars/main.yml
            grep -rl "ens18" . | xargs sed -i 's/ens18/eth0/g'
            make aether-pingall
            ansible-galaxy collection install kubernetes.core
            ansible-galaxy collection install ansible.posix
            make k8s-install
            kubectl get pods --all-namespaces
            make 5gc-install
            ansible-galaxy collection install community.docker:2.7.3 --force
            ansible-galaxy collection install ansible.utils:2.8.0 --force
            make gnbsim-docker-install
            make gnbsim-install
            """ 
	   }
	  }
    
    stage("Run Gnbsim Test"){
      steps {
        sh """
        cd $WORKSPACE/aether-onramp
        kubectl get pods -n omec
        sleep 120
        make gnbsim-simulator-run
        cd /home/ubuntu
        ssh -i "aether-qa.pem" ubuntu@172.31.35.35 "docker exec  gnbsim-1 cat summary.log"
        """
      }
    }
    
    stage("Validate GNB-SIM Run Test Results"){
      steps {
        catchError(message:'Gnbsim Validation is failed', buildResult:'FAILURE', stageResult:'FAILURE')
        { 
        sh """
        cd /home/ubuntu
        ssh -i "aether-qa.pem" ubuntu@172.31.35.35 "docker exec  gnbsim-1 cat summary.log" | grep "Profile Status: PASS"  || true
        """
        }
      }
    }
    
   stage("Collect GNBSIM And AMF Logs"){
      steps {
        sh '''
        cd /home/ubuntu
        kubectl get pods -n omec
        logfile1=\$(ssh -i "aether-qa.pem" ubuntu@172.31.35.35 "docker exec  gnbsim-1 ls " | grep "gnbsim1-.*.log")  || true
        echo "${logfile1}"  || true
        ssh -i "aether-qa.pem" ubuntu@172.31.35.35 "docker cp gnbsim-1:/gnbsim/bin/${logfile1} /tmp/logs/gnbsim/${logfile1}" || true
        ssh -i "aether-qa.pem" ubuntu@172.31.35.35 "cat /tmp/logs/gnbsim/${logfile1}" || true
        cd  $WORKSPACE/
	    mkdir logs
        AMF_POD_NAME=\$(kubectl get pods -n omec | grep amf | awk 'NR==1{print \$1}') 
        echo "${AMF_POD_NAME}"
        kubectl logs $AMF_POD_NAME -n omec > logs/2server_2004_default_amf.log
        WEBUI_POD_NAME=\$(kubectl get pods -n omec | grep webui | awk 'NR==1{print \$1}') 
        echo "${WEBUI_POD_NAME}"
        kubectl logs $WEBUI_POD_NAME -n omec > logs/2server_2004_default_webui.log
        UDR_POD_NAME=\$(kubectl get pods -n omec | grep udr | awk 'NR==1{print \$1}') 
        echo "${UDR_POD_NAME}"
        kubectl logs $UDR_POD_NAME -n omec > logs/2server_2004_default_udr.log
        UDM_POD_NAME=\$(kubectl get pods -n omec | grep udm | awk 'NR==1{print \$1}') 
        echo "${UDM_POD_NAME}"
        kubectl logs $UDM_POD_NAME -n omec > logs/2server_2004_default_udm.log
        AUSF_POD_NAME=\$(kubectl get pods -n omec | grep ausf | awk 'NR==1{print \$1}') 
        echo "${AUSF_POD_NAME}"
        kubectl logs $AUSF_POD_NAME -n omec > logs/2server_2004_default_ausf.log
        SMF_POD_NAME=\$(kubectl get pods -n omec | grep smf | awk 'NR==1{print \$1}') 
        echo "${SMF_POD_NAME}"
        kubectl logs $SMF_POD_NAME -n omec > logs/2server_2004_default_smf.log
        UPF_POD_NAME=\$(kubectl get pods -n omec | grep upf | awk 'NR==1{print \$1}') 
        echo "${UPF_POD_NAME}"
        kubectl logs $UPF_POD_NAME -n omec -c bessd > logs/2server_2004_default_upf.log
        
        '''
      }
    }
    
    stage("Archive Artifacts"){
        steps {
            
            // Archive Pods Logs 
            archiveArtifacts allowEmptyArchive: true, artifacts: "**/logs/*.log", followSymlinks: false
        }
    }

  }
  
  post {
      
        always {
            sh """
            cd $WORKSPACE/aether-onramp
            make monitor-uninstall
            make roc-uninstall
            make gnbsim-uninstall
            make 5gc-uninstall
            make k8s-uninstall
            make aether-uninstall
           """
               
        }      
        // triggered when red sign
        failure {
            slackSend color: "danger", message: "FAILED ${env.JOB_NAME} ${env.BUILD_NUMBER} ${env.BUILD_URL}" 

        }
    }
         
}
