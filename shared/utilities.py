import sys
from os import stat, chdir, mkdir, remove, path, listdir, access, R_OK
from shutil import move, copy
from tarfile import open as open_tar
from difflib import ndiff
from filecmp import cmp
from platform import system
from subprocess import check_call
from configurationShared import examplesName, inputFileEndings, outputFileEndings, additionalInputFileEndings
from configurationCustomized import winscp, rootDirectory


def message(mode='ERROR', text=None, not_supported=None):
    """
    print message
    :param mode: ['INFO', 'WARNING', 'ERROR'] (string)
        INFO: only text
        WARNING: text and name of function where call is from
        ERROR: text and name of function where call is from
    :param text:  message (string)
    :param not_supported: print '*** is not supported' as an option to print text variable
    :return:
    """
    if not_supported:
        print_message = not_supported + ' is not supported'
    else:
        print_message = text

    if mode == 'INFO':
        in_function = ''
    else:
        in_function = ' in function ' + sys._getframe(1).f_code.co_name

    print(mode + in_function + ' - ' + print_message)



def select_from_options(option_dict, message_text):
    """
    select by user input from dictionary with options
    recalls itself in case of non-proper user input
    :param option_dict: {string: string, ...} key is value to type in to select
    :param message_text: (string) printed with the dictionary keys and values
    to ask user for input, e.g. 'Select option type'
    :return: (one-char string) selected option (=selected key of dictionary)
    """
    while True:
        print('\n ' + message_text + ':')
        for key, option in option_dict.items():
            print('    ' + option)
        option_selected = input('\n')

        if option_selected in option_dict:
            break
        else:
            message(mode='ERROR', text='Operation type ' + str(option_selected) + ' does not exist. Try again.')

    return str(option_selected)

def adapt_path(directory_path):
    """
    converts windows path into linux (unix) according to platform where script runs
    :param directory_path: (string) path to adapt
    :return:
    """
    if system() == 'Windows':
        return directory_path
    elif system() == 'Linux':
        return directory_path.replace('\\', '/')
    else:
        message(mode='ERROR', not_supported=system())


def adapt_path_computer_selected(directory_path, operating_system):
    """
    converts windows path into linux (unix) and vice verca according to platform of selected computer
    used for plotting operations (all local while simulation operations might be remote)
    :param directory_path: (string) path to adapt
    :param operating_system:
    :return:
    """
    if operating_system == 'windows':
        return directory_path.replace('/', '\\')
    elif operating_system == 'linux':
        return directory_path.replace('\\', '/')
    else:
        message(mode='ERROR', not_supported=operating_system)


def generate_folder(root, level_list):
    """
    generate directory folder if it does not already exists
    :param root: (string)
    :param level_list: (string list) level in folder hierarchy starting with root
    :return:
    """
    directory = root
    for level in level_list:
        directory = adapt_path(directory + level + '\\')
        try:
            stat(directory)
        except:
            mkdir(directory)


def unix2dos(file, output_flag=True):
    """
    converts file into dos format by adding carriage return \r
    :param file: (string) path and file name
    :param output_flag: (bool)
    :return:
    """
    file = adapt_path(file)

    if output_flag:
        message(mode='INFO', text='    Convert to dos')
    try:
        infile = open(file, 'r')
        outfile = open('dos_' + file, 'w')  # write into new file with suffix dos_
    except Exception as e:
        message(mode='ERROR', text="*****")
    else:
        for line in infile:
            line = line.rstrip() + '\r\n'
            outfile.write(line)
        infile.close()
        outfile.close()
        move('dos_' + file, file)  # remove suffix dos_ - overwrite original file


def dos2unix(file, output_flag=True):
    """
    converts file into unix format by removing carriage return \r
    :param file: (string) path and file name
    :param output_flag: (bool)
    :return:
    """
    file = adapt_path(file)

    if output_flag:
        message(mode='INFO', text='    Convert to dos')
    try:
        text = open(file, 'rb').read().replace('\r\n', '\n')
        open(file, 'wb').write(text)
    except Exception as e:
        message(mode='ERROR', text="*****")


def convert_file(file):
    """
    convert file according to platform. i.e. to unix if Linux, to dos if Windows
    :param file: (string) path and file name
    :return:
    """
    file = adapt_path(file)

    if system() == 'Linux':
        dos2unix(file, output_flag=False)
    elif system() == 'Windows':
        unix2dos(file, output_flag=False)
    else:
        message(mode='ERROR', not_supported=system())


def remove_file(file):
    """
    if file exists, remove it
    :param file: (string) path and file name
    :return:
    """
    file = adapt_path(file)
    message(mode='INFO', text='    Removing ' + file)

    try:
        remove(file)
    except Exception as e:
        message(mode='ERROR', text="*****")


def clear_file(file):
    """
    clear content of file
    :param file: (string) path and file name
    :return:
    """
    file = adapt_path(file)

    try:
        open(file, 'w').close()
    except Exception as e:
        message(mode='ERROR', text="*****")


def compare_files(file1, file2):
    try:
        return cmp(file1, file2)
    except:
        message(mode='ERROR', text="error")


def append_to_file(file, new_text):
    """
    append new text to file
    :param file: (string) path and file name
    :param new_text: (string)
    :return:
    """
    file = adapt_path(file)

    try:
        f = open(file, 'a')
    except Exception as e:
        message(mode='ERROR', text="*****")
    else:
        f.write(new_text)


