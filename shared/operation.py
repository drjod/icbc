import subprocess
import message
import shutil
import configurationShared
import fileinput
import item
import subject
import platform
import tarfile
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized
import gateToCluster

#################################################################
#  class: Operation
#  Task:
#      
#

class Operation:

    _selectedOperation = ' '
    _selectedOperationType = ' '   
    _item = ' '
    _operationList = [] 
    
    #################################################################
    #  Operation: constructor
    #
               
    def __init__( self, subject ):
        self._subject = subject

    #################################################################
    #  Operation: destructor
    #
    
    def __del__( self ):
        pass 
            
    #################################################################
    #  Operation: selectOperation
    #  Task:
    #      user input 
    #      set __selectedOperation (string) 
    #
                       
    def selectOperation( self, preselectedOperation ):
    
        if preselectedOperation == ' ':
            print( '\nSelect operation:\n' )        
            for operation in self._operationList:
                print( operation )                           
            self._selectedOperation = input( '\n' )
        else:
            self._selectedOperation = preselectedOperation            
    
             
    #################################################################
    #  Operation: 
             
    def getSelectedOperation( self ):
                   
        return self._selectedOperation

    #################################################################
    #  Operation: 
    
    def run( self, item, location ):
        
        if location == 'local': 
            self.operate( item ) 
        else:
            gateToCluster.operate( self._subject, item, 
                                  self._selectedOperationType, self._selectedOperation )    
                        
#################################################################
#  class: Building
#  Task:
#     
#

class Building(Operation):

            
    #################################################################
    #  Building: constructor
    #
           
    def __init__( self, subject ):

        self._selectedOperationType = 'b'

        self._operationList[:]=[]                                    
        self._operationList.append( '    (c)ompile' )                  
        self._operationList.append( '    (u)pdate release file' )      
        self._operationList.append( '    re(s)elect' )                     
            
        Operation.__init__( self, subject )
        
    #################################################################
    #  Building: operate
    #  Task:
    #      configure build and call operation for this build
    #
                                     
    def operate( self, build ):
        
        self._item = build
        #self.__cConfiguration = cConfiguration              
        #self.__directoryBuildbuild = self._subject.adaptPath( self._subject.getRootDirectory() + 'sources\\' + 'Build_' + self.__cConfiguration + '\\' )   
        
        if self._selectedOperation == 'c':
            self.compileRelease()  
        elif self._selectedOperation == 'u':
            self.updateRelease()                                                                             
        else:
            message.console( type='ERROR', notSupported='Operation' + self.__selectedOperation )                          
  
    #################################################################
    #  Building: run
    #  Task:
    #      run one of the selected test items with selected code
    #
                                   
    def compileRelease( self ): 
        message.console( type='INFO', text='Compiling ' + self._item.getConfiguration()  )
        
        if platform.system() == 'Windows':                     
            subprocess.check_call( self._subject.getCompilationCommand( self._item ) )   
        elif platform.system() == 'Linux':
            subprocess.Popen(self._subject.getCompilationCommand( self._item ), shell=True)               
        else:
            message.console( type='ERROR', notSupported=platform.system() )  

            
    #################################################################
    #  Building: updateRelease
    #  Task:
    #      copy and rename windows binaries
    #
                                   
    def updateRelease( self ):   
        try: 
            os.stat(self._subject.getDirectory() + 'releases' )
        except:
            os.mkdir(self._subject.getDirectory() + 'releases' ) 
        
        message.console( type='INFO', text='Updating release ' + platform.system() + ' ' + self._item.getConfiguration() )   
      
        if os.path.isfile( self._subject.getExecutable( self._item ) ) and os.access( self._subject.getExecutable( self._item ), os.R_OK ): 
            shutil.copy( self._subject.getExecutable( self._item ), self._subject.getExecutableForRelease( self._item ) )  
        else:
            message.console( type='ERROR', text='Binary does not exist - nothing done' )                         
           
                               
#################################################################
#  class: Testing
#  Task:
#      configure and execute operations 
#

