import subprocess
import message
import shutil
import os
import configuration
import fileinput

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
    # paths    
    __root_directory_examples = ''  
    __directory_example = ''
    
    __examplesName = ''
    
    #################################################################
    #  Operation: constructor
    #
           
    def __init__( self, cComputer, cCode, cBranch, root_directory, operating_system ):
        self.__cComputer = cComputer
        self.__cCode = cCode
        self.__cBranch = cBranch
        self.__root_directory = root_directory
        self.__operating_system = operating_system
            
        # config
        if self.__operating_system == 'windows':
            self.__root_directory_examples = self.__root_directory + 'testingEnvironment\\' \
            + self.__cCode + '\\' + self.__cBranch + '\\examples\\files\\'
        elif self.__operating_system == 'linux': 
            self.__root_directory_examples = self.__root_directory + 'testingEnvironment/' + \
            self.__cCode + '/' + self.__cBranch + '/examples/files/'
        else:
            print('ERROR - Operating system ' + self.__operating_system + ' not supported')
            
        self.__examplesName = 'testCase'  
            
    #################################################################
    #  Operation: destructor
    #
    
    def __del__( self ):
        pass  
                               
    #################################################################
    #  Operation: select
    #  Task:
    #      user input 
    #      set __selectedOperation (string) 
    #
                       
    def select( self, preselectedOperation ):
    
        if preselectedOperation == '':
            # set operations vector
            operations = []
            operations.append( '    (r)un ' + self.__cCode )
            operations.append( '    (u)pdate ' + self.__operating_system +  ' releases' )
            operations.append( '    (i)mport files from repository' )
            operations.append( '    e(x)port files to repository' )
            operations.append( '    (c)lean folder from results' )
            operations.append( '    replace (n)ans in tec files' )
            operations.append( '    re(s)elect' )
            
            # select
            print( '\nSelect operation:\n' )        
            for operation in operations:
                print( operation )                           
            self.__selectedOperation = input( '\n' )
        else:
            self.__selectedOperation = preselectedOperation            
        
        return self.__selectedOperation
        
    #################################################################
    #  Operation: setPathToExample
    #  Task:
    #      set path to test example
    #
                   
    def setPathToExample( self):  
        if self.__operating_system == 'windows':    
            self.__directory_example = self.__root_directory_examples + \
            self.__cType + '\\' + self.__cCase + '\\' + self.__cConfiguration + '\\'     
        elif self.__operating_system == 'linux':       
            self.__directory_example = self.__root_directory_examples + \
            self.__cType + '/' + self.__cCase + '/' + self.__cConfiguration + '/'     
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
        
        self.setPathToExample()
        
        if self.__selectedOperation == 'r':
            self.run() 
        elif self.__selectedOperation == 'u':
            self.updateRelease()  
        elif self.__selectedOperation == 'i':
            self.importFromRepository()
        elif self.__selectedOperation == 'x':
            self.exportToRepository() 
        elif self.__selectedOperation == 'c':
            self.cleanFolder() 
        elif self.__selectedOperation == 'n':
            self.replaceNans()                                                        
        else:
            message.console( type='ERROR', notSupported='Operation' ) 
       
    #################################################################
    #  Operation: run
    #  Task:
    #      run one of the selected test examples with selected code
    #
                                   
    def run( self ):   
        message.console( type='INFO', text='Running ' + str( self.__cType ) + ' ' + str( self.__cCase ) + ' ' + str( self.__cConfiguration ) )
               
        if self.__operating_system == 'windows':    
            executable = self.__root_directory + 'testingEnvironment\\' + self.__cCode + '\\' + self.__cBranch + \
            '\\releases\\' + self.__cCode + '_' + self.__cBranch + '_' + 'windows' + '_' + self.__cConfiguration + '.exe' 
            
        # message.console( type='INFO', text='Executable: ' + executable )  
        # message.console( type='INFO', text='Example:    ' + self.__directory_example + self.__examplesName )    
            
        with open ( self.__directory_example + 'out.txt', 'wb' ) as f:
            if self.__operating_system == 'windows':  
                subprocess.check_call( executable + ' ' + self.__directory_example + self.__examplesName, stdout=f )   
            elif self.__operating_system == 'linux':
                subprocess.check_call( 'qsub ' + self.__directory_example + 'run.bat', stdout=f )               
            else:
                message.console( type='ERROR', notSupported=self.__operating_system )
                      
    #################################################################
    #  Operation: importFromRepository
    #  Task:
    #      copy input files from repository into folder for test runs
    #
                                   
    def importFromRepository( self ):           
        message.console( type='INFO', text='Importing ' + str( self.__cType ) + ' ' + str( self.__cCase ) )   
        path = self.__root_directory + 'testingEnvironment'
        
        levels = [ self.__cCode, self.__cBranch, 'examples', 'files', self.__cType, self.__cCase, self.__cConfiguration ]       
        for level in levels:
            path = path + '\\' + level           
            try:
                os.stat(path)
            except:
                os.mkdir(path)        
                      
        for ending in configuration.inputFileEndings:                    
            fileName = self.__root_directory + 'testingEnvironment\\repository\\' + self.__cType + '\\' + self.__cCase + '\\testCase.' + ending
            if os.path.isfile(fileName) and os.access(fileName, os.R_OK):   
                shutil.copy( fileName, path )    
        
    #################################################################
    #  Operation: exportToRepository
    #  Task:
    #      copy input files into repository       
    #
                                   
    def exportToRepository( self ):   
        message.console( type='INFO', text='Exporting ' + str( self.__cType ) + ' ' + str( self.__cCase ) )   
        path = self.__root_directory + 'testingEnvironment'
        
        levels = [ 'repository', self.__cType, self.__cCase ]       
        for level in levels:
            path = path + '\\' + level        
            try:
                os.stat(path)
            except:
                os.mkdir(path) 
                    
        for ending in configuration.inputFileEndings:                    
            fileName = self.__root_directory + 'testingEnvironment\\' + self.__cCode + '\\' + self.__cBranch + '\\examples\\files\\' + self.__cType + '\\' + self.__cCase + '\\' + self.__cConfiguration + '\\testCase.' + ending
            if os.path.isfile(fileName) and os.access(fileName, os.R_OK):   
                shutil.copy( fileName, path )
        			 
    #################################################################
    #  Operation: cleanFolder
    #  Task:
    #      delete *.tec, *.txt, *.asc       
    #
                                   
    def cleanFolder( self ):   
    
        message.console( type='INFO', text='Clean folder ' + str( self.__cType ) + ' ' + str( self.__cCase ) + ' ' + str( self.__cConfiguration ) )
        exampleFolder = self.__root_directory + 'testingEnvironment\\' + self.__cCode + '\\' + self.__cBranch + '\\examples\\files\\' + self.__cType + '\\' + self.__cCase + '\\' + self.__cConfiguration
        for file in os.listdir( exampleFolder ):
            for ending in configuration.outputFileEndings: 
                if file.endswith( '.' + ending ):
                    os.remove( exampleFolder + '\\' + file ) 
                    
    #################################################################
    #  Operation: replaceNans
    #  Task:
    #      delete *.tec, *.txt, *.asc       
    #
                                   
    def replaceNans( self ):    
    
        message.console( type='INFO', text='Replace nans ' + str( self.__cType ) + ' ' + str( self.__cCase ) + ' ' + str( self.__cConfiguration ) )
        exampleFolder = self.__root_directory + 'testingEnvironment\\' + self.__cCode + '\\' + self.__cBranch + '\\examples\\files\\' + self.__cType + '\\' + self.__cCase + '\\' + self.__cConfiguration
        for file in os.listdir( exampleFolder ): 
            if file.endswith( '.tec' ):
                print ( '   ' + file )
                with fileinput.FileInput( exampleFolder + '\\' + file, inplace=True ) as fileToSearchIn:
                    for line in fileToSearchIn:
                        print( line.replace( 'nan', '999' ), end='' )
                
                    