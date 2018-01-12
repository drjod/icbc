from os import path, environ


class Item:
    """
    parent of Build, Sim, Plot
    it and its childs hold data for Building, Simulating, Plotting like the Operation class, but (test) case-specific
    """
    def __init__(self, subject=None, configuration=None, directory=None):
        self._subject, self._configuration, self._directory = subject, configuration, directory

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
        Item.__init__(self, subject, configuration, path.join(subject.directory, 'Build_{}'.format(configuration)))


class Test(Item):
    """
    parent of Sim and Plot
    """
    def __init__(self, subject, item_type, item_case, item_configuration, flow_process, element_type, directory):
        self._type, self._case = item_type, item_case
        self._flow_process, self._element_type = flow_process, element_type

        self.__directory_local = path.join(environ['HOME'], 'testingEnvironment',
                                           subject.computer, subject.code, subject.branch, 'examples', 'files',
                                           item_type, item_case, flow_process, element_type, item_configuration)

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

    @property
    def directory_local(self):
        return self.__directory_local

    def name(self):
        return '{} {} {} {} {}'.format(
            self._type, self._case, self._flow_process, self._element_type, self._configuration)


class Sim(Test):
    """
    used in simulation operations
    """
    def __init__(self, subject, item_type, item_case, item_configuration, flow_process, element_type):

        self.__directory_repository = path.join(subject.root_directory, 'testingEnvironment', 'repository',
                                                item_type, item_case, flow_process, element_type)
     
        Test.__init__(self, subject, item_type, item_case, item_configuration, flow_process, element_type,
                      path.join(subject.directory, 'examples', 'files',
                      item_type, item_case, flow_process, element_type, item_configuration))

    @property
    def directory_repository(self):
        return self.__directory_repository


class Plot(Test):
    """
    used in plotting operations
    """
    def __init__(self, subject, item_type, item_case, item_configuration, flow_process, element_type):

        # directory_local put to test to get get_results operation to simulation

        #self.__directory_local = path.join(environ['HOME'], 'testingEnvironment',
        #                            subject.computer, subject.code,  subject.branch, 'examples', 'files',
        #                                   item_type, item_case, flow_process, element_type, item_configuration)
        # directory local exists to do local plotting operations for remote computer
        # if local computer, it's the same folder like 'directory' for simulating

        Test.__init__(self, subject, item_type, item_case, item_configuration, flow_process, element_type,
                      path.join(subject.directory, 'examples', 'files',
                                item_type, item_case, flow_process, element_type, item_configuration))

    #@property
    #def directory_local(self):
    #    return self.__directory_local

