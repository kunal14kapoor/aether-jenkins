from operator import attrgetter
from pathlib import Path

import pytest

from jenkins_jobs.errors import JenkinsJobsException
from jenkins_jobs.modules import project_multibranch
from tests.enum_scenarios import scenario_list

fixtures_dir = Path(__file__).parent / "error_fixtures"


@pytest.fixture(
    params=scenario_list(fixtures_dir),
    ids=attrgetter("name"),
)
def scenario(request):
    return request.param


def test_error(check_generator, expected_error):
    with pytest.raises(JenkinsJobsException) as excinfo:
        check_generator(project_multibranch.WorkflowMultiBranch)
    error = "\n".join(excinfo.value.lines)
    print()
    print(error)
    assert error.replace(str(fixtures_dir) + "/", "") == expected_error
