from shared import message
from os import path
from call import Call
from setting import select_from_options
from item import Build, Sim, Plot
from gateToCluster import GateToCluster
from collections import OrderedDict


class Operation:
    """
    parent class of Building, Plotting, Simulating
    """
    _operation_dict = OrderedDict()  # depends on self._selected_operation_type
    _selected_operation, _selected_operation_type = str(), str()
    _item, _gateToCluster = None, None  # class Build, Sim, or Plot (Item) - class GateToCluster

    def __init__(self, subject):
        """
        :param subject: (class Subject)
        """
        self._subject = subject

        self._gateToCluster = GateToCluster(self._subject) if self._subject.remote_flag else None
        self.__operate = self._gateToCluster.operate if self._subject.remote_flag else operate_local

    def __del__(self):
        pass

    @property
    def selected_operation(self):
        return self._selected_operation

    @property
    def selected_operation_type(self):
        return self._selected_operation_type

    def execute(self, command):
        """
        splits between local and remote
        :param command: (string) is complete command with arguments,
                                  e.g. "python shared.py run {{outputfile}, executable, {item}"
                                       "call, None {script_partition} {nr_cpus} -e -asci {item_directory}"
        :return:
        """
        self.__operate(command)  # points either at self.operate_local or at gateToCluster.GateToCluster.operate

    def execute_python(self, *args):
        """
        to run python on any computer with one of the static member function of shared.Commands
        :param args: (strings) 0: name of static function of shared.Commands,
                                  following args args[1]... are arguments of the selected static function
        :return:
        """
        command = '{} {}'.format(self._subject.python, path.join(self._subject.icbc_directory, 'shared.py'))
        for arg in args:
            command += ' {}'.format(arg)

        self.execute(command)

    def select_operation(self, selected_operation):
        """
        set self._selected_operation
        from user input if not already selected via previous loop or constructor of Environment
        else from setting.operation (which is passed to here as function argument)
        Required:
            self._operation_dict (dict)
        :param selected_operation: (string, None if operation not already selected)
        :return:
        """
        print('\n-----------------------------------------------------------------\n') 
        print('Test subject {} {}\n             on {}'.format(
            self._subject.code, self._subject.branch, self._subject.computer))

        self._selected_operation = selected_operation if selected_operation else \
            select_from_options(self._operation_dict, 'Select operation')

    def generate_item_instance(self, item_type, item_case, item_configuration, flow_process, element_type):
        """
        generate Build, Sim or Plot according to chosen operation
        :param operation_inst:
        :param item_type:
        :param item_case:
        :param item_configuration:
        :param flow_process:
        :param element_type
        :return: child of Item instance (Build, Sim, Plot)
        """
        if self._selected_operation_type == 'b':  # building
            return Build(self._subject, item_configuration)
        elif self._selected_operation_type == 's':  # simulating
            return Sim(self._subject, item_type, item_case, item_configuration, flow_process, element_type)
        elif self._selected_operation_type == 'p':  # plotting
            return Plot(self._subject, item_type, item_case, item_configuration, flow_process, element_type)
        else:
            message(mode='ERROR', not_supported=self._selected_operation_type)
            return 1  # check this


def operate_local(command):
    """
    subprocess call on local computer
    :param command: (string)
    :return:
    """
    Call.execute(command)