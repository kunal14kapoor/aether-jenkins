
from unittest import mock


def test_delete_single_job(mocker, default_config_file, execute_jenkins_jobs):
    """
    Test handling the deletion of a single Jenkins job.
    """

    mocker.patch("jenkins_jobs.cli.subcommand.base.JenkinsManager.delete_jobs")
    mocker.patch("jenkins_jobs.cli.subcommand.base.JenkinsManager.delete_views")

    args = ["--conf", default_config_file, "delete", "test_job"]
    execute_jenkins_jobs(args)


def test_delete_multiple_jobs(mocker, default_config_file, execute_jenkins_jobs):
    """
    Test handling the deletion of multiple Jenkins jobs.
    """

    mocker.patch("jenkins_jobs.cli.subcommand.base.JenkinsManager.delete_jobs")
    mocker.patch("jenkins_jobs.cli.subcommand.base.JenkinsManager.delete_views")

    args = ["--conf", default_config_file, "delete", "test_job1", "test_job2"]
    execute_jenkins_jobs(args)


def test_delete_using_glob_params(
    mocker, fixtures_dir, default_config_file, execute_jenkins_jobs
):
    """
    Test handling the deletion of multiple Jenkins jobs using the glob
    parameters feature.
    """

    delete_job_mock = mocker.patch("jenkins_jobs.builder.JenkinsManager.delete_job")

    args = [
        "--conf",
        default_config_file,
        "delete",
        "--path",
        str(fixtures_dir / "cmd-002.yaml"),
        "*bar*",
    ]
    execute_jenkins_jobs(args)
    calls = [mock.call("bar001"), mock.call("bar002")]
    delete_job_mock.assert_has_calls(calls, any_order=True)
    assert delete_job_mock.call_count == len(
        calls
    ), "Jenkins.delete_job() was called '%s' times when " "expected '%s'" % (
        delete_job_mock.call_count,
        len(calls),
    )
