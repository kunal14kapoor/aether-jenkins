
"""
Deprecated: please use :ref:`project_pipeline` instead.

The workflow Project module handles creating Jenkins workflow projects.
You may specify ``workflow`` in the ``project-type`` attribute of
the :ref:`Job` definition.
For now only inline scripts are supported.

Requires the Jenkins :jenkins-plugins:`Workflow Plugin <workflow-aggregator>`.

In order to use it for job-template you have to escape the curly braces by
doubling them in the DSL: { -> {{ , otherwise it will be interpreted by the
python str.format() command.

:Job Parameters:
    * **dsl** (`str`): The DSL content.
    * **sandbox** (`bool`): If the script should run in a sandbox (default
      false)

Job example:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_workflow_template001.yaml

Job template example:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_workflow_template002.yaml

"""
import logging
import xml.etree.ElementTree as XML

import jenkins_jobs.modules.base
import jenkins_jobs.modules.helpers as helpers


class Workflow(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        logger = logging.getLogger(__name__)
        logger.warning("Workflow job type is deprecated, please use Pipeline job type")

        xml_parent = XML.Element("flow-definition", {"plugin": "workflow-job"})
        xml_definition = XML.SubElement(
            xml_parent,
            "definition",
            {
                "class": "org.jenkinsci.plugins." "workflow.cps.CpsFlowDefinition",
                "plugin": "workflow-cps",
            },
        )

        mapping = [("dsl", "script", None), ("sandbox", "sandbox", False)]
        helpers.convert_mapping_to_xml(
            xml_definition, data, mapping, fail_required=True
        )

        return xml_parent
