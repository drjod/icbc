import item
import message
import configurationShared
import platform
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized

class Subject:  
     
    __directory = ''
    
    ##############################################
    #  Subject: constructor
    #
    
    def __init__( self, computer , user, code, branch ):
        
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
                      
    def getDirectory( self ):
        return self.__directory 
        
    #################################################################
    #  Subject: 
    #  Setter 
 
    #def setComputer( self, computer ):
    #    self.__computer = computer    
    #def setCode( self, code ):
    #    self.__code = code 
    #def setBranch( self, branch ):
    #    self.__branch = branch
                               
    def select( self, setting_inst ):
    
        if self.__computer == ' ':                                                                                 
            self.__computer = setting_inst.selectGroup( 'computer' )[0]    # only one entry in list here and in the following     
        if self.__user == ' ':                                                                                 
            self.__user = setting_inst.selectGroup( 'user' )[0]               
        if self.__code == ' ':                                                                                 
            self.__code = setting_inst.selectGroup( 'codes' )[0]        
        if self.__branch == ' ':                                                                                 
            self.__branch = setting_inst.selectGroup( 'branches' )[0] 

        self.__directory = self.adaptPath( configurationCustomized.rootDirectory + '\\testingEnvironment\\' + self.__computer + '\\' + self.__code + '\\' + self.__branch + '\\' )
                                                                            
        message.console( type='INFO', text=self.__directory )

    #################################################################
    #  Subject: path
    #  Task:
    #      converts windows path into linux (unix)
    #
        
    def adaptPath( self, path ):   
        if platform.system() == 'Windows':  
            return path  
        elif platform.system() == 'Linux':
            path = path.replace( '\\', '/' )
            return path               
        else:
            message.console( type='ERROR', notSupported=platform.system() )
            
            
    #################################################################
    #  Subject: generate Folder
    #  Task:
    #      
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
    #  Subject: ExecutableToRelease
    #  Task:
    #      
    #        item can be build or test           
                
    def getExecutableForRelease( self, item ):
           
        if platform.system() == 'Windows':
            return self.__directory + 'releases\\' + self.__code + '_' + self.__branch + '_' + platform.system() + '_' + item.getConfiguration() + '.exe'  
        elif platform.system() == 'Linux':
            return self.__directory + 'releases/' + self.__code + '_' + self.__branch + '_' + platform.system() + '_' + item.getConfiguration()
        else:
            message.console( type='ERROR', notSupported=platform.system() )
                    
    #################################################################
    #  Subject: Executable
    #  Task:
    #       item can be build or test  
    #      to do: intel compiler name, check if exe exists             
                
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
    #      
    #              
               
    def getCompilationCommand( self, item ):
    
        if platform.system() == 'Windows':
            return configurationCustomized.visualStudio + ' ' + item.getDirectory() + 'OGS.sln' +  ' /build release ' + item.getDirectory() + 'OGS.sln' # change item to subject???
        elif platform.system() == 'Linux':
            return self.getDirectory() + 'compileInKiel.sh ' + self.getDirectory() + ' ' + item.getConfiguration() + ' Release' 
        else:
            message.console( type='ERROR', notSupported=platform.system() )                                                                          

    #################################################################
    #  Subject:
    #  Task:
    #      nor used
    #              
    #           self.__subject.getExecutable() + ' ' + self.__directoryInstance + configurationShared.itemsName
    
    def getRunCommand( self, test ):
    
        pass
        #if platform.system() == 'Windows':           
        #    return configurationCustomized.visualStudio + ' ' + buildDirectory + 'OGS.sln' +  ' /build release ' + buildDirectory + 'OGS.sln'
        #elif platform.system() == 'Linux':
        #    return 'make -C ' + self.__rootDirectory + 'sources/' + 'Build_' + configuration + '/make'
        #else:
        #    message.console( type='ERROR', notSupported=platform.system() )                            