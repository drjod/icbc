import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'access'))
import environment
mod = __import__( 'database' )
# import msvcrt 

_superuser = 'jens'
_computer = str(sys.argv[1])
_code = str(sys.argv[2])
_branch = str(sys.argv[3])
configuration = str(sys.argv[4])

operation_type_list = ['building', 'simulating']

for _operation_type in operation_type_list:

    if _operation_type == 'building':   # builing
        operation_list = ['clear', 'build']
    elif _operation_type == 'simulating':   # simulating
        operation_list = ['clear', 'run', 'wait', 'pack']
    elif _operation_type == 'plotting':   # plotting
        operation_list = ['clear', 'get', 'preplot', 'jpg', 'wait'] 
    else: 
        print ('ERROR - operation type {} not known'.format(_operation_type))
        exit()
        # msvcrt.getch()

    print ('\n----------------------------------------------------------------------')
    print ('--------------------------------------------(oo)----------------------')
    print ( _operation_type )
    print ('----------------------------------------------------------------------\n')

    for _operation in operation_list:
        print ('\n----------------------(^^)-------------')
        print ('{} - {}\n'.format(_operation_type, _operation) )
        
        object = environment.Environment(superuser=_superuser, computer=_computer, code=_code, branch=_branch,
                                         configuration_list=[configuration],
                                         operation_type=_operation_type[0], operation=_operation[0], 
                                         test_mode='2', db_user=mod.user, db_password=mod.pwd)

        object.run()
        del object

    print ('Finished {} on {}'.format(_operation_type, _computer))
   
# msvcrt.getch()

