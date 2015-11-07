import subprocess
import message
import shutil
import configurationShared
import fileinput
import item
import subject
import platform
import tarfile
import shutil
import utilities
import simulationData
import imp
import sys, os, glob
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized
import gateToCluster
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pwds'))


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

    _simulationData = ''    # put to Simulation below

    
    #################################################################
    #  Operation: constructor
    #
               
    def __init__( self, subject ):
        self._subject = subject
        self._gateFlag = False
    #################################################################
    #  Operation: destructor
    #
    
    def __del__( self ):
        pass 
    # getter             
    def getSelectedOperation( self ):                  
        return self._selectedOperation
 
                       
    #################################################################
    #  Operation: selectOperation
    #  Task:
    #      user input if operation has not been already selected (preselectedOperation !=' ') 
    #  Arguments:
    #      preselectedOperation (string)
    #  Requirements:
    #      _operationList (strings) 
    #  Returns    
    #      selectedOperation (string)
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
    #
    #

    def run( self, item, simulationData ):

        self._simulationData = simulationData
        if self._subject.getLocation() == 'remote' and configurationCustomized.location == 'local' and not self._selectedOperationType == 'p':
            
            gateToCluster.operate( self._subject, item, 
                                  self._selectedOperationType, self._selectedOperation, self._simulationData
                                  ) 
        else:   
            self.operate( item )                
                        
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
        
        if self._selectedOperation == 'c':
            self.compileRelease()  
        elif self._selectedOperation == 'u':
            self.updateRelease()                                                                             
        else:
            message.console( type='ERROR', notSupported='Operation ' + self.__selectedOperation )                          
  
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
            #print (self._subject.getCompilationCommand( self._item ))
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

