def repo = 'https://github.com/kunal14kapoor/aether-jenkins.git'
def branch = 'main'

// URL to the pipelines directory
def pipelinesUrl = "${repo}/jjb/pipeline?ref=${branch}"

// Get list of pipeline scripts from the GitHub API
def pipelines = new groovy.json.JsonSlurper().parse(new URL(pipelinesUrl).newReader())

pipelines.each { file ->
    if (file.name.endsWith('.groovy')) {
        def jobName = file.name.replace('.groovy', '')
        def scriptUrl = file.download_url
        def pipelineScript = new URL(scriptUrl).text

        pipelineJob(jobName) {
            definition {
                cps {
                    script(pipelineScript)
                    sandbox() // Optional: run in a secure sandbox
                }
            }
        }
    }
}


