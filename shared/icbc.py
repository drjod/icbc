import environment
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pwds'))
mod = __import__( 'mysql2' )


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



      
environment = environment.Environment( superuser = 'jens',  
                                       code = 'ogs', 
                                       mySQL_password = mod.pwd )
environment.run()

 




