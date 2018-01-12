from shared import message
from configuration import examplesName, outputFile
from os import path


class Subject:
    """
    hosts data that depend on
    1. platform (operating system, directories, user)
    2. tested subject (code, branch, ...)
    (TODO: split both parts and put later in folder customized)
    """
    __remote_flag = bool()
    __directory, __root_directory, __plot_directory, __gate_directory, __icbc_directory \
        = str(), str(), str(), str(), str()
    __hostname, __compiler = str(), str()
    __python = str()  # python command

    def __init__(self, superuser, computer, user, code, branch):
        """
        :param superuser:
        :param computer:
        :param user:
        :param code:
        :param branch:
        """
        self.__superuser, self.__computer, self.__user, self.__code, self.__branch = \
            superuser, computer, user, code, branch

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
    def remote_flag(self):
        return self.__remote_flag

    @property
    def directory(self):
        return self.__directory

    @property
    def root_directory(self):
        return self.__root_directory

    @property
    def plot_directory(self):
        return self.__plot_directory

    @property
    def gate_directory(self):
        return self.__gate_directory

    @property
    def icbc_directory(self):
        return self.__icbc_directory

    @property
    def hostname(self):
        return self.__hostname

    @property
    def python(self):
        return self.__python

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
            message(mode='INFO', text='Set computer {}'.format(self.__computer))
        if self.__user:
            message(mode='INFO', text='Set user {}'.format(self.__user))
        if self.__code:
            message(mode='INFO', text='Set code {}'.format(self.__code))
        if self.__branch:
            message(mode='INFO', text='Set branch {}'.format(self.__branch))

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
                self.__user = setting_inst.get_name_list('users')[0]
        else:
            self.__user = setting_inst.gateToDatabase.query_username(self.__superuser, self.__computer)

        if not self.__code:
            self.__code = setting_inst.get_name_list('codes')[0]
        if not self.__branch:
            self.__branch = setting_inst.get_name_list('branches')[0]

        self.__root_directory = setting_inst.gateToDatabase.query_column_entry(
            'computer', self.__computer, 'root_directory')
        self.__remote_flag = setting_inst.gateToDatabase.query_column_entry(
            'computer', self.__computer, 'remote_flag')
        self.__directory = path.join(self.__root_directory, 'testingEnvironment',
                                     self.__computer, self.__code, self.__branch)
        self.__plot_directory = path.join(self.__root_directory, 'testingEnvironment',
                                          self.__computer, self.__code, self.__branch,
                                          'examples', 'plots')
        self.__hostname = setting_inst.gateToDatabase.query_column_entry(
            'computer', self.__computer, 'hostname')
        self.__compiler = setting_inst.gateToDatabase.query_column_entry(
            'computer', self.__computer, 'compiler')
        self.__python = setting_inst.gateToDatabase.query_column_entry(
            'computer', self.__computer, 'python3')
        self.__icbc_directory = path.join(self.__root_directory, 'testingEnvironment', 'icbc', 'src')
        self.__gate_directory = path.join(self.__root_directory, 'testingEvironment', self.__computer, 'gate')

        # message(mode='INFO', text=self.__directory)

    def get_built_file_for_release(self, item):
        """
        give built file a name, e.g. ogs_kb1_Linux_OGS_FEM and return it with path
        :param item: (class Item)
        :return: (string) path and name of built file for release, '1' if OP not supported
        """
        return path.join(self.__directory, 'releases', '{}_{}_{}'.format(
            self.__code, self.__branch, item.configuration))

    def get_built_file(self, item):
        """
        get the built (.exe,...) to run test cases
        it is in the folder, where it is created in the compilation process
        only supports code ogs
        :param item: (class Item)
        :return: (string) path and name of built file
        """
        if self.__code == 'ogs':
            return path.join(self.__directory, 'Build_Release_{}'.format(self.__compiler), item.configuration,
                             'bin','ogs_{}'.format(item.configuration))
        else:
            message(mode='ERROR', not_supported=self.__code)

    def get_build_command(self, item):
        """
        on windows: build via visual studio
        on linux: build via script compileInKiel.sh
        :param item:
        :return:
        """
        return '{} {} {} Release'.format(path.join(
            self.__root_directory, 'testingEnvironment', self.__computer, self.__code, self.__branch,
            'compileInKiel.sh'),
            self.directory, item.configuration)

    def get_execution_command(self, item):
        """
        set command to run test case according to platform
        :param item:
        :return: (3 strings) executable, test case, output
        """
        mpi_command = str()
        if item.configuration == 'OGS_FEM_MPI' or item.configuration == 'OGS_FEM_PETSC':
            mpi_command = 'mpirun -n 2 '

        return path.join(mpi_command, self.__directory, 'Build_Release_{}'.format(self.__compiler), item.configuration,
                         'bin', 'ogs_{}'.format(item.configuration)), \
               path.join(item.directory, examplesName),\
               path.join(item.directory, outputFile)
               
