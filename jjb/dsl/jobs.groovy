pipeline {
    agent any
    stages {
        stage('Create Jobs') {
            steps {
                script {
                    // Directory containing YAML files for pipeline configurations
                    def yamlFilesDir = '${WORKSPACE}/jjb/template'

                    // Read YAML files from the directory
                    def yamlFiles = findFiles(glob: "${yamlFilesDir}/*.yaml")

                    yamlFiles.each { yamlFile ->
                        def config = readYaml(file: "${yamlFilesDir}/${yamlFile.name}")
                        createPipelineJobFromYaml(config)
                    }
                }
            }
        }
    }
}

def createPipelineJobFromYaml(config) {
    def pipelineFile = config.pipeline-script
    def description = config.description
    def trigger = config.triggers
    def jobName = config.name
    
    def pipelineScript = readFileFromWorkspace(pipelineFile)
    
    pipelineJob(jobName) {
        description(description) // Set description for the job
        triggers {
            cron(trigger) // Set trigger for the job
        }
        definition {
            cps {
                script(pipelineScript)
            }
        }
    }
}

def readFileFromWorkspace(filePath) {
    def fileContent = readFile(filePath)
    return fileContent
}
