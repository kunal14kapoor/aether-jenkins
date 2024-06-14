
import os
from operator import attrgetter
from pathlib import Path

import pytest

from jenkins_jobs.errors import JenkinsJobsException
from tests.enum_scenarios import scenario_list

fixtures_dir = Path(__file__).parent / "error_fixtures"


@pytest.fixture(
    params=scenario_list(fixtures_dir),
    ids=attrgetter("name"),
)
def scenario(request):
    return request.param


# Override to avoid scenarios usage.
@pytest.fixture
def config_path():
    return os.devnull


# Override to avoid scenarios usage.
@pytest.fixture
def plugins_info():
    return None


def test_error(check_parser, scenario, expected_error):
    with pytest.raises(JenkinsJobsException) as excinfo:
        check_parser(scenario.in_path)
    error = "\n".join(excinfo.value.lines)
    print()
    print(error)
    canonical_error = error.replace(str(fixtures_dir) + "/", "").replace(
        str(fixtures_dir), "fixtures-dir"
    )
    assert canonical_error == expected_error
