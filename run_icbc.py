from os import path
from sys import version, version_info, path as syspath
if not path.join(path.dirname(__file__), 'access') in syspath:
    syspath.append(path.join(path.dirname(__file__), 'access'))
if not path.join(path.dirname(__file__), 'src') in syspath:
    syspath.append(path.join(path.dirname(__file__), 'src'))
from environment import Environment
from shared import message

"""
START icbc

  Requirements:
     Put password files in folder ..\access
     (each password in separate file)
     Password for database:
         in ..\access\database.py write pwd = '*****'
     Password for rzcluster
         in ..\access\rzcluster.py write pwd = '*****'
"""


mod = __import__('database')
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
