import item
import message
import configurationShared
import platform
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized

class Subject:  
     
    __directory = ''
    __operatingSystem = ' '
    __location = ' '
    __rootDirectory = ''
    __plotDirectory = ''
    __gateDirectory = ''

    ##############################################
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
    
        if self.__computer == ' ':                                                                                 
            self.__computer = setting_inst.selectGroup( 'computer' )[0]    # only one entry in list here and in the following 
        if self.__superuser == ' ':        
            if self.__user == ' ':                                                                                 
                self.__user = setting_inst.selectGroup( 'user' )[0]    
        else:
            self.__user = setting_inst.getUser( self.__superuser, self.__computer )
                                 
        if self.__code == ' ':                                                                                 
            self.__code = setting_inst.selectGroup( 'codes' )[0]        
        if self.__branch == ' ':                                                                                 
            self.__branch = setting_inst.selectGroup( 'branches' )[0] 
 
        if configurationCustomized.location == 'local':
            self.__rootDirectory = setting_inst.getRootDirectory( self.__computer, self.__user ) 
            self.__location = setting_inst.getLocation( self.__computer )
            self.__operatingSystem = setting_inst.getOperatingSystem( self.__computer )
            self.__directory = self.adaptPath( self.__rootDirectory + '\\testingEnvironment\\' + self.__computer + '\\' + self.__code + '\\' + self.__branch + '\\' )
            self.__gateDirectory =  self.adaptPath( self.__rootDirectory + '\\testingEnvironment\\' + self.__computer + '\\gate\\' ) 
            self.__plotDirectory =  self.adaptPath( configurationCustomized.rootDirectory + '\\testingEnvironment\\' + self.__computer + '\\' + self.__code + '\\' + self.__branch + '\\examples\\plots\\' )  
            self.__hostname = setting_inst.getHostname( self.__computer )
        else:
            self.__location = 'remote'
            self.__directory = self.adaptPath( configurationCustomized.rootDirectory + '\\testingEnvironment\\' + self.__computer + '\\' + self.__code + '\\' + self.__branch + '\\' )
            self.__gateDirectory =  self.adaptPath( configurationCustomized.rootDirectory + '\\testingEnvironment\\' + self.__computer + '\\gate\\' )                                                              
        #message.console( type='INFO', text=self.__directory )

    #################################################################
    #  Subject: adaptPath
    #  Task:
    #      converts windows path into linux (unix) according to platform where script runs
    #
        
    def adaptPath( self, path ):   
        if platform.system() == 'Windows':  
            return path  
        elif platform.system() == 'Linux':
            return path.replace( '\\', '/' )              
        else:
            message.console( type='ERROR', notSupported=platform.system() )
            
    #################################################################
    #  Subject: adaptPathSelectedComputer
    #  Task:
    #      converts windows path into linux (unix) and vice verca according to platform of selected computer
    #      used for plotting operations (all local while simulation operations might be remote)
        
    def adaptPathSelectedComputer( self, path ):   
        if self.__operatingSystem == 'windows':  
            return path.replace( '/', '\\' )   
        elif self.__operatingSystem == 'linux':
            return path.replace( '\\', '/' )              
        else:
            message.console( type='ERROR', notSupported=self.__operatingSystem )
                        
    #################################################################
    #  Subject: generate Folder
    #  Task:
    #     called if folder is missing 
    #        
        
    def generateFolder( self, root, folderList ):  
     
        path = root  
        for folder in folderList:   
            path =  self.adaptPath( path + '\\' + folder   )
        
            try:
                os.stat( path )
            except:
                os.mkdir( path ) 
                
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
            message.console( type='ERROR', notSupported=platform.system() )
                    
    #################################################################
    #  Subject: getExecutable
    #  Task:
    #        used to run code           
                
    def getExecutable( self, item ):
        if platform.system() == 'Windows':
            if self.__code == 'ogs': 
                return self.__directory + 'Build_' + item.getConfiguration() + '\\' + '\\bin\\Release\\ogs.exe'
            else:
                message.console( type='ERROR', notSupported=self.__code) 
        elif platform.system() == 'Linux':
            if self.__code == 'ogs':
                return self.__directory + 'Build_Release_intel1502' + '/' + item.getConfiguration() + '/bin/ogs_' + item.getConfiguration()
            else:
                message.console( type='ERROR', notSupported=self.__code)                        
        else:
            message.console( type='ERROR', notSupported=platform.system() )
   
            
    #################################################################
    #  Subject:
    #  Task:
    #      Sets compilation command according to platform 
    #              
               
    def getCompilationCommand( self, item ):
    
        if platform.system() == 'Windows':
            return configurationCustomized.visualStudio + ' ' + item.getDirectory() + 'OGS.sln' +  ' /build release ' + item.getDirectory() + 'OGS.sln' # change item to subject???
        elif platform.system() == 'Linux':
            return configurationCustomized.rootDirectory + 'testingEnvironment/scripts/' + 'compileInKiel.sh ' + self.getDirectory() + ' ' + item.getConfiguration() + ' Release'
        else:
            message.console( type='ERROR', notSupported=platform.system() )                                                                          

                         