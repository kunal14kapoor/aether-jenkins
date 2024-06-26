import time
from multiprocessing import cpu_count

from jenkins_jobs.parallel import concurrent


def test_parallel_correct_order():
    expected = list(range(10, 20))

    @concurrent
    def parallel_test(num_base, num_extra):
        return num_base + num_extra

    parallel_args = [{"num_extra": num} for num in range(10)]
    result = parallel_test(10, concurrent=parallel_args)
    assert result == expected


def test_parallel_time_less_than_serial():
    @concurrent
    def wait(secs):
        time.sleep(secs)

    before = time.time()
    # ten threads to make it as fast as possible
    wait(concurrent=[{"secs": 1} for _ in range(10)], n_workers=10)
    after = time.time()
    assert after - before < 5


def test_parallel_single_thread():
    expected = list(range(10, 20))

    @concurrent
    def parallel_test(num_base, num_extra):
        return num_base + num_extra

    parallel_args = [{"num_extra": num} for num in range(10)]
    result = parallel_test(10, concurrent=parallel_args, n_workers=1)
    result == expected


def test_use_auto_detect_cores(mocker):
    mock = mocker.patch("jenkins_jobs.parallel.cpu_count", wraps=cpu_count)

    @concurrent
    def parallel_test():
        return True

    result = parallel_test(concurrent=[{} for _ in range(10)], n_workers=0)
    assert result == [True for _ in range(10)]
    mock.assert_called_once_with()
