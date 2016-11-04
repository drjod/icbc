from os import path
from sys import path as syspath
syspath.append(path.join(path.dirname(__file__), '..', 'customized'))
from simulationData import SimulationData
from subject import Subject
from operation import Building, Simulating, Plotting
from item import Build, Sim, Plot
from utilities import message, adapt_path
from configurationCustomized import location, verbosity
from setting import testing, mySQL, Setting


class Environment:
    """
    main object of icbc:
        hosts instance of classes subject, setting
    """
    __reselect_flag = False
    __current_operation = str()  # used to reselect operation

    def __init__(self, superuser=None, computer=None, user=None, code=None, branch=None,
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
        self.__testing = testing(test_mode, test_level)

        mysql_inst = mySQL(mysql_user, mysql_password, mysql_host, mysql_schema)
        self.__subject_inst = Subject(superuser, computer, user, code, branch)
        self.__setting_inst = Setting(type_list, case_list, configuration_list,
                                      operation_type, operation,
                                      self.__testing, mysql_inst)

        if int(verbosity) > 1:
            # print message for already set variables
            if not computer:
                message(mode='INFO', text='Set computer ' + computer)
            if not user:
                message(mode='INFO', text='Set user ' + user)
            if not code:
                message(mode='INFO', text='Set code ' + code)
            if not branch:
                message(mode='INFO', text='Set branch ' + branch)
            if not type_list[0]:
                for i in range(0, len(type_list)):
                    message(mode='INFO', text='Set type ' + type_list[i])
            if not case_list[0][0]:
                for i in range(0, len(case_list)):
                    for j in range(0, len(case_list[i])):
                        message(mode='INFO', text='Set case ' + case_list[i][j])
            if not configuration_list[0]:
                for i in range(0, len(configuration_list)):
                    message(mode='INFO', text='Set configuration ' + configuration_list[i])
            if not operation_type:
                message(mode='INFO', text='Set operation type ' + operation_type)
            if not operation:
                message(mode='INFO', text='Set operation ' + operation)
            print('\n-----------------------------------------------------------------')

    def __del__(self):
        del self.__subject_inst
        del self.__setting_inst

    def run(self):
        """
        main function of icbc:
            1. set subject to test and test items (user input or preset by passing arguments with constructor)
            2. generate operation instance (configure, select and execute operation)
            3. if the script is executed on a local computer, database calls are done
            4. loop over items _lists to call operation potentially 
               (if operation is finally called for item depends on test mode)
            recalls itself if operation was not preselected
        :return: 0: success - 2: No test item
        """
        if location == 'local':
            self.__setting_inst.connect_to_mysql()
        self.__subject_inst.select(self.__setting_inst)

        selected_operation_type = self.__setting_inst.select_operation_type()
        operation_inst = self.set_current_operation(selected_operation_type)
        # current_operation is environment member (selectedOperation could be reselect)
        
        if operation_inst.selected_operation == 's':  # reselect
            self.__setting_inst.reselect(self.__subject_inst)  # decide what to reselect
            self.__reselect_flag = True  # than no operation executed
        else:
            if selected_operation_type == 's' and self.__current_operation == 'o':
                # the selected operation is to compare results with references
                open(adapt_path(self.__subject_inst.directory + "references\\deviatingFiles.log"), 'w').close()
                # clears file content - for regression testing

            if location == 'local':
                self.__setting_inst.set_lists_for_items(selected_operation_type, self.__current_operation,
                                                  self.__subject_inst.computer)

            if self.__reselect_flag:
                self.__reselect_flag = False
                # do no operation, rather repeat run with empty string for entity to reselect
            elif self.__setting_inst.itemConstituents.type_list is None \
                    or self.__setting_inst.itemConstituents.case_list is None \
                    or self.__setting_inst.itemConstituents.configuration_list is None:
                message(mode='ERROR', text='No test item - No operation')
                return 2
            else:
                type_list_counter = 0
                # item_configuration is None
     
                for item_type in self.__setting_inst.itemConstituents.type_list:
                    for item_case in self.__setting_inst.itemConstituents.case_list[type_list_counter]:
                        for item_configuration in self.__setting_inst.itemConstituents.configuration_list:
                            
                            if self.check_if_item_involved(item_case) == '1':
                                self.go_for_item_run(operation_inst, item_type, item_case, item_configuration)

                    if len(self.__setting_inst.itemConstituents.case_list) > 1:
                        type_list_counter += 1
                    # else do not increment to avoid segmentation fault (case __list is not used)

                # print( '\n_________________________________________________________________' )
            del operation_inst
        
        if location == 'local':
            self.__setting_inst.disconnect_from_mysql()  # to reconnect each run in case of table update
        
        if not self.__setting_inst.operation_preselected:
            self.run()   # repeat if operation was not preselected (test mode or remote)

        return 0

    def set_current_operation(self, operation_type):
        """
        :param operation_type: one-character string [b: building,s: simulating,p: plotting]
        :return: Building, Simulating, Plotting from operation
        requirements:
            members __reselect_flag, __subject_inst, __setting_inst
        """
        if operation_type == 'b': # building
            operation_inst = Building(self.__subject_inst)
        elif operation_type == 's':  # simulating
            operation_inst = Simulating(self.__subject_inst)
        elif operation_type == 'p':  # plotting  
            operation_inst = Plotting(self.__subject_inst)
        else:    
            message(mode='ERROR', not_supported=operation_type)

        if not self.__reselect_flag:
            selected_operation = operation_inst.select_operation(self.__setting_inst.operation_preselected)
            if selected_operation != 's':  # s stands for reselect
                self.__current_operation = selected_operation  # reselect not chosen

        return operation_inst
                            
    def check_if_item_involved(self, item_case):
        """
        check testMode, state, testLevel 
        used for simulation, plotting  operation type (case item exists)
        (all items (i.e. configurations) involved in building operation type)
        :param case:
        :return:
        """
        execute_flag = '1'

        if location == 'local' and item_case:
            if self.__testing.mode == '0':
                # no test mode - select everything by typing on console 
                #                and than the items in the loop (in environment run) is involved
                pass
            elif self.__testing.mode == '1':
                # via browser
                execute_flag = self.__setting_inst.query_column_for_case(item_case, 'state')  # database query
            elif self.__testing.mode == '2':
                # via CI tool
                if int(self.__testing.level) < int(self.__setting_inst.query_column_for_case(item_case, 'test_level')):
                    execute_flag = '0'
            else:
                message(mode='ERROR', not_supported=self.__testing.mode)
        return execute_flag

    def go_for_item_run(self, operation_inst, item_type, item_case, item_configuration):
        """
        generate item instance
        generate simulationData - write files (for numerics, processing) 
        and then call operation run function        
        :param operation_inst: 
        :param item_type:
        :param item_case:
        :param item_configuration:
        :return: 
        """
        selected_operation_type = operation_inst.selected_operation_type

        if selected_operation_type == 'b':  # building
            item_inst = Build(self.__subject_inst, item_configuration)
        elif selected_operation_type == 's':  # simulating
            item_inst = Sim(self.__subject_inst, item_type, item_case, item_configuration)
        elif selected_operation_type == 'p':  # plotting
            item_inst = Plot(self.__subject_inst, item_type, item_case, item_configuration)
        else:
            message(mode='ERROR', not_supported=operation_inst.selected_operation_type)
            return 0

        sim_data = SimulationData(selected_operation_type, operation_inst.selected_operation)
        if location == 'local':
            # do mysql queries
            if sim_data.read_file_flags.numerics:
                sim_data = self.__setting_inst.set_numerics_data(sim_data, item_type, item_case, item_configuration)
                if self.__subject_inst.location == 'remote':
                    # file transfer
                    sim_data.write_numerics_data(item_configuration)
            if sim_data.read_file_flags.processing:
                sim_data = self.__setting_inst.set_processing_data(sim_data, item_type, item_case, item_configuration)
                if self.__subject_inst.location == 'remote':
                    # file transfer
                    sim_data.write_processing_data(item_configuration)

        operation_inst.run(item_inst, sim_data)

        del sim_data
        del item_inst
