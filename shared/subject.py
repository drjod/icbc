from sys import path as syspath
from os import path
syspath.append(path.join(path.dirname(__file__), '..', 'customized'))
from utilities import message, adapt_path
from configurationShared import examplesName
from platform import system
from configurationCustomized import location, rootDirectory, compiler, localBuild, localRun, outputFile


class Subject:
    """
    hosts data that depend on
    1. platform (operating system, directories, user)
    2. tested subject (code, branch, ...)
    (TODO: split both parts and put later in folder customized)
    """
    __directory = str()
    __operating_system = str()
    __location = str()
    __rootDirectory = str()
    __plotDirectory = str()
    __gateDirectory = str()  # to transfer files between local and remote

    def __init__(self, superuser, computer , user, code, branch, id_local_process):
        """
        :param superuser:
        :param computer:
        :param user:
        :param code:
        :param branch:
        """
        self.__superuser = superuser
        self.__computer = computer
        self.__user = user
        self.__code = code
        self.__branch = branch
        self.__id_local_process = id_local_process

    def __del__(self):
        pass

    @property
    def computer(self):
        return self.__computer

    @property
    def user(self):
        return self.__user

    @property
    def code(self):
        return self.__code

    @property
    def branch(self):
        return self.__branch

    @property
    def id_local_process(self):
        return self.__id_local_process

    @property
    def location(self):
        return self.__location

    @property
    def directory(self):
        return self.__directory

    @property
    def directory_root(self):
        return self.__rootDirectory

    @property
    def directory_plot(self):
        return self.__plotDirectory

    @property
    def directory_gate(self):
        return self.__gateDirectory

    @property
    def operating_system(self):
        return self.__operating_system

    @property
    def hostname(self):
        return self.__hostname

    @computer.setter
    def computer(self, value):
        self.__computer = value

    @user.setter
    def user(self, value):
        self.__user = value

    @code.setter
    def code(self, value):
        self.__code = value

    @branch.setter
    def branch(self, value):
        self.__branch = value

    def print_selected_variables(self):
        """
        print subject variables which have already been selected, meaning they hav not the value None
        the variables are computer, user, code, branch
        :return:
        """
        if self.__computer:
            message(mode='INFO', text='Set computer ' + self.__computer)
        if self.__user:
            message(mode='INFO', text='Set user ' + self.__user)
        if self.__code:
            message(mode='INFO', text='Set code ' + self.__code)
        if self.__branch:
            message(mode='INFO', text='Set branch ' + self.__branch)

    def select(self, setting_inst):
        """

        :param setting_inst:
        :return:
        """
        if not self.__computer:
            self.__computer = setting_inst.get_name_list('computer')[0]
            # only one entry in list here and in the following
        if not self.__superuser:
            if not self.__user:
                self.__user = setting_inst.get_name_list('user')[0]
        else:
            self.__user = setting_inst.query_username(self.__superuser, self.__computer)

        if not self.__code:
            self.__code = setting_inst.get_name_list('codes')[0]
        if not self.__branch:
            self.__branch = setting_inst.get_name_list('branches')[0]
 
        if location == 'local':
            self.__rootDirectory = setting_inst.query_directory_root(self.__computer, self.__user)
            self.__location = setting_inst.query_location(self.__computer)
            self.__operating_system = setting_inst.query_operating_system(self.__computer)
            #self.__directory = adapt_path(self.__rootDirectory + 'testingEnvironment\\'
            # + self.__computer + '\\' + self.__code + '\\' + self.__branch + '\\')
            #self.__gateDirectory = adapt_path(self.__rootDirectory + 'testingEnvironment\\'
            # + self.__computer + '\\gate\\')
            self.__plotDirectory = adapt_path(rootDirectory + 'testingEnvironment\\' + self.__computer + '\\'
                                             + self.__code + '\\' + self.__branch + '\\examples\\plots\\')
            self.__hostname = setting_inst.query_hostname(self.__computer)
        else:
            self.__location = 'remote'

        self.__directory = adapt_path(rootDirectory + 'testingEnvironment\\'
                                     + self.__computer + '\\' + self.__code + '\\' + self.__branch + '\\')
        self.__gateDirectory = adapt_path(rootDirectory + 'testingEnvironment\\' + self.__computer + '\\gate\\')

        # message(mode='INFO', text=self.__directory)

    def get_built_file_for_release(self, item):
        """
        give built file a name, e.g. ogs_kb1_Linux_OGS_FEM and return it with path
        :param item: (class Item)
        :return: (string) path and name of built file for release
        """
        if system() == 'Windows':
            return self.__directory + 'releases\\' + self.__code + '_' + self.__branch + '_' \
                   + system() + '_' + item.configuration + '.exe'
        elif system() == 'Linux':
            return self.__directory + 'releases/' + self.__code + '_' + self.__branch + '_' \
                   + system() + '_' + item.configuration
        else:
            message(mode='ERROR', not_supported=system())

    def get_built_file(self, item):
        """
        get the built (.exe,...) to run test cases
        it is in the folder, where it is created in the compilation process
        only supports code ogs
        :param item: (class Item)
        :return: (string) path and name of built file
        """
        if system() == 'Windows':
            if self.__code == 'ogs':
                return self.__directory + 'Build_' + item.configuration + '\\' + '\\bin\\Release\\ogs.exe'
            else:
                message(mode='ERROR', not_supported=self.__code)
        elif system() == 'Linux':
            if self.__code == 'ogs':
                return self.__directory + 'Build_Release_' + compiler + '/' \
                       + item.configuration + '/bin/ogs_' + item.configuration
            else:
                message(mode='ERROR', not_supported=self.__code)
        else:
            message(mode='ERROR', not_supported=system())

    def get_build_command(self, item):
        """
        on windows: build via visual studio
        on linux: build via script compileInKiel.sh
        :param item:
        :return:
        """
        if system() == 'Windows':
            return localBuild + ' ' + self.__computer + ' ' + self.__code + ' ' \
                   + self.__branch + ' ' + item.configuration
        elif system() == 'Linux':
            return rootDirectory + 'testingEnvironment/scripts/' + 'compileInKiel.sh ' \
                   + self.directory + ' ' + item.configuration + ' Release'
        else:
            message(mode='ERROR', not_supported=system())

    def get_execution_command(self, item):
        """
        set command to run test case according to platform
        :param item:
        :return:
        """
        if location == 'local':
            if system() == 'Windows':
                return localRun + ' ' + self.__computer + ' ' + self.__code + ' ' + self.__branch + ' ' \
                       + item.type + ' ' + item.case + ' ' + item.configuration + ' ' + examplesName
            elif system() == 'Linux':
                return self.__directory + 'Build_Release_' + compiler + '/' + item.configuration \
                       + '/bin/ogs_' + item.configuration + ' ' + item.directory \
                       + '/' + examplesName + ' > ' + item.directory + '/' + outputFile
            else:
                message(mode='ERROR', not_supported=system())
                return -1
        elif location == 'remote':
            return 'qsub ' + item.directory + 'run.pbs'
        else:
            message(mode='ERROR', not_supported=location)
            return -1
