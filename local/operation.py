import subprocess
import message

#################################################################
#  class: Operation
#  Task:
#      configure and execute operations 
#

class Operation:
   # test examples
    __cType = ''
    __cCase = ''
    __cConfiguration = ''
    # operations
    __operations = []
    __selectedOperation = ''
    # paths    
    __root_directory = 'C:\\'
    __root_directory_examples = ''  
    __directory_example = ''
    
    __examplesName = ''
    
    #################################################################
    #  Operation: constructor
    #
           
    def __init__( self, cComputer, cCode, cBranch, operating_system ):
        self.__cComputer = cComputer
        self.__cCode = cCode
        self.__cBranch = cBranch
        self.__operating_system = operating_system

    #################################################################
    #  Operation: destructor
    #
    
    def __del__( self ):
        pass  
             
    #################################################################
    #  Operation: globalConfig
    #  Task:
    #      set operations vector
    #      set path to examples (global)
    #
                       
    def globalConfig( self):
    
        self.__operations[:] = []
        self.__operations.append('(r)un')
        # add operations here
        # path to examples
        if self.__operating_system == 'windows':
            self.__root_directory_examples = self.__root_directory + 'testingEnvironment\\' \
            + self.__cCode + '\\' + self.__cBranch + '\\examples\\'
        elif self.__operating_system == 'linux': 
            self.__root_directory_examples = self.__root_directory + 'testingEnvironment/' + \
            self.__cCode + '/' + self.__cBranch + '/examples/'
        else:
            print('ERROR - Operating system ' + self.__operating_system + ' not supported')
           
        self.__examplesName = 'testCase'   
        
    #################################################################
    #  Operation: select
    #  Task:
    #      user input 
    #      set __selectedOperation (string) 
    #
                       
    def select( self ):
 
        print( '\nSelect operation:\n' )           
        for operation in self.__operations:
            print( operation )
                       
        self.__selectedOperation = input( '\n' )    
        
    #################################################################
    #  Operation: configureExample
    #  Task:
    #      set path to test example
    #
                   
    def configureExample( self):
    
        if self.__operating_system == 'windows':    
            self.__directory_example = self.__root_directory_examples + \
            self.__cType + '\\' + self.__cCase + '\\'# + self.__cConfiguration + '\\'     
        elif self.__operating_system == 'linux':       
            self.__directory_example = self.__root_directory_examples + \
            self.__cType + '/' + self.__cCase + '/' #+ self.__cConfiguration + '/'     
        else:
            message.console( type='ERROR', notSupported=self.__operating_system )
        
    #################################################################
    #  Operation: operate
    #  Task:
    #      configure and run operation
    #
                                     
    def operate( self, cType, cCase, cConfiguration ):
        self.__cType = cType
        self.__cCase = cCase
        self.__cConfiguration = cConfiguration        
        
        self.configureExample()
        
        if self.__selectedOperation == 'r':
            self.run()   
        else:
            message.console( type='ERROR', notSupported='Operation' ) 
       
    #################################################################
    #  Operation: run
    #  Task:
    #      run one of the selected test examples with selected code
    #
                                   
    def run( self ):          
        if self.__operating_system == 'windows':    
            executable = self.__root_directory + 'testingEnvironment\\' + self.__cCode + '\\' + self.__cBranch + \
            '\\releases\\' + self.__cCode + '_' + self.__cBranch + '_' + 'windows' + '_' + self.__cConfiguration + '.exe' 
          
        print(executable)
        print(self.__directory_example)
        with open ('output.txt', 'wb') as f:
            if self.__operating_system == 'windows':  
                subprocess.check_call(executable + ' ' + self.__directory_example + self.__examplesName, stdout=f)   
            elif self.__operating_system == 'linux':
                subprocess.check_call('qsub ' + self.__directory_example + 'run.bat', stdout=f)               
            else:
                message.console( type='ERROR', notSupported=self.__operating_system )
        
             
        
        
        
        
