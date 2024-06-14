import os.path

import pytest

import jenkins_jobs


# Override fixture - do not use this mock.
@pytest.fixture(autouse=True)
def job_cache_mocked(mocker):
    pass


def test_save_on_exit(mocker):
    """
    Test that the cache is saved on normal object deletion
    """
    mocker.patch("jenkins_jobs.builder.JobCache.get_cache_dir", lambda x: "/bad/file")

    save_mock = mocker.patch("jenkins_jobs.builder.JobCache.save")
    mocker.patch("os.path.isfile", return_value=False)
    mocker.patch("jenkins_jobs.builder.JobCache._lock")
    jenkins_jobs.builder.JobCache("dummy")
    save_mock.assert_called_with()


def test_cache_file(mocker):
    """
    Test providing a cachefile.
    """
    mocker.patch("jenkins_jobs.builder.JobCache.get_cache_dir", lambda x: "/bad/file")

    test_file = os.path.abspath(__file__)
    mocker.patch("os.path.join", return_value=test_file)
    mocker.patch("yaml.safe_load")
    mocker.patch("jenkins_jobs.builder.JobCache._lock")
    jenkins_jobs.builder.JobCache("dummy").data = None
