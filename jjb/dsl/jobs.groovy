def repo = 'https://github.com/kunal14kapoor/aether-jenkins.git'
def branch = 'main'

pipelineJob('example-pipeline-1') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url(repo)
                    }
                    branches(branch)
                }
            }
            scriptPath('pipelines/aetheronramp_quickstart_2004_default_charts.groovy')
        }
    }
}

