from utilities import message, select_from_options
from copy import deepcopy
from sys import path as syspath, exc_info
from os import path
from processing import Processing
from numerics import Global, Processes


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
        self.id_name_pair = list()  # for data base access - each entry contains an id and nam
        #                             as a dictionar {'id': ..., 'name':} obtained from databa


class Setting:
    """
    console input
    hosts TestCases lists, gateToMySQL
    operation, operation_type
    """
    __selectedTypeIdList = list()  # for tree structure (types, cases) - to know selected type when cases are selected

    def __init__(self, type_list, case_list, configuration_list, operation_type,
                 operation, test_mode, db_inst):
    
        self.__item_constituents = ItemConstituents(type_list, case_list, configuration_list)
        self.__operation_type = operation_type  # building or testing
        self.__operation = operation
        self.__test_mode = test_mode  # to switch off select
        self.__db_inst = db_inst
        self.__gateToMySQL = None
        
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
                message(mode='INFO', text='Set type ' + self.__item_constituents.type_list[i])
        if self.__item_constituents.case_list[0][0]:
            for i in range(0, len(self.__item_constituents.case_list)):
                for j in range(0, len(self.__item_constituents.case_list[i])):
                    message(mode='INFO', text='Set case ' + self.__item_constituents.case_list[i][j])
        if self.__item_constituents.configuration_list[0]:
            for i in range(0, len(self.__item_constituents.configuration_list)):
                message(mode='INFO', text='Set configuration ' + self.__item_constituents.configuration_list[i])

        if self.__operation_type:
            message(mode='INFO', text='Set operation type ' + self.__operation_type)
        if self.__operation:
            message(mode='INFO', text='Set operation ' + self.__operation)

    def connect_to_mysql(self):
        pass

    def disconnect_from_mysql(self):
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

    @property
    def test_mode(self):
        return self.__test_mode

    def query_location(self, computer_name):
        pass

    def query_operating_system(self, computer_name):
        pass
 
    def query_directory_root(self, computer_name, user_name):
        pass

    def query_hostname(self, computer_name):
        pass
    
    def query_username(self, superuser_name, computer_name):
        pass
                                                      
    def query_column_entry_for_name(self, table, case_name, column_name):
        pass

    def select_operation_type(self):
        return self.__operation_type

    def reselect(self, subject):
        pass

    def neutralize_previous_selections(self, subject, option_selected):
        pass

    def get_name_list(self, table, computer=None):
        pass

    def get_table_data_from_database(self, table, computer, lists_inst):
        pass
       
    def select_id(self, table, lists_inst):
        pass

    def id2name(self, table, id_selected, lists_inst):
        pass    

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
            if len(self.__item_constituents.type_list) == 0 or not self.__item_constituents.type_list[0]:
                return self.get_name_list(table='types')
            else:
                return self.__item_constituents.type_list
        elif level == 'cases':
            if len(self.__item_constituents.case_list) == 0 or self.__item_constituents.case_list[0] == [None]:
                return self.get_name_list(table='cases')
            else:
                return self.__item_constituents.case_list
        elif level == 'configurations':
            if len(self.__item_constituents.configuration_list) == 0 \
                    or not self.__item_constituents.configuration_list[0]:
                return self.get_name_list(table='configurations', computer=computer_of_subject)
            else:
                return self.__item_constituents.configuration_list 		

    def set_processing_data(self, sim_data, item_type, item_configuration):
        pass

    def set_numerics_data(self, sim_data, item_case, item_configuration):
        pass

    def convert_numerics_entry_of_db_to_specification(self, item_configuration, entry, numerics_type):
        pass

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


def get_list_id(selected_id, id_list):
    pass