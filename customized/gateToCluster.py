from os import remove, path, access, R_OK
from sys import path as syspath
from subprocess import call
syspath.append(path.join(path.dirname(__file__), '..', 'customized'))
syspath.append(path.join(path.dirname(__file__), '..', 'pwds'))
from utilities import message, adapt_path
from configurationCustomized import rootDirectory, winscp


def operate(subject, item, operation_type, operation, simulation_data):
    """

    :param subject: (class Subject)
    :param item: (class Item)
    :param operation_type: (one-char string)
    :param operation: (one-char string)
    :param simulation_data: (string)
    :return:
    """

    # the naming allows to upload several shell_scripts by separate icbc instances
    if operation_type == 's':  # simulating
        shell_script = adapt_path(rootDirectory + 'testingEnvironment\\scripts\\icbc\\temp\\remoteRun' + '_' +
                                  operation_type + '_' + operation + '_' + item.type + '_' +
                                  item.case + '_' + item.configuration + '.sh')
    else:  # building depends only on configuration (plotting is always local)
        shell_script = adapt_path(rootDirectory + 'testingEnvironment\\scripts\\icbc\\temp\\remoteRun' + '_' +
                                  operation_type + '_' + operation + '_' + item.configuration + '.sh')

    upload_files(item, simulation_data)
    write_shell_script_for_remote_run(subject, item, operation_type, operation, shell_script)
    execute_shell_script_on_remote_computer(subject, shell_script)


def execute_shell_script_on_remote_computer(subject, shell_script):
    """

    :param subject: (class Subject)
    :param shell_script: (string)
    :return:
    """
    mod = __import__(subject.computer)
    try:
        call('plink ' + subject.user + '@' + subject.hostname + ' -pw ' + mod.pwd + ' -m ' + shell_script, shell=True)
    except Exception as e:
        message(mode='ERROR', text="*****")

    if path.isfile(shell_script) and access(shell_script, R_OK):
        remove(shell_script)


def write_shell_script_for_remote_run(subject, item, operation_type, operation, shell_script):
    """

    :param subject: (Subject)
    :param item: (Item)
    :param operation_type: (one-char string)
    :param operation: (one-char string)
    :param shell_script: (string)
    :return:
    """
    try:
        f = open(shell_script, 'w')
    except Exception as e:
        message(mode='ERROR', text="*****")
    else:
        f.write('#!/bin/sh\n')
        f.write('module load python3.3\n')
        f.write('python ' + subject.directory_root + 'testingEnvironment/scripts/icbc/customized/run_remote.py ')
        f.write(subject.computer + ' ' + subject.user + ' ' + subject.code + ' ' + subject.branch + ' ')
        if operation_type == 'b':  # building
            f.write('No No  ' + item.configuration + ' ')
        else:
            f.write(item.type + ' ' + item.case + ' ' + item.configuration + ' ')
        f.write(operation_type + ' ' + operation)
        f.close()


def upload_files(item, simulation_data):
    """
    upload files with data for numerics and prallelization
    :param item: (class Item)
    :param simulation_data: (class Simulation Data)
    :return:
    """
    try:
        if simulation_data.read_file_flags.numerics:
            call(winscp + ' /script=' + rootDirectory +
                 'testingEnvironment\\scripts\\icbc\\customized\\winscp_uploadNumericsData_' +
                 item.configuration + '.txt', shell=True)
            print('\n')
        if simulation_data.read_file_flags.processing:
            call(winscp + ' /script=' + rootDirectory +
                 'testingEnvironment\\scripts\\icbc\\customized\\winscp_uploadProcessingData_' +
                 item.configuration + '.txt', shell=True)
            print('\n')
    except Exception as e:
        message(mode='ERROR', text="*****")
