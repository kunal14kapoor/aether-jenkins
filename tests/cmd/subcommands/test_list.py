
from collections import namedtuple

import pytest


JobsScenario = namedtuple("JobsScnenario", "name jobs globs found")

jobs_scenarios = [
    JobsScenario("single", jobs=["job1"], globs=[], found=["job1"]),
    JobsScenario("multiple", jobs=["job1", "job2"], globs=[], found=["job1", "job2"]),
    JobsScenario(
        "multiple_with_folder",
        jobs=["folder1", "folder1/job1", "folder1/job2"],
        globs=[],
        found=["folder1", "folder1/job1", "folder1/job2"],
    ),
    JobsScenario(
        "multiple_with_glob",
        jobs=["job1", "job2", "job3"],
        globs=["job[1-2]"],
        found=["job1", "job2"],
    ),
    JobsScenario(
        "multiple_with_multi_glob",
        jobs=["job1", "job2", "job3", "job4"],
        globs=["job1", "job[24]"],
        found=["job1", "job2", "job4"],
    ),
]


@pytest.mark.parametrize(
    "scenario",
    [pytest.param(s, id=s.name) for s in jobs_scenarios],
)
def test_from_jenkins_tests(
    capsys, mocker, default_config_file, execute_jenkins_jobs, scenario
):
    def get_jobs():
        return [{"fullname": fullname} for fullname in scenario.jobs]

    mocker.patch("jenkins_jobs.builder.JenkinsManager.get_jobs", side_effect=get_jobs)

    args = ["--conf", default_config_file, "list"] + scenario.globs
    execute_jenkins_jobs(args)

    expected_out = "\n".join(scenario.found)
    captured = capsys.readouterr()
    assert captured.out.rstrip() == expected_out


YamlScenario = namedtuple("YamlScnenario", "name globs found")

yaml_scenarios = [
    YamlScenario("all", globs=[], found=["bam001", "bar001", "bar002", "baz001"]),
    YamlScenario(
        "some",
        globs=["*am*", "*002", "bar001"],
        found=["bam001", "bar001", "bar002"],
    ),
]


@pytest.mark.parametrize(
    "scenario",
    [pytest.param(s, id=s.name) for s in yaml_scenarios],
)
def test_from_yaml_tests(
    capsys, fixtures_dir, default_config_file, execute_jenkins_jobs, scenario
):
    path = fixtures_dir / "cmd-002.yaml"

    execute_jenkins_jobs(
        ["--conf", default_config_file, "list", "-p", str(path)] + scenario.globs
    )

    expected_out = "\n".join(scenario.found)
    captured = capsys.readouterr()
    assert captured.out.rstrip() == expected_out
