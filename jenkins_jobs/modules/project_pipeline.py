
"""
The Pipeline Project module handles creating Jenkins Pipeline projects
(formerly known as the Workflow projects).
You may specify ``pipeline`` in the ``project-type`` attribute of
the :ref:`Job` definition.

Requires the Jenkins :jenkins-plugins:`Pipeline Plugin <workflow-aggregator>`.

In order to write an inline script within a job-template you have to escape the
curly braces by doubling them in the DSL: { -> {{ , otherwise it will be
interpreted by the python str.format() command.

:Job Parameters:
    * **sandbox** (`bool`): If the script should run in a sandbox (default
      false)
    * **dsl** (`str`): The DSL content or,
    * **pipeline-scm** (`str`): in case "Pipeline as code" feature is used.
      Then you should specify:

        * **scm**: single ``scm`` component (or a reference) describing the
          source code repository
        * **script-path**: path to the Groovy file containing the job's steps
          (optional, default: ``Jenkinsfile``)
        * **lightweight-checkout** (`bool`): If selected, try to obtain the
          Pipeline script contents directly from the SCM without performing a
          full checkout. (optional, default: ``false``)

Note that ``dsl`` and ``pipeline-scm`` parameters are mutually exclusive.

Inline DSL job example:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_pipeline_template001.yaml

Inline DSL job template example:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_pipeline_template002.yaml

"Pipeline as code" example:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_pipeline_template004.yaml

"Pipeline as code" example using templates:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_pipeline_template005.yaml

"Pipeline as nested stage" example :

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_pipeline_template006.yaml

.. _Pipeline as code: https://jenkins.io/solutions/pipeline/

"""
import xml.etree.ElementTree as XML

from jenkins_jobs.errors import JenkinsJobsException
import jenkins_jobs.modules.base


class Pipeline(jenkins_jobs.modules.base.Base):
    sequence = 0
    error_msg = "You cannot declare both 'dsl' and 'pipeline-scm' on a " "pipeline job"

    def root_xml(self, data):
        xml_parent = XML.Element("flow-definition", {"plugin": "workflow-job"})
        if "dsl" in data and "pipeline-scm" in data:
            raise JenkinsJobsException(self.error_msg)
        if "dsl" in data:
            xml_definition = XML.SubElement(
                xml_parent,
                "definition",
                {
                    "class": "org.jenkinsci.plugins." "workflow.cps.CpsFlowDefinition",
                    "plugin": "workflow-cps",
                },
            )
            XML.SubElement(xml_definition, "script").text = data["dsl"]
        elif "pipeline-scm" in data:
            xml_definition = XML.SubElement(
                xml_parent,
                "definition",
                {
                    "class": "org.jenkinsci.plugins.workflow.cps."
                    "CpsScmFlowDefinition",
                    "plugin": "workflow-cps",
                },
            )
        else:
            raise JenkinsJobsException(
                "Either 'dsl' or 'pipeline-scm' " "is required for pipeline job"
            )

        needs_workspace = data.get("sandbox", False)
        XML.SubElement(xml_definition, "sandbox").text = str(needs_workspace).lower()

        return xml_parent
