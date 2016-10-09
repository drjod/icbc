import subject, item, simulationData
import utilities, configurationShared
import platform, subprocess, shutil, tarfile, fileinput
import imp, sys, os, glob, time
import difflib
from shutil import copyfile
from filecmp import cmp
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

    _selectedOperation = None
    _selectedOperationType = None   
    _item = None
    _operationList = [] 

    _simulationData = None   # put to Simulation below

    
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
    def getSelectedOperationType( self ):                  
        return self._selectedOperationType

                       
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
    
        print( '\n-----------------------------------------------------------------\n' ) 
        print('Test subject ' + self._subject.getCode() + ' ' + self._subject.getBranch())
        print('             on ' +  self._subject.getComputer() )
        if not preselectedOperation:
            print( '\nSelect operation:\n' )        
            for operation in self._operationList:
                print( operation )                           
            self._selectedOperation = input( '\n' )
        else:
            self._selectedOperation = preselectedOperation    
        return self._selectedOperation          
               
    #################################################################
    #  Operation.run(): 
    #      direct to cluster or load data files (if necessary) and do operation
    #

    def run( self, item, simulationData ):

        self._simulationData = simulationData
   
        if self._subject.getLocation() == 'remote' and configurationCustomized.location == 'local' and not self._selectedOperationType == 'p':
            
            gateToCluster.operate( self._subject, item, 
                                    self._selectedOperationType, self._selectedOperation, self._simulationData ) 
        else:   
            if configurationCustomized.location == 'remote':
                # file transfer
                if simulationData.getReadFileFlags()._numerics  == True: 
                    simulationData.importNumDataFiles( item.getConfiguration() )
                    simulationData.getNumDataFromModules( item.getConfiguration() )
                if simulationData.getReadFileFlags()._processing  == True: 
                    simulationData.importProcessingDataFiles( item.getConfiguration() )
                    simulationData.getProcessingDataFromModule( item.getConfiguration() )
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
        self._operationList.append( '    (b)uild' )                  
        self._operationList.append( '    (u)pdate' )   
        self._operationList.append( '    (c)lear' )     
        self._operationList.append( '    (w)ait' )                  
        self._operationList.append( '    re(s)elect' )                     
            
        Operation.__init__( self, subject )
        
    #################################################################
    #  Building: operate
    #  Task:
    #      configure build and call operation for this build
    #
                                     
    def operate( self, build ):
        
        self._item = build 
        
        if self._selectedOperation == 'b':
            self.buildRelease()  
        elif self._selectedOperation == 'u':
            self.updateRelease()  
        elif self._selectedOperation == 'c':
            self.clearFolder()     
        elif self._selectedOperation == 'w':
            self.wait()                                                                                                   
        else:
            utilities.message( type='ERROR', notSupported='Operation ' + self._selectedOperation )                          
  
    #################################################################
    #  Building: run
    #  Task:
    #      run one of the selected test items with selected code
    #
                                   
    def buildRelease( self ): 
        utilities.message( type='INFO', text='Building ' + self._item.getConfiguration()  )
        try:
            subprocess.Popen( self._subject.getBuildCommand( self._item ), shell=True )   
        except:
            utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] )            
            
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
        
        utilities.message( type='INFO', text='Updating release ' + platform.system() + ' ' + self._item.getConfiguration() )   
      
        if os.path.isfile( self._subject.getExecutable( self._item ) ) and os.access( self._subject.getExecutable( self._item ), os.R_OK ): 
            shutil.copy( self._subject.getExecutable( self._item ), self._subject.getExecutableForRelease( self._item ) )  
        else:
            utilities.message( type='ERROR', text='Binary does not exist - nothing done' )                         
           
    #################################################################
    #  Building: clearFolder
    #  Task:
    #      Deleate release binaries
    #
                                   
    def clearFolder( self ):   

        utilities.message( type='INFO', text='Removing release ' + platform.system() + ' ' + self._item.getConfiguration() )   
        try:
            os.remove(self._subject.getExecutable( self._item ))
        except OSError:
            utilities.message( type='ERROR', text='%s' % sys.exc_info()[0]  )

    #################################################################
    #  Building: Wait
    #  Task:
    #      Wait until release exists
    #
                                   
    def wait( self ):   
        utilities.message( type='INFO', text='Waiting for release ' + platform.system() + ' ' + self._item.getConfiguration() )  
        waitForFile(self._subject.getExecutable( self._item ))

                   
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
    #     adapt simulationDate.setReadFileFlags according to letters r, n, .... for selected operation
    #
             
    def __init__( self, subject ):

        self._selectedOperationType = 's'

        self._operationList[:]=[] 
        self._operationList.append( '    (r)un ' + subject.getCode() )
        self._operationList.append( '    write (n)um' )
        self._operationList.append( '    (c)lear folder from results' )
        self._operationList.append( '    (w)ait' )
        self._operationList.append( '    s(t)ore results as reference' )
        self._operationList.append( '    c(o)mpare results with reference' )
        if subject.getLocation() == 'remote':
            self._operationList.append( '    (i)mport files from repository (gate)' )
            self._operationList.append( '    e(x)port files to repository (gate)' )
            self._operationList.append( '    wri(t)e pbs' )
            self._operationList.append( '    (m)esh partition' )
            self._operationList.append( '    (p)ack results' )                 
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
            self.runItem()  
        elif self._selectedOperation == 'n':
            self.writeNum()               
        elif self._selectedOperation == 'c':
            self.clearFolder()
        elif self._selectedOperation == 't':
            self.storeResultsAsReference()
        elif self._selectedOperation == 'o':
            self.compareResultsWithReference()
        elif self._selectedOperation == 'i' and self._subject.getLocation() == 'remote':
            self.importFromRepository()
        elif self._selectedOperation == 'I' and self._subject.getLocation() == 'remote':
            self._gateFlag = True
            self.importFromRepository()
        elif self._selectedOperation == 'x' and self._subject.getLocation() == 'remote':
            self.exportToRepository()
        elif self._selectedOperation == 'X' and self._subject.getLocation() == 'remote':
            self._gateFlag = True
            self.exportToRepository()
        elif self._selectedOperation == 't' and self._subject.getLocation() == 'remote':
            self.writePbs()  
        elif self._selectedOperation == 'm' and self._subject.getLocation() == 'remote':
            self.meshPartition()  
        elif self._selectedOperation == 'p' and self._subject.getLocation() == 'remote':
            self.packResults()   
        elif self._selectedOperation == 'w':
            self.wait() 
        elif self._selectedOperation == '0':       
            utilities.message( type='INFO', text='No Operation' )                                                                         
        else:
            utilities.message( type='ERROR', notSupported='Operation ' + self._selectedOperation ) 
       
    #################################################################
    #  Simulating: runItem
    #  Task:
    #      run code
    #
                                   
    def runItem( self ): 
        
        utilities.message( type='INFO', text='Running ' + self._item.getNameString() )
        
        if os.path.exists ( self._item.getDirectory() ):                           
            try:
                subprocess.call( self._subject.getItemExecutionCommand( self._item ), shell=True)
            except:
                utilities.message( type='ERROR', text='%s' % sys.exc_info()[0]  )    
        else:
            utilities.message( type='ERROR', text='Directory missing' )
        
                      
    #################################################################
    #  Simulating: importFromRepository
    #  Task:
    #      copy input files from source directory into folder for test runs
    #      folder is generated if it is missing
    #      I: source is gate (for file transfer between computer)     
    #      i: source is repository (for file transfer between branches)
                                   
    def importFromRepository( self ):      

        utilities.message( type='INFO', text='Importing ' + self._item.getNameString() )              
        if self._gateFlag == True:
            utilities.message( type='INFO', text='    From gate' )     
            sourceDirectory = self._subject.getGateDirectory()
        else:
            utilities.message( type='INFO', text='    From repository' )
            sourceDirectory = self._item.getDirectoryRepository() 
     
        # make test folder if it does not exist  
        testList = [ # 'testingEnvironment', self._subject.getName(), self._subject.getCode(), self._subject.getBranch(), 
                       'examples', 'files' , self._item.getType(), self._item.getCase(), self._item.getConfiguration() ]         
        utilities.generateFolder( self._subject.getDirectory(), testList )

        endingList = []
        if self._subject.getLocation() == 'remote':                     # no input on remote cluster
            endingList = list(configurationShared.inputFileEndings)
        else:                                                         # but on local computer
            selectedEndingGroup = input( '(e)nding, (n)ame or (a)ll\n' )
        
            # set variable(s) to  
            if str( selectedEndingGroup ) == 'e':
                selectedEnding = input( '\n' )
                endingList.append(selectedEnding)
            elif str( selectedEndingGroup ) == 'a':
                endingList = list(configurationShared.inputFileEndings)
            elif str( selectedEndingGroup ) == 'n':
                name = input( '\n' )
            

        # import
        if  os.path.exists ( sourceDirectory ):           
            if self._gateFlag == True:
                # dos2unix
                utilities.message( type='INFO', text='    Convert file(s) to unix' )                      
            for ending in endingList:  
                fileName = sourceDirectory + configurationShared.examplesName + '.' + ending       
                if os.path.isfile( fileName ) and os.access(fileName, os.R_OK):   
                    if self._gateFlag == True:
                        # dos2unix
                        utilities.dos2unix( fileName )
                    shutil.copy( fileName, self._item.getDirectory() )   
                    
            for file in os.listdir( sourceDirectory ):  # to copy additional files, e.g. for external chemical solver
                fileName = sourceDirectory + file
                for ending in configurationShared.additionalFileEndings: 
                    if file.endswith( '.' + ending ) and not fileName == sourceDirectory + configurationShared.examplesName + '.out':
                        if self._gateFlag == True:
                            # dos2unix
                            if not file.endswith( '.exe' ):
                                utilities.dos2unix( fileName )
                        utilities.message( type='INFO', text='    Importing additional file ' + file ) 
                        shutil.copy( fileName , self._item.getDirectory() ) 
                                             
        else:
            utilities.message( type='ERROR', text='Repository directory missing' )
                    
    #################################################################
    #  Simulating: exportToRepository
    #  Task:
    #      copy input files into destination folder       
    #      X: destination is gate (for file transfer between computer)     
    #      x: destination is repository (for file transfer between branches)
    #      destination folder generated if it is missing
                                           
    def exportToRepository( self ):   

        utilities.message( type='INFO', text='Exporting ' + self._item.getNameString() )   
        if self._gateFlag == True:
            utilities.message( type='INFO', text='Into gate' )
            destinationDirectory = self._subject.getGateDirectory()
        else:
            utilities.message( type='INFO', text='Into repository' )
            destinationDirectory = self._item.getDirectoryRepository() 
        # make repository folder if it does not exist                
        repositoryList = [ 'testingEnvironment', self._subject.getComputer(), 'repository', self._item.getType(), self._item.getCase() ]                   
        utilities.generateFolder ( configurationCustomized.rootDirectory, repositoryList )
        # export  
        if os.path.exists ( self._item.getDirectory() ):                  
            for ending in configurationShared.inputFileEndings:      
                fileName = self._item.getDirectory() + configurationShared.examplesName + '.' + ending                   
                if os.path.isfile(fileName) and os.access(fileName, os.R_OK):   
                    shutil.copy( fileName, destinationDirectory )

            for file in os.listdir( self._item.getDirectory() ):  # to copy additional files, e.g. for external chemical solver
                fileName = self._item.getDirectory() + file
                for ending in configurationShared.additionalFileEndings: 
                    if file.endswith( '.' + ending ):
                        utilities.message( type='INFO', text='    Exporting additional file ' + file )
                        shutil.copy( fileName , destinationDirectory ) 
        else:
            utilities.message( type='ERROR', text='Directory missing' )

    #################################################################
    #  Simulating: writeNum
    #  Task:
    #      generate *.num
    #
                                   
    def writeNum( self ): 
        
        utilities.message( type='INFO', text='Write *.num ' + self._item.getNameString() )
        
        if os.path.exists ( self._item.getDirectory() ):   
            self._simulationData.writeNum( self._item.getDirectory() )
        else:
            utilities.message( type='ERROR', text='Directory missing' ) 

  
    #################################################################
    #  Simulating: writePbs
    #  Task:
    #      generate run.pbs
    #
                                   
    def writePbs( self ): 
        
        utilities.message( type='INFO', text='Write run.pbs ' + self._item.getNameString() )

        if os.path.exists ( self._item.getDirectory() ):   
            self._simulationData.writePbs( self._item.getDirectory(), self._subject.getExecutable( self._item ), self._item.getType() )
        else:
            utilities.message( type='ERROR', text='Directory missing' ) 
                    
   
            
                          
    #################################################################
    #  Simulating: Mesh partition
    #  Task:
    #      call partition shell script

    def meshPartition( self ): 
        
        utilities.message( type='INFO', text='Mesh partition ' + self._item.getNameString() )

        if os.path.exists ( self._item.getDirectory() ):   
            self._simulationData.partitionMesh( self._item.getDirectory() )
        else:
            utilities.message( type='ERROR', text='Directory missing' ) 

    #################################################################
    #  Simulating: clearFolder
    #  Task:
    #      delete *.tec, *.txt, *.plt, *.vtk and results.tar       
    #      (remote folder for remote computer)
                                   
    def clearFolder( self ):   

        utilities.message( type='INFO', text='Clear simulation folder ' + self._item.getNameString() )
        #
        if os.path.exists ( self._item.getDirectory() ):
            
            for file in os.listdir( self._item.getDirectory() ):
                for ending in configurationShared.outputFileEndings: 
                    if file.endswith( '.' + ending ):
                        utilities.removeFile( self._item.getDirectory() + file ) 
                                        
                myRemoteTarFile = self._item.getDirectory() + 'results.tar' 
                if os.path.isfile( myRemoteTarFile ): 
                    utilities.removeFile( myRemoteTarFile )
           
            utilities.removeFile( self._item.getDirectory() + configurationCustomized.outputFile )
        else:
            utilities.message( type='ERROR', text='Directory missing' )           

                                               
    #################################################################
    #
    # Simulating: packResults
    # Task:
    #    pack results on remote computer into tar file to download them later on

    def packResults( self ):   
         
        if self._subject.getLocation() == 'remote':
            utilities.message( type='INFO', text='Pack results ' + self._item.getNameString() )

            if os.path.exists ( self._item.getDirectory() ):
                myTarfile = self._item.getDirectory() + 'results.tar'  
                if os.path.isfile( myTarfile ):
                    os.remove( myTarfile )

                os.chdir(self._item.getDirectory())
                try:
                    tar = tarfile.open( myTarfile, 'w')
                except:
                    utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] )
                else:
                    for extension in configurationShared.outputFileEndings:   
                        for file in os.listdir( self._item.getDirectory()  ):
                            if file.endswith('.' + extension):
                                tar.add( file )    
                    tar.close()
            else:     
                utilities.message( type='ERROR', text='Directory missing' )
        else:
            utilities.message( type='INFO', text=self._subject.getComputer() + ' is local - Nothing done' )            
            
    #################################################################
    #  Simulating: Wait
    #  Task:
    #      Wait until outputFile exists
    #
                                   
    def wait( self ):   

        utilities.message( type='INFO', text='Waiting for output file ' + self._item.getNameString() )
        #
        waitForFile(self._item.getDirectory() + configurationCustomized.outputFile)

    #################################################################
    #  Simulating: storeAsReference
    #  Task:
    #      copy results into reference folder
    #      (generates folder for references if it does not exist)
    #      each computer, case, branch has own reference folder

    def storeResultsAsReference(self):

        utilities.message(type='INFO', text='Store results as reference ' + self._item.getNameString())

        referenceDirectory = utilities.adaptPath( self._subject.getDirectory() + "references\\" + self._item.getType() + "\\" + self._item.getCase() + "\\" +self._item.getConfiguration() + "\\" )
        if not os.path.exists(referenceDirectory):
            os.makedirs(referenceDirectory)


        if os.path.exists(self._item.getDirectory()):
            for extension in configurationShared.outputFileEndings:
                for file in os.listdir(self._item.getDirectory()):
                    if file.endswith('.' + extension):
                        copyfile(self._item.getDirectory() + file , referenceDirectory + file)

        else:
            utilities.message(type='ERROR', text='Directory missing')

    #################################################################
    #  Simulating: compareResultsWithReference
    #  Task:
    #      compare results with results in reference folder for regression tests
    #

    def compareResultsWithReference(self):

        utilities.message(type='INFO', text='Compare result files with references ' + self._item.getNameString())

        referenceDirectory = utilities.adaptPath(
            self._subject.getDirectory() + "references\\" + self._item.getType() + "\\" + self._item.getCase() + "\\" + self._item.getConfiguration() + "\\")

        if not os.path.exists(referenceDirectory):
            utilities.message(type='ERROR', text='Directory with reference files missing')
            return

        if os.path.exists(self._item.getDirectory()):

            open(referenceDirectory + 'deviations.log', 'w').close()  # clear file content

            for file in os.listdir(referenceDirectory):
                if not file == configurationCustomized.outputFile and not file == 'deviations.log' :
                    equal = cmp(self._item.getDirectory() + file, referenceDirectory + file)
                    if not equal:
                        utilities.message(type='INFO', text= 'Deviating file: ' + file)
                        with open(utilities.adaptPath(self._subject.getDirectory() + 'references\\deviatingFiles.log'), 'a') as f:
                            f.write(self._item.getDirectory() + file + '\n')

                        with open(referenceDirectory + 'deviations.log', 'a') as f, open(self._item.getDirectory() + file, 'r') as f1, open(referenceDirectory + file, 'r') as f2:
                            f.write('------------------------------------------------------------------------------\n')
                            f.write(file + '\n')
                            diff = difflib.ndiff(f1.readlines(), f2.readlines())
                            for line in diff:
                                if line.startswith('-'):
                                    f.write(line)
                                elif line.startswith('+'):
                                    f.write('\t\t' + line)
                            #for i, line in enumerate(diff):
                            #    if line.startswith(' '):
                            #        continue
                            #    f.write('Line {}: {}'.format(i, line))
        else:
            utilities.message(type='ERROR', text='Directory missing')

