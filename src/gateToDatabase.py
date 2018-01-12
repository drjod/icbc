from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from shared import message


class GateToDatabase:
    """
    fetch entries from SQL database tables
    """
    def __init__(self, db_inst):

        try:
            # connect to database
            engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
                db_inst.user, db_inst.password, db_inst.host, db_inst.schema))
            base = automap_base()
            base.prepare(engine, reflect=True)

            self.__metadata = MetaData()
            self.__metadata.bind = engine

            self.__session = Session(engine)

        except Exception as err:
            message(mode='ERROR', text='{}'.format(err))

        # self.__superusers_table = base.classes.superusers  # id, name, computer_id, user_id
        # self.__users_table = base.classes.users  # id, name
        # self.__computer_table = base.classes.computer  # id, name, operating_system, remote_flag, hostname,
        # root_directory,
        # self.__modi_table = base.classes.modi  # id, computer_id, configuration_id
        # self.__codes_table = base.classes.codes  # id, name
        # self.__branches_table = base.classes.branches  # id, name

        # self.__examples_table = base.classes.examples  # id, type_id, case_id
        # self.__types_table = base.classes.types  # id, name, number_cpus
        # self.__cases_table = base.classes.cases  # id, name, mass_flag, heat_flag, coupled_flag,
        # deformation_flag, overland_flag, fluid_momentum_flag, active
        # self.__configurations_table = base.classes.configurations  # id, name, processing,
        # preconditioner_table_name, solver_table_name

        # self.__flow_processes_table = base.classes.flow_processes  # id, name, nonlinear_flag, active
        # self.__element_types_table = base.classes.element_types  # id, name, active

        # self.__numerics_table = base.classes.numerics  # id, case_id, flow_process_id, element_type_id,
        # theta_[flow, mass, heat], solver_[flow, mass_heat][OGS_FEM, ...],
        # preconditioner_[flow, mass_heat][OGS_FEM, ...]
        # self.__solver_table = base.classes.solver  # id, name, specification
        # self.__solver_mkl_table = base.classes.solver_mkl  # id, name, specification
        # self.__solver_petsc_table = base.classes.solver_petsc  # id, name, specification
        # self.__preconditioner_table = base.classes.preconditioner  # id, name, specification
        # self.__preconditioner_mkl_table = base.classes.preconditioner_mkl  # id, name, specification
        # self.__preconditioner_petsc_table = base.classes.preconditioner_petsc  # id, name, specification

    def __del__(self):
        message(mode='INFO', text='Disconnect from database')
        # close database
        #self.__cnx.close()

    def query_column_entry(self, table, entry, column, variable='name'):
        """

        :param table: (string)
        :param name: (string)
        :param column: (string)
        :return:
        """
        if variable == 'name':
            table_row = self.__session.query(
                Table(table, self.__metadata, autoload=True)).filter_by(name=entry).first()
        elif variable == 'id':
            table_row = self.__session.query(
                Table(table, self.__metadata, autoload=True)).filter_by(id=entry).first()
        else:
            message('error', 'variable {} not supported'.format(variable))
        return getattr(table_row, column)

    def query_numerics_column_entry(self, case_name, flow_process_name, element_type_name, column):
        """

        :param table: (string)
        :param name: (string)
        :param column: (string)
        :return:
        """
        query = self.__session.query(Table("numerics", self.__metadata, autoload=True)).join(
            Table("cases", self.__metadata, autoload=True)).filter_by(name=case_name).join(
            Table("flow_processes", self.__metadata, autoload=True)).filter_by(name=flow_process_name).join(
            Table("element_types", self.__metadata, autoload=True)).filter_by(name=element_type_name)

        return getattr(query.first(), column)

    def query_flow_process_name_list(self, case_name):
        """

        :param case_name: (string)
        :return: (string list)
        """
        numerics = self.__session.query(Table('numerics', self.__metadata, autoload=True)).join(
            Table('cases', self.__metadata, autoload=True)).filter_by(name=case_name).all()

        flow_processes = [self.__session.query(Table('flow_processes', self.__metadata, autoload=True)).filter_by(
            id=numerics_item.flow_process_id).first() for numerics_item in numerics]

        flow_process_names = [flow_process.name for flow_process in flow_processes]
        flow_process_names = list(set(flow_process_names))  # remove non-unique items

        if not flow_process_names:
            message('WARNING', 'No flow process found in database')

        return flow_process_names

    def query_element_type_name_list(self, case_name, flow_process_name_list):
        """

        :param case_name: (string)
        :param flow_process_name_list: (list of strings)
        :return: nested list of strings [[], []]
        """
        name_nested_list = list()

        query = self.__session.query(Table('cases', self.__metadata, autoload=True)).filter_by(name=case_name)
        if query.count() == 1:
            case = query.first()
            numerics = self.__session.query(
                Table('numerics', self.__metadata, autoload=True)).filter_by(case_id=case.id)
        else:
            message('WARNING', 'No unique entry found in table cases with name {}'.format(case_name))
            return None

        for flow_process_name in flow_process_name_list:
            inner_list = list()
            query = self.__session.query(Table('flow_processes', self.__metadata, autoload=True)).filter_by(
                name=flow_process_name)
            if query.count() == 1:
                flow_process = query.first()

                numerics_for_flow_process = numerics.filter_by(flow_process_id=flow_process.id).all()
                for item in numerics_for_flow_process:
                    query = self.__session.query(Table('element_types', self.__metadata, autoload=True)).filter_by(
                        id=item.element_type_id)
                    if query.count() == 1:
                        inner_list.append(query.first().name)
                    else:
                        message('WARNING', 'No unique entry found in table element_type with id {}'.format(
                            item.element_type_id))
                        return None
            else:
                message('WARNING', 'No unique entry found in table flow_processes with name {}'.format(
                    flow_process_name))
                return None

            name_nested_list.append(inner_list)

        if not name_nested_list:  # empty list
            message('WARNING', 'No element_type found in database')

        return name_nested_list

    def query_username(self, superuser_name, computer_name):
        """
        query a username for a given superuser and computer_name
            by first querying user id from superuser table
        :param superuser_name: (string)
        :param computer_name: (string)
        :return: (string ) username
        """
        query = self.__session.query(Table('users', self.__metadata, autoload=True)).join(
            Table('superusers', self.__metadata, autoload=True)).filter_by(name=superuser_name).join(
            Table('computer', self.__metadata, autoload=True)).filter_by(name=computer_name)

        return query.first().name

    def query_id_name_pair_list(self, table, item_id, computer_name='-', selected_type_id='-1'):
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
        :param computer_name: (string) for option 3
        :param selected_type_id: (string) for option 4
        :return: list of dictionaries {'id': (string), 'name' (string)} (order might change)
                  - None if exception
        """
        # query = self.__session.query(Table('computer', self.__metadata, autoload=True)).filter_by(name=computer_name)
        # if query.count() == 1:
        #     computer_id = query.first().id

        if item_id == 'a':
            if table == 'computer' or table == 'users' or table == 'codes' or table == 'branches' or table == 'types':
                query = self.__session.query(Table(table, self.__metadata, autoload=True)).all()
                result = [{'id': item.id, 'name': item.name} for item in query]
            elif table == 'cases':  # specific type selected
                query = self.__session.query(Table('examples', self.__metadata, autoload=True)).filter_by(
                    type_id=selected_type_id).all()
                cases_id = [item.case_id for item in query]
                query = self.__session.query(Table('cases', self.__metadata, autoload=True)).all()
                result = [{'id': item.id, 'name': item.name} for item in query if item.id in cases_id]
            elif table == 'configurations':  # depends on selected computer
                query = self.__session.query(Table('modi', self.__metadata, autoload=True)).join(
                    Table('computer', self.__metadata, autoload=True)).filter_by(name=computer_name)

                configurations_id = [item.configuration_id for item in query]
                query = self.__session.query(Table('configurations', self.__metadata, autoload=True)).all()
                result = [{'id': item.id, 'name': item.name} for item in query if item.id in configurations_id]
            else:
                message(mode='ERROR', notSupported=table)
                return None  # exception
        else:
            # self.query("SELECT * FROM ' + table + ' WHERE id={}".format(item_id))
            message('WARNING', 'item_id has to be a (all)')
            return None  # exception

        return result
