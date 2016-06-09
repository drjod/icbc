import subject, item, simulationData
import utilities, configurationShared
import platform, subprocess, shutil, tarfile, fileinput
import imp, sys, os, glob
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
    #      direct to cluster or reload data files (if necessary) and do operation
    #

    def run( self, item, simulationData, level ):

        self._simulationData = simulationData
        if self._subject.getLocation() == 'remote' and configurationCustomized.location == 'local' and not self._selectedOperationType == 'p':
            
            gateToCluster.operate( self._subject, item, 
                                   self._selectedOperationType, self._selectedOperation, self._simulationData, 
                                   level
                                 ) 
        else:   

            self._simulationData .reloadDataFiles()   
            if self._selectedOperationType == 'b':   # building
                self.operate( item )   
            else:  # simulating or plotting
                if int(level) <= int( configurationShared.testingLevel ):
                    self.operate( item )  
                else:    
                    utilities.message( type='INFO', text= 'Case ' + item.getCase() + ' has level ' + level + ' - testing level is ' + configurationShared.testingLevel )               
                        
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
            utilities.message( type='ERROR', notSupported='Operation ' + self.__selectedOperation )                          
  
    #################################################################
    #  Building: run
    #  Task:
    #      run one of the selected test items with selected code
    #
                                   
    def compileRelease( self ): 
        utilities.message( type='INFO', text='Compiling ' + self._item.getConfiguration()  )
        try:
            if platform.system() == 'Windows':       
                subprocess.check_call( self._subject.getCompilationCommand( self._item ) )   
            elif platform.system() == 'Linux':
                subprocess.Popen(self._subject.getCompilationCommand( self._item ), shell=True)   
            else:
                utilities.message( type='ERROR', notSupported=platform.system() )  
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
        self._operationList.append( '    write (n)um' )
        self._operationList.append( '    (c)lean folder from results' )
        if subject.getLocation() == 'remote':
            self._operationList.append( '    (i)mport files from repository (gate)' )
            self._operationList.append( '    e(x)port files to repository (gate)' )
            self._operationList.append( '    write (p)bs' )
            self._operationList.append( '    (m)esh partition' )
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
        elif self._selectedOperation == 'n':
            self.writeNum()               
        elif self._selectedOperation == 'c':
            self.cleanFolder()             
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
        elif self._selectedOperation == 'p' and self._subject.getLocation() == 'remote':
            self.writePbs()  
        elif self._selectedOperation == 'm' and self._subject.getLocation() == 'remote':
            self.meshPartition()  
        elif self._selectedOperation == 'k' and self._subject.getLocation() == 'remote':
            self.packResults()   
        elif self._selectedOperation == '0':       
            utilities.message( type='INFO', text='No Operation' )                                                                         
        else:
            utilities.message( type='ERROR', notSupported='Operation ' + self._selectedOperation ) 
       
    #################################################################
    #  Simulating: runTest
    #  Task:
    #      run code
    #
                                   
    def runTest( self ): 
        
        utilities.message( type='INFO', text='Running ' + self._item.getNameString() )

        if os.path.exists ( self._item.getDirectory() ):                           
            os.chdir(self._item.getDirectory())  # permits call of addtional (chemical) solver 
            if platform.system() == 'Windows':        
                with open ( self._item.getDirectory() + 'out.txt', 'wb' ) as f:
                    try:
                        subprocess.check_call( self._subject.getExecutable( self._item ) + ' ' + self._item.getDirectory() + configurationShared.examplesName, stdout=f )   
                    except:
                        utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] )
            elif platform.system() == 'Linux':
                if os.path.isfile( self._item.getDirectory() + 'run.pbs' ): 
                    try:
                        subprocess.Popen('qsub ' + self._item.getDirectory() + 'run.pbs', shell=True)
                    except:
                        utilities.message( type='ERROR', text='%s' % sys.exc_info()[0]  )
                else:
                    utilities.message( type='ERROR', text='Pbs missing' )                         
            else:
                utilities.message( type='ERROR', notSupported=platform.system() )  
              
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
    #  Simulating: cleanFolder
    #  Task:
    #      delete *.tec, *.txt, *.plt, *.vtk and results.tar       
    #      (remote folder for remote computer)
                                   
    def cleanFolder( self ):   

        utilities.message( type='INFO', text='Clean simulation folder ' + self._item.getNameString() )
        #
        if os.path.exists ( self._item.getDirectory() ):
            for file in os.listdir( self._item.getDirectory() ):
                for ending in configurationShared.outputFileEndings: 
                    if file.endswith( '.' + ending ):
                        os.remove( self._item.getDirectory() + file ) 
                
                myRemoteTarFile = self._item.getDirectory() + 'results.tar' 
                if os.path.isfile( myRemoteTarFile ): 
                    os.remove( myRemoteTarFile )

        else:
            utilities.message( type='ERROR', text='Directory missing' )           
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
         
        utilities.message( type='INFO', text='Pack results ' + self._item.getNameString() )

        if self._subject.getLocation() == 'remote':
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
        self._operationList.append( '    (c)lean folder' )                    
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
            self.cleanFolder()                                                                                                     
        else:
            utilities.message( type='ERROR', notSupported='Operation ' + self._selectedOperation )             
            
            
                                                          
    #################################################################
    #  Plotting: getResults
    #  Task:
    #      download and unpack tar file from remote to local computer, than convert files into dos-format  
    #
                                   
    def getResults( self ):   
 
        utilities.message( type='INFO', text='Get results ' + self._item.getNameString() )

        mod = __import__( self._subject.getComputer() )   
        # make repository folder if it does not exist                
        repositoryList = [ 'testingEnvironment', self._subject.getComputer(), self._subject.getCode(), self._subject.getBranch(), 'examples', 'files', self._item.getType(), self._item.getCase(), self._item.getConfiguration() ]                   
        utilities.generateFolder( configurationCustomized.rootDirectory, repositoryList )
           
        if self._subject.getLocation() == 'remote':
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
    #  Plotting: replaceNans
    #  Task:
    #      replace each nan by 999 in all tec files 
    
                                   
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
    #            #with fileinput.FileInput( self._item.getLocalDirectory() + file, inplace=True ) as fileToSearchIn:
    #            #    for line in fileToSearchIn:
    #            #        print( line.replace( 'nan', '999' ))

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
                    # replace nans
                    #infile = open(file,'r') 
                    #outfile = open( 'new_' + file, 'w') 
                    #for line in infile: 
                    #    line = line.replace( 'nan', '999' )
                    #    outfile.write(line) 
                    #infile.close() 
                    #outfile.close()         
                    #shutil.move('new_' + file, file)                     
                     
                    try:            
                        subprocess.check_call(configurationCustomized.preplot + ' ' + self._item.getDirectory() + file ) 
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
                    subprocess.check_call( configurationCustomized.tecplot + ' ' + layout + ' -b -p ' + self._subject.getPlotDirectory() + '_genJPG.mcr' ) 
                except:
                    utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] ) 

                os.remove( self._subject.getPlotDirectory() + '_genJPG.mcr' )           
  
        else:
            utilities.message( type='ERROR', text='Directory missing' )    
            
            
    #################################################################
    #  Plotting: cleanFolder
    #  Task:
    #      delete *.tec, *.txt, *.asc, *plt and results.tar       
    #      (local folder for remote computer)
                                   
    def cleanFolder( self ):   

        utilities.message( type='INFO', text='Clean plotting folder ' + self._item.getNameString() )
        #
        if os.path.exists ( self._item.getDirectory() ):
            for file in os.listdir( self._item.getDirectory() ):
                for ending in configurationShared.outputFileEndings: 
                    if file.endswith( '.' + ending ):
                        os.remove( self._item.getDirectory() + file ) 
                
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
                                             


          