from subject import Subject
from building import Building
from simulating import Simulating
from plotting import Plotting
from shared import message
from setting import Setting


class Environment:
    """
    main object of icbc:
        hosts instance of classes subject, setting
    """
    def __init__(self, superuser=None, computer=None, user=None, code=None, branch=None,
                 type_list=[None], case_list=[[None]], configuration_list=[None],
                 flow_process_list=[None], element_type_list=[[None]],
                 operation_type=None, operation=None,
                 test_mode='0',
                 db_user=None, db_password=None,
                 db_host='localhost', db_schema='testing_environment'):
        """
        These parameters can be preselected:
            belong to (test) Subject:
                :param superuser: has accounts on separate computer
                :param computer:
                :param user:
                :param code: belongs to source code tree
                :param branch: belongs to source code tree
            belong to (test) Item:
                :param type_list: belongs to example tree
                :param case_list: belongs to example tree
                :param configuration_list: belongs to example tree
                :param flow_process_list:
                :param element_type_list:
            :param operation_type: one-character string [b: building,s: simulating,p: plotting]
            :param operation: one-character string - meaning depends on operation_type
            :param test_mode:
        Parameters to access database:
            :param db_user:
            :param db_password:
            :param db_host:
            :param db_schema:
        """
        self.__flow_process_name_list, self.__element_type_name_list = flow_process_list, element_type_list

        self.__subject_inst = Subject(superuser, computer, user, code, branch)
        self.__setting_inst = Setting(type_list, case_list, configuration_list,
                                      operation_type, operation, test_mode,
                                      db_user, db_password, db_host, db_schema)

        self.__subject_inst.print_selected_variables()
        self.__setting_inst.print_selected_variables()
        print('\n-----------------------------------------------------------------')

    def run(self):
        """
        main function of icbc:
            1. connect to and disconnect from data base if on local computer
            2. call select functions
            3. call loop if selections successfully made
        :return: 0
        """
        operation_inst = self.select()  # rerun if reselect chosen
        if operation_inst == 1:
            self.run()  # rerun

        self.loop(operation_inst)

        if self.__setting_inst.test_mode == '0':  # control with shell
            self.run()

        return 0

    def select(self):
        """
        select
        1. select operation type and operation
        2. do configurations which are independent of test item
        3. select test items
        :return: (Operation(Building, Simulating, or Plotting)) operation instance; 1 if operation reselect or exception
        """
        self.__subject_inst.select(self.__setting_inst)

        selected_operation_type = self.__setting_inst.select_operation_type()
        operation_inst = self.select_operation(selected_operation_type)
        if not operation_inst:
            return 1  # error in select operation

        if operation_inst.selected_operation == 's':  # reselect
            self.__setting_inst.reselect(self.__subject_inst)  # decide what to reselect
            return 1

        operation_inst.configure()

        self.__setting_inst.select_items_to_test(selected_operation_type,
                                                 operation_inst.selected_operation, self.__subject_inst.computer)

        if self.__setting_inst.operation == 'reselect':
            self.__setting_inst.operation = None
            self.run()  # now reselection is finished, rerun to select next operation

        return operation_inst

    def select_operation(self, operation_type):
        """
        1. generate operation instance,
        2. call select_operation where operation is chosen
        :param operation_type: one-character string [b: building,s: simulating,p: plotting]
        :return: operation instance Building, Simulating, Plotting; 1 if error
        """
        if operation_type == 'b':
            operation_inst = Building(self.__subject_inst)
        elif operation_type == 's':
            operation_inst = Simulating(self.__subject_inst)
        elif operation_type == 'p':
            operation_inst = Plotting(self.__subject_inst)
        else:
            message(mode='ERROR', not_supported=operation_type)
            return None

        operation_inst.select_operation(self.__setting_inst.operation)

        return operation_inst

    def loop(self, operation_inst):
        """
        loop over type, case, and configuration lists
        :param operation_inst: (class Building, Simulating, Plotting (Operation))
        :return:
        """
        constituents = self.__setting_inst.item_constituents
        type_list_counter = 0
        for item_type in constituents.type_list:
            for item_case in constituents.case_list[type_list_counter]:
                self.__flow_process_name_list, self.__element_type_name_list = \
                    self.__setting_inst.get_inner_loop_elements(item_case)
                for item_configuration in constituents.configuration_list:
                    if self.__setting_inst.item_is_to_test(item_case):
                        self.loop_inner(operation_inst, item_type, item_case, item_configuration)
            if len(constituents.case_list) > 1:
                type_list_counter += 1

    def loop_inner(self, operation_inst, item_type, item_case, item_configuration):
        """
        loop over flow process name and element type
        generate item instance before calling run for operation
        :param operation_inst: (class Building, Simulating, or Plotting)
        :param item_type: (string)
        :param item_case: (string)
        :param item_configuration: (string)
        :return:
        """
        for index, flow_process_name in enumerate(self.__flow_process_name_list):
            for element_type_name in self.__element_type_name_list[index]:
                # take all for building or plotting
                if operation_inst.selected_operation_type == 'b' or operation_inst.selected_operation_type == 'p' or \
                        (self.__setting_inst.gateToDatabase.query_column_entry(
                            'flow_processes', flow_process_name, 'active') and
                             self.__setting_inst.gateToDatabase.query_column_entry(
                                 'element_types', element_type_name, 'active')):

                    item_inst = operation_inst.generate_item_instance(item_type, item_case, item_configuration,
                                                                      flow_process_name, element_type_name)
                    operation_inst.configure_for_item(item_type, item_case, item_configuration,
                                                      flow_process_name, element_type_name, self.__setting_inst)
                    operation_inst.run(item_inst)
