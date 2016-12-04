from os import path
from sys import version, version_info, path as syspath
syspath.append(path.join(path.dirname(__file__), 'access'))
syspath.append(path.join(path.dirname(__file__), 'shared'))
from environment import Environment
from utilities import message

mod = __import__('database')


#################################################################
#  icbc 0.2 by JOD
#  
#  Requirements:
#     Put password files in folder ..\access
#     (each password in separate file)
#     Password for database:
#         in ..\access\database.py write pwd = '*****'
#     Password for rzcluster
#         in ..\access\rzcluster.py write pwd = '*****'
#

message(mode="INFO", text="Running python {}".format(version))
if version_info < (3, 5):
    message(mode="WARNING", text="Python 3.5 required")

environment = Environment(superuser='jens',
                          db_user=mod.user,
                          db_password=mod.pwd,
                          computer='ibiza',
                          code='ogs',
                          branch='ogs_kb1')


environment.run()
