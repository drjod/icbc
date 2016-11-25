from sys import path as syspath, argv
from os import path
syspath.append(path.join(path.dirname(__file__), '..', 'shared'))
import environment
from configurationCustomized import location
from platform import node, system
from utilities import message

message(mode='INFO', text='On {} {} {}'.format(location, node(), system()))

environment = environment.Environment(computer=argv[1],
                                      user=argv[2],
                                      code=argv[3],
                                      branch=argv[4],
									  id_local_process=argv[5],
                                      type_list=[argv[6]],
                                      case_list=[[argv[7]]],
                                      configuration_list=[argv[8]],
									  flow_process_list=[argv[9]],
									  element_type_list=[[argv[10]]],
                                      operation_type=argv[11],
                                      operation=argv[12],
                                      db_user=str(),
                                      db_password=str(),
                                      db_host=str(),
                                      db_schema=str())
                  
environment.run()
