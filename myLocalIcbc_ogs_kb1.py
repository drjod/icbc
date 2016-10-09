import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'pwds'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))
import environment
mod = __import__( 'mysql2' )

environment = environment.Environment(superuser = 'jens', computer='amak', code='ogs', branch = 'ogs_kb1', mySQL_password = mod.pwd )
environment.run()





 




