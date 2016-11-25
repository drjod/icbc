from os import remove, path, access, R_OK, getpid
from sys import path as syspath
from subprocess import call, check_call
syspath.append(path.join(path.dirname(__file__), '..', 'pwds'))
from utilities import message, adapt_path, adapt_path_computer_selected, remove_file
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
    shell_script = '{}{}remoteRun_{}.sh'.format(
        rootDirectory, adapt_path('testingEnvironment\\scripts\\icbc\\temp\\'), getpid())

    upload_files(subject, simulation_data)
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
        call('C:\\\"Program Files (x86)\"\\PuTTY\\plink {}@{} -pw {} -m {}'.format(
            subject.user, subject.hostname, mod.pwd, shell_script), shell=True)
    except Exception as err:
        message(mode='ERROR', text='{0}'.format(err))

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
    except Exception as err:
        message(mode='ERROR', text='{0}'.format(err))
    else:
        f.write('#!/bin/sh\n')
        f.write('module load python3.3\n')
        f.write('python3 {}testingEnvironment/scripts/icbc/customized/run_remote.py '.format(subject.directory_root))
        f.write('{} {} {} {} {} '.format(subject.computer, subject.user, subject.code, subject.branch, getpid()))
        if operation_type == 'b':  # building
            f.write('None None  {} None None '.format(item.configuration))
        elif operation_type == 's':  # simulating
            f.write('{} {} {} {} {} '.format(
                item.type, item.case, item.configuration, item.flow_process, item.element_type))
        elif operation_type == 'p':  # plotting
            f.write(' {} {} {} None None '.format(item.type, item.case, item.configuration))
        f.write('{} {}'.format(operation_type, operation))
        f.close()


def upload_files(subject, simulation_data):
    """
    upload files with data for numerics and prallelization by calling winscp
    then remove files from temp directory on local computer
    :param item: (class Item)
    :param simulation_data: (class Simulation Data)
    :return:
    """
    mod = __import__(subject.computer)  # module with password for remote computer
    directory_local_temp = '{}{}'.format(rootDirectory, adapt_path('testingEnvironment\\scripts\\icbc\\temp\\'))
    directory_remote_temp = '{}{}'.format(subject.directory_root, adapt_path_computer_selected(
        'testingEnvironment\\scripts\\icbc\\temp\\', subject.operating_system))
    command_list = list()

    try:
        if simulation_data.read_file_flags.numerics:
            command_list.append('put {0}numerics_global_{2}.py {1}numerics_global_{2}.py'.format(
                directory_local_temp, directory_remote_temp, getpid()))
            command_list.append('put {0}numerics_flow_{2}.py {1}numerics_flow_{2}.py'.format(
                directory_local_temp, directory_remote_temp, getpid()))
            if simulation_data.numerics_global.processes.mass_flag:
                command_list.append('put {0}numerics_mass_{2}.py {1}numerics_mass_{2}.py'.format(
                    directory_local_temp, directory_remote_temp, getpid()))
            if simulation_data.numerics_global.processes.heat_flag:
                command_list.append('put {0}numerics_heat_{2}.py {1}numerics_heat_{2}.py'.format(
                    directory_local_temp, directory_remote_temp, getpid()))

            call_winscp(command_list, subject.user, subject.hostname, mod.pwd, False)
            remove_file('{}numerics_global_{}.py'.format(directory_local_temp, getpid()), False)
            remove_file('{}numerics_flow_{}.py'.format(directory_local_temp, getpid()), False)
            if simulation_data.numerics_global.processes.mass_flag:
                remove_file('{}numerics_mass_{}.py'.format(directory_local_temp, getpid()), False)
            if simulation_data.numerics_global.processes.heat_flag:
                remove_file('{}numerics_heat_{}.py'.format(directory_local_temp, getpid()), False)
        if simulation_data.read_file_flags.processing:
            command_list.clear()
            command_list.append('put {0}processing_{2}.py {1}processing_{2}.py'.format(
                directory_local_temp, directory_remote_temp, getpid()))

            call_winscp(command_list, subject.user, subject.hostname, mod.pwd, False)
            remove_file('{}processing_{}.py'.format(directory_local_temp, getpid()), False)

    except Exception as err:
        message(mode='ERROR', text='{0}'.format(err))


def download_file_with_winscp(file_winscp, tarfile_remote, user, hostname, password, output_flag=True):
    """
    1. write file for winscp
    2. execute winscp to download file from remote computer
    :param file_winscp: (string)
    :param tarfile_remote: (string)
    :param user: (string)
    :param hostname: (string)
    :param password: (string)
    :param output_flag: (bool)
    :return:
    """
    write_winscp_file(file_winscp, ['get {}'.format(tarfile_remote)], user, hostname, password, output_flag)
    try:
        check_call(winscp + ' /script={}'.format(file_winscp))
        print('\n')
    except Exception as err:
        message(mode='ERROR', text='{0}'.format(err))


def write_winscp_file(file_winscp, winscp_command_list, user, hostname, password, output_flag=True):
    """

    :param file_winscp: (string)
    :param winscp_command_list: (string list)
    :param user: (string)
    :param hostname: (string)
    :param password: (string)
    :param output_flag: (bool)
    :return:
    """
    file_winscp = adapt_path(file_winscp)

    if output_flag:
        message(mode='INFO', text='    Write winscp file')
    try:
        f = open(file_winscp, 'w')
    except OSError as err:
        message(mode='ERROR', text='OS error: {0}'.format(err))
    else:
        f.write('option batch abort \n')
        f.write('option confirm off \n')
        f.write('open sftp://{}:{}@{}/ \n'.format(user, password, hostname))
        for command in winscp_command_list:
            f.write('{} \n'.format(command))
        f.write('exit')
        f.close()


def call_winscp(winscp_command_list, user, hostname, password, output_flag=True):
    """
    file is marked and identified with process id
    :param winscp_command_list:
    :param user:
    :param hostname:
    :param password:
    :param output_flag:
    :return:
    """
    temp_winscp_file = '{}{}winscp_file_{}.txt'.format(rootDirectory, adapt_path(
        'testingEnvironment\\scripts\\icbc\\temp\\'), getpid())
    write_winscp_file(temp_winscp_file, winscp_command_list, user, hostname, password, output_flag)
    try:
        check_call('{} /script={}'.format(winscp, temp_winscp_file))
    except Exception as err:
        message(mode='ERROR', text='{0}'.format(err))
    remove_file(temp_winscp_file, False)
    print('\n')

