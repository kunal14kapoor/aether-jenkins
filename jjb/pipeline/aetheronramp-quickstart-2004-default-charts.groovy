// SPDX-FileCopyrightText: 2023 Open Networking Foundation <info@opennetworking.org>
// SPDX-License-Identifier: LicenseRef-ONF-Member-Only-1.0
pipeline {

  agent {
        //label 'ubuntu-18.04-t3a2xlarge-mumbai'
        label "Mumbai-B2-20.04"
    }
  
  stages{
      
    stage('Clean workspace'){
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
            sudo cp /home/ubuntu/hosts.ini hosts.ini
            #sudo cp /home/ubuntu/sdcore-5g-values-new.yaml  deps/5gc/roles/core/templates/sdcore-5g-values.yaml
            sudo cp vars/main-quickstart.yml vars/main.yml
            grep -rl "ens18" . | xargs sed -i 's/ens18/eth0/g'
            sudo sed -i "s/10.76.28.113/\$(hostname -I | awk '{ print \$1 }')/" vars/main.yml
            #pipx install --include-deps ansible --force
            #pipx ensurepath
            make aether-pingall
            ansible-galaxy collection install kubernetes.core
            make k8s-install
            ansible-galaxy collection install ansible.posix
            make 5gc-install
            #ansible-galaxy collection install community.docker:2.7.3 --force
            #ansible-galaxy collection install ansible.utils:2.8.0 --force
            #make gnbsim-docker-install
            make gnbsim-install
            #make gnbsim-simulator-run
            #docker exec gnbsim-1 cat summary.log
            
           """ 
	   }
    }
    stage('Run GNB-SIM Test'){
	    steps {
	        retry(2) {
	            sh """
	                cd $WORKSPACE/aether-onramp
	                sleep 120
	                kubectl get pods -n omec
                    make gnbsim-simulator-run
                    docker exec gnbsim-1 cat summary.log
            
            """
	       } 
	    }
	}
	
	stage ('GNB-SIM validation'){
	    steps {
	        catchError(message:'Gnbsim Validation is failed', buildResult:'FAILURE', stageResult:'FAILURE')
	        {
	        sh """
	        docker exec gnbsim-1 cat summary.log  | grep "Profile Status: PASS"
	        
            """
	        }    
	    }
	}
	
    stage("Collect GNBSIM and AMF Logs "){
      steps {
        sh '''
        cd  $WORKSPACE/
	    mkdir logs
        kubectl get pods -n omec
        logfile=\$(docker exec gnbsim-1 ls | grep "gnbsim1-.*.log")
        echo "${logfile}"
        docker cp gnbsim-1:/gnbsim/bin/${logfile} logs/${logfile}
        #cat logs/${logfile}
	    AMF_POD_NAME=\$(kubectl get pods -n omec | grep amf | awk 'NR==1{print \$1}') 
        echo "${AMF_POD_NAME}"
        kubectl logs $AMF_POD_NAME -n omec > logs/quickstart_2004_default_amf.log
        WEBUI_POD_NAME=\$(kubectl get pods -n omec | grep webui | awk 'NR==1{print \$1}') 
        echo "${WEBUI_POD_NAME}"
        kubectl logs $WEBUI_POD_NAME -n omec > logs/quickstart_2004_default_webui.log
        UDR_POD_NAME=\$(kubectl get pods -n omec | grep udr | awk 'NR==1{print \$1}') 
        echo "${UDR_POD_NAME}"
        kubectl logs $UDR_POD_NAME -n omec > logs/quickstart_2004_default_udr.log
        UDM_POD_NAME=\$(kubectl get pods -n omec | grep udm | awk 'NR==1{print \$1}') 
        echo "${UDM_POD_NAME}"
        kubectl logs $UDM_POD_NAME -n omec > logs/quickstart_2004_default_udm.log
        AUSF_POD_NAME=\$(kubectl get pods -n omec | grep ausf | awk 'NR==1{print \$1}') 
        echo "${AUSF_POD_NAME}"
        kubectl logs $AUSF_POD_NAME -n omec > logs/quickstart_2004_default_ausf.log
        SMF_POD_NAME=\$(kubectl get pods -n omec | grep smf | awk 'NR==1{print \$1}') 
        echo "${SMF_POD_NAME}"
        kubectl logs $SMF_POD_NAME -n omec > logs/quickstart_2004_default_smf.log
            
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
      
        // only triggered when blue or green sign
//            success {
//                slackSend color: "good", message: "PASSED ${env.JOB_NAME} ${env.BUILD_NUMBER} ${env.BUILD_URL}"           
//                }
        // triggered when red sign
            failure {
                slackSend color: "danger", message: "FAILED ${env.JOB_NAME} ${env.BUILD_NUMBER} ${env.BUILD_URL}" 

           }
         }
}
