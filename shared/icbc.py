from environment import Environment
from os import path
from utilities import message
from sys import version, version_info, path as syspath
syspath.append(path.join(path.dirname(__file__), '..', 'pwds'))
mod = __import__('database')

#################################################################
#  icbc 0.2 by JOD
#  
#  Requirements:
#     Put password files in folder ..\pwds 
#     (each password in separate file)
#     Password for database:
#         in ..\pwds\database.py write pwd = '*****'
#     Password for rzcluster
#         in ..\pwds\rzcluster.py write pwd = '*****'
#

message(mode="INFO", text="Running python {}".format(version))
if version_info < (3, 5):
    message(mode="WARNING", text="Python 3.5 required")

environment = Environment(superuser='jens',
                          code='ogs',
                          db_password=mod.pwd,
                          # computer='amak',
                          branch='ogs_kb1',
                          #operation_type='s',
                          #operation='r',
                          #type_list=["2D_xy_balancing_LIQUID"],
                          # case_list=[["advection_quad_xy_LIQUID"]],
                          # configuration_list=["OGS_FEM"]
                          )


environment.run()
