

"""
The Freestyle Project module handles creating freestyle Jenkins
projects (i.e., those that do not use Maven).  You may specify
``freestyle`` in the ``project-type`` attribute to the :ref:`Job`
definition if you wish, though it is the default, so you may omit
``project-type`` altogether if you are creating a freestyle project.

Example::

  job:
    name: test_job
    project-type: freestyle
"""

import xml.etree.ElementTree as XML

import jenkins_jobs.modules.base


class Freestyle(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        xml_parent = XML.Element("project")
        return xml_parent
