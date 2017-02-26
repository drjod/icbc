from shared import message
from copy import deepcopy
from collections import OrderedDict
from processing import Processing
from gateToDatabase import GateToDatabase


class Database:
    def __init__(self, user, password, host, schema):
        self.user, self.password, self.host, self.schema = user, password, host, schema


class ItemConstituents:
    def __init__(self, type_list, case_list, configuration_list):
        self.type_list, self.case_list, self.configuration_list = type_list, case_list, configuration_list


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
                 operation, test_mode, db_user, db_password, db_host, db_schema):
    
        self.__item_constituents = ItemConstituents(type_list, case_list, configuration_list)
        self.__operation_type, self.__operation = operation_type, operation  # type: building or testing
        self.__test_mode = test_mode  # 0: with shell ,
        # 1: control via browser (case has stage in database), 2: with CI
        message(mode='INFO', text='Connect {} to database {} at {}'.format(db_user, db_schema, db_host))
        self.__gateToDatabase = GateToDatabase(Database(db_user, db_password, db_host, db_schema))
        
    def __del__(self):
        pass

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
    def test_mode(self):
        return self.__test_mode

    @property
    def gateToDatabase(self):
        return self.__gateToDatabase

    def print_selected_variables(self):
        """
        print variables which have already been selected, e.g. to print preselected values
        meaning they have not value None or [None] (for type, configuration) or [[None]] (for case)
        the variables are: type, case, configuration, operation_type, operation
        (member variables of class Subject can be printed via separate Subject member function)
        :return:
        """
        constituents = self.__item_constituents
        if constituents.type_list != [None]:
            message(mode='INFO', text='Set type list {}'.format(constituents.type_list))
        if constituents.case_list != [[None]]:
            message(mode='INFO', text='Set case nested list {}'.format(constituents.case_list))
        if constituents.configuration_list != [None]:
            message(mode='INFO', text='Set configuration list {}'.format(constituents.configuration_list))

        if self.__operation_type:
            message(mode='INFO', text='Set operation type {}'.format(self.__operation_type))
        if self.__operation:
            message(mode='INFO', text='Set operation {}'.format(self.__operation))

    def query_process_numerics_data(self, numerics_type, process, item_case, item_configuration='no_configuration'):
        """
        query entry for solver_dir, preconditioner_dir, or theta_dir from cases table for a process and configuration
        :param numerics_type: (string )[solver, preconditioner, theta]
        :param process: (string) [flow, mass, heat]
        :param item_case: (string)
        :param item_configuration: (string) 'no_configuration' for numerics_type theta
        :return:
        """
        column_name_in_cases_table = '{}_{}'.format(numerics_type, process) if \
            item_configuration == 'no_configuration' else '{}_{}_{}'.format(numerics_type, process, item_configuration)

        column_entry = self.__gateToDatabase.query_column_entry(
            'cases', self.__gateToDatabase.query_id_for_name('cases', item_case), column_name_in_cases_table)

        return self.convert_numerics_entry_in_cases_table_to_specification(
            item_configuration, column_entry, numerics_type) if \
            numerics_type == 'solver' or numerics_type == 'preconditioner' else \
            column_entry  # theta

    def select_operation_type(self):
        """
        prepare dictionary [building, simulating, plotting] for self.select_from_options() and call it
        side-effect: set self__operation_type if not already set
        :return: ((one-character) tring) selected operation type
        """
        if not self.__operation_type:
            self.__operation_type = select_from_options(
                OrderedDict([('b', '(b)uilding'), ('s', '(s)imulating'), ('p', '(p)lotting')]),
                'Select operation type')
        return self.__operation_type

    def reselect(self, subject):
        """
        prepare dictionary [operation type, computer, ...] for self.select_from_options() and call it
        call self.neutralize_previous_selections() to set previous settings to None
        this condition (value is None) lets user reselect values in functions select_*
        :param subject: (class Subject) stores variables computer, user, code, branch
        :return:
        """
        option_dict = OrderedDict([('p', 'o(p)eration type'), ('c', '(c)omputer'), ('o', 'c(o)de'),
                                   ('b', '(b)ranch'), ('n', 'co(n)figuration')])
        if self.__operation_type == 's' or self.__operation_type == 'p':
            option_dict.update({'e': '(e)xample', 't': '(t)ype', 'a': 'c(a)se'})

        self.reconfigure_for_new_selection(subject, select_from_options(option_dict, 'Select'))

    def reconfigure_for_new_selection(self, subject, option_selected):
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
            subject.user = None  # user must be reselected, too
            self.__item_constituents.configuration_list = [None]  # also configurations since they depend on computer
        if option_selected == 'o':  # code
            subject.code = None
            subject.branch = None  # branch must be reselected, too
        if option_selected == 'b':  # branch
            subject.branch = None
        if option_selected == 't' or option_selected == 'e':  # type | example
            self.__item_constituents.type_list = [None]
            self.__item_constituents.case_list = [[None]]  # case must be reselected, too
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

        # for table cases if in table types all or range  was selected know already names, so return them directly
        if len(lists_inst.name) > 0:
            return lists_inst.name
        else:
            if table == 'cases':
                return [self.id2name(table, self.select_id(table, lists_inst), lists_inst)]
            else:
                return self.id2name(table, self.select_id(table, lists_inst), lists_inst)

    def get_table_data_from_database(self, table, computer, lists_inst):
        """
        fill lists_inst.id_name_pair with data from database
        each entry is dictionary of form {'id': ..., 'name': ... }
        if table is cases and more than one type selected, fill lists_inst.name directly
        since select_id for case not required
        class member to have access to __selectedTypeIdList
        :param table: (string)
        :param computer: (string) used since not all configurations available on every computer
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
                'configurations', 'a', computer)
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
        id_name = dict() # use dict to print ids sorted in table where id is selected
        for row in lists_inst.id_name_pair:
            lists_inst.nameSub.append(deepcopy(str(row['name'])))
            lists_inst.id.append(deepcopy(str(row['id'])))
            id_name.update({deepcopy(str(row['id'])): deepcopy(str(row['name']))})

        id_name_sorted = OrderedDict(sorted(id_name.items(), key=lambda t: int(t[0])))
        if self.__test_mode == '0':
            print('\nSelect from {}:\n'.format(table))
            for key, value in id_name_sorted.items():
                print('    {} {}'.format(key, value))
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
            return deepcopy(lists_inst.nameSub) if table == 'cases' else lists_inst.nameSub
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
            return deepcopy(lists_inst.name) if table == 'cases' else lists_inst.name
    
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
            return self.get_name_list(table='types') if \
                self.__item_constituents.type_list == [None] else self.__item_constituents.type_list
        elif level == 'cases':
            return self.get_name_list(table='cases') if \
                            self.__item_constituents.case_list == [[None]] else self.__item_constituents.case_list
        elif level == 'configurations':
            return self.get_name_list(table='configurations', computer=computer_of_subject) if \
                self.__item_constituents.configuration_list == [None] else self.__item_constituents.configuration_list
        else:
            message(mode='ERROR', not_supported='level ' + level)

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
        elif operation_type == 's' \
            or operation_type == 'p':   # simulating / plotting (all item constituents (type, case, configuration))
            self.__item_constituents.type_list = self.select_constituent_of_items_to_test(level='types')
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

        processing.number_cpus = self.__gateToDatabase.query_column_entry('types', item_type, 'number_cpus')
        processing.mode = self.__gateToDatabase.query_column_entry('configurations', item_configuration, 'processing')

        sim_data.processing = processing

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
        num_global = sim_data.numerics_global
        num_global_processes = num_global.processes

        num_global_processes.flow = flow_process_name
        num_global_processes.mass_flag = self.__gateToDatabase.query_column_entry(
            'cases', item_case, 'mass_flag')
        num_global_processes.heat_flag = self.__gateToDatabase.query_column_entry(
            'cases', item_case, 'heat_flag')
        num_global_processes.deformation_flag = self.__gateToDatabase.query_column_entry(
            'cases', item_case, 'deformation_flag')
        num_global_processes.fluid_momentum_flag = self.__gateToDatabase.query_column_entry(
            'cases', item_case, 'fluid_momentum_flag')
        num_global_processes.overland_flag = self.__gateToDatabase.query_column_entry(
            'cases', item_case, 'overland_flag')
        num_global.coupled_flag = self.__gateToDatabase.query_column_entry(
            'cases', item_case, 'coupled_flag')
        num_global.non_linear_flag = self.__gateToDatabase.query_column_entry(
            'flow_processes', flow_process_name, 'nonlinear_flag')
        num_global.lumping_flag = self.__gateToDatabase.query_numerics_column_entry(
            item_case, flow_process_name, element_type_name, 'flow_lumping_flag')
        # solver, preconditioner, theta
        self.set_numerics_directories(sim_data, item_case, item_configuration,
                                      flow_process_name, element_type_name, 'flow')
        if num_global_processes.mass_flag:
            self.set_numerics_directories(sim_data, item_case, item_configuration,
                                          flow_process_name, element_type_name, 'mass')
        if num_global_processes.heat_flag:
            self.set_numerics_directories(sim_data, item_case, item_configuration,
                                          flow_process_name, element_type_name, 'heat')
        if num_global_processes.deformation_flag:
            self.set_numerics_directories(sim_data, item_case, item_configuration,
                                          flow_process_name, element_type_name, 'deformation')
        if num_global_processes.fluid_momentum_flag:
            self.set_numerics_directories(sim_data, item_case, item_configuration,
                                          flow_process_name, element_type_name, 'fluid_momentum')
        if num_global_processes.overland_flag:
            self.set_numerics_directories(sim_data, item_case, item_configuration,
                                          flow_process_name, element_type_name, 'overland_flow')

    def set_numerics_directories(self, sim_data, item_case, item_configuration,
                                 flow_process_name, element_type_name, process):
        sim_data.solver_dir[process] = self.convert_numerics_entry_in_cases_table_to_specification(
            item_configuration, self.__gateToDatabase.query_numerics_column_entry(
            item_case, flow_process_name, element_type_name,
                'solver_' + process + '_' + item_configuration.lower()), 'solver')
        sim_data.preconditioner_dir[process] = self.convert_numerics_entry_in_cases_table_to_specification(
            item_configuration, self.__gateToDatabase.query_numerics_column_entry(
                item_case, flow_process_name, element_type_name,
                'preconditioner_' + process + '_' + item_configuration.lower()), 'preconditioner')
        sim_data.theta_dir[process] = self.__gateToDatabase.query_numerics_column_entry(
            item_case, flow_process_name, element_type_name, 'theta_' + process)

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
                    'configurations', item_configuration, numerics_type + '_table_name')
                return self.__gateToDatabase.query_column_entry(solver_table_name, entry, 'specification', 'id')
            else:
                return '-1'
        except Exception as err:
            message(mode='ERROR', text="{}".format(err))

    def item_is_to_test(self, item_case):
        """
        check test_mode, state,
        used for simulation, plotting  operation type (case item exists)
        (all items (i.e. configurations) involved in building operation type)
        :param item_case: (string or None)
        :return: (bool )False: not involved, True: involved or ERROR
        """
        execute_flag = True

        if self.__test_mode == '0':
            # no test mode - select everything by typing on console
            #                and than the items in the loop (in environment run) is involved
            pass
        elif self.__test_mode == '1':
            # via browser
            execute_flag = self.__gateToDatabase.query_column_entry('cases', item_case, 'state')
        elif self.__test_mode == '2':
            # via CI tool
            if not self.__gateToDatabase.query_column_entry('cases', item_case, 'active'):
                execute_flag = False
        else:
            message(mode='ERROR', not_supported=self.__test_mode)  # returns '1'

        return execute_flag  # remote always '1'

    def get_inner_loop_elements(self, item_case):
        """
        set lists with process name and element type
        :param item_case: (string)
        :return:
        """
        if item_case is None:
            flow_process_name_list = [None]
            element_type_name_list = [[None]]
        else:
            flow_process_name_list = self.__gateToDatabase.query_flow_process_name_list(item_case)
            element_type_name_list = self.__gateToDatabase.query_element_type_name_list(
                item_case, flow_process_name_list)

        return flow_process_name_list, element_type_name_list


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

    message(mode='WARNING', text='Conversion failed')
    return None


def select_from_options(option_dict, message_text):
    """
    select by user input from dictionary with options
    recalls itself in case of non-proper user input (for simplicity, it checks only
    if lower-case string is in dictionary)
    :param option_dict: either dictionary {string: string, ...} or OrderedDict([(string, string), ...])
                        key is value to type in to select
    :param message_text: (string) printed with the dictionary keys and values
    to ask user for input, e.g. 'Select option type'
    :return: (one-char string) selected option (=selected key of dictionary)
    """
    while True:
        print('\n ' + message_text + ':')

        for key, option in option_dict.items():
            print('    {}'.format(option))
        option_selected = input('\n')

        if option_selected.lower() in option_dict:
            break
        else:
            message(mode='ERROR', text='Operation type {} does not exist. Try again.'.format(option_selected))

    return str(option_selected)


def string_represents_non_negative_number_or_potentially_valid_character(value):
    """
    check if value is single char 'a' or can be casted to integer and is larger than 0
    displays warning, if this is not the case
    :param value: (string): input to be checked
    :return: True : ok - False : exception
    """
    if value == 'a' or value == 'r':  # for all or range (range in table)
        return True

    try:
        val = int(value)
    except ValueError:
        message(mode='WARNING', text='Not a number')
        return False

    return True if val >= 0 else False

