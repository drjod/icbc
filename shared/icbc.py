from environment import Environment
from os import path
from sys import path as syspath
syspath.append(path.join(path.dirname(__file__), '..', 'pwds'))
mod = __import__('mysql2')

#################################################################
#  icbc 0.2 by JOD
#  
#  Requirements:
#     Put password files in folder ..\pwds 
#     (each password in separate file)
#     Password for mySQL:
#         in ..\pwds\mysql2.py write pwd = '*****'
#     Password for rzcluster
#         in ..\pwds\rzcluster.py write pwd = '*****'
#     etc.

environment = Environment(superuser='jens',
                          code='ogs',
                          mysql_password=mod.pwd)
environment.run()
