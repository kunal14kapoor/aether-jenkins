
from jenkins_jobs.builder import JenkinsManager
from jenkins_jobs.errors import JenkinsJobsException
import jenkins_jobs.cli.subcommand.base as base


class DeleteSubCommand(base.JobsSubCommand):
    def parse_args(self, subparser):
        delete = subparser.add_parser("delete")

        self.parse_option_recursive_exclude(delete)

        delete.add_argument("name", help="name of job", nargs="+")
        delete.add_argument(
            "-p",
            "--path",
            default=None,
            help="colon-separated list of paths to YAML files " "or directories",
        )
        delete.add_argument(
            "-j",
            "--jobs-only",
            action="store_true",
            dest="del_jobs",
            default=False,
            help="delete only jobs",
        )
        delete.add_argument(
            "-v",
            "--views-only",
            action="store_true",
            dest="del_views",
            default=False,
            help="delete only views",
        )

    def execute(self, options, jjb_config):
        builder = JenkinsManager(jjb_config)

        if options.del_jobs and options.del_views:
            raise JenkinsJobsException(
                '"--views-only" and "--jobs-only" cannot be used together.'
            )

        if options.path:
            roots = self.load_roots(jjb_config, options.path)
            jobs = base.filter_matching(roots.generate_jobs(), options.name)
            views = base.filter_matching(roots.generate_views(), options.name)
            job_names = [j.name for j in jobs]
            view_names = [v.name for v in views]
        else:
            job_names = options.name
            view_names = options.name

        if options.del_jobs:
            builder.delete_jobs(job_names)
        elif options.del_views:
            builder.delete_views(view_names)
        else:
            builder.delete_jobs(job_names)
            builder.delete_views(view_names)
