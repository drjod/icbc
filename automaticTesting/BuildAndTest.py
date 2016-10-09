import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pwds'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
import environment

mod = __import__( 'mysql2' )
 

_superuser='jens'
_computer=str(sys.argv[1])
_operatingSystem=str(sys.argv[2])
_code=str(sys.argv[3])
_branch=str(sys.argv[4])


operationTypeList = ['building', 'simulating']  #, 'plotting']  

operationList = [['clear','build','wait'], ['clear','run',]] # 'wait', 'pack'], ['clear','get','preplot','jpg','wait']]  
         

i=0
for _operationType in operationTypeList:

    print ('\n----------------------------------------------------------------------')
    print ('--------------------------------------------(oo)----------------------')
    print ( _operationType )
    print ('----------------------------------------------------------------------\n')


    for _operation in operationList[i]:


        print ('\n----------------------(^^)-------------')
        print (_operationType + ' - ' +  _operation + '\n' )

        object = environment.Environment(superuser = _superuser, computer=_computer, code=_code, branch = _branch, 
                                         operationType = _operationType[0], operation = _operation[0],  
                                         testMode = '2', testLevel = '1',
                                         mySQL_password = mod.pwd )


        object.run()

        del object





    print ('Finished ' + _operationType + ' of ' + _code + ' ' + _branch + ' on ' + _computer )
    i=i+1

    





print ('Finished Build n Test of ' + _code + ' ' + _branch + ' on ' + _computer )




