

"""
The MultiJob Project module handles creating MultiJob Jenkins projects.
You may specify ``multijob`` in the ``project-type`` attribute of
the :ref:`Job` definition.

This project type may use :py:func:`jenkins_jobs.modules.builders.multijob` \
builders.

Requires the Jenkins :jenkins-plugins:`Multijob Plugin <jenkins-multijob-plugin>`.

Example::

  job:
    name: test_job
    project-type: multijob
    builders:
      - multijob:
          name: PhaseOne
          condition: SUCCESSFUL
          projects:
            - name: PhaseOneJobA
              current-parameters: true
              git-revision: true
            - name: PhaseOneJobB
              current-parameters: true
              property-file: build.props
      - multijob:
          name: PhaseTwo
          condition: UNSTABLE
          projects:
            - name: PhaseTwoJobA
              current-parameters: true
              predefined-parameters: foo=bar
            - name: PhaseTwoJobB
              current-parameters: false
"""

import xml.etree.ElementTree as XML

import jenkins_jobs.modules.base


class MultiJob(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        xml_parent = XML.Element(
            "com.tikal.jenkins.plugins.multijob." "MultiJobProject"
        )
        return xml_parent
