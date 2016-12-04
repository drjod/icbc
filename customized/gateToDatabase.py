import psycopg2
import psycopg2.extras
from utilities import message


class GateToDatabase:
    """
    fetch entries from SQL database tables
    """
    def __init__(self, db_inst):
        # connect to database
        self.__cnx = get_connection(db_inst)

    def __del__(self):
        # close database
        self.__cnx.close()

    def query_id_from_numerics_table(self, case_name, flow_process_name, element_type_name):
        """

        :param case_name:
        :param flow_process_name:
        :param element_type_name:
        :return:
        """
        case_id = self.query_id_for_name("cases", case_name)
        flow_process_id = self.query_id_for_name("flow_processes", flow_process_name)
        element_type_id = self.query_id_for_name("element_types", element_type_name)
        query_text = "SELECT id from numerics WHERE case_id={} AND flow_process_id={} AND element_type_id={}".format(
            case_id, flow_process_id, element_type_id)
        row_list = self.query(query_text)

        if not row_list[0]:
            message(mode='ERROR', text='Could not find id from numerics table for {} and {}'.format(
                flow_process_name, element_type_name))
            return '-1'  # exception
        else:
            return str(row_list[0]['id'])

    def query_name_for_id(self, table, item_id):
        """
        query a name from a table for a given id
        requirement:
            name must be in 2nd colum in SQL table
        :param table: (string): name of table in SQL schema
        :param item_id: (string): id where name is searched to
        :return: name (string) or '-1' if no name found (exception)
        """
        if item_id == 'a': 
            return 'all ' + table  # console output

        query_text = "SELECT * FROM {} WHERE id={}".format(table, item_id)
        row_list = self.query(query_text)
        if row_list[0] is not None:
            return str(row_list[0]['name'])
            # each row_list entry is dictionary {..., 'id': (string), 'name' (string), ...}
        else:
            message(mode='ERROR', text='Name for id {} not found in table {}'.format(item_id, table))
            return '-1'  # exception
            
    def query_id_for_name(self, table, name):
        """
        query an id from a table for a given name
        requirement:
            table columns must be: id, name, ...
            name must be unique in table (not checked)
        :param table: (string): name of table in SQL schema
        :param name: (string): entry in column name
        :return: id (string) or '-1' if no id found (exception)
        """
        if not name:   # empty string
            return None  # no name given get_table_data_from_database
        else:
            # query_text = "SELECT {} FROM computer WHERE name=%s"
            # .format(table, name)
            # .encode(encoding='UTF-8', errors='strict')
            # query_text2 = query_text.decode(encoding='UTF-8', errors='strict')
            # .format(table, name)
            # row_list = self.query("SELECT id FROM " + str(table) + " WHERE name=%s", [name])
            query_text = "SELECT id from {} WHERE name='{}'".format(table, name)
            row_list = self.query(query_text)
            if row_list[0] is not None:
                return str(row_list[0]['id'])  # each row_list entry is dictionary {'id': (string)}
            else:
                message(mode='ERROR', text='Column id for {} not found in table {}'.format(name, table))
                return '-1'  # exception
                       
    def query_id_name_pair_list(self, table, item_id, computer_id='-1', selected_type_id='-1'):
        """
        query list of rows from table and extract id-name pairs as dictionaries of form {..., 'id': ..., 'name' ...}
        each list entry is a dictionary
        options:
            1. all
            2. for specific id
            3. configurations for specific computer
            4. cases for specific example type
        requirement:
            if all cases requested, running_type_id must be given
        :param table: (string): name of table in SQL schema
        :param item_id: (string) entry in id column (primary key) (e.g. option 2.)
        :param computer_id: (string) for option 3
        :param selected_type_id: (string) for option 4
        :return: list of dictionaries {'id': (string), 'name' (string)} (order might change)
                  - '-1' if table not supported (exception)
        """
        if item_id == 'a':
            if table == 'computer' or table == 'users' or table == 'codes' or table == 'branches' or table == 'types':
                row_list = self.query("SELECT * FROM {}".format(table))
            elif table == 'cases':  # specific type selected
                query_text = "SELECT c.* FROM examples e, cases c WHERE e.case_id = c.id and e.type_id={}".format(
                    selected_type_id)
                row_list = self.query(query_text)
            elif table == 'configurations':  # depends on selected computer
                query_text = "SELECT c.* FROM modi m, configurations c " +\
                             "WHERE m.configuration_id = c.id and m.computer_id={}".format(computer_id)
                row_list = self.query(query_text)
            else:
                message(mode='ERROR', notSupported=table)
                return '-1'  # exception
        else:
            self.query("SELECT * FROM ' + table + ' WHERE id={}".format(item_id))

        return row_list
        # return extract_id_name_pairs(row_list)

    def query_column_entry(self, table, item_id, column_name):
        """
        query a column entry from a table for a given id
        :param table: (string): name of table in SQL schema
        :param item_id: (string): entry in id column (primary key)
        :param column_name: (string) name of column where entry is searched from
        :return: (string) column entry, '-1' if no entry found (exception)
        """
        row_list = self.query("SELECT {} FROM {} WHERE id={}".format(column_name, table, item_id))
        if not row_list[0]:
            message(mode='ERROR', text='Column entry of {} not found for id {}'.format(column_name, item_id))
            return '-1'  # exception
        else:
            return str(row_list[0][column_name])

    def query_ids_from_column_entries(self, table, column_name, entry):
        """
        ...
        :param table: (string): name of table in SQL schema
        :param item_id: (string): entry in id column (primary key)
        :param column_name: (string) name of column where entry is searched from
        :param entry: (string)
        :return: (string) column entry, '-1' if no entry found (exception)
        """
        result_list = list()
        row_list = self.query("SELECT t.id FROM {} t WHERE t.{}={}".format(table, column_name, entry))
        try:
            a = row_list[0]
        except:
            message(mode='ERROR', text='Column entry {} of {} not found'.format(entry, column_name))
            return '-1'  # exception
        else:
            i = 0
            while True:
                try:
                    a = row_list[i]
                except:
                    break
                else:
                    result_list.append(row_list[i]['id'])
                    i += 1
            return result_list

    def query_directory_root(self, computer_id, user_id):
        """
        query a root directory from the paths table for a given computer and user id
        :param computer_id: (string)
        :param user_id: (string)
        :return: (string) root directory; '-1' if no root directory found (exception)
        """
        query_text = "SELECT p.root FROM paths p WHERE p.computer_id={} AND p.user_id={}".format(computer_id, user_id)
        row_list = self.query(query_text)
        if not row_list[0]:
            message(mode='ERROR', text='Path not found for computer id {} - user id {}'.format(computer_id, user_id))
            return '-1'  # exception
        else:
            return str(row_list[0]['root'])

    def query_userid(self, superuser_name, computer_name):
        """
        query a user id from superuser table for a superuser and computer name
        :param superuser_name: (string)
        :param computer_name: (string)
        :return: (string) user id; '-1' if no user id found (exception)
        """
        query_text = "SELECT s.user_id FROM superusers s WHERE s.name='{}' AND s.computer_id={}".format(
            superuser_name, self.query_id_for_name('computer', computer_name))
        row_list = self.query(query_text)
        if not row_list[0]:
            message(mode='ERROR', text='User id not found for superuser {} on {}'.format(superuser_name, computer_name))
            return '-1'  # exception
        else:
            return str(row_list[0]['user_id'])

    def query(self, query_text, parameter_list=[]):
        """
        make db query for a given text
        :param query_text: (string)
        :param parameter_list: (string list)
        :return: list of dictionary with query results, [None] if exception
        """
        try:
            with self.__cnx.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                if len(parameter_list) > 0:
                    cursor.execute(query_text, parameter_list)
                else:
                    cursor.execute(query_text)
                return cursor.fetchall()
        except Exception as err:
            message(mode='ERROR', text="{}".format(err))
            return [None]


def get_connection(db_inst):
    """
    connect to database
    exit with error message if connection fails
    :param db_inst:
    :return: database connection
    """
    try:
        # db_connection = pymysql.connect(user=db_inst.user, password=db_inst.password,
        #                                 host=db_inst.host, db=db_inst.schema,
        #                                 cursorclass=pymysql.cursors.DictCursor)

        db_connection = psycopg2.connect(user=db_inst.user, password=db_inst.password,
                                         host=db_inst.host, dbname=db_inst.schema)

    except Exception as err:
        message(mode='ERROR', text="{}".format(err))
        exit(1)
    else:
        return db_connection


# def extract_id_name_pairs(row_list):
#     """
#     extract dictionaries with id-name pairs from cursor
#     :param row_list: each list entry is dictionary {'id': (string), 'name': (string),}
#     :return: list of dictionaries with 'id-name pairs
#     """
#     id_name_pair_list = list()
#     for row in row_list:
#         id_name_pair = {
#             'id': row['id'],
#             'name': row['name']
#         }
#         id_name_pair_list.append(id_name_pair)
#     return id_name_pair_list