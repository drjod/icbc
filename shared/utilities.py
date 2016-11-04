import sys
from os import stat, chdir, mkdir, remove, path, listdir, access, R_OK
from shutil import move, copy
from tarfile import open as open_tar
from difflib import ndiff
from platform import system
from subprocess import check_call
from configurationShared import verbosity, examplesName, outputFileEndings, additionalFileEndings
from configurationCustomized import winscp

def message(mode='ERROR', text=None, not_supported=None):
    """
    prints message if verbosity > 0
    :param mode: ['INFO', 'WARNING', 'ERROR'] (string)
        Info: only text
        Warning: text and name of function where call is from
        Error: text and name of function where call is from
    :param text:  message (string)
    :param not_supported: prints '*** is not supported' as an option to text (string)
    :return:
    """
    if verbosity > 0:
        if not_supported:
            print_message = not_supported + ' is not supported'
        else:
            print_message = text

        if mode == 'INFO':
            in_function = ''
        else:
            in_function = ' in function ' + sys._getframe(1).f_code.co_name
            
        print(mode + in_function + ' - ' + print_message)


def unix2dos(file):
    """
    :param file:
    :return:
    """
    infile = open(file,'r')
    outfile = open('dos_' + file, 'w')
    for line in infile:
        line = line.rstrip() + '\r\n'
        outfile.write(line)
    infile.close()
    outfile.close()         
    move('dos_' + file, file)


def dos2unix(file):
    text = open(file, 'rb').read().replace('\r\n', '\n')
    open(file, 'wb').write(text)


def adapt_path(path):
    """
    converts windows path into linux (unix) according to platform where script runs
    :param path:
    :return:
    """
    if system() == 'Windows':
        return path
    elif system() == 'Linux':
        return path.replace('\\', '/')
    else:
        message(mode='ERROR', not_supported=system())


def adapt_path_computer_selected(path, operating_system):
    """
    converts windows path into linux (unix) and vice verca according to platform of selected computer
    used for plotting operations (all local while simulation operations might be remote)
    :param path:
    :param operating_system:
    :return:
    """
    if operating_system == 'windows':
        return path.replace('/', '\\')
    elif operating_system == 'linux':
        return path.replace('\\', '/')
    else:
        message(mode='ERROR', not_supported=operating_system)


def generate_folder(root, folder_list):
    """
    called if folder is missing
    :param root:
    :param folder_list:
    :return:
    """
    path = root
    for folder in folder_list:
        path = adapt_path(path + folder + '\\')
        
        try:
            stat(path)
        except:
            mkdir(path)


def remove_file(file_name):
    """
    if file exists, remove it
    :param file_name:
    :return:
    """
    try:
        remove(file_name)
        message(mode='INFO', text='Removing ' + file_name)
    except OSError:
        pass


def select_from_options(option_dict, message_text):
    """
    select by user input from dictionary with options
    recalls itself in case of non-proper user input
    :param option_dict: {string: string, ...} key is value to type in to select
    :param message_text: (string) printed with the dictionary keys and values
    to ask user for input, e.g. 'Select option type'
    :return: (one-char string) selected option (=selected key of dictionary)
    """
    print('\n ' + message_text + ':')
    for key, option in option_dict.items():
        print('    ' + option)
    option_selected = input('\n')

    if option_selected in option_dict:
        return str(option_selected)
    else:
        message(mode='ERROR', text='Operation type ' + str(option_selected) + ' does not exist. Try again.')
        select_from_options(option_dict, message_text)


def record_differences_between_files(file_name, directory, directory_reference, log_file_name):
    """
    writes fifferences between result file and its reference file in log file
    log file is than in reference directory
    :param file_name: (string)
    :param directory: (string)
    :param directory_reference: (string)
    :param log_file_name: (string)
    :return: 0: success, 1 cannot open one od the files
    """
    try:
        f = open(directory_reference + log_file_name, 'a')
        f1 = open(directory + file_name, 'r')
        f2 = open(directory_reference + file_name, 'r')
    except IOError:
        message(mode='ERROR', text='Cannot open file')
        return 100
    else:
        f.write('------------------------------------------------------------------------------\n')
        f.write(file_name + '\n')
        diff = ndiff(f1.readlines(), f2.readlines())
        for line in diff:
            if line.startswith('-'):
                f.write(line)
            elif line.startswith('+'):
                f.write('\t\t' + line)
                # for i, line in enumerate(diff):
                #    if line.startswith(' '):
                #        continue
                #    f.write('Line {}: {}'.format(i, line))
        return 0


def download_file_with_winscp(file_winscp, tarfile_remote, user, hostname, password):
    """
    write file for winscp and execute wiscp to download file from remote computer
    :param file_winscp: (string)
    :param tarfile_remote: (string)
    :param user: (string)
    :param hostname: (string)
    :param password: (string)
    :return: 0: success, 101: could not open OSError, 200: error when calling winscp
    """
    message(mode='INFO', text='    Download')
    file_winscp = adapt_path(file_winscp)
    try:
        f = open(file_winscp, 'w')
    except OSError as err:
        message(mode='ERROR', text='OS error: {0}'.format(err))
        return 101
    else:
        f.write('option batch abort \n')
        f.write('option confirm off \n')
        f.write('open sftp://' + user + ':' + password + '@' + hostname + '/ \n')
        f.write('get ' + tarfile_remote + ' \n')
        f.write('exit')
        f.close()

    try:
        check_call(winscp + ' /script=' + file_winscp)
    except:
        message(mode='ERROR', text='%s' % sys.exc_info()[0])
        return 200
    return 0


def unpack_tar_file(tarfile_name, directory):
    """

    :param tarfile_name: (string)
    :param directory: (string)
    :return: 0: success, 102 failed to open tar
    """
    print(' ')
    message(mode='INFO', text='    Unpack')
    if path.isfile(directory + tarfile_name):
        chdir(directory)
        try:
            tar = open_tar(directory + tarfile_name)
        except:
            message(mode='ERROR', text='Tar call failed')
            return 102
        else:
            tar.extractall()
            tar.close()
            remove(directory + tarfile_name)
            return 0

def pack_tar_file(directory):
    """

    :param directory:
    :return:
    """
    tar_file = directory + 'results.tar'
    if path.isfile(tar_file): # remove old tar file if it exists
        remove(tar_file)

    chdir(directory)
    try:
        tar = open_tar(tar_file, 'w')
    except:
        message(mode='ERROR', text='%s' % sys.exc_info()[0])
    else:
        for extension in outputFileEndings:
            for file in listdir(directory):
                if file.endswith('.' + extension):
                    tar.add(file)
        tar.close()


def import_files(directory_source, directory_destination, ending_list, gate_flag):
    if path.exists(directory_source):
        if gate_flag:  # just for stdout
            message(mode='INFO', text='    Convert file(s) to unix')
        for ending in ending_list:
            file_name = directory_source + examplesName + '.' + ending
            if path.isfile(file_name) and access(file_name, R_OK):
                if gate_flag and system() == 'Linux':
                    dos2unix(file_name)
                copy(file_name, directory_destination)

        for file in listdir(directory_source):  # to copy additional files, e.g. for external chemical solver
            file_name = directory_source + file
            for ending in additionalFileEndings:
                if file.endswith('.' + ending) and file_name != directory_source + examplesName + '.out':
                    if gate_flag:
                        if system() == 'Linux':
                            dos2unix(file_name)
                    message(mode='INFO', text='    Importing additional file ' + file)
                    copy(file_name, directory_destination)

    else:
        message(mode='ERROR', text='Repository directory missing')