class Simulating(Operation):
 
    #################################################################
    #  Simulating: constructor
    #  Task:
    #     testing operations that can be local or remote (e.g. writing files, run code)
           
    def __init__( self, subject ):

        self._selectedOperationType = 's'

        self._operationList[:]=[] 
        self._operationList.append( '    (r)un ' + subject.getCode() )
        self._operationList.append( '    (i)mport files from repository (gate)' )
        self._operationList.append( '    e(x)port files to repository (gate)' )
        self._operationList.append( '    (w)rite files' )
        self._operationList.append( '    (m)esh partition' )
        self._operationList.append( '    (c)lean folder from results' )
        self._operationList.append( '    pac(k) results' )            
        self._operationList.append( '    re(s)elect' )
        
        
        Operation.__init__( self, subject )
        
             
    #################################################################
    #  Simulating: operate
    #  Task:
    #      link to operation
    #
                                     
    def operate( self, sim ):
    
        self._item = sim
                                                                      
        if self._selectedOperation == 'r':
            self.runTest()  
        elif self._selectedOperation == 'i':
            self.importFromRepository()
        elif self._selectedOperation == 'I':
            self._gateFlag = True
            self.importFromRepository()
        elif self._selectedOperation == 'x':
            self.exportToRepository()
        elif self._selectedOperation == 'X':
            self._gateFlag = True
            self.exportToRepository()
        elif self._selectedOperation == 'w':
            self.writeFiles()               
        elif self._selectedOperation == 'm':
            self.meshPartition()  
        elif self._selectedOperation == 'c':
            self.cleanFolder() 
        elif self._selectedOperation == 'k':
            self.packResults()                                                                               
        else:
            message.console( type='ERROR', notSupported='Operation ' + self._selectedOperation ) 
       
    #################################################################
    #  Simulating: runTest
    #  Task:
    #      run code
    #
                                   
    def runTest( self ): 
        
        message.console( type='INFO', text='Running ' + self._item.getNameString() )
 
        if os.path.exists ( self._item.getDirectory() ):                           
            if platform.system() == 'Windows':        
                with open ( self._item.getDirectory() + 'out.txt', 'wb' ) as f:
                    subprocess.check_call( self._subject.getExecutable( self._item ) + ' ' + self._item.getDirectory() + configurationShared.examplesName, stdout=f )   
            elif platform.system() == 'Linux':
                if os.path.isfile( self._item.getDirectory() + 'run.pbs' ): 
                    subprocess.Popen('qsub ' + self._item.getDirectory() + 'run.pbs', shell=True)
                else:
                    message.console( type='ERROR', text='Pbs missing' )                         
            else:
                message.console( type='ERROR', notSupported=platform.system() )  
              
        else:
            message.console( type='ERROR', text='Directory missing' )
        
                      
    #################################################################
    #  Simulating: importFromRepository
    #  Task:
    #      copy input files from source directory into folder for test runs
    #      folder is generated if it is missing
    #      I: source is gate (for file transfer between computer)     
    #      i: source is repository (for file transfer between branches)
                                   
    def importFromRepository( self ):      

        message.console( type='INFO', text='Importing ' + self._item.getNameString() )              
        if self._gateFlag == True:
            message.console( type='INFO', text='From gate' )     
            sourceDirectory = self._subject.getGateDirectory()
        else:
            message.console( type='INFO', text='From repository' )
            sourceDirectory = self._item.getDirectoryRepository() 
     
        # make test folder if it does not exist  
        testList = [ # 'testingEnvironment', self._subject.getName(), self._subject.getCode(), self._subject.getBranch(), 
                       'examples', 'files' , self._item.getType(), self._item.getCase(), self._item.getConfiguration() ]         
        self._subject.generateFolder ( self._subject.getDirectory(), testList )
        # import
        if  os.path.exists ( sourceDirectory ):                                 
            for ending in configurationShared.inputFileEndings:  
                fileName = sourceDirectory + configurationShared.examplesName + '.' + ending       
                if os.path.isfile( fileName ) and os.access(fileName, os.R_OK):   
                    if self._gateFlag == True:
                        utilities.dos2unix( fileName )
                    shutil.copy( fileName, self._item.getDirectory() )    
        else:
            message.console( type='ERROR', text='Repository directory missing' )
                    
    #################################################################
    #  Simulating: exportToRepository
    #  Task:
    #      copy input files into destination folder       
    #      X: destination is gate (for file transfer between computer)     
    #      x: destination is repository (for file transfer between branches)
    #      destination folder generated if it is missing
                                           
    def exportToRepository( self ):   

        message.console( type='INFO', text='Exporting ' + self._item.getNameString() )   
        if self._gateFlag == True:
            message.console( type='INFO', text='Into gate' )
            destinationDirectory = self._subject.getGateDirectory()
        else:
            message.console( type='INFO', text='Into repository' )
            destinationDirectory = self._item.getDirectoryRepository() 
        # make repository folder if it does not exist                
        repositoryList = [ 'testingEnvironment', self._subject.getComputer(), 'repository', self._item.getType(), self._item.getCase() ]                   
        self._subject.generateFolder ( configurationCustomized.rootDirectory, repositoryList )
        # export  
        if os.path.exists ( self._item.getDirectory() ):                  
            for ending in configurationShared.inputFileEndings:      
                fileName = self._item.getDirectory() + configurationShared.examplesName + '.' + ending                   
                if os.path.isfile(fileName) and os.access(fileName, os.R_OK):   
                    shutil.copy( fileName, destinationDirectory )
        else:
            message.console( type='ERROR', text='Directory missing' )

    #################################################################
    #  Simulating: writeFiles
    #  Task:
    #      generate *.pbs and *.num
    #
                                   
    def writeFiles( self ): 

        message.console( type='INFO', text='Generate files ' + self._item.getNameString() )
        
        if os.path.exists ( self._item.getDirectory() ):   
            if platform.system() == 'Linux':

                message.console( type='INFO', text='    PBS' )
                if  self._simulationData.getProcessing() == 'sequential':            
                    ncpus = '1'              
                    command = ''
                    place = 'group=host'
                else:  # parallel
                    ncpus = self._simulationData.getNumberOfCPUs()
                    command = 'mpirun -r rsh -machinefile $PBS_NODEFILE -n ' + ncpus + ' '
                    place = 'scatter'
         
                f = open( self._item.getDirectory() + 'run.pbs', 'w' )
                f.write( '#!/bin/bash\n' )
                f.write( '#PBS -o ' + self._subject.getDirectory() + 'screenout.txt\n' )
                f.write( '#PBS -j oe\n' )  
                f.write( '#PBS -r n\n' )
                f.write( '#PBS -l walltime=2:00:00\n' )
                f.write( '#PBS -l select=1:ncpus=' + ncpus + ':mem=3gb\n' )
                f.write( '#PBS -l place=' + place + '\n' )
                f.write( '#PBS -q angus\n' )
                f.write( '#PBS -N test\n' )
                f.write( '\n' )
                f.write( 'cd $PBS_O_WORKDIR\n' )
                f.write( '\n' )
                f.write( '. /usr/share/Modules/init/bash\n' ) 
                f.write( '\n' )
                f.write( '. /cluster/Software/intel14/composer_xe_2015.2.164/bin/compilervars.sh  intel64\n' )
                f.write( '. /cluster/Software/intel14/composer_xe_2015.2.164/mkl/bin/intel64/mklvars_intel64.sh\n' )
                f.write( '. /cluster/Software/intel14/impi/5.0.3.048/intel64/bin/mpivars.sh\n' )
                f.write( '\n' ) 
                f.write( 'time ' + command + self._subject.getExecutable( self._item ) + ' ' + self._item.getDirectory() + configurationShared.examplesName + '\n' )
                f.write( '\n' ) 
                f.write( 'qstat -f $PBS_JOBID\n' )
                f.write( 'exit\n' )                                                                                                 
                f.close()
                            
            ##############################################
            message.console( type='INFO', text='    NUM' )

            self._simulationData.writeNumerics( self._item.getDirectory() )

        else:
            message.console( type='ERROR', text='Directory missing' ) 

    
    #################################################################
    #  Simulating: Mesh partition
    #  Task:
    #      call partition shell script

    def meshPartition( self ): 
        
        message.console( type='INFO', text='Mesh partition ' + self._item.getNameString() )

        partitionScript = configurationCustomized.rootDirectory + self._subject.adaptPath( 'testingEnvironment\\scripts\\' ) + 'partition.sh'

        if os.path.exists ( self._item.getDirectory() ):          
            os.chdir(self._item.getDirectory())
            myMeshfile = self._item.getDirectory() + configurationShared.examplesName + '.msh'
            if os.path.isfile( myMeshfile ):            
               if self._simulationData.getProcessing() == 'mpi_elements': # for OGS_FEM_MPI
                   subprocess.Popen( partitionScript + ' ' + self._simulationData.getNumberOfCPUs() + ' -n -binary ' +  self._item.getDirectory(), shell=True )    
               if self._simulationData.getProcessing() == 'mpi_nodes':    # for OGS_FEM_PETSC
                   subprocess.Popen( partitionScript + ' ' + self._simulationData.getNumberOfCPUs() + ' -e -asci ' +  self._item.getDirectory(), shell=True )                                                
            else:
                message.console( type='ERROR', text='Mesh file missing' )              
        else:
            message.console( type='ERROR', text='Directory missing' ) 

    #################################################################
    #  Simulating: cleanFolder
    #  Task:
    #      delete *.tec, *.txt, *.asc       
    # 
                                   
    def cleanFolder( self ):   

        message.console( type='INFO', text='Clean folder ' + self._item.getNameString() )
        #
        if os.path.exists ( self._item.getDirectory() ):
            for file in os.listdir( self._item.getDirectory() ):
                for ending in configurationShared.outputFileEndings: 
                    if file.endswith( '.' + ending ):
                        os.remove( self._item.getDirectory() + file ) 
        else:
            message.console( type='ERROR', text='Directory missing' )           
        #if configurationCustomized.location == 'remote':
        #    for file in os.listdir( self._item.getLocalDirectory() ):
        #        for ending in configurationShared.outputFileEndings: 
        #            if file.endswith( '.' + ending ):
        #                os.remove( self._item.getLocalDirectory() + file ) 
                                             
  
    #################################################################
    #
    # Simulating: packResults
    # Task:
    #    pack results on remote computer into tar file to download them later on

    def packResults( self ):   
         
        message.console( type='INFO', text='Pack results ' + self._item.getNameString() )

        if self._subject.getLocation() == 'remote':
            if os.path.exists ( self._item.getDirectory() ):
                myTarfile = self._item.getDirectory() + 'results.tar'  
                if os.path.isfile( myTarfile ):
                    os.remove( myTarfile )

                os.chdir(self._item.getDirectory())
                tar = tarfile.open( myTarfile, 'w')
                for extension in configurationShared.outputFileEndings:   
                    for file in os.listdir( self._item.getDirectory()  ):
                        if file.endswith('.' + extension):
                            tar.add( file )    
                tar.close()
            else:     
                message.console( type='ERROR', text='Directory missing' )
        else:
            message.console( type='INFO', text=self._subject.getComputer() + ' is local - Nothing done' )            
            
