
"""
View support for All view-type.

To create an all view specify ``all`` in the ``view-type`` attribute
to the :ref:`view_all` definition.

Example:

    .. literalinclude::
        /../../tests/views/fixtures/view-all-minimal.yaml
"""

import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base
import jenkins_jobs.modules.helpers as helpers


class All(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        root = XML.Element("hudson.model.AllView")

        mapping = [
            ("name", "name", None),
            ("description", "description", ""),
            ("filter-executors", "filterExecutors", False),
            ("filter-queue", "filterQueue", False),
        ]
        helpers.convert_mapping_to_xml(root, data, mapping, fail_required=True)

        XML.SubElement(root, "properties", {"class": "hudson.model.View$PropertyList"})

        return root
