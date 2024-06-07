import groovy.yaml.YamlSlurper

// Function to create pipeline job from YAML configuration
def createPipelineJobFromYaml(yamlFilePath) {
    def config = new YamlSlurper().parse(new File(yamlFilePath))
    def pipelineFile = config['pipeline-script']
    def description = config['description']
    def trigger = config['triggers']
    def jobName = config['name'] ?: getJobNameFromFilename(pipelineFile)
    
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

// Function to get job name from filename
def getJobNameFromFilename(filename) {
    return filename.take(filename.lastIndexOf('.'))
}

// Function to read file content from workspace
def readFileFromWorkspace(filePath) {
    def fileContent = readFile(filePath)
    return fileContent
}

// Directory containing YAML files for pipeline configurations
def yamlFilesDir = '${WORKSPACE}/jjb/template/'

// Read pipeline configurations from YAML files
def yamlFiles = new File(yamlFilesDir).listFiles().findAll { it.name.endsWith('.yaml') }

yamlFiles.each { yamlFile ->
    createPipelineJobFromYaml(yamlFile)
}

