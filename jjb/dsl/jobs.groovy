import groovy.io.FileType

// Path to the directory containing pipeline scripts, using $WORKSPACE
def scriptsDirectory = new File("${WORKSPACE}/jjb/pipeline")

// Ensure the directory exists
if (!scriptsDirectory.exists()) {
    throw new RuntimeException("Directory ${scriptsDirectory} does not exist")
}

// Iterate over each Groovy file in the directory
scriptsDirectory.eachFileRecurse(FileType.FILES) { file ->
    if (file.name.endsWith('.groovy')) {
        def jobName = file.name.replace('.groovy', '')
        def pipelineScript = file.text

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
