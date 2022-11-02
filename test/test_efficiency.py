import pytest
import logging

from pytest import assume
from utils import runcmd

# ********************** fixture **********************

@pytest.fixture(scope='module')
def setup_module_test_efficiency(setup_session_test_tpu_perf, request):

    task, cfg = setup_session_test_tpu_perf
    task_name = task['task_name']

    logging.info("setup_module_test_efficiency called. [{}]".format(task_name))

    test_case_txt = task['test_case_txt']
    ret_regex_list=[r'ERROR', r'Command failed, please check (.*)']
    if task_name == 'test_nntc':
        retcode, ret_str = runcmd(cmd='bash -c \"python3 -m tpu_perf.build --time --list {}\"'.format(test_case_txt), ret_regex_list=ret_regex_list)
    elif task_name == 'test_mlir':
        retcode, ret_str = runcmd(cmd='bash -c \"python3 -m tpu_perf.build --mlir --list {}\"'.format(test_case_txt), ret_regex_list=ret_regex_list)
    else:
        logging.error(f'Unrecognized task name: {task_name}')
    with assume:
        assert retcode == 0
        assert len(ret_str[0]) == 0

    def teardown_module_test_efficiency():
        logging.info("teardown_module_test_efficiency called. [{}]".format(task_name))

    request.addfinalizer(teardown_module_test_efficiency)

    return task, cfg