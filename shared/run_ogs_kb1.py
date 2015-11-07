import environment
import os, sys, glob
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pwds'))
mod = __import__( 'mysql2' )

environment = environment.Environment(computer='amak', code='ogs', branch = 'ogs_kb1', user = 'delfs', mySQL_password = mod.pwd )
environment.run()





 




