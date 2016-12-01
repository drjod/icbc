from utilities import message, select_from_options, str2bool
from utilities import is_in_list, string_represents_non_negative_number_or_potentially_valid_character
from copy import deepcopy
from processing import Processing
from gateToDatabase import GateToDatabase


class Testing:
    def __init__(self, mode, level):
        self.mode = mode   # 0: with shell , 1: control via browser (case has stage in database), 2: with CI
        self.level = level  # for testing with jenkins - each test case has a level this variable is compared with


class Database:
    def __init__(self, user, password, host, schema):
        self.user = user
        self.password = password
        self.host = host
        self.schema = schema


class ItemConstituents:
    def __init__(self, type_list, case_list, configuration_list):
        self.type_list = type_list
        self.case_list = case_list
        self.configuration_list = configuration_list


class ListsCollection:  # stores lists for member get_name_list
    def __init__(self):
        self.id = list()       # stores selected ids
        self.name = list()     # contains selected names (derived from id)
        self.nameSub = list()  # to generate nested nameList for table cases, which depends on selected type
        self.id_name_pair = list()  # for data base access - each entry contains an id and name
        #                             as a dictionary {'id': ..., 'name':} obtained from databa


class Setting:
    """
    console input
    hosts TestCases lists, gateToDatabase
    operation, operation_type
    """
    __selectedTypeIdList = list()  # for tree structure (types, cases) - to know selected type when cases are selected

    def __init__(self, type_list, case_list, configuration_list, operation_type,
                 operation, testing_properties, db_inst):
    
        self.__item_constituents = ItemConstituents(type_list, case_list, configuration_list)
        self.__operation_type = operation_type  # building or testing
        self.__operation = operation
        self.__testing = testing_properties  # to switch off select
        self.__db_inst = db_inst
        self.__gateToDatabase = None
        
    def __del__(self):
        pass

    def print_selected_variables(self):
        """
        print variables which have already been selected, e.g. to print preselected values
        meaning they have not value None or [None] (for type, configuration) or [[None]] (for case)
        the variables are: type, case, configuration, operation_type, operation
        (member variables of class Subject can be printed via separate Subject member function)
        :return:
        """
        if self.__item_constituents.type_list[0]:
            for i in range(0, len(self.__item_constituents.type_list)):
                message(mode='INFO', text='Set type {}'.format(self.__item_constituents.type_list[i]))
        if self.__item_constituents.case_list[0][0]:
            for i in range(0, len(self.__item_constituents.case_list)):
                for j in range(0, len(self.__item_constituents.case_list[i])):
                    message(mode='INFO', text='Set case {}'.format(self.__item_constituents.case_list[i][j]))
        if self.__item_constituents.configuration_list[0]:
            for i in range(0, len(self.__item_constituents.configuration_list)):
                message(mode='INFO', text='Set configuration {}'.format(self.__item_constituents.configuration_list[i]))

        if self.__operation_type:
            message(mode='INFO', text='Set operation type {}'.format(self.__operation_type))
        if self.__operation:
            message(mode='INFO', text='Set operation {}'.format(self.__operation))

    def connect_to_db(self):
        message(mode='INFO', text='Connect {} to database {} {}'.format(
            self.__db_inst.user, self.__db_inst.host, self.__db_inst.schema))

        self.__gateToDatabase = GateToDatabase(self.__db_inst)

    def disconnect_from_db(self):
        # message(mode='INFO', text='Disconnecting')
        del self.__gateToDatabase

    @property
    def item_constituents(self):
        return self.__item_constituents

    @property
    def operation_type(self):
        return self.__operation_type

    @property
    def operation(self):
        return self.__operation

    @operation.setter
    def operation(self, value):
        self.__operation = value

    @property
    def testing(self):
        return self.__testing

    def query_flow_process_name_list(self, case_name):
        """
        :param case_name: (string)
        :return: (string list)
        """
        name_list = list()

        numerics_id_list = self.__gateToDatabase.query_ids_from_column_entries(
            'numerics', 'case_id', self.__gateToDatabase.query_id_for_name('cases', case_name))

        flow_process_id_list = list()

        for numerics_id in numerics_id_list:
            flow_process_id = self.__gateToDatabase.query_column_entry(
                'numerics', numerics_id, 'flow_process_id')
            if not is_in_list(flow_process_id, flow_process_id_list):
                flow_process_id_list.append(flow_process_id)
                name_list.append(self.__gateToDatabase.query_name_for_id('flow_processes', flow_process_id))
        return name_list

    def query_element_type_name_list(self, case_name, flow_process_name_list):
        """

        :param case_name:
        :param flow_process_name_list:
        :return:
        """
        name_nested_list = [[]]
        name_nested_list.clear()

        numerics_id_list = self.__gateToDatabase.query_ids_from_column_entries(
            'numerics', 'case_id', self.__gateToDatabase.query_id_for_name('cases', case_name))

        for flow_process_name in flow_process_name_list:
            name_inner_list = list()
            for numerics_id in numerics_id_list:
                running_flow_process_name = self.__gateToDatabase.query_name_for_id(
                    'flow_processes', self.__gateToDatabase.query_column_entry('numerics', numerics_id, 'flow_process_id'))
                if flow_process_name == running_flow_process_name:
                    flow_process_id = self.__gateToDatabase.query_column_entry(
                        'numerics', numerics_id, 'element_type_id')
                    name_inner_list.append(self.__gateToDatabase.query_name_for_id('element_types', flow_process_id))
            name_nested_list.append(name_inner_list)

        return name_nested_list

    def query_location(self, computer_name):
        """
        query location (local or remote) from computer table for given computer name
            by first querying computer id
        :param computer_name: (string)
        :return: (string) location
        """
        return self.__gateToDatabase.query_column_entry('computer',
                                                     self.__gateToDatabase.query_id_for_name('computer', computer_name),
                                                     'location')

    def query_operating_system(self, computer_name):
        """
        query an operating system from computer table for a given conputer name
            by first querying computer_id
        :param computer_name:
        :return:
        """
        return self.__gateToDatabase.query_column_entry('computer',
                                                     self.__gateToDatabase.query_id_for_name('computer', computer_name),
                                                     'operating_system')
 
    def query_directory_root(self, computer_name, user_name):
        """
        query a root directory from paths table for a given computer and user name
            by querying first computer and user id
        :param computer_name: (string)
        :param user_name: (string)
        :return: (string) root directory
        """
        return self.__gateToDatabase.query_directory_root(self.__gateToDatabase.query_id_for_name('computer', computer_name),
                                                       self.__gateToDatabase.query_id_for_name('users', user_name))

    def query_hostname(self, computer_name):
        """
        query a hostname from computer table for a given computer name
            by querying first computer id from computer name
        :param computer_name: (string)
        :return: (string) hostname
        """
        return self.__gateToDatabase.query_column_entry('computer',
                                                     self.__gateToDatabase.query_id_for_name('computer', computer_name),
                                                     'hostname')
    
    def query_username(self, superuser_name, computer_name):
        """
        query a username for a given superuser and computer_name
            by first querying user id from superuser table
        :param superuser_name: (string)
        :param computer_name: (string)
        :return: (string ) username
        """
        return self.__gateToDatabase.query_name_for_id('users',
                                                    self.__gateToDatabase.query_userid(
                                                        superuser_name, computer_name))
                                                      
    def query_column_entry_for_name(self, table, name, column_name):
        """
        query a column entry from table for a name
            by first querying case id
        :param table: (string)
        :param case_name: (string)
        :param column_name: (string)
        :return: (string) column entry
        """
        return self.__gateToDatabase.query_column_entry(table, self.__gateToDatabase.query_id_for_name(
            table, name), column_name)

    def query_process_numerics_data(self, numerics_type, process, item_case, item_configuration='no_configuration'):
        """
        query entry for solver_dir, preconditioner_dir, or theta_dir from cases table for a process and configuration
        :param numerics_type: (string )[solver, preconditioner, theta]
        :param process: (string) [flow, mass, heat]
        :param item_case: (string)
        :param item_configuration: (string) 'no_configuration' for numerics_type theta
        :return:
        """
        if item_configuration == 'no_configuration':
            column_name_in_cases_table = '{}_{}'.format(numerics_type, process)
        else:
            column_name_in_cases_table = '{}_{}_{}'.format(numerics_type, process, item_configuration)

        column_entry = self.__gateToDatabase.query_column_entry(
            'cases', self.__gateToDatabase.query_id_for_name('cases', item_case), column_name_in_cases_table)

        if numerics_type == 'solver' or numerics_type == 'preconditioner':
            return self.convert_numerics_entry_in_cases_table_to_specification(
                item_configuration, column_entry, numerics_type)
        else:  # theta
            return column_entry

    def select_operation_type(self):
        """
        prepare dictionary [building, simulating, plotting] for self.select_from_options() and call it
        :return: ((one-character) tring) selected operation type
        """
        if not self.__operation_type:
            operation_type_dict = {'b': '(b)uilding', 's': '(s)imulating', 'p': '(p)lotting'}
            self.__operation_type = select_from_options(operation_type_dict, 'Select operation type')
        return self.__operation_type

    def reselect(self, subject):
        """
        prepare dictionary [operation type, computer, ...] for self.select_from_options() and call it
        call self.neutralize_previous_selections() to set previous settings to None
        this condition (value is None) lets user reselect values in functions select_*
        :param subject: (class Subject) stores variables computer, user, code, branch
        :return:
        """
        option_dict = {'p': 'o(p)eration type', 'c': '(c)omputer', 'o': 'c(o)de',
                       'b': '(b)ranch', 'n': 'co(n)figuration'}
        if self.__operation_type == 's' or self.__operation_type == 'p':
            option_dict_amendments = {'e': '(e)xample', 't': '(t)ype', 'a': 'c(a)se'}
            option_dict.update(option_dict_amendments)
        option_selected = select_from_options(option_dict, 'Select')
        self.neutralize_previous_selections(subject, option_selected)

    def neutralize_previous_selections(self, subject, option_selected):
        """
        1.  set previously selected entities in subject, self.item,
            or self.__operation type to None (case_list to [' '])
        2.  sets always operation None such that it must reselected, too
        used by self.reselect(), which provides the selected option

        :param subject: (Subject)
        :param option_selected: (one-char string)
        :return:
        """
        if option_selected == 'c':  # computer
            subject.computer = None
            subject.user = None  # user must be reselected too
            self.__item_constituents.configuration_list = [None]  # also configurations since they depend on computer
        if option_selected == 'o':  # code
            subject.code = None
            subject.branch = None  # branch must be reselected too
        if option_selected == 'b':  # branch
            subject.branch = None
        if option_selected == 't' or option_selected == 'e':  # type | example
            self.__item_constituents.type_list = [None]
            self.__item_constituents.case_list = [[None]]  # case must be reselected too
            self.__selectedTypeIdList.clear()
        if option_selected == 'a' or option_selected == 'e':  # case | example
            self.__item_constituents.case_list = [[None]]
        if option_selected == 'n' or option_selected == 'e':  # configuration | example
            self.__item_constituents.configuration_list = [None]
        if option_selected == 'p':  # operation type
            self.__operation_type = None

        self.__operation = 'reselect'  # operation is checked for this value 'reselect'
        #                                after all selections are made in next loop
        #                                this way, the intended reselection is before the next process selection

    def get_name_list(self, table, computer=None):
        """
        1. get table data from data base (an item consists of the data base entries id and name)
        2. use the ids to let the user select an id (or ids for tables type, case, configurations)
        3. derive name(s) from id(s)
        :param table: (string) name of table in SQL schema
        :param computer: (string) name of computer
        :return:  names (list of strings, nested list if table = 'cases')
                  for a table obtained from database and user selection
                  contains one element except if table is type, case, configuration, where name_list can contain
                  more elements
        """
        lists_inst = ListsCollection()

        self.get_table_data_from_database(table, computer, lists_inst)
        if len(lists_inst.name) > 0:  # for table cases if in table types all or range  was selected
            return lists_inst.name  # know already names, so return them directly

        selected_id = self.select_id(table, lists_inst)
        name_list = self.id2name(table, selected_id, lists_inst)

        del lists_inst
        return name_list

    def get_table_data_from_database(self, table, computer, lists_inst):
        """
        fill lists_inst.id_name_pair with data from database
        each entry is dictionary of form {'id': ..., 'name': ... }
        if table is cases and more than one type selected, fill lists_inst.name directly
        since select_id for case not required
        class member to have access to __selectedTypeIdList
        :param table: (string)
        :param computer: (string) used since nao all configurations available on all computer
        :param lists_inst: (class listsCollection)
        :return:
        """
        if table == 'cases':  # has sublist for each type (nested list)
            if len(self.__selectedTypeIdList) > 1:  # more than one type was selected
                for typeId in self.__selectedTypeIdList:
                    lists_inst.id_name_pair = self.__gateToDatabase.query_id_name_pair_list(
                        'cases', 'a', selected_type_id=typeId)
                    for row in lists_inst.id_name_pair:
                        lists_inst.nameSub.append(str(row['name']))
                    lists_inst.name.append(deepcopy(lists_inst.nameSub))
                    # append to name to return this directly (without select_id)
                    lists_inst.nameSub.clear()
            else:  # cases for specific type
                lists_inst.id_name_pair = self.__gateToDatabase.query_id_name_pair_list(
                    'cases', 'a', selected_type_id=self.__selectedTypeIdList[0])
        elif table == 'configurations':  # since it depends on computer
            lists_inst.id_name_pair = self.__gateToDatabase.query_id_name_pair_list(
                'configurations', 'a', self.__gateToDatabase.query_id_for_name('computer', computer))
        else:  # computer, user, ... (anything but cases, configurations - see list in environment constructor)
            lists_inst.id_name_pair = self.__gateToDatabase.query_id_name_pair_list(table, 'a')
       
    def select_id(self, table, lists_inst):
        """
        print options on console
        fill lists_inst.nameSub with names from id-name-pairs in lists_inst
        recalls itself if not proper user input
        Requirements:
            id_name_pairs in lists_inst must be set
        :param table:
        :param lists_inst:
        :return:
        """
        for row in lists_inst.id_name_pair:
            lists_inst.nameSub.append(deepcopy(str(row['name'])))
            lists_inst.id.append(deepcopy(str(row['id'])))

        if self.__testing.mode == '0':
            # print options
            print('\nSelect from {}:\n'.format(table))
            for index, inst_id in enumerate(lists_inst.id):
                print('   {} {}'.format(inst_id, lists_inst.nameSub[index]))
            print('   a all')
            if table == 'types':  # range only for types supported
                print('   r range')
            # select
            #
            selected_id = input('\n   by entering value: ')
        else:
            # TESTLEVEL: preselect anything but examples (types, cases, configurations)
            # and specify state (for jsp) or level (for CI) in database
            # all examples are selected here and level is checked later on
            selected_id = 'a'

        if table == 'types':
            self.set_type_ids(selected_id, lists_inst)
        print('\n-----------------------------------------------------------------')

        if not string_represents_non_negative_number_or_potentially_valid_character(selected_id):
            return self.select_id(table, lists_inst)
        return selected_id

    def set_type_ids(self, selected_id, lists_inst):
        """
        set self.__selectedTypeIdList
        :param selected_id: (string)
        :param lists_inst: (string list)
        :return:
        """
        if selected_id == 'a':  # selected all
            for i in range(0, len(lists_inst.id)):
                self.__selectedTypeIdList.append(deepcopy(lists_inst.id[i]))
        elif selected_id == 'r':  # selected range - so get the lower and upper range limits now
            lower_range = input('\n       From: ')
            upper_range = input('\n         To: ')
            for i in range(int(lower_range), int(upper_range) + 1):
                self.__selectedTypeIdList.append(deepcopy(lists_inst.id[i]))
        else:
            self.__selectedTypeIdList.append(deepcopy(selected_id))

    def id2name(self, table, id_selected, lists_inst):
        """
        Convert id to name (list) and return this as a nested list [['...']]
        class member to have access to __selectedTypeIdList
        :param table:
        :param id_selected:
        :param lists_inst:
        :return:
        """
        if id_selected == 'a':
            if table == 'cases':
                lists_inst.name.append(deepcopy(lists_inst.nameSub))
                return lists_inst.name
            else:
                return lists_inst.nameSub
        elif id_selected == 'r':
            if table == 'types':
                for id_running in self.__selectedTypeIdList:
                    lists_inst.name.append(deepcopy(lists_inst.nameSub[get_list_id(id_running, lists_inst.id)]))
                return lists_inst.name
            else:
                message(mode='ERROR', text='Range supported only for types')
                return None
        else:  # single item
            lists_inst.name.append(deepcopy(lists_inst.nameSub[get_list_id(id_selected, lists_inst.id)]))
            if table == 'cases':
                name_list2 = list()
                name_list2.append(deepcopy(lists_inst.name))
                return name_list2
            else:
                return lists_inst.name
    
    def select_constituent_of_items_to_test(self, level, computer_of_subject=None):
        """
        calls member function selectNames to get item constituents
        if they are not previously selected (i.e. in environment constructor or anywhere in last operations)
        :param level:
        :param computer_of_subject:
        :return: list (string) for one item  constituent (meaning: types, cases, configuration)
              nested list if table = 'cases'
        """
        if level == 'types':
            if self.__item_constituents.type_list == [None]:
                #len(self.__item_constituents.type_list) == 0 or not self.__item_constituents.type_list[0]:
                return self.get_name_list(table='types')
            else:
                return self.__item_constituents.type_list
        elif level == 'cases':
            if self.__item_constituents.case_list == [[None]]:
                #len(self.__item_constituents.case_list) == 0 or self.__item_constituents.case_list[0] == [None]:
                return self.get_name_list(table='cases')
            else:
                return self.__item_constituents.case_list
        elif level == 'configurations':
            if self.__item_constituents.configuration_list == [None]:
                #len(self.__item_constituents.configuration_list) == 0 \
                #    or not self.__item_constituents.configuration_list[0]:
                return self.get_name_list(table='configurations', computer=computer_of_subject)
            else:
                return self.__item_constituents.configuration_list
        else:
            message(mode='ERROR', not_supported='level ' + level)

    def convert_numerics_entry_in_cases_table_to_specification(self, item_configuration, entry, numerics_type):
        """
        :param item_configuration:
        :param entry:
        :param numerics_type: 'solver' or 'preconditioner'
        :return:
        """
        try:
            if entry != 'null':
                solver_table_name = self.__gateToDatabase.query_column_entry(
                    'configurations', self.__gateToDatabase.query_id_for_name('configurations', item_configuration),
                    numerics_type + '_table_name')
                return self.__gateToDatabase.query_column_entry(solver_table_name, entry, 'specification')
            else:
                return '-1'
        except Exception as err:
            message(mode='ERROR', text="{}".format(err))

    def select_items_to_test(self, operation_type, operation, computer):
        """
        generate examples Lists to loop over in Environment run
        :param operation_type:
        :param operation:
        :param computer:
        :return:
        """
        if operation_type == 'b':  # building (only configuration)
            self.__item_constituents.type_list = [None]
            self.__item_constituents.case_list = [[None]]
            self.__item_constituents.configuration_list = self.select_constituent_of_items_to_test(
                level='configurations', computer_of_subject=computer)
        elif operation_type == 's':  # simulating (all item constituents (type, case, configuration))
            self.__item_constituents.type_list = self.select_constituent_of_items_to_test(level='types')
            self.__item_constituents.case_list = self.select_constituent_of_items_to_test(level='cases')
            self.__item_constituents.configuration_list = self.select_constituent_of_items_to_test(
                level='configurations', computer_of_subject=computer)
        elif operation_type == 'p':  # plotting
            self.__item_constituents.type_list = self.select_constituent_of_items_to_test(level='types')
            if operation == 'j' or operation == 'w':  # generate or wait for JPG (only type)
                self.__item_constituents.case_list = [[None]]
                self.__item_constituents.configuration_list = [None]
            else:  # all item constituents  (type, case, configuration)
                self.__item_constituents.case_list = self.select_constituent_of_items_to_test(level='cases')
                self.__item_constituents.configuration_list = self.select_constituent_of_items_to_test(
                    level='configurations', computer_of_subject=computer)
        else:
            message(mode='ERROR', not_supported='operation_type {}'.format(operation_type))

    def set_processing_data(self, sim_data, item_type, item_configuration):
        """
        get processing (parallelization) data from database and store in sim_data
        :param sim_data: (class SimulationData)
        :param item_type: (string)
        :param item_configuration: (string)
        :return:
        """
        processing = Processing()

        processing.number_cpus = self.__gateToDatabase.query_column_entry(
            'types', self.__gateToDatabase.query_id_for_name('types', item_type), 'number_cpus')
        processing.mode = self.__gateToDatabase.query_column_entry(
            'configurations', self.__gateToDatabase.query_id_for_name('configurations', item_configuration), 'processing')

        sim_data.processing = processing

    def set_numerics_directories(self, sim_data, item_case, item_configuration,
                                 flow_process_name, element_type_name, process):
        sim_data.solver_dir[process] = self.convert_numerics_entry_in_cases_table_to_specification(
            item_configuration, self.__gateToDatabase.query_column_entry(
                'numerics', self.__gateToDatabase.query_id_from_numerics_table(
                    item_case, flow_process_name, element_type_name),
                'solver_' + process + '_' + item_configuration.lower()), 'solver')
        sim_data.preconditioner_dir[process] = self.convert_numerics_entry_in_cases_table_to_specification(
            item_configuration, self.__gateToDatabase.query_column_entry(
                'numerics', self.__gateToDatabase.query_id_from_numerics_table(
                    item_case, flow_process_name, element_type_name),
                'preconditioner_' + process + '_' + item_configuration.lower()), 'preconditioner')
        sim_data.theta_dir[process] = self.__gateToDatabase.query_column_entry(
            'numerics', self.__gateToDatabase.query_id_from_numerics_table(
                item_case, flow_process_name, element_type_name),
            'theta_' + process)

    def set_numerics_data(self, sim_data, item_case, item_configuration, flow_process_name, element_type_name):
        """
        get mumerics and parallelization data from database and store in sim_data
        data are used later on to write *.num *.pbs files
        :param sim_data: (class SimulationData)
        :param item_case: (string)
        :param item_configuration: (string)
        :param flow_process_name: (string)
        :param element_type_name: (string)
        :return:
        """
        # numerics global
        case_id = self.__gateToDatabase.query_id_for_name('cases', item_case)
        sim_data.numerics_global.processes.flow = flow_process_name
        sim_data.numerics_global.processes.mass_flag = str2bool(self.__gateToDatabase.query_column_entry(
            'cases', case_id, 'mass_flag'))
        sim_data.numerics_global.processes.heat_flag = str2bool(self.__gateToDatabase.query_column_entry(
            'cases', case_id, 'heat_flag'))
        sim_data.numerics_global.processes.deformation_flag = str2bool(self.__gateToDatabase.query_column_entry(
            'cases', case_id, 'deformation_flag'))
        sim_data.numerics_global.processes.fluid_momentum_flag = str2bool(self.__gateToDatabase.query_column_entry(
            'cases', case_id, 'fluid_momentum_flag'))
        sim_data.numerics_global.processes.overland_flag = str2bool(self.__gateToDatabase.query_column_entry(
            'cases', case_id, 'overland_flag'))

        sim_data.numerics_global.coupled_flag = str2bool(self.__gateToDatabase.query_column_entry(
            'cases', case_id, 'coupled_flag'))
        sim_data.numerics_global.lumping_flag = str2bool(self.__gateToDatabase.query_column_entry(
            'numerics', self.__gateToDatabase.query_id_from_numerics_table(
                item_case, flow_process_name, element_type_name),
            'flow_lumping_flag'))
        sim_data.numerics_global.non_linear_flag = str2bool(self.__gateToDatabase.query_column_entry(
            'flow_processes', self.__gateToDatabase.query_id_for_name(
                'flow_processes', flow_process_name), 'nonlinear_flag'))
        # solver, preconditioner, theta
        self.set_numerics_directories(sim_data, item_case, item_configuration,
                                      flow_process_name, element_type_name, 'flow')
        if sim_data.numerics_global.processes.mass_flag:
            self.set_numerics_directories(sim_data, item_case, item_configuration,
                                          flow_process_name, element_type_name, 'mass')
        if sim_data.numerics_global.processes.heat_flag:
            self.set_numerics_directories(sim_data, item_case, item_configuration,
                                          flow_process_name, element_type_name, 'heat')
        if sim_data.numerics_global.processes.deformation_flag:
            self.set_numerics_directories(sim_data, item_case, item_configuration,
                                          flow_process_name, element_type_name, 'deformation')
        if sim_data.numerics_global.processes.fluid_momentum_flag:
            self.set_numerics_directories(sim_data, item_case, item_configuration,
                                          flow_process_name, element_type_name, 'fluid_momentum')
        if sim_data.numerics_global.processes.overland_flag:
            self.set_numerics_directories(sim_data, item_case, item_configuration,
                                          flow_process_name, element_type_name, 'overland_flow')


def get_list_id(selected_id, id_list):
    """
    Convert from global id to local id
    :param selected_id: (string)
    :param id_list: (string)
    :return: (int) id
    """
    for index, idInst in enumerate(id_list):
        if idInst == selected_id:
            return index
