
import logging

import yaml

from jenkins_jobs.builder import JenkinsManager
import jenkins_jobs.cli.subcommand.base as base


logger = logging.getLogger(__name__)


class GetPluginsInfoSubCommand(base.BaseSubCommand):
    def parse_args(self, subparser):
        plugins_info = subparser.add_parser(
            "get-plugins-info", help="get plugins info yaml by querying Jenkins server."
        )

        plugins_info.add_argument(
            "-o",
            "--output-file",
            default="plugins_info.yaml",
            dest="plugins_info_file",
            help="file to save output to.",
        )

    def execute(self, options, jjb_config):
        builder = JenkinsManager(jjb_config)
        plugin_data = builder.jenkins.get_plugins_info()
        plugins_info = []
        for plugin in plugin_data:
            info = {
                "longName": str(plugin["longName"]),
                "shortName": str(plugin["shortName"]),
                "version": str(plugin["version"]),
            }
            plugins_info.append(info)

        if options.plugins_info_file:
            with open(options.plugins_info_file, "w") as outfile:
                outfile.write(yaml.dump(plugins_info))
            logger.info("Generated {} file".format(options.plugins_info_file))
        else:
            print(yaml.dump(plugins_info))