def record_regression_of_file(file_affected_name, directory, directory_reference, log_file_name, output_flag=True):
    """
    writes differences between result file and its reference file in log file
    log file is than in reference directory
    :param file_affected_name: (string)
    :param directory: (string)
    :param directory_reference: (string)
    :param log_file_name: (string)
    :param output_flag: (bool)
    :return:
    """
    directory = adapt_path(directory)
    directory_reference = adapt_path(directory_reference)

    if output_flag:
        message(mode='INFO', text='Record regression of file ' + file_affected_name)
    try:
        f = open(directory_reference + log_file_name, 'a')
        f1 = open(directory + file_affected_name, 'r')
        f2 = open(directory_reference + file_affected_name, 'r')
    except IOError:
        message(mode='ERROR', text='Cannot open file')
    else:
        f.write('------------------------------------------------------------------------------\n')
        f.write(file_affected_name + '\n')
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


def download_file_with_winscp(file_winscp, tarfile_remote, user, hostname, password, output_flag=True):
    """
    write file for winscp and execute wiscp to download file from remote computer
    :param file_winscp: (string)
    :param tarfile_remote: (string)
    :param user: (string)
    :param hostname: (string)
    :param password: (string)
    :param output_flag: (bool)
    :return: 0: success, 101: could not open OSError, 200: error when calling winscp
    """
    file_winscp = adapt_path(file_winscp)

    if output_flag:
        message(mode='INFO', text='    Download tar file')
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
    except Exception as e:
        message(mode='ERROR', text="*****")
        return 200
    return 0


def unpack_tar_file(directory):
    """
    extract files in results.tar which is in directory into this directory
    then remove the results.tar file from directory
    :param directory: (string)
    :return:
    """
    message(mode='INFO', text='    Unpack')
    tar_file = adapt_path(directory + 'results.tar')

    try:
        chdir(directory)
        tar = open_tar(tar_file)
    except FileNotFoundError:
        message(mode='ERROR', text='No tar file')
    except Exception as e:
        message(mode='ERROR', text="*****")
    else:
        tar.extractall()
        tar.close()
        remove(tar_file)


def pack_tar_file(directory):
    """
    pack files with configurationShared.outputFileEndings into results.tar in directory
    before that, remove old tar file if it exists
    :param directory: (string)
    :return:
    """
    message(mode='INFO', text='    Pack')
    tar_file = adapt_path(directory + 'results.tar')

    try:
        if path.isfile(tar_file):  # remove old tar file if it exists
            remove(tar_file)
        chdir(directory)
        tar = open_tar(tar_file, 'w')
    except Exception as e:
        message(mode='ERROR', text="*****")
    else:
        for extension in outputFileEndings:
            for file in listdir(directory):
                if file.endswith('.' + extension):
                    tar.add(file)
        tar.close()


def copy_input_files(directory_source, directory_destination, output_flag=True):
    """
    copy all files which are in repository or gate with name configurationShared.examplesName and ending in
    configurationShared.inputFileEndings
    files are converted in the source directory to unix or dos according to platform
    :param directory_source:
    :param directory_destination:
    :param output_flag:
    :return:
    """
    directory_source = adapt_path(directory_source)
    directory_destination = adapt_path(directory_destination)

    if path.exists(directory_source):
        for ending_running in inputFileEndings:
            file_running = directory_source + examplesName + '.' + ending_running
            if path.isfile(file_running) and access(file_running, R_OK):
                convert_file(file_running)
                if output_flag:
                    message(mode='INFO', text='    Copy file ' + examplesName + '.' + ending_running)
                try:
                    copy(file_running, directory_destination)
                except Exception as e:
                    message(mode='ERROR', text="*****")

        copy_additional_input_files(directory_source, directory_destination)
    else:
        message(mode='ERROR', text='Repository directory missing')


def copy_additional_input_files(directory_source, directory_destination, output_flag=True):
    """
    copy all files that end with ending in configurationShared.additionalInputFileEndings
    they are copied separately here, because they have a different name than configurationShared.fileName
    they are supposed to be for external chemical solver
    :param directory_source: (string)
    :param directory_destination: (string)
    :param output_flag: (bool)
    :return:
    """
    directory_source = adapt_path(directory_source)
    directory_destination = adapt_path(directory_destination)

    for file_name_running in listdir(directory_source):
        file_running = directory_source + file_name_running
        for ending in additionalInputFileEndings:
            if file_name_running.endswith('.' + ending):
                convert_file(file_running)
                if output_flag:
                    message(mode='INFO', text='    Copy file ' + file_name_running)
                try:
                    copy(file_running, directory_destination)
                except Exception as e:
                    message(mode='ERROR', text="*****")


def write_tecplot_macro_for_jpg(directory, item_type):
    """
    write tecplot macro to generate jpg
    :param directory: (string) path to directory where tecplot layout is
    :param item_type: (string)
    :return:
    """
    directory = adapt_path(directory)

    chdir(directory)
    try:
        f = open(directory + '_genJPG.mcr', 'w')
    except Exception as e:
            message(mode='ERROR', text="*****")
    else:
        f.write('#!MC 1300\n')
        f.write('#-----------------------------------------------------------------------\n')
        f.write('$!EXPORTSETUP EXPORTFORMAT = JPEG\n')
        f.write('$!EXPORTSETUP IMAGEWIDTH = 1500\n')
        f.write('#-----------------------------------------------------------------------\n')
        f.write("$!EXPORTSETUP EXPORTFNAME = \'" + directory + "results_"
                + item_type + ".jpg\'\n")
        f.write('$!EXPORT\n')
        f.write('EXPORTREGION = ALLFRAMES\n')
        f.close()


def check_string_represents_non_negative_number_or_a(value):
    """
    check if value is single char 'a' or can be casted to integer and is larger than 0
    displays warning, if this is not the case
    :param value: (string): input to be checked
    :return: True : ok - False : exception
    """
    if value == 'a':
        return True

    try:
        val = int(value)
    except ValueError:
        message(mode='WARNING', text='Not a number')
        return False

    if val >= 0:
        return True
    else:
        return False