#################################################################
#  icbc class Plotting    
#
        

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
        if subject.getLocation() == 'remote':
            self._operationList.append( '    (g)et results' )
        self._operationList.append( '    (p)replot' )
        self._operationList.append( '    generate (j)pg' )  
        self._operationList.append( '    replace (n)ans and inds' )
        self._operationList.append( '    (c)lear folder' )      
        self._operationList.append( '    (w)ait' )                        
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
            self.generateJpg()  
        elif self._selectedOperation == 'n':
            self.replaceNansAndInds()   
        elif self._selectedOperation == 'c':
            self.clearFolder()         
        elif self._selectedOperation == 'w':
            self.wait()                                                                                                              
        else:
            utilities.message( type='ERROR', notSupported='Operation ' + self._selectedOperation )             
            
            
                                                          
    #################################################################
    #  Plotting: getResults
    #  Task:
    #      download and unpack tar file from remote to local computer, than convert files into dos-format  
    #
                                   
    def getResults( self ):   
 
        if self._subject.getLocation() == 'remote':
            utilities.message( type='INFO', text='Get results ' + self._item.getNameString() )

            mod = __import__( self._subject.getComputer() )   
            # make repository folder if it does not exist                
            repositoryList = [ 'testingEnvironment', self._subject.getComputer(), self._subject.getCode(), self._subject.getBranch(), 'examples', 'files', self._item.getType(), self._item.getCase(), self._item.getConfiguration() ]                   
            utilities.generateFolder( configurationCustomized.rootDirectory, repositoryList )
            
            if os.path.exists ( self._item.getDirectory() ):      
                # clear local directory
                files = glob.glob( self._item.getDirectory() + '*' )
                for file in files:
                    os.remove(file)
                # download with winscp     
                utilities.message( type='INFO', text='    Download' )
                myWinscpFile = utilities.adaptPath( configurationCustomized.rootDirectory + '\\testingEnvironment\\scripts\\icbc\\customized\\winscp_downloadResults.txt' ) 
                myTarfile = self._item.getDirectorySelectedComputer() + 'results.tar'      
                try:
                    f = open( myWinscpFile, 'w' ) 
                except OSError as err:
                    utilities.message( type='ERROR', text='OS error: {0}'.format(err) ) 
                else:
                    f.write( 'option batch abort \n' )
                    f.write( 'option confirm off \n' )
                    f.write( 'open sftp://' + self._subject.getUser() + ':' + mod.pwd + '@' + self._subject.getHostname() + '/ \n' )
                    f.write( 'get ' + myTarfile + ' ' + self._item.getDirectory() + ' \n' )     
                    f.write( 'exit' )            
                    f.close()

                try:
                    subprocess.check_call( configurationCustomized.winscp + ' /script=' + myWinscpFile )    
                except:
                    utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] )      
                # unpack
                print(' ')
                utilities.message( type='INFO', text='    Unpack' )
                myLocalTarFile = self._item.getDirectory() + 'results.tar' 
                if os.path.isfile( myLocalTarFile ): 
                    os.chdir( self._item.getDirectory() )  
                    try:           
                        tar = tarfile.open( myLocalTarFile )
                    except:
                        utilities.message( type='ERROR', text='Tar call failed' )   
                    else:    
                        tar.extractall()
                        tar.close()  
                        os.remove( myLocalTarFile )
                       
                # unix2dos
                utilities.message( type='INFO', text='    Convert to dos' )
                for file in os.listdir( self._item.getDirectory() ): 
                    utilities.unix2dos( file )
            else:
                utilities.message( type='ERROR', text='Directory missing' )
        else:
            utilities.message( type='INFO', text=self._subject.getComputer() + ' is local - Nothing done' )
                                            
    #################################################################
    #  Plotting: replaceNansAndInds
    #  Task:
    #      replace each nan by 999 and remove each IND in all tec files 
    
                                   
    def replaceNansAndInds( self ):    
     
        utilities.message( type='INFO', text='Replace nans and inds' + self._item.getNameString() )
     
        if os.path.exists ( self._item.getDirectory() ):                               
            os.chdir(self._item.getDirectory()) 
            for file in os.listdir( self._item.getDirectory() ): 
                if file.endswith( '.tec' ):
                    utilities.message( type='INFO', text='File: ' + file )  
                    try:
                        infile = open(file,'r') 
                        outfile = open( 'new_' + file, 'w') 
                    except OSError as err:
                        utilities.message( type='ERROR', text='OS error: {0}'.format(err) )
                    else:
                        for line in infile: 
                            line = line.replace( 'nan', '999' )
                            line = line.replace( '#IND', '' )
                            outfile.write(line) 
                        infile.close() 
                        outfile.close()         
                        shutil.move('new_' + file, file)                
        else:
            utilities.message( type='ERROR', text='Directory missing' )                                        

    #################################################################
    #  Plotting: preplot
    #  Task:
    #      call preplot to generate *.plt's          
    #
  
    def preplot( self ): 
    
        utilities.message( type='INFO', text='Preplot ' + self._item.getNameString() )

        if os.path.exists ( self._item.getDirectory() ): 
            os.chdir(self._item.getDirectory()) 
            for file in os.listdir( self._item.getDirectory() ): 
                if file.endswith( '.tec' ):
                    utilities.message( type='INFO', text='File: ' + file )                                          
                    try:            
                        subprocess.call(configurationCustomized.preplot + ' ' + self._item.getDirectory() + file, shell=True ) 
                    except:
                        utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] )                
     
        else:
            utilities.message( type='ERROR', text='Directory missing' ) 
             
    #################################################################
    #  Plotting: generateJpgs
    #  Task:
    #      generate JPG with tecplot           
    #
                                   

    def generateJpg( self ):         

        utilities.message( type='INFO', text='Generate Jpg ' + self._item.getType() )
   
        if os.path.exists ( self._subject.getPlotDirectory() ): 

            layout = self._subject.getPlotDirectory()  + self._item.getType() + '.lay'
              
            os.chdir( self._subject.getPlotDirectory() )
            try:
                f = open( self._subject.getPlotDirectory() + '_genJPG.mcr', 'w' )
            except OSError as err:
                    utilities.message( type='ERROR', text='OS error: {0}'.format(err) )
            else:
                f.write( '#!MC 1300\n' )
                f.write( '#-----------------------------------------------------------------------\n' )
                f.write( '$!EXPORTSETUP EXPORTFORMAT = JPEG\n' )
                f.write( '$!EXPORTSETUP IMAGEWIDTH = 1500\n' )
                f.write( '#-----------------------------------------------------------------------\n' )
                f.write( "$!EXPORTSETUP EXPORTFNAME = \'" + self._subject.getPlotDirectory() + "results_" + self._item.getType() + ".jpg\'\n" )
                f.write( '$!EXPORT\n' )
                f.write( 'EXPORTREGION = ALLFRAMES\n' )
                f.close()
                print (configurationCustomized.tecplot + ' ' + layout + ' -b -p ' + self._subject.getPlotDirectory() + '_genJPG.mcr')
                try:
                    subprocess.call( configurationCustomized.tecplot + ' ' + layout + ' -b -p ' + self._subject.getPlotDirectory() + '_genJPG.mcr', shell=True ) 
                except:
                    utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] ) 

                utilities.removeFile( self._subject.getPlotDirectory() + '_genJPG.mcr' )           
  
        else:
            utilities.message( type='ERROR', text='Directory missing' )    
            
            
    #################################################################
    #  Plotting: clearFolder
    #  Task:
    #      delete *.tec, *.txt, *.asc, *plt and results.tar       
    #      (local folder for remote computer)
                                   
    def clearFolder( self ):   

        utilities.message( type='INFO', text='Clear plotting folder ' + self._item.getNameString() )
        #
        utilities.removeFile( self._subject.getPlotDirectory() + "results_" + self._item.getType() + ".jpg" )

        if os.path.exists ( self._item.getDirectory() ):
            for file in os.listdir( self._item.getDirectory() ):
                for ending in configurationShared.outputFileEndings: 
                    if file.endswith( '.' + ending ):
                        if self._subject.getLocation() == 'remote' or not (ending =='tec'):    # do not delete tec if local
                            utilities.removeFile( self._item.getDirectory() + file ) 
                                      
                #myLocalTarFile = self._item.getDirectory() + 'results.tar'  # done in getResults()
                #if os.path.isfile( myLocalTarFile ): 
                #    os.remove( myLocalTarFile )

        else:
            utilities.message( type='ERROR', text='Directory missing' )           
        #if configurationCustomized.location == 'remote':
        #    for file in os.listdir( self._item.getLocalDirectory() ):
        #        for ending in configurationShared.outputFileEndings: 
        #            if file.endswith( '.' + ending ):
        #                os.remove( self._item.getLocalDirectory() + file ) 

    #################################################################
    #  Plotting: Wait
    #  Task:
    #      Wait until jpg file exists
    #
                                   
    def wait( self ):   

        utilities.message( type='INFO', text='Waiting for jpg file ' + self._item.getType() )
        #
        waitForFile(self._subject.getPlotDirectory() + "results_" + self._item.getType() + ".jpg" )

 #################################################################
 #  Wait
 #  Task:                                             
 #      Used by members to wait until a file exists
 #      prints a dot each second when waiting

def waitForFile( fileName ):

    sys.stdout.flush()
    start = time.time()

    i=1
    while (not os.path.exists( fileName )):
        if ( time.time()-start > i):
            sys.stdout.write('.')
            sys.stdout.flush()
            i=i+1
            

          