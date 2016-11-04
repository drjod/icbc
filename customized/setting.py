from utilities import message, select_from_options
from copy import deepcopy
from sys import path as syspath, exc_info
from os import path
from processing import Processing
from numerics import Global, processes
syspath.append(path.join(path.dirname(__file__), '..', 'customized'))
import gateToMySQL


class testing:
    def __init__(self, mode, level):
        self.mode = mode   # 0: no testing , 1: control via browser (case has stage in database), 2: with CI
        self.level = level  # for testing with jenkins - each test case has a level this variable is compared with


class mySQL:
    def __init__(self, user, password, host, schema):
        self.user = user
        self.password = password
        self.host = host
        self.schema = schema


class itemConstituents:
    def __init__(self, type_list, case_list, configuration_list):
        self.type_list = type_list
        self.case_list = case_list
        self.configuration_list = configuration_list


class lists:  # stores lists for member set_names
    def __init__(self):
        self.name = list()     # contains selected names
        self.nameSub = list()  # to generate nested nameList for table cases, which depends on selected type
        self.id = list()       # stores selected ids
        self.items = list()    # entries contain id and name from database
     

class Setting:
    """
    console input
    hosts TestCases lists, gateToMySQL
    operation_preselected, operation_type
    """
    __selectedTypeIdList = list()  # for tree structure (types, cases) - to know selected type when cases are selected

    def __init__(self, type_list, case_list, configuration_list, operation_type,
                 operation_preselected, testing, mySQL_struct):
    
        self.__itemConstituents = itemConstituents(type_list, case_list, configuration_list)
        self.__operation_type = operation_type                           # building or testing
        self.__operation_preselected = operation_preselected             # if specified, operation done only once
        self.__testing = testing  # to switch off select
        self.__mySQL_struct = mySQL_struct
        #self.__gateToMySQL = gateToMySQL.GateToMySQL(mySQL_struct)   
        #message(mode='INFO', text='Connect ' + mySQL_struct.user + ' to '
        # + mySQL_struct.host + ' ' + mySQL_struct.schema )
        
    def __del__(self):
        pass
        # del self.__gateToMySQL
        
    def connect_to_mysql(self):
        message(mode='INFO', text='Connect ' + self.__mySQL_struct.user + ' to database ' + self.__mySQL_struct.host +
                                  ' ' + self.__mySQL_struct.schema)

        self.__gateToMySQL = gateToMySQL.GateToMySQL(self.__mySQL_struct)

    def disconnect_from_mysql(self):
        #message(mode='INFO', text='Disconnecting' )
        del self.__gateToMySQL

    @property
    def itemConstituents(self):
        return self.__itemConstituents

    @property
    def operation_preselected(self):
        return self.__operation_preselected

    def query_location(self, computer_name):
        return self.__gateToMySQL.query_column_entry('computer',
                                                     self.__gateToMySQL.query_id_for_name('computer', computer_name),
                                                     'location')

    def query_operating_system(self, computer_name):
        return self.__gateToMySQL.query_column_entry('computer',
                                                     self.__gateToMySQL.query_id_for_name('computer', computer_name),
                                                     'operating_system')
 
    def query_directory_root(self, computer_name, user_name): 
        return self.__gateToMySQL.query_directory_root(self.__gateToMySQL.query_id_for_name('computer', computer_name),
                                                       self.__gateToMySQL.query_id_for_name('user', user_name))

    def query_hostname(self, computer_name):
        return self.__gateToMySQL.query_column_entry('computer',
                                                     self.__gateToMySQL.query_id_for_name('computer', computer_name),
                                                     'hostname')
    
    def query_user(self, superuser_name, computer_name):
        return self.__gateToMySQL.query_name_for_id('user',
                                                    self.__gateToMySQL.query_id_of_superuser(
                                                        superuser_name, computer_name))
                                                      
    def query_column_for_case(self, case_name, column_name):
        return self.__gateToMySQL.query_column_entry('cases', self.__gateToMySQL.query_id_for_name(
            'cases', case_name), column_name)

    def select_operation_type(self):
        """
        prepare dictionary [building, simulating, plotting] for self.select_from_options() and call it
        :return: ((one-character) string) selected operation type
        """
        if not self.__operation_type:
            operation_type_dict = {'b': '(b)uilding', 's': '(s)imulating', 'p': '(p)lotting'}
            return select_from_options(operation_type_dict, 'Select operation type')

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
        set previously selected entities in subject, self.item, or self.__operation type to None (case_list to [' '])
        used by self.reselect(), which provides the selected option
        :param subject: (Subject)
        :param option_selected: (one-char string)
        :return:
        """
        if option_selected == 'c':  # computer
            subject.computer = None
            subject.user = None  # user must be reselected too
            self.__itemConstituents.configuration_list = [None]  # and also configurations since they depend on computer
        if option_selected == 'o':  # code
            subject.code = None
            subject.branch = None  # branch must be reselected too
        if option_selected == 'b':  # branch
            subject.branch = None
        if option_selected == 't' or str(option_selected) == 'e':  # type | example
            self.__itemConstituents.type_list = [None]
            self.__itemConstituents.case_list = [[None]]  # case must be reselected too
            self.__selectedTypeIdList.clear()
        if option_selected == 'a' or str(option_selected) == 'e':  # case | example
            self.__itemConstituents.case_list = [[None]]
        if option_selected == 'n' or str(option_selected) == 'e':  # configuration | example
            self.__itemConstituents.configuration_list = [None]
        if option_selected == 'p':  # operation type
            self.__operation_type = None

    def set_names(self, table, computer=None):
        """

        :param table: (string) name of table in SQL schema
        :param computer: (string)
        :return:  names (list of strings, nested list if table = 'cases')
        for a table obtained from database and user selection
        """
        lists_inst = lists()

        self.get_items_from_database(table, computer, lists_inst)
        if len(lists_inst.name) > 0:  # for table cases if in table types all or range  was selected
            return lists_inst.name  # know already names, so return them directly
        selected_id = self.select_id(table, lists_inst)
        names = self.id2name(table, selected_id, lists_inst)

        del lists_inst
        return names

    def get_items_from_database(self, table, computer, lists_inst):
        """
        fill lists_inst.items with instances (id, name) from database
        if table cases and more than on type selected, fill lists_inst.name directly
        since select_id for case not required
        class member to have access to __selectedTypeIdList
        :param table:
        :param computer:
        :param lists_inst:
        :return:
        """
        if table == 'cases':  # has sublist for each type (nested list)
            if len(self.__selectedTypeIdList) > 1:  # more than one type was selected
                for typeId in self.__selectedTypeIdList:
                    lists_inst.items = self.__gateToMySQL.query_names_of_id_group(
                        'cases', 'a', selected_type_id=typeId)
                    for row in lists_inst.items:
                        lists_inst.nameSub.append(str(row['name']))
                    lists_inst.name.append(deepcopy(lists_inst.nameSub))
                    # append to name to return this directly (without select_id)
                    lists_inst.nameSub.clear()
            else:  # cases for specific type
                lists_inst.items = self.__gateToMySQL.query_names_of_id_group(
                    'cases', 'a', selected_type_id=self.__selectedTypeIdList[0])
        elif table == 'configurations':  # since it depends on computer
            lists_inst.items = self.__gateToMySQL.query_names_of_id_group(
                'configurations', 'a', self.__gateToMySQL.query_id_for_name('computer', computer))
        else:  # computer, user, ... (anything but cases, configurations - see list in environment constructor)
            lists_inst.items = self.__gateToMySQL.query_names_of_id_group(table, 'a')
       
    def select_id(self, table, lists_inst):
        """
        print options on console
        fill lists_inst.nameSub with names from lists_inst_items
        Requirements:
            items in lists_inst must be set
        :param table:
        :param lists_inst:
        :return:
        """
        if self.__testing.mode == '0':
            # print options
            print('\nSelect from ' + table + ':\n')

        for row in lists_inst.items:
            if self.__testing.mode == '0':
                print('   ' + str(row['id']) + ' ' + str(row['name']))
            lists_inst.nameSub.append(deepcopy(str(row['name'])))
            lists_inst.id.append(deepcopy(str(row['id'])))
 
        if not(self.__testing.mode == '0'):
            # TESTLEVEL: preselect anything but examples (types, cases, configurations)
            # and specify state (for jsp) or level (for CI) in database
            # all examples are selected here and level is checked later on
            selected_id = 'a'
        else:
            print('   a all')
            if table == 'types':  # range only for types supported
                print('   r range')
            # select
            #
            selected_id = input('\n   by typing number: ')

        if table == 'types':  # set self.__selectedTypeIdList
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
        print('\n-----------------------------------------------------------------')
         
        return selected_id

    def id2name(self, table, id_selected, lists_inst):
        """
        Convert id to name (list) and return this as a nested list [['...']]
        class member to have access to __selectedTypeIdList
        :param table:
        :param selected_id:
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
                nameList2 = list()
                nameList2.append(deepcopy(lists_inst.name))
                return nameList2
            else:
                return lists_inst.name

    def check_selected_id(self, table, id_selected):
        """
        looks if a number has been typed in
        no check whether selected item exists
        :param table: (string): name of table in SQL schema
        :param selected_id: (string): input to be checked
        :return: True : ok - False : exception
        """
        if table == 'types' or table == 'cases' or table == 'branches' or table == 'configurations':
            if id_selected == 'a':
                return True  # all selected
        try:
            val = int(id_selected)
        except ValueError:
            message(mode='WARNING', text='That was not a number')
            return False

        return True
    
    def set_constituents_for_item(self, group_type, computer_of_subject=None):
        """
        calls member function selectNames to get item constituents
        if they are not previously selected (i.e. in environment constructor or anywhere in last operations)
        :param group_type:
        :param computer_of_subject:
        :return: list (string) for one item  constituent (meaning: types, cases, configuration)
              nested list if table = 'cases'
        """
        if group_type == 'types':
            if len(self.__itemConstituents.type_list) == 0 or not self.__itemConstituents.type_list[0]:
                return self.set_names(table='types')
            else:
                return self.__itemConstituents.type_list
        elif group_type == 'cases':
            if len(self.__itemConstituents.case_list) == 0 or self.__itemConstituents.case_list[0] == [None]:
                return self.set_names(table='cases')
            else:
                return self.__itemConstituents.case_list
        elif group_type == 'configurations':
            if len(self.__itemConstituents.configuration_list) == 0 \
                    or not self.__itemConstituents.configuration_list[0]:
                return self.set_names(table='configurations', computer=computer_of_subject)
            else:
                return self.__itemConstituents.configuration_list             

    def set_processing_data(self, sim_data, item_type, item_case, item_configuration):
        """

        :param simData:
        :param type:
        :param case:
        :param configuration:
        :return:
        """
        proc = Processing()
        proc.set(self.__gateToMySQL.query_column_entry(
            'types', self.__gateToMySQL.query_id_for_name('types', item_type), 'numberOfCPUs'),
            self.__gateToMySQL.query_column_entry('configurations', self.__gateToMySQL.query_id_for_name(
                'configurations', item_configuration), 'processing'))
        sim_data.setProcessing(proc)
        return sim_data

    def set_numerics_data(self, sim_data, item_type, item_case, item_configuration):
        """
        get mumerics and parallelization data frpm mySQL database
        data are used later on to write *.num *.pbs files
        :param sim_data: SimulationData
        :param item_type:
        :param item_case:
        :param item_configuration:
        :return:
        """
        numerics_global = Global()
        prcs = processes()

        preconditioner = []
        solver = []
        theta = []
        # this prcs is put into numerics_global
        prcs.set(self.__gateToMySQL.query_name_for_id('flow_processes',
                                                            self.__gateToMySQL.query_column_entry('cases',
                                                            self.__gateToMySQL.query_id_for_name('cases', item_case),
                                                            'flow_id')),
                                                        self.__gateToMySQL.query_column_entry('cases',
                                                            self.__gateToMySQL.query_id_for_name('cases', item_case),
                                                            'mass_flag'),
                                                        self.__gateToMySQL.query_column_entry('cases',
                                                            self.__gateToMySQL.query_id_for_name('cases', item_case),
                                                            'heat_flag')) 
        # general numerics data
        numerics_global.set (prcs,
                          self.__gateToMySQL.query_column_entry(
                              'cases', self.__gateToMySQL.query_id_for_name('cases', item_case), 'coupled_flag'),
                          self.__gateToMySQL.query_column_entry(
                              'cases', self.__gateToMySQL.query_id_for_name('cases', item_case), 'lumping_flow'),
                          self.__gateToMySQL.query_column_entry(
                              'cases', self.__gateToMySQL.query_id_for_name('cases', item_case), 'nonlinear_flag'))
        # the data that dependent on process
        column_entry = self.__gateToMySQL.query_column_entry(
            'cases', self.__gateToMySQL.query_id_for_name('cases', item_case), 'solver_flow_' + item_configuration)
        if column_entry != 'None':
            solver.append(self.convert_numerics_entry_of_db_to_specification(
                item_configuration, column_entry, 'solver'))
         
        column_entry = self.__gateToMySQL.query_column_entry(
            'cases', self.__gateToMySQL.query_id_for_name('cases', item_case), 'solver_mass_' + item_configuration)
        if column_entry != 'None':
            solver.append(self.convert_numerics_entry_of_db_to_specification(
                item_configuration, column_entry, 'solver'))

        column_entry =  self.__gateToMySQL.query_column_entry(
            'cases', self.__gateToMySQL.query_id_for_name('cases', item_case), 'solver_heat_' + item_configuration)
        if column_entry != 'None':
            solver.append(self.convert_numerics_entry_of_db_to_specification(
                item_configuration, column_entry, 'solver'))
        
        column_entry = self.__gateToMySQL.query_column_entry(
            'cases', self.__gateToMySQL.query_id_for_name(
                'cases', item_case), 'preconditioner_flow_' + item_configuration)
        if column_entry != 'None':
            preconditioner.append(self.convert_numerics_entry_of_db_to_specification(
                item_configuration, column_entry, 'preconditioner'))
        
        column_entry = self.__gateToMySQL.query_column_entry(
            'cases',self.__gateToMySQL.query_id_for_name(
                'cases', item_case), 'preconditioner_mass_' + item_configuration)
        if column_entry != 'None':
            preconditioner.append(
                self.convert_numerics_entry_of_db_to_specification(item_configuration, column_entry, 'preconditioner'))

        column_entry = self.__gateToMySQL.query_column_entry(
            'cases',self.__gateToMySQL.query_id_for_name(
                'cases', item_case), 'preconditioner_heat_' + item_configuration)
        if column_entry != 'None':
            preconditioner.append(self.convert_numerics_entry_of_db_to_specification(item_configuration,
                                                                                     column_entry, 'preconditioner'))

        column_entry = self.__gateToMySQL.query_column_entry(
            'cases', self.__gateToMySQL.query_id_for_name('cases', item_case), 'theta_flow')
        if column_entry != 'None':
            theta.append(column_entry)

        column_entry = self.__gateToMySQL.query_column_entry(
            'cases', self.__gateToMySQL.query_id_for_name('cases', item_case), 'theta_mass')
        if column_entry != 'None':
            theta.append(column_entry)

        column_entry = self.__gateToMySQL.query_column_entry(
            'cases', self.__gateToMySQL.query_id_for_name('cases', item_case), 'theta_heat')
        if column_entry != 'None':
            theta.append(column_entry)

        # store data in simulationData.simData() - local in environment.run()
        sim_data.setNum(numerics_global, solver, preconditioner, theta)

        return sim_data

    def convert_numerics_entry_of_db_to_specification(self, item_configuration, entry, numerics_type):
        """
        :param configuration:
        :param entry:
        :param numerics_type: 'solver' or 'preconditioner'
        :return:
        """
        value = ''
        try:
            if entry != 'null':
                solverTableName = self.__gateToMySQL.query_column_entry(
                    'configurations', self.__gateToMySQL.query_id_for_name('configurations', item_configuration),
                    numerics_type + '_table_name')
                return self.__gateToMySQL.query_column_entry(solverTableName, entry, 'specification')
            else:
                return '-1'
        except:
            message(mode='ERROR', text='%s' % exc_info()[0])

    def set_lists_for_items(self, operation_type, operation, computer):
        """
        generate examples Lists to loop over in Environment run
        :param operation_type:
        :param operation:
        :param computer:
        :return:
        """
        if operation_type == 'b':  # building (only configuration)
            self.__itemConstituents.type_list = [None]
            self.__itemConstituents.case_list = [None]
            self.__itemConstituents.configuration_list = self.set_constituents_for_item(
                group_type='configurations', computer_of_subject=computer)
        elif operation_type == 's':  # simulating (all item constituents (type, case, configuration))
            self.__itemConstituents.type_list =  self.set_constituents_for_item(group_type='types')
            self.__itemConstituents.case_list = self.set_constituents_for_item(group_type='cases')
            self.__itemConstituents.configuration_list = self.set_constituents_for_item(
                group_type='configurations', computer_of_subject=computer)
        elif operation_type == 'p':  # plotting
            self.__itemConstituents.type_list = self.set_constituents_for_item(group_type='types')
            if operation == 'j' or operation == 'w': # generate or wait for JPG (only type)
                self.__itemConstituents.case_list = [None]
                self.__itemConstituents.case_list = [None]
            else:  # all item constituents  (type, case, configuration)
                self.__itemConstituents.case_list = self.set_constituents_for_item(group_type='cases')
                self.__itemConstituents.case_list = self.set_constituents_for_item(
                    group_type='configurations', computer_of_subject=computer)


def get_list_id(selected_id, id_list):
    """
    Convert from global id to local id
    :param selected_id:
    :param id_list:
    :return:
    """
    i = 0
    for idInst in id_list:
        if not (idInst == selected_id):
            i += 1
        else:
            break
    return i
