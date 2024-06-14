

"""
The folder Project module handles creating Jenkins folder projects.
You may specify ``folder`` in the ``project-type`` attribute of
the :ref:`Job` definition.

Requires the Jenkins :jenkins-plugins:`CloudBees Folders Plugin
<cloudbees-folder>`.

Job example:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_folder_template001.yaml

Job template example:

    .. literalinclude::
      /../../tests/yamlparser/job_fixtures/project_folder_template002.yaml

"""

import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base
from jenkins_jobs.modules.helpers import convert_mapping_to_xml


class Folder(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        xml_parent = XML.Element(
            "com.cloudbees.hudson.plugins.folder.Folder", plugin="cloudbees-folder"
        )
        attributes = {
            "class": "com.cloudbees.hudson.plugins.folder." "icons.StockFolderIcon"
        }
        XML.SubElement(xml_parent, "icon", attrib=attributes)
        XML.SubElement(xml_parent, "views")
        attributes = {"class": "hudson.views.DefaultViewsTabBar"}
        XML.SubElement(xml_parent, "viewsTabBar", attrib=attributes)

        mappings = [("", "primaryView", "All"), ("", "healthMetrics", "")]
        convert_mapping_to_xml(xml_parent, data, mappings, True)

        return xml_parent
