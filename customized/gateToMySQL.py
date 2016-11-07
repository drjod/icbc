import mysql.connector
from mysql.connector import errorcode
from utilities import message


class GateToMySQL:
    """
    fetch entries from SQL database tables
    """
    def __init__(self, mysql_inst):
        # connect to database
        self.__cnx = get_connection(mysql_inst)

    def __del__(self):
        # close data base
        self.__cnx.close()
               
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
                         
        cursor = self.__cnx.cursor(buffered=True)
        query(cursor, "SELECT * FROM " + table + " WHERE id=" + str(item_id))
        row = cursor.fetchone()
        if row is not None:
            return str(row[1])
        else:
            message(mode='ERROR', text='Name for id ' + str(item_id) + ' not found in table ' + str(table))
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
            return ''  # no name given get_table_data_from_database
        else:    
            cursor = self.__cnx.cursor(buffered=True)
            query(cursor,"SELECT t.id FROM " + table + " t WHERE t.name='" + str(name) + "'")
            row = cursor.fetchone()
            if row is not None:
                return str(row[0])
            else:
                message(mode='ERROR', text='Column id for ' + str(name) + ' not found in table ' + str(table))
                return '-1'  # exception
                       
    def query_id_name_pair_list(self, table, item_id, computer_id='-1', selected_type_id='-1'):
        """
        query list of rows from table and extract id-name pairs as dictionaries of form {'id': ..., 'name' ...}
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
        :return: list of dictionaries {'id': ..., 'name' ...} - '-1' if table not supported (exception)
        """
        # set cursor       
        cursor = self.__cnx.cursor(buffered=True) 
        if item_id == 'a':
            if table == 'computer' or table == 'user' or table == 'codes' or table == 'branches' or table == 'types':
                query(cursor, 'SELECT * FROM ' + table)
            elif table == 'cases':  # specific type selected
                query(cursor, "SELECT c.* FROM examples e, cases c WHERE e.case_id = c.id and e.type_id=" +
                      selected_type_id)
            elif table == 'configurations':  # depends on selected computer
                query(cursor,
                      "SELECT c.* FROM modi m, configurations c WHERE m.configuration_id = c.id and m.computer_id=" +
                      computer_id)
            else:
                message(mode='ERROR', notSupported=table)
                return '-1'  # exception
        else:    
            cursor.execute("SELECT * FROM ' + table + ' WHERE id=" + str(item_id))

        return extract_id_name_pairs(cursor)

    def query_column_entry(self, table, item_id, column_name):
        """
        query a column entry from a table for a given id
        :param table: (string): name of table in SQL schema
        :param item_id: (string): entry in id column (primary key)
        :param column_name: (string) name of column where entry is searched from
        :return: (string) column entry, '-1' if no entry found (exception)
        """
        # set cursor
        cursor = self.__cnx.cursor(buffered=True) 
        query(cursor, "SELECT t." + column_name + " FROM " + table + " t WHERE t.id=" + str(item_id))
        row = cursor.fetchone()
        if not row:
            message(mode='ERROR', text='Column entry of ' +
                                       str(column_name) + ' not found for id ' + str(item_id))
            return '-1'  # exception
        else:
            return str(row[0])

    def query_directory_root(self, computer_id, user_id):
        """
        query a root directory from the paths table for a given computer and user id
        :param computer_id: (string)
        :param user_id: (string)
        :return: (string) root directory; '-1' if no root directory found (exception)
        """
        # set cursor
        cursor = self.__cnx.cursor(buffered=True) 
        query(cursor, "SELECT p.root FROM paths p WHERE p.computer_id=" +
              str(computer_id) + " AND p.user_id=" + str(user_id))
        row = cursor.fetchone()
        if not row:
            message(mode='ERROR', text='Path not found for computer id ' +
                                       str(computer_id) + ' - user id ' + str(user_id))
            return '-1'  # exception
        else:
            return str(row[0])

    def query_userid(self, superuser_name, computer_name):
        """
        query a user id from superuser table for a superuser and computer name
        :param superuser_name: (string)
        :param computer_name: (string)
        :return: (string) user id; '-1' if no user id found (exception)
        """
        # set cursor
        cursor = self.__cnx.cursor(buffered=True) 
        query(cursor, "SELECT s.user_id FROM superuser s WHERE s.name='" + str(superuser_name) +
              "' AND s.computer_id=" + self.query_id_for_name('computer', computer_name))
        #  
        row = cursor.fetchone()
        if not row:
            message(mode='ERROR', text='User id not found for superuser ' +
                                       str(superuser_name) + ' on ' + str(computer_name))
            return '-1'  # exception
        else:
            return str(row[0])


def extract_id_name_pairs(cursor):
    """
    extract dictionaries with id-name pairs from cursor
    :param cursor:
    :return: list of dictionaries with 'id-name pairs
    """
    id_name_pair_list = list()
    row = cursor.fetchone()

    while row is not None:
        id_name_pair = {
            'id': row[0],
            'name': row[1]
        }
        id_name_pair_list.append(id_name_pair)
        row = cursor.fetchone()

    return id_name_pair_list


def query(cursor, query_text):
    try:
        cursor.execute(query_text)
    except Exception as e:
        message(mode='ERROR', text="*****")


def get_connection(mysql_inst):
    """
    connect to database
    exit with error message if connection fails
    :param mysql_inst:
    :return: database connection
    """
    try:
        db_connection = mysql.connector.connect(user=mysql_inst.user, password=mysql_inst.password,
                                                host=mysql_inst.host, database=mysql_inst.schema)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            message(mode='ERROR', text='User name or password wrong')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            message(mode='ERROR', text='Database does not exist')
        else:
            message(mode='ERROR', text=err)
        exit(1)
    else:
        return db_connection
