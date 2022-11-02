import os
import re
import logging
import subprocess
from typing import Union, Tuple, List

def change_dir(dir):
    os.chdir(dir)
    logging.info('Current working dir: {}'.format(os.getcwd()))

def log_line(line, test_case_filename=None):
    error_regex = re.compile(r'(?i)\b(error|fail(ed)?|fault)\b')
    no_error_regex = re.compile(r'(?i)\b(no error)\b')
    warning_regex = re.compile(r'(?i)\b(warn(ing)?)\b')
    out_line = "{}{}".format('' if not test_case_filename else test_case_filename + ' :', line)
    if not error_regex.search(line) or no_error_regex.search(line):
        if not warning_regex.search(line):
            logging.info(out_line)
        else:
            logging.warning(out_line)
    else:
        logging.error(out_line)

#执行shell命令
def runcmd(
    cmd:str,
    ret_regex_list:list=None,
    timeout:int=0,
    timeout_signal:Union[int, str]='SIGINT',
    bufsize:int=-1,
    shell=False,
    subprocess_wait_time:int=60,
    workdir:str=None
) -> Union[int, Tuple[int, List[List[str]]]]:

    cwd = os.getcwd()
    workdir = './' if not workdir else workdir
    change_dir(workdir)
    if timeout:
        cmd = 'timeout -s {} {} {}'.format(timeout_signal, timeout, cmd)
    if not shell:
        cmd =  cmd.split()
    if ret_regex_list:
        ret = [[] for i in range(len(ret_regex_list))]
    logging.info('run command: {}'.format(cmd))
    logging.info('*********** run command start ***********')
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True, universal_newlines=True, bufsize=bufsize, shell=shell)
    for line in proc.stdout:
        line = line.strip()
        if ret_regex_list:
            for i, regex in enumerate(ret_regex_list):
                if type(regex) == str:
                    groups = re.findall(regex, line)
                else:
                    groups = regex.findall(line)
                if not groups:
                    continue
                if len(groups) > 1:
                    logging.error('regex extraction error')
                    logging.error('regex: {}'.format(regex))
                    assert len(groups) > 1
                ret[i].append(groups[0])
        log_line(line)
    try:
        proc.wait(timeout=subprocess_wait_time)
    except subprocess.TimeoutExpired:
        logging.error("{}: Test Time Out".format(cmd))
        proc.kill()
    logging.info('*********** run command end ***********')
    change_dir(cwd)
    if ret_regex_list:
        return proc.returncode, ret
    return proc.returncode