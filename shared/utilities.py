import sys
from os import stat, chdir, makedirs, remove, path, listdir, access, R_OK
from shutil import move, copy
from tarfile import open as open_tar
from difflib import ndiff
from imp import reload
from filecmp import cmp
from platform import system
from configurationShared import examplesName, inputFileEndings, outputFileEndings, additionalInputFileEndings


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
        print_message = '{} is not supported'.format(not_supported)
    else:
        print_message = text

    if mode == 'INFO':
        in_function = ''
    else:
        in_function = ' in function {}'.format(sys._getframe(1).f_code.co_name)

    print('{}{} - {}'.format(mode, in_function, print_message))


def select_from_options(option_dict, message_text):
    """
    select by user input from dictionary with options
    recalls itself in case of non-proper user input (for simplicity, it checks only
    if lower-case string is in dictionary)
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

        if option_selected.lower() in option_dict:
            break
        else:
            message(mode='ERROR', text='Operation type {} does not exist. Try again.'.format(option_selected))

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


def generate_folder(directory):
    """
    makes dirs including subdirectories if they do not exist
    :param directory: (string)
    :return:
    """
    directory = adapt_path(directory)
    try:
        stat(directory)
    except:
        message(mode='INFO', text='    Generate folder {}'.format(directory))
        makedirs(directory)


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
        outfile = open('dos_{}'.format(file), 'w')  # write into new file with suffix dos_
    except Exception as err:
        message(mode='ERROR', text="{}".format(err))
    else:
        for line in infile:
            line = line.rstrip() + '\r\n'
            outfile.write(line)
        infile.close()
        outfile.close()
        move('dos_{}'.format(file), file)  # remove suffix dos_ - overwrite original file


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
    except Exception as err:
        message(mode='ERROR', text="{0}".format(err))


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


def copy_file(file, destination):
    """
    copy file, rename it optionally
    :param file: (string) name + path
    :param destination: (string) destination directory or path with new file name
    :return:
    """
    try:
        copy(file, destination)
    except Exception as err:
        message(mode='ERROR', text="{}".format(err))


def move_file(file, destination):
    """
    move file, rename it optionally
    :param file: (string) name + path
    :param destination: (string) destination directory or path with new file name
    :return:
    """
    try:
        move(file, destination)
    except Exception as err:
        message(mode='ERROR', text="{}".format(err))


def remove_file(file, output_flag=True):
    """
    if file exists, remove it, else do nothing
    :param file: (string) path and file name
    :param output_flag: (bool)
    :return:
    """
    file = adapt_path(file)
    if not path.isfile(file):
        return
    else:
        if output_flag:
            message(mode='INFO', text='    Removing ' + file)

        try:
            remove(file)
        except Exception as err:
            message(mode='WARNING', text="{}".format(err))


def clear_file(file):
    """
    clear content of file
    :param file: (string) path and file name
    :return:
    """
    file = adapt_path(file)

    try:
        open(file, 'w').close()
    except Exception as err:
        message(mode='ERROR', text="{}".format(err))


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
    except Exception as err:
        message(mode='ERROR', text="{}".format(err))
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
        message(mode='INFO', text='Record regression of file {}'.format(file_affected_name))
    try:
        f = open(directory_reference + log_file_name, 'a')
        f1 = open(directory + file_affected_name, 'r')
        f2 = open(directory_reference + file_affected_name, 'r')
    except IOError:
        message(mode='ERROR', text='Cannot open file')
    else:
        f.write('------------------------------------------------------------------------------\n')
        f.write('{}\n'.format(file_affected_name))
        diff = ndiff(f1.readlines(), f2.readlines())
        for line in diff:
            if line.startswith('-'):
                f.write(line)
            elif line.startswith('+'):
                f.write('\t\t{}'.format(line))
                # for i, line in enumerate(diff):
                #    if line.startswith(' '):
                #        continue
                #    f.write('Line {}: {}'.format(i, line))


def unpack_tar_file(directory):
    """
    extract files in results.tar which is in directory into this directory
    then remove the results.tar file from directory
    :param directory: (string)
    :return:
    """
    message(mode='INFO', text='    Unpack')
    tar_file = adapt_path('{}results.tar'.format(directory))

    try:
        chdir(directory)
        tar = open_tar(tar_file)
    except FileNotFoundError:
        message(mode='ERROR', text='No tar file')
    except Exception as err:
        message(mode='ERROR', text="{}".format(err))
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
    tar_file = adapt_path('{}results.tar'.format(directory))

    try:
        if path.isfile(tar_file):  # remove old tar file if it exists
            remove(tar_file)
        chdir(directory)
        tar = open_tar(tar_file, 'w')
    except Exception as err:
        message(mode='ERROR', text="{}".format(err))
    else:
        for extension in outputFileEndings:
            for file in listdir(directory):
                if file.endswith('.{}'.format(extension)):
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
            file_running = '{}{}.{}'.format(directory_source, examplesName, ending_running)
            if path.isfile(file_running) and access(file_running, R_OK):
                convert_file(file_running)
                if output_flag:
                    message(mode='INFO', text='    Copy file {}.{}'.format(examplesName, ending_running))
                copy_file(file_running, directory_destination)

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
            if file_name_running.endswith('.{}'.format(ending)):
                convert_file(file_running)
                if output_flag:
                    message(mode='INFO', text='    Copy file {}'.format(file_name_running))
                copy_file(file_running, directory_destination)


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
        f = open('{}_genJPG.mcr'.format(directory), 'w')
    except Exception as err:
            message(mode='ERROR', text="{}".format(err))
    else:
        f.write('#!MC 1300\n')
        f.write('#-----------------------------------------------------------------------\n')
        f.write('$!EXPORTSETUP EXPORTFORMAT = JPEG\n')
        f.write('$!EXPORTSETUP IMAGEWIDTH = 1500\n')
        f.write('#-----------------------------------------------------------------------\n')
        f.write("$!EXPORTSETUP EXPORTFNAME = \'{}results_{}.jpg\'\n".format(directory, item_type))
        f.write('$!EXPORT\n')
        f.write('EXPORTREGION = ALLFRAMES\n')
        f.close()


def string_represents_non_negative_number_or_potentially_valid_character(value):
    """
    check if value is single char 'a' or can be casted to integer and is larger than 0
    displays warning, if this is not the case
    :param value: (string): input to be checked
    :return: True : ok - False : exception
    """
    if value == 'a' or value == 'r':  # for all or range (range in table)
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


def str2bool(value_str):
    """
    converts string to bool
    :return:
    """
    if value_str == '0' or value_str == 'False':
        return False
    else:
        return True


def bool2str(value_bool):
    """
    converts string to bool
    :return:
    """
    if value_bool:
        return '1'
    else:
        return '0'


def is_in_list(value, the_list):
    """
    checks if value is in list
    :param value:
    :param the_list:
    :return: True if value is in list, else False
    """
    try:
        help_var = the_list.index(value)
    except:
        return False
    else:
        return True
