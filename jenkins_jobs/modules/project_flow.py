

"""
The flow Project module handles creating Jenkins flow projects.
You may specify ``flow`` in the ``project-type`` attribute of
the :ref:`Job` definition.

Requires the Jenkins :jenkins-plugins:`Build Flow Plugin <build-flow-plugin>`.

In order to use it for job-template you have to escape the curly braces by
doubling them in the DSL: { -> {{ , otherwise it will be interpreted by the
python str.format() command.

:Job Parameters:
    * **dsl** (`str`): The DSL content. (optional)
    * **needs-workspace** (`bool`): This build needs a workspace. \
    (default false)
    * **dsl-file** (`str`): Path to the DSL script in the workspace. \
    Has effect only when `needs-workspace` is true. (optional)

Job example:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_flow_template001.yaml

Job template example:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_flow_template002.yaml

Job example runninng a DSL file from the workspace:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_flow_template003.yaml

"""

import xml.etree.ElementTree as XML

import jenkins_jobs.modules.base
from jenkins_jobs.modules.helpers import convert_mapping_to_xml


class Flow(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        xml_parent = XML.Element("com.cloudbees.plugins.flow.BuildFlow")

        needs_workspace = data.get("needs-workspace", False)
        mapping = [
            ("dsl", "dsl", ""),
            ("needs-workspace", "buildNeedsWorkspace", False),
        ]
        convert_mapping_to_xml(xml_parent, data, mapping, fail_required=True)
        if needs_workspace and "dsl-file" in data:
            XML.SubElement(xml_parent, "dslFile").text = data["dsl-file"]

        return xml_parent
