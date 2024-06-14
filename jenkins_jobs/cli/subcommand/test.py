
import logging
import sys

import jenkins_jobs.cli.subcommand.update as update


logger = logging.getLogger(__name__)


class TestSubCommand(update.UpdateSubCommand):
    def parse_args(self, subparser):
        test = subparser.add_parser("test")

        self.parse_option_recursive_exclude(test)

        self.parse_arg_path(test)
        self.parse_arg_names(test)

        test.add_argument(
            "--config-xml",
            action="store_true",
            dest="config_xml",
            default=False,
            help="use alternative output file layout using config.xml files",
        )
        test.add_argument(
            "-p",
            "--plugin-info",
            dest="plugins_info_path",
            default=None,
            help="path to plugin info YAML file",
        )
        test.add_argument(
            "-o", dest="output_dir", default=sys.stdout, help="path to output XML"
        )

    def execute(self, options, jjb_config):
        if not options.config_xml:
            logger.warning(
                "(Deprecated) The default output behavior of"
                " `jenkins-jobs test` when given the --output"
                " flag will change in JJB 3.0."
                " Instead of writing jobs to OUTPUT/jobname;"
                " they will be written to OUTPUT/jobname/config.xml."
                " The new behavior can be enabled by the passing"
                " `--config-xml` parameter."
            )

        builder, xml_jobs, xml_views = self.make_jobs_and_views_xml(
            jjb_config, options.path, options.names
        )

        builder.update_jobs(
            xml_jobs,
            output=options.output_dir,
            n_workers=1,
            config_xml=options.config_xml,
        )
        builder.update_views(
            xml_views,
            output=options.output_dir,
            n_workers=1,
            config_xml=options.config_xml,
        )