class Plotting(Operation):

    
    #################################################################
    #  Plotting: constructor
    #  Task: 
    #      testing operations on local computer (concerning simulations that can be local or remote) 
    #      (e.g. downloading results, plotting )     
    #
            
    def __init__( self, subject ):

        self._selectedOperationType = 'p'

        self._operationList[:]=[] 
        self._operationList.append( '    (g)et results' )
        self._operationList.append( '    (p)replot' )
        self._operationList.append( '    generate (j)pgs' )             
        self._operationList.append( '    re(s)elect' )
        
        
        Operation.__init__( self, subject )
        
             
    #################################################################
    #  Plotting: operate
    #  Task:
    #      link to operation
    #
                                     
    def operate( self, plot ):
    
        self._item = plot
                                                                      
        if self._selectedOperation == 'g':
            self.getResults()   
        elif self._selectedOperation == 'p':
            self.preplot()  
        elif self._selectedOperation == 'j':
            self.generateJpgs()                                                                               
        else:
            message.console( type='ERROR', notSupported='Operation ' + self._selectedOperation )             
            
            
                                                          
    #################################################################
    #  Plotting: getResults
    #  Task:
    #      download and unpack tar file from remote to local computer, than convert files into dos-format  
    #
                                   
    def getResults( self ):   
 
        message.console( type='INFO', text='Get results ' + self._item.getNameString() )

        mod = __import__( self._subject.getComputer() )      
        if self._subject.getLocation() == 'remote':
            if os.path.exists ( self._item.getDirectory() ):      
                # clear local directory
                files = glob.glob( self._item.getDirectory() + '*' )
                for file in files:
                    os.remove(file)
                # download with winscp     
                message.console( type='INFO', text='    Download' )
                myWinscpFile = self._subject.adaptPath( configurationCustomized.rootDirectory + '\\testingEnvironment\\scripts\\icbc\\customized\\winscp_downloadResults.txt' ) 
                myTarfile = self._item.getDirectorySelectedComputer() + 'results.tar'      
                f = open( myWinscpFile, 'w' ) 
                f.write( 'option batch abort \n' )
                f.write( 'option confirm off \n' )
                f.write( 'open sftp://' + self._subject.getUser() + ':' + mod.pwd + '@' + self._subject.getHostname() + '/ \n' )
                f.write( 'get ' + myTarfile + ' ' + self._item.getDirectory() + ' \n' )     
                f.write( 'exit' )            
                f.close()

                subprocess.check_call( configurationCustomized.winscp + ' /script=' + myWinscpFile )         
                # unpack
                print(' ')
                message.console( type='INFO', text='    Unpack' )
                myLocalTarFile = self._item.getDirectory() + 'results.tar' 
                if os.path.isfile( myLocalTarFile ): 
                    os.chdir( self._item.getDirectory() )             
                    tar = tarfile.open( myLocalTarFile )
                    tar.extractall()
                    tar.close()  
                    os.remove( myLocalTarFile )

                # unix2dos
                message.console( type='INFO', text='    Convert to dos' )
                for file in os.listdir( self._item.getDirectory() ): 
                    utilities.unix2dos( file )
            else:
                message.console( type='ERROR', text='Directory missing' )
        else:
            message.console( type='INFO', text=self._subject.getComputer() + ' is local - Nothing done' )
                                            
    #################################################################
    #  Plotting: replaceNans
    #  Task:
    #      replace each nan by 999 in all tec files 
    #
    #                               
    #def replaceNans( self ):    
    # 
    #    message.console( type='INFO', text='Replace nans ' + self._item.getNameString() )
    # 
    #    if os.path.exists ( self._item.getLocalDirectory() ):                               
    #        os.chdir(self._item.getLocalDirectory()) 
    #        for file in os.listdir( self._item.getLocalDirectory() ): 
    #            if file.endswith( '.tec' ):
    #                message.console( type='INFO', text='File: ' + file )  
    #            
    #                infile = open(file,'r') 
    #                outfile = open( 'new_' + file, 'w') 
    #                for line in infile: 
    #                    line = line.replace( 'nan', '999' )
    #                    outfile.write(line) 
    #                infile.close() 
    #                outfile.close()         
    #                shutil.move('new_' + file, file)                
    #    else:
    #        message.console( type='ERROR', text='Directory missing' )                                        
    #            #with fileinput.FileInput( self._item.getLocalDirectory() + file, inplace=True ) as fileToSearchIn:
    #            #    for line in fileToSearchIn:
    #            #        print( line.replace( 'nan', '999' ))

    #################################################################
    #  Plotting: preplot
    #  Task:
    #      replace nan's with 999 and call preplot to generate *.plt's          
    #
          

    def preplot( self ): 
    
        message.console( type='INFO', text='Preplot ' + self._item.getNameString() )

        if os.path.exists ( self._item.getDirectory() ): 
            os.chdir(self._item.getDirectory()) 
            for file in os.listdir( self._item.getDirectory() ): 
                if file.endswith( '.tec' ):
                    message.console( type='INFO', text='File: ' + file )   
                    # replace nans
                    infile = open(file,'r') 
                    outfile = open( 'new_' + file, 'w') 
                    for line in infile: 
                        line = line.replace( 'nan', '999' )
                        outfile.write(line) 
                    infile.close() 
                    outfile.close()         
                    shutil.move('new_' + file, file)                     
                     
                    #print (configurationCustomized.preplot + ' ' + self._item.getDirectory() + file)           
                    subprocess.check_call(configurationCustomized.preplot + ' ' + self._item.getDirectory() + file ) 
                                    
     
 
    #################################################################
    #  Plotting: generateJpgs
    #  Task:
    #      generate JPG with tecplot           
    #
                                   

    def generateJpgs( self ):         

        message.console( type='INFO', text='Generate Jpgs ' + self._item.getType() )
   
        if os.path.exists ( self._subject.getPlotDirectory() ): 

            layout = self._subject.getPlotDirectory()  + self._item.getType() + '.lay'
              
            os.chdir( self._subject.getPlotDirectory() )

            f = open( self._subject.getPlotDirectory() + '_genJPG.mcr', 'w' )
            f.write( '#!MC 1300\n' )
            f.write( '#-----------------------------------------------------------------------\n' )
            f.write( '$!EXPORTSETUP EXPORTFORMAT = JPEG\n' )
            f.write( '$!EXPORTSETUP IMAGEWIDTH = 1500\n' )
            f.write( '#-----------------------------------------------------------------------\n' )
            f.write( "$!EXPORTSETUP EXPORTFNAME = \'" + self._subject.getPlotDirectory() + "results_" + self._item.getType() + ".jpg\'\n" )
            f.write( '$!EXPORT\n' )
            f.write( 'EXPORTREGION = ALLFRAMES\n' )
            f.close()

            subprocess.check_call( configurationCustomized.tecplot + ' ' + layout + ' -b -p ' + self._subject.getPlotDirectory() + '_genJPG.mcr' ) 

            os.remove( self._subject.getPlotDirectory() + '_genJPG.mcr' )           
  
        else:
            message.console( type='ERROR', text='Directory missing' )    
            
            



          