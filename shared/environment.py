from os import path
from sys import path as syspath
syspath.append(path.join(path.dirname(__file__), '..', 'customized'))
from subject import Subject
from operation import Building, Simulating, Plotting
from item import Build, Sim, Plot
from utilities import message, adapt_path, clear_file
from configurationCustomized import location
from setting import Testing, MySQL, Setting


class Environment:
    """
    main object of icbc:
        hosts instance of classes subject, setting
    """
    def __init__(self, superuser=None, computer=None, user=None, code=None, branch=None, id_local_process='unused',
                 type_list=[None], case_list=[[None]], configuration_list=[None],
                 operation_type=None, operation=None,
                 test_mode='0', test_level='0',
                 mysql_user='root', mysql_password='*****', mysql_host='localhost', mysql_schema='testing_environment'):
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
            :param operation_type: one-character string [b: building,s: simulating,p: plotting]
            :param operation: one-character string - meaning depends on operation_type
            :param test_mode:
            :param test_level:
        Parameters to access database:
            :param mysql_user:
            :param mysql_password:
            :param mysql_host:
            :param mysql_schema:
        """
        self.__testing = Testing(test_mode, test_level)

        mysql_inst = MySQL(mysql_user, mysql_password, mysql_host, mysql_schema)
        self.__subject_inst = Subject(superuser, computer, user, code, branch, id_local_process)
        self.__setting_inst = Setting(type_list, case_list, configuration_list,
                                      operation_type, operation,
                                      self.__testing, mysql_inst)

        if location == 'local':
            self.__subject_inst.print_selected_variables()
            self.__setting_inst.print_selected_variables()
        print('\n-----------------------------------------------------------------')

    def __del__(self):
        del self.__subject_inst
        del self.__setting_inst

    def run(self):
        """
        main function of icbc:
            1. connect to and disconnect from data base if on local computer
            2. call select functions
            3. call loop if selects successful
        :return: 0
        """
        if location == 'local':
            self.__setting_inst.connect_to_mysql()

        operation_inst = self.select()  # rerun if reselect chosen
        if operation_inst == 1:
            self.run()  # rerun

        self.loop(operation_inst)
        del operation_inst

        if location == 'local':
            self.__setting_inst.disconnect_from_mysql()  # to reconnect each run in case of table update
            if self.__setting_inst.testing.mode == '0':  # control with shell
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
        if operation_inst == 1:
            return 1

        if operation_inst.selected_operation == 's':  # reselect
            self.__setting_inst.reselect(self.__subject_inst)  # decide what to reselect
            return 1

        self.configure(operation_inst)

        self.__setting_inst.select_items_to_test(selected_operation_type,
                                                 self.__setting_inst.operation, self.__subject_inst.computer)

        if self.__setting_inst.operation == 'reselect':
            self.__setting_inst.operation = None
            self.run()  # now reselection is finished, rerun to select next operation

        # if list entries for test item incomplete,
        # do no operation, rather repeat run with empty string for entity to reselect
        if self.__setting_inst.item_constituents.type_list is [None] \
                or self.__setting_inst.item_constituents.case_list is [[None]] \
                or self.__setting_inst.item_constituents.configuration_list is [None]:
            message(mode='ERROR', text='No test item - No operation')
            return 1

        return operation_inst

    def select_operation(self, operation_type):
        """
        1. generate operation instance,
        2. call select_operation where operation is chosen
        :param operation_type: one-character string [b: building,s: simulating,p: plotting]
        :return: operation instance Building, Simulating, Plotting; 1 if error
        """
        if operation_type == 'b':  # building
            operation_inst = Building(self.__subject_inst)
        elif operation_type == 's':  # simulating
            operation_inst = Simulating(self.__subject_inst)
        elif operation_type == 'p':  # plotting
            operation_inst = Plotting(self.__subject_inst)
        else:
            message(mode='ERROR', not_supported=operation_type)
            return 1

        operation_inst.select_operation(self.__setting_inst.operation)

        return operation_inst

    def configure(self, operation_inst):
        """
        0.  call function to set flags for file uploads
        1.  if operation is to compare results with references, clear log file with names of
            deviating files from previous runs
        2. check if list entries for test items exit
        :param operation_inst: (class Building, Simulating, Plotting (Operation))
        :return: 0 if success; 1 if lists for item not complete
        """
        operation_inst.set_upload_file_flags()

        if self.__setting_inst.operation_type == 's' and self.__setting_inst.operation == 'o':
            # the selected operation is to compare results with references
            clear_file(adapt_path(self.__subject_inst.directory + "references\\deviatingFiles.log"))

    def loop(self, operation_inst):
        """
        loop over type, case, and configuration lists
        :param operation_inst: (class Building, Simulating, Plotting (Operation))
        :return:
        """
        type_list_counter = 0
        for item_type in self.__setting_inst.item_constituents.type_list:
            for item_case in self.__setting_inst.item_constituents.case_list[type_list_counter]:
                for item_configuration in self.__setting_inst.item_constituents.configuration_list:

                    if self.check_if_item_is_to_test(item_case) == '1':
                        self.go_for_run_item(operation_inst, item_type, item_case, item_configuration)

            if len(self.__setting_inst.item_constituents.case_list) > 1:
                type_list_counter += 1

    def check_if_item_is_to_test(self, item_case):
        """
        check testMode, state, testLevel
        used for simulation, plotting  operation type (case item exists)
        (all items (i.e. configurations) involved in building operation type)
        :param item_case: (string or None)
        :return: '0': not involved, '1' involved or ERROR
        """
        execute_flag = '1'

        if location == 'local' and item_case:
            if self.__testing.mode == '0':
                # no test mode - select everything by typing on console
                #                and than the items in the loop (in environment run) is involved
                execute_flag = '1'
            elif self.__testing.mode == '1':
                # via browser
                execute_flag = self.__setting_inst.query_column_for_case(item_case, 'state')  # database query
            elif self.__testing.mode == '2':
                # via CI tool
                if int(self.__testing.level) < int(self.__setting_inst.query_column_for_case(item_case, 'test_level')):
                    execute_flag = '0'
            else:
                message(mode='ERROR', not_supported=self.__testing.mode)  # returns '1'

        return execute_flag  # remote always '1'

    def go_for_run_item(self, operation_inst, item_type, item_case, item_configuration):
        """
        1. generate (and delete) item instance
        2. call write files (for numerics, processing)
        3. call operation run function
        :param operation_inst: (class Building, Simulating, or Plotting)
        :param item_type: (string)
        :param item_case: (string)
        :param item_configuration: (string)
        :return:
        """
        item_inst = self.generate_item_instance(operation_inst, item_type, item_case, item_configuration)

        operation_inst.write_files_for_upload(item_type, item_case, item_configuration,
                                              self.__setting_inst, self.__subject_inst.location)
        operation_inst.run(item_inst)

        del item_inst

    def generate_item_instance(self, operation_inst, item_type, item_case, item_configuration):
        """
        generate Build, Sim or Plot according to chosen operation
        :param operation_inst:
        :param item_type:
        :param item_case:
        :param item_configuration:
        :return: child of Item instance (Build, Sim, Plot)
        """
        if operation_inst.selected_operation_type == 'b':  # building
            return Build(self.__subject_inst, item_configuration)
        elif operation_inst.selected_operation_type == 's':  # simulating
            return Sim(self.__subject_inst, item_type, item_case, item_configuration)
        elif operation_inst.selected_operation_type == 'p':  # plotting
            return Plot(self.__subject_inst, item_type, item_case, item_configuration)
        else:
            message(mode='ERROR', not_supported=operation_inst.selected_operation_type)
            return 1  # check this

