import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pwds'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
import environment
mod = __import__( 'mysql2' )
import msvcrt 

_superuser='jens'
_operationType=str(sys.argv[1])
_computer=str(sys.argv[2])
_code=str(sys.argv[3])
_branch=str(sys.argv[4])
_configuration=str(sys.argv[5])

_configurationList=[]
_configurationList.append(_configuration)

operationTypeList = []
operationTypeList.append(_operationType)  

if _operationType[0] == 'b':   # builing
    operationList = [['clear','build']]  
elif _operationType[0] == 's':   # simulating
    operationList = [['clear', 'num','run','wait', 'pack']]
elif _operationType[0] == 'p':   # plotting
    operationList = [['clear','get','preplot','jpg','wait']] 
else: 
    print ('ERROR - operation type ' + _operationType + ' not known')
    msvcrt.getch()


i=0
for _operationType in operationTypeList:

    print ('\n----------------------------------------------------------------------')
    print ('--------------------------------------------(oo)----------------------')
    print ( _operationType )
    print ('----------------------------------------------------------------------\n')


    for _operation in operationList[i]:


        print ('\n----------------------(^^)-------------')
        print (_operationType + ' - ' +  _operation + '\n' )
        
        object = environment.Environment(superuser = _superuser, computer=_computer, code=_code, branch = _branch, configurationList=_configurationList,
                                         operationType = _operationType[0], operation = _operation[0], 
                                         testMode = "1",
                                         mySQL_password = mod.pwd )


        object.run()

        del object





    print ('Finished ' + _operationType +' on ' + _computer )
    i=i+1

    






msvcrt.getch()