class Testing(Operation):

    
    #################################################################
    #  Testing: constructor
    #
           
    def __init__( self, subject ):

        self._selectedOperationType = 't'

        self._operationList[:]=[] 
        self._operationList.append( '    (r)un ' + subject.getCode() )
        self._operationList.append( '    (i)mport files from repository' )
        self._operationList.append( '    e(x)port files to repository' )
        self._operationList.append( '    (c)lean folder from results' )
        self._operationList.append( '    (d)ownload results' )
        self._operationList.append( '    replace (n)ans in tec files' )
        self._operationList.append( '    (p)replot')
        self._operationList.append( '    generate (j)pgs' )            
        self._operationList.append( '    re(s)elect' )
        
        
        Operation.__init__( self, subject )
        
             
    #################################################################
    #  Testing: operate
    #  Task:
    #      configure and run operation
    #
                                     
    def operate( self, test ):
    
        self._item = test
                                                                      
        if self._selectedOperation == 'r':
            self.runTest()  
        elif self._selectedOperation == 'i':
            self.importFromRepository()
        elif self._selectedOperation == 'x':
            self.exportToRepository() 
        elif self._selectedOperation == 'c':
            self.cleanFolder() 
        elif self._selectedOperation == 'd':
            self.downloadResults() 
        elif self._selectedOperation == 'n':
            self.replaceNans()  
        elif self._selectedOperation == 'p':
            self.preplot()   
        elif self._selectedOperation == 'j':
            self.generateJpgs()                                                                               
        else:
            message.console( type='ERROR', notSupported='Operation' + self.__selectedOperation ) 
       
    #################################################################
    #  Testing: run
    #  Task:
    #      run one of the selected test items with selected code
    #
                                   
    def runTest( self ): 
        
        message.console( type='INFO', text='Running ' + self._item.getNameString() )
                    
        if platform.system() == 'Windows':        
            with open ( self._item.getDirectory() + 'out.txt', 'wb' ) as f:
                subprocess.check_call( self._subject.getExecutable( self._item ) + ' ' + self._item.getDirectory() + configurationShared.examplesName, stdout=f )   
        elif platform.system() == 'Linux':
            subprocess.Popen('qsub ' + self._item.getDirectory() + 'run.pbs', shell=True)                     
        else:
            message.console( type='ERROR', notSupported=platform.system() )  
              

        
                      
    #################################################################
    #  Testing: importFromRepository
    #  Task:
    #      copy input files from repository into folder for test runs
    #
                                   
    def importFromRepository( self ):           
        message.console( type='INFO', text='Importing ' + self._item.getNameString() )      
        # make test folder if it does not exist  
        testList = [ # 'testingEnvironment', self._subject.getName(), self._subject.getCode(), self._subject.getBranch(), 
                       'examples', 'files' , self._item.getType(), self._item.getCase(), self._item.getConfiguration() ]         
        self._subject.generateFolder ( self._subject.getDirectory(), testList )
        # import              
        for ending in configurationShared.inputFileEndings:  
            fileName = self._item.getDirectoryRepository() + configurationShared.examplesName + '.' + ending       
            if os.path.isfile( fileName ) and os.access(fileName, os.R_OK):   
                shutil.copy( fileName, self._item.getDirectory() )    
        
    #################################################################
    #  Testing: exportToRepository
    #  Task:
    #      copy input files into repository       
    #
                                   
    def exportToRepository( self ):   
        message.console( type='INFO', text='Exporting ' + self._item.getNameString() )   
        # make repository folder if it does not exist                
        repositoryList = [ 'testingEnvironment', self._subject.getComputer(), 'repository', self._item.getType(), self._item.getCase() ]                   
        self._subject.generateFolder ( configurationCustomized.rootDirectory, repositoryList )
        # export            
        for ending in configurationShared.inputFileEndings:      
            fileName = self._item.getDirectory() + configurationShared.examplesName + '.' + ending                   
            if os.path.isfile(fileName) and os.access(fileName, os.R_OK):   
                shutil.copy( fileName, self._item.getDirectoryRepository() )

    #################################################################
    #  Testing: cleanFolder
    #  Task:
    #      delete *.tec, *.txt, *.asc       
    #
                                   
    def cleanFolder( self ):   
        message.console( type='INFO', text='Clean folder ' + self._item.getNameString() )
        #
        for file in os.listdir( self._item.getDirectory() ):
            for ending in configurationShared.outputFileEndings: 
                if file.endswith( '.' + ending ):
                    os.remove( self._item.getDirectory() + file ) 
                    
        if configurationCustomized.location == 'remote':
            for file in os.listdir( self._item.getLocalDirectory() ):
                for ending in configurationShared.outputFileEndings: 
                    if file.endswith( '.' + ending ):
                        os.remove( self._item.getLocalDirectory() + file ) 
                                             
            
    #################################################################
    #  Testing: downLoadResults
    #  Task:
    #      download *.tec, *.txt, *.asc       
    #
                                   
    def downloadResults( self ):   
          
        #shutil.rmtree( self._item.getDirectory() + '/results' ) # remove results folder if exists
        #os.mkdir( self._item.getDirectory() + '/results' )  
        #os.mkdir( self._item.getDirectory() + '/results/packed' )

        tar = tarfile.open(self._item.getDirectory() + 'results.tar', 'w')

        for ending in configurationShared.outputFileEndings:  
            fileName = self._item.getDirectory() + configurationShared.examplesName + '.' + ending       
            if os.path.isfile( fileName ) and os.access(fileName, os.R_OK): 
                tar.add( fileName )  
                #shutil.copy( fileName, self._item.getDirectory() + '/results/packed' )  
        tar.close()

        #subprocess.Popen('tar cfv results *tec *txt', shell=True)     
            
        f = open( 'F:\\tools\\icbc-0.2\\icbc\\customized\\winscp_downloadResults.txt', 'w' )
        f.write( 'option batch abort \n' )
        f.write( 'option confirm off \n' )
        f.write( 'open sftp://sungw389:fuwyek90@rzcluster.rz.uni-kiel.de/ \n' )
        f.write( 'get ' + self._item.getDirectory() + 'results.tar ' + self._item.getLocalDirectory()  )
                
        f.close()
               

                             
    #################################################################
    #  Testing: replaceNans
    #  Task:
    #      replace each nan by 999 in all tec files 
    #
                                   
    def replaceNans( self ):    
    
        message.console( type='INFO', text='Replace nans ' + self._item.getNameString() )
            
        for file in os.listdir( self._item.getDirectory() ): 
            if file.endswith( '.tec' ):
                message.console( type='INFO', text='File: ' + file )                     
                with fileinput.FileInput( self._item.getDirectory() + file, inplace=True ) as fileToSearchIn:
                    for line in fileToSearchIn:
                        print( line.replace( 'nan', '999' ))
                
    #################################################################
    #  Testing: preplot
    #  Task:
    #      preplot for all tec files in folder            
    #
                                   
    def preplot( self ): 
        
        message.console( type='INFO', text='Preplot ' + self._item.getNameString() )
        for file in os.listdir( self._item.getDirectory() ): 
            if file.endswith( '.tec' ):
                message.console( type='INFO', text='File: ' + file )    
                #print (configurationCustomized.preplot + ' ' + self._item.getDirectory() + file)           
                subprocess.check_call(configurationCustomized.preplot + ' ' + self._item.getDirectory() + file ) 
               
 
    #################################################################
    #  Testing:generateJpgs
    #  Task:
    #      generate JPG with tecplot           
    #
                                   
    def generateJpgs( self ): 
    
        message.console( type='INFO', text='Generate Jpgs ' + self._item.getType() )

        directoryPlots = self._subject.getDirectory() + 'examples\\plots\\'       # always windows  
        directoryPlots = directoryPlots.replace( '/', '\\' )
        
        layout = directoryPlots + self._item.getType() + '.lay'
        
        f = open( directoryPlots + '_genJPG.mcr', 'w' )
        f.write( '#!MC 1300\n' )
        f.write( '#-----------------------------------------------------------------------\n' )
        f.write( '$!EXPORTSETUP EXPORTFORMAT = JPEG\n' )
        f.write( '$!EXPORTSETUP IMAGEWIDTH = 1500\n' )
        f.write( '#-----------------------------------------------------------------------\n' )
        f.write( "$!EXPORTSETUP EXPORTFNAME = \'" + directoryPlots + "results_" + self._item.getType() + ".jpg\'\n" )
        f.write( '$!EXPORT\n' )
        f.write( 'EXPORTREGION = ALLFRAMES\n' )
        
        f.close()
        
        subprocess.check_call( configurationCustomized.tecplot + ' -b -p ' + directoryPlots + '_genJPG.mcr' ) 
        
        os.remove( directoryPlots + '_genJPG.mcr' )         
        
        