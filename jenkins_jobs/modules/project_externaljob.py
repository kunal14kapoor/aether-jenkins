

"""
The External Job Project module handles creating ExternalJob Jenkins projects.
You may specify ``externaljob`` in the ``project-type`` attribute of the
:ref:`Job` definition.

This type of job allows you to record the execution of a process run outside
Jenkins, even on a remote machine. This is designed so that you can use
Jenkins as a dashboard of your existing automation system.

Requires the Jenkins :jenkins-plugins:`External Monitor Job Type Plugin
<external-monitor-job>`.

Example:

    .. literalinclude:: /../../tests/general/fixtures/project-type005.yaml

"""

import xml.etree.ElementTree as XML

import jenkins_jobs.modules.base


class ExternalJob(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        xml_parent = XML.Element("hudson.model.ExternalJob")
        return xml_parent
