import subject
from utilities import adapt_path, adapt_path_computer_selected
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
from configurationCustomized import rootDirectory


class Item:
    """
    Parent of Build, Sim, Plot
    hosts directory, subject, configuration for specific test case or item if building operation
    """
    def __init__(self, subject=None, configuration=None, directory=None):
        if subject is not None and configuration is not None and directory is not None:
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
    Used in building operations
    """
    def __init__(self, subject, configuration):
        Item.__init__(self, subject, configuration,
                           adapt_path(subject.directory + 'Build_' + configuration + '\\'))


class Test(Item):
    """
    Parent of Sim and Plot
    """
    def __init__(self, subject, item_type, item_case, item_configuration, directory):
        self.__type = item_type
        self.__case = item_case

        Item.__init__(self, subject, item_configuration, directory)

    @property
    def type(self):
        return self.__type

    @property
    def case(self):
        return self.__case

    def name(self):
        return self.__type + ' ' + self.__case + ' ' + self._configuration


class Sim(Test):
    """
    Used in simulation operations
    """
    def __init__(self, subject, item_type, item_case, item_configuration):
        self.__directory_repository = adapt_path(rootDirectory +
                                                 'testingEnvironment\\' + subject.computer +
                                                 '\\repository\\' + item_type + '\\' + item_case + '\\')
     
        Test.__init__(self, subject, item_type, item_case, item_configuration,
                      adapt_path(subject.directory + 'examples\\files\\' + item_type + '\\' +
                                 item_case + '\\' + item_configuration + '\\'))  # test case directory

    @property
    def directory_repository(self):
        return self.__directory_repository
                                              

class Plot(Test):    
    """
    Used in plotting operations
    """
    def __init__(self, subject, item_type, item_case, item_configuration):
        example = item_type + '\\'
        if item_case:
            example = example + item_case + '\\'
        if item_configuration:
            example = example + item_configuration + '\\'

        directory_local = adapt_path(rootDirectory + 'testingEnvironment\\' +
                                     subject.computer + '\\' + subject.code + '\\' +
                                     subject.branch + '\\examples\\files\\' + example)
        self.__directory_computer_selected = adapt_path_computer_selected(subject.directory +
                                                                          'examples\\files\\' +
                                                                          example, subject.operating_system)
 
        Test.__init__(self, subject, item_type, item_case, item_configuration, directory_local)

    @property
    def directory_computer_selected(self):
        return self.__directory_computer_selected
