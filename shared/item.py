from utilities import adapt_path, adapt_path_computer_selected
from sys import path as syspath
from os import path
syspath.append(path.join(path.dirname(__file__), '..', 'customized'))
from configurationCustomized import rootDirectory


class Item:
    """
    parent of Build, Sim, Plot
    hosts directory, subject, configuration for specific test case or item if building operation
    """
    def __init__(self, subject=None, configuration=None, directory=None):

        self._subject = subject
        self._configuration = configuration
        self._directory = directory
 
    def __del__(self):
        del self._subject

    @property
    def configuration(self):
        return self._configuration

    @property
    def directory(self):
        return self._directory


class Build(Item):
    """
    used in building operations
    """
    def __init__(self, subject, configuration):
        Item.__init__(self, subject, configuration, adapt_path('{}Build_{}\\'.format(subject.directory, configuration)))


class Test(Item):
    """
    parent of Sim and Plot
    """
    def __init__(self, subject, item_type, item_case, item_configuration, flow_process, element_type, directory):
        self._type = item_type
        self._case = item_case
        self._flow_process = flow_process
        self._element_type = element_type

        Item.__init__(self, subject, item_configuration, directory)

    @property
    def type(self):
        return self._type

    @property
    def case(self):
        return self._case

    @property
    def flow_process(self):
        return self._flow_process

    @property
    def element_type(self):
        return self._element_type

    def name(self):
        return '{} {} {} {} {}'.format(
            self._type, self._case, self._flow_process, self._element_type, self._configuration)


class Sim(Test):
    """
    used in simulation operations
    """
    def __init__(self, subject, item_type, item_case, item_configuration, flow_process, element_type):

        self.__directory_repository = adapt_path(  # independent of configuration (one folder for all)
            '{}testingEnvironment\\{}\\repository\\{}\\{}\\{}\\{}\\'.format(
                rootDirectory, subject.computer, item_type, item_case, flow_process, element_type))
     
        Test.__init__(self, subject, item_type, item_case, item_configuration, flow_process, element_type, adapt_path(
            '{}examples\\files\\{}\\{}\\{}\\{}\\{}\\'.format(
                subject.directory, item_type, item_case, flow_process, element_type, item_configuration)))

    @property
    def directory_repository(self):
        return self.__directory_repository


class Plot(Test):
    """
    used in plotting operations
    """
    def __init__(self, subject, item_type, item_case, item_configuration, flow_process, element_type):
        example = '{}\\'.format(item_type)
        if item_case:
            example = '{}{}\\{}\\{}\\'.format(example, item_case, flow_process, element_type)
        if item_configuration:
            example = '{}{}\\'.format(example, item_configuration)

        directory_local = adapt_path('{}testingEnvironment\\{}\\{}\\{}\\examples\\files\\{}'.format(
            rootDirectory, subject.computer, subject.code,  subject.branch, example))
        self.__directory_computer_selected = adapt_path_computer_selected('{}examples\\files\\{}'.format(
            subject.directory, example), subject.operating_system)
 
        Test.__init__(self, subject, item_type, item_case, item_configuration,
                      flow_process, element_type, directory_local)

    @property
    def directory_computer_selected(self):
        return self.__directory_computer_selected

