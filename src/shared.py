import sys
from os import stat, chdir, makedirs, remove, path, listdir, access, R_OK
from shutil import move, copy
from tarfile import open as open_tar
from difflib import ndiff
from filecmp import cmp
from time import time
from subprocess import call
from configuration import examplesName, inputFileEndings, additionalInputFileEndings, outputFile, outputFileEndings
from functools import reduce


def message(mode='ERROR', text=None, not_supported=None, output_flag=True):
    """
    print message
    :param mode: ['INFO', 'WARNING', 'ERROR'] (string)
        INFO: only text
        WARNING: text and name of function where call is from
        ERROR: text and name of function where call is from
    :param text:  message (string)
    :param not_supported: print '*** is not supported' as an option to print text variable
    :param output_flag: setting this flag False switches output of
    :return:
    """
    if output_flag:
        print_message = '{} is not supported'.format(not_supported) if not_supported else text

        in_function = '' if mode == 'INFO' else ' in function {}'.format(sys._getframe(1).f_code.co_name)
        print('{}{} - {}'.format(mode, in_function, print_message))


class Commands:
    """
    commands that are used on local and remote computer
    """
    @staticmethod
    def call(*args):
        """
        subprocess call
        :param args: 0: name of output file or None,
        the following arguments belong to the command which is executed
        :return:
        """
        try:
            out_file = None if args[0] is None else open(args[0], 'w')
            command = reduce(lambda x, y: '{} {} '.format(x, y), args[1:])  # concat args for command (with empty space)
            call(command, stdout=out_file, shell=True)
        except Exception as err:
            message(mode='ERROR', text="{}".format(err))

    @staticmethod
    def generate_folder(directory):
        """
        makes dirs including subdirectories if they do not exist
        :param directory: (string)
        :return:
        """
        try:
            stat(directory)
        except:
            message(mode='INFO', text='    Generate folder {}'.format(directory))
            makedirs(directory)

    @staticmethod
    def copy_file(item, destination, output_flag=True, folder=None, ending_flag=False):
        """
        copy file (rename it optionally) if it exists, else do nothing - file or ending with folder can be passed
        :param item: (string) file or ending
        :param destination: (string)
        :param output_flag: (bool) print INFO that removing file and print WARNING if file does not exist
        :param folder: (string) required if ending passed
        :param ending_flag: (bool) set true if item is a file ending
        :return:
        """
        if ending_flag:
            for file_item in listdir(folder):
                if file_item.endswith(item):
                    Commands.copy_file(path.join(folder, file_item), destination, output_flag=output_flag)
        if not path.isfile(item):
            return

        try:
            message('INFO', text='Copying {}'.format(item), output_flag=output_flag)
            copy(item, destination)
        except Exception as err:
            message(mode='WARNING', text="{}".format(err), output_flag=output_flag)

    @staticmethod
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

    @staticmethod
    def remove_results(folder):
        """
        remove every simulation output from folder - no error messages
        :param folder: (string)
        :return:
        """
        for ending in outputFileEndings:
            for file_item in listdir(folder):
                if file_item.endswith(ending):
                    Commands.remove_file(path.join(folder, file_item), False)

        Commands.remove_file(path.join(folder, 'results.tar'), False)
        Commands.remove_file(path.join(folder, outputFile), False)


    @staticmethod
    def remove_file(file, output_flag=True):
        """
        if file exists, remove it, else do nothing
        :param file: (string) file or ending
        :param output_flag: (bool) print INFO that removing file and print WARNING if file does not exist
        :return:
        """
        message(mode='INFO', text='    Removing {}'.format(file), output_flag=output_flag)
        try:
            remove(file)
        except Exception as err:
            message(mode='WARNING', text="{}".format(err), output_flag=output_flag)

    @staticmethod
    def clear_file(file):
        """
        clear content of file
        generates the file if it does not exist
        :param file: (string) path and file name
        :return:
        """
        try:
            open(file, 'w').close()
        except Exception as err:
            message(mode='ERROR', text="{}".format(err))

    @staticmethod
    def compare_files(file1, file2):
        try:
            return cmp(file1, file2)
        except Exception as err:
            message(mode='ERROR', text="{}".format(err))

    @staticmethod
    def append_to_file(file, new_text):
        """
        append new text to file
        :param file: (string) path and file name
        :param new_text: (string)
        :return:
        """
        try:
            f = open(file, 'a')
        except Exception as err:
            message(mode='ERROR', text="{}".format(err))
        else:
            f.write(new_text)

    @staticmethod
    def wait_for_file(file_name):
        """
        Used by members to wait until a file exists
        prints a dot each second when waiting
        :param file_name:
        :return:
        """
        sys.stdout.flush()
        start = time()

        i = 1
        while not path.exists(file_name):
            if time()-start > i:
                sys.stdout.write('.')
                sys.stdout.flush()
                i += 1
        print('\n')

    @staticmethod
    def show_file_content(file):
        """
        print file content
        no error if file does not exists
        """
        try:
            log = open(file, 'r')
            message(mode='INFO', text='    Recorded:')
            for line in log:
                print(line)
        except:
            message(mode='INFO', text='    Nothing recorded')

    @staticmethod
    def record_regression_for_folder(directory_item, directory_reference, directory_subject,
                                     configuration, output_file):
        """
        compare results with results in reference folder for regression tests
        if file disagrees, write file name into file 'deviatingFiles_{configuration}.log' in sub ject references folder
        then call record_differences_between_files(). It writes deviations into 'deviations.log' in item folder
        :param directory_item: (string)
        :param directory_reference: (string)
        :param directory_subject: (string)
        :param configuration: (string)
        :param output_file: (string) to exclude this file form the comparison
        :return:
        """
        for file_name in listdir(directory_reference):
            if file_name not in [output_file, 'deviations.log']:
                result_comparison_flag = Commands.compare_files(path.join(directory_item, file_name),
                                                                path.join(directory_reference, file_name))
                if not result_comparison_flag:
                    # files disagree
                    message(mode='INFO', text='Deviating file: {}'.format(file_name))
                    Commands.append_to_file(
                        path.join(directory_subject, 'references', 'deviatingFiles_{}.log'.format(configuration)),
                        '{}\n'.format(path.join(directory_item, file_name)))
                    Commands.record_regression(
                        file_name, directory_item, directory_reference, 'deviations.log', output_flag=False)

    @staticmethod
    def record_regression(file_affected_name, directory, directory_reference, log_file_name, output_flag=True):
        """
        writes differences between result file and its reference file in log file
        log file is than in reference directory
        called by Commands.record_regression_for_folder
        :param file_affected_name: (string)
        :param directory: (string)
        :param directory_reference: (string)
        :param log_file_name: (string)
        :param output_flag: (bool)
        :return:
        """
        message(mode='INFO', text='Record regression of file {}'.format(file_affected_name), output_flag=output_flag)
        try:
            f = open(path.join(directory_reference, log_file_name), 'a')
            f1 = open(path.join(directory, file_affected_name), 'r')
            f2 = open(path.join(directory_reference, file_affected_name), 'r')
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

    @staticmethod
    def pack_tar_file(directory):
        """
        pack files with configuration.outputFileEndings into results.tar in directory
        before that, remove old tar file if it exists
        :param directory: (string)
        :return:
        """
        message(mode='INFO', text='    Pack results.tar')
        tar_file = path.join(directory, 'results.tar')

        try:
            if path.isfile(tar_file):  # remove old tar file if it exists
                remove(tar_file)
            chdir(directory)
            tar = open_tar(tar_file, 'w')

            for extension in outputFileEndings:
                for file_item in listdir(directory):
                    if file_item.endswith('.{}'.format(extension)):
                        tar.add(file_item)
            tar.close()

        except Exception as err:
            message(mode='ERROR', text="{}".format(err))

    @staticmethod
    def unpack_tar_file(directory):
        """
        extract files in results.tar which is in directory into this directory
        then remove the results.tar file from directory
        :param directory: (string)
        :return:
        """
        message(mode='INFO', text='    Unpack results.tar')
        tar_file = path.join(directory, 'results.tar')
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

    @staticmethod
    def copy_input_files(directory_source, directory_destination, output_flag=True):
        """
        copy all files which are in repository or gate with name configuration.examplesName and ending in
        configuration.inputFileEndings
        files are converted in the source directory to unix or dos according to platform
        :param directory_source: (string)
        :param directory_destination: (string)
        :param output_flag: (string)
        :return:
        """
        for ending_running in inputFileEndings:
            file_running = path.join(directory_source, '{}.{}'.format(examplesName, ending_running))
            if path.isfile(file_running) and access(file_running, R_OK):
                message(mode='INFO',
                        text='    Copy file {}.{}'.format(examplesName, ending_running), output_flag=output_flag)
                Commands.copy_file(file_running, directory_destination)

        Commands.copy_additional_input_file(directory_source, directory_destination, additionalInputFileEndings)

    @staticmethod
    def copy_additional_input_file(directory_source, directory_destination,
                                   additional_input_file_endings, output_flag=True):
        """
        copy all files that end with ending in configuration.additionalInputFileEndings
        they are copied separately here, because they have a different name than configuration.fileName
        they are supposed to be for external chemical solver
        called by Commands.copy_input_files
        :param directory_source: (string)
        :param directory_destination: (string)
        :param additional_input_file_endings: (strings list)
        :param output_flag: (bool)
        :return:
        """
        for file_name_running in listdir(directory_source):
            file_running = path.join(directory_source, file_name_running)
            for ending in additional_input_file_endings:
                if file_name_running.endswith('.{}'.format(ending)):
                    message(mode='INFO', text='    Copy file {}'.format(file_name_running), output_flag=output_flag)
                    Commands.copy(file_running, directory_destination)


if __name__ == '__main__':
    # execute static member function of class Commands above
    # the member function is selected via arguments this script is called
    # sys.argv[1] (string): name of static function
    # the following arguments sys.argv[2:] become arguments of the called member function
    getattr(Commands, sys.argv[1])(*sys.argv[2:])
