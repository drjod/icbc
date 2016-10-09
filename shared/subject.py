import item
import utilities, configurationShared
import platform
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized

#################################################################
# icbc class Subject
# Task:
#     hosts data that depend on 
#     1. platform (operating system, directories, user) 
#     2. tested subject (code, branch, ...)   
#     (TODO: split both parts and put later in folder customized)
#

class Subject:  
     
    __directory = None
    __operatingSystem = None
    __location = None
    __rootDirectory = None
    __plotDirectory = None
    __gateDirectory = None  # to transfer files between local and remote

    ##################################################################
    #  Subject: constructor
    #
    
    def __init__( self, superuser, computer , user, code, branch ):
        
        self.__superuser = superuser
        self.__computer = computer
        self.__user = user
        self.__code = code
        self.__branch = branch

    #################################################################
    #  Subject: destructor
    #
    
    def __del__( self ):
        pass   
 
    #################################################################
    #  Subject: getter
    #                 
                                    
    def getComputer( self ):
        return self.__computer    
    def getUser( self ):
        return self.__user  
    def getCode( self ):
        return self.__code  
    def getBranch( self ):
        return self.__branch
    def getLocation( self ):
        return self.__location                      
    def getDirectory( self ):
        return self.__directory 
    def getRootDirectory( self ):
        return self.__rootDirectory
    def getPlotDirectory( self ):
        return self.__plotDirectory
    def getGateDirectory( self ):
        return self.__gateDirectory
    def getOperatingSystem( self ):
        return self.__operatingSystem 
    def getHostname( self ):
        return self.__hostname
                
    #################################################################
    #  Subject: 
    #  Setter - used in reselect
 
    def setComputer( self, computer ):
        self.__computer = computer   
    def setUser( self, user ):
        self.__user = user          
    def setCode( self, code ):
        self.__code = code 
    def setBranch( self, branch ):
        self.__branch = branch
                               
    def select( self, setting_inst ):
    
        if not self.__computer:                                                                                 
            self.__computer = setting_inst.setNames( 'computer' )[0]    # only one entry in list here and in the following 
        if not self.__superuser:        
            if not self.__user:                                                                                 
                self.__user = setting_inst.setNames( 'user' )[0]    
        else:
            self.__user = setting_inst.getUser( self.__superuser, self.__computer )
                                 
        if not self.__code:                                                                                 
            self.__code = setting_inst.setNames( 'codes' )[0]        
        if not self.__branch:                                                                                 
            self.__branch = setting_inst.setNames( 'branches' )[0] 
 
        if configurationCustomized.location == 'local':
            self.__rootDirectory = setting_inst.getRootDirectory( self.__computer, self.__user ) 
            self.__location = setting_inst.getLocation( self.__computer )
            self.__operatingSystem = setting_inst.getOperatingSystem( self.__computer )
            #self.__directory = utilities.adaptPath( self.__rootDirectory + 'testingEnvironment\\' + self.__computer + '\\' + self.__code + '\\' + self.__branch + '\\' )
            #self.__gateDirectory = utilities.adaptPath( self.__rootDirectory + 'testingEnvironment\\' + self.__computer + '\\gate\\' )
            self.__plotDirectory = utilities.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\' + self.__computer + '\\' + self.__code + '\\' + self.__branch + '\\examples\\plots\\' )  
            self.__hostname = setting_inst.getHostname( self.__computer )
        else:
            self.__location = 'remote'

        self.__directory = utilities.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\' + self.__computer + '\\' + self.__code + '\\' + self.__branch + '\\' )
        self.__gateDirectory = utilities.adaptPath(configurationCustomized.rootDirectory + 'testingEnvironment\\' + self.__computer + '\\gate\\' )

        #utilities.message( type='INFO', text=self.__directory )


              
    #################################################################
    #  Subject: getExecutableForRelease
    #  Task:
    #      Store executables         
                
    def getExecutableForRelease( self, item ):
           
        if platform.system() == 'Windows':
            return self.__directory + 'releases\\' + self.__code + '_' + self.__branch + '_' + platform.system() + '_' + item.getConfiguration() + '.exe'  
        elif platform.system() == 'Linux':
            return self.__directory + 'releases/' + self.__code + '_' + self.__branch + '_' + platform.system() + '_' + item.getConfiguration()
        else:
            utilities.message( type='ERROR', notSupported=platform.system() )
                    
    #################################################################
    #  Subject: getExecutable
    #  Task:
    #        used to run code           
                
    def getExecutable( self, item ):
        if platform.system() == 'Windows':
            if self.__code == 'ogs': 
                return self.__directory + 'Build_' + item.getConfiguration() + '\\' + '\\bin\\Release\\ogs.exe'
            else:
                utilities.message( type='ERROR', notSupported=self.__code) 
        elif platform.system() == 'Linux':
            if self.__code == 'ogs':
                return self.__directory + 'Build_Release_' + configurationCustomized.compiler + '/' + item.getConfiguration() + '/bin/ogs_' + item.getConfiguration()
            else:
                utilities.message( type='ERROR', notSupported=self.__code)                        
        else:
            utilities.message( type='ERROR', notSupported=platform.system() )
   
            
    #################################################################
    #  Subject:
    #  Task:
    #      Sets build command according to platform 
    #              
               
    def getBuildCommand( self, item ):
    
        if platform.system() == 'Windows':    
            return configurationCustomized.localBuild + ' ' + self.__computer + ' ' + self.__code + ' ' + self.__branch + ' ' + item.getConfiguration()
            # + ' ' + configurationCustomized.visualStudio
        elif platform.system() == 'Linux':
            return configurationCustomized.rootDirectory + 'testingEnvironment/scripts/' + 'compileInKiel.sh ' + self.getDirectory() + ' ' + item.getConfiguration() + ' Release'
        else:
            utilities.message( type='ERROR', notSupported=platform.system() )                                                                          

    #################################################################
    #  Subject:
    #  Task:
    #      Sets command to run test case according to platform 
    #              
               
    def getItemExecutionCommand( self, item ):
    

        if configurationCustomized.location == 'local':
            if platform.system() == 'Windows':
                return configurationCustomized.localRun + ' ' + self.__computer + ' ' + self.__code + ' ' + self.__branch + ' ' + item.getType() + ' ' + item.getCase() + ' ' + item.getConfiguration() + ' ' + configurationShared.examplesName
            elif platform.system() == 'Linux':
                return self.__directory + 'Build_Release_' + configurationCustomized.compiler + '/' + item.getConfiguration() + '/bin/ogs_' + item.getConfiguration() + ' ' + item.getDirectory() + '/' + configurationShared.examplesName + ' > ' + item.getDirectory() + '/' + configurationCustomized.outputFile
            else:
                utilities.message(type='ERROR', notSupported=platform.system())
                return -1
        elif configurationCustomized.location == 'remote':
            return 'qsub ' + item.getDirectory() + 'run.pbs'
        else:
            utilities.message(type='ERROR', notSupported=configurationCustomized.location)
            return -1