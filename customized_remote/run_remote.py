from sys import path as syspath, argv
from os import path
syspath.append(path.join(path.dirname(__file__), '..', 'shared'))
import environment
from configurationCustomized import location
from platform import node, system
from utilities import message

message(mode='INFO', text='On ' + location + ' ' + node() + ' ' + system())

environment = environment.Environment(computer = argv[1],
                                      user = argv[2],
                                      code = argv[3],
                                      branch = argv[4],
									  id_local_process = argv[5],
                                      type_list= [argv[6]],
                                      case_list= [[argv[7]]],
                                      configuration_list= [argv[8]],
                                      operation_type= argv[9],
                                      operation = argv[10],
                                      mysql_user = str(),
                                      mysql_password = str(),
                                      mysql_host = str(),
                                      mysql_schema = str())
                  
environment.run()
