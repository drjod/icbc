import subject
import message 
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import setting
import configurationCustomized

##############################################
# class Item 
# Task:
#    Parent of Test, Build
#    hosts directory, subject, configuration for specific test case or item if building operation
#

class Item:  

    def __init__( self, subject, configuration, directory ):     
        self._subject = subject
        self._configuration = configuration
        self._directory = directory
 
        #message.console( type='INFO', text='item ' + configuration )
                              
        #self.__levelsRepository = [ self.__rootDirectory, 'testingEnvironment', name, 'repository', self.__cType, self.__cCase ] 
        #self.__levelsitem = [ self.__rootDirectory), 'testingEnvironment', name, code, branch, 'items', 'files', self.__cType, self.__cCase, self.__cConfiguration ]    


    def __del__( self ):
        del self._subject   
    # getter              
    def getSubject( self ):
        return self._subject 
    def getConfiguration( self ):
        return self._configuration                                        
    def getDirectory( self ):
        return self._directory 

#################################################################
#  class Test
#  Task:
#    hosts type case for specific test case
#    used for testing operation
#
                                            
class Test(Item):

    
    def __init__( self, subject, type, case, configuration ):
    
        self.__type = type
        self.__case = case        
        self.__directoryRepository = subject.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\'+ subject.getComputer() \
                                                        + '\\repository\\' + type + '\\' + case + '\\' )           
        # message.console( type='INFO', text='item ' + self.getNameString() ) 
         
        # !!!! change F:
        #if configurationCustomized.location == 'local':
        self.__localDirectory =  'F:\\testingEnvironment\\' + subject.getComputer() + '\\' + subject.getCode() + '\\' + subject.getBranch()  + '\\examples\\output\\' + self.__type + '\\' + self.__case + '\\' + configuration  + '\\'  
        #print(self.__localDirectory)
        Item.__init__( self, subject, configuration,
                       subject.adaptPath( subject.getDirectory() + 'examples\\files\\' \
                                          + type + '\\' + case + '\\' + configuration + '\\' ) # test case directory
                     )
    # getter    
    def getDirectoryRepository( self ):
        return self.__directoryRepository   
    def getLocalDirectory( self ):
        return self.__localDirectory 
                 
    def getNameString( self ): 
        return self.__type + ' ' + self.__case + ' ' + self._configuration   
    def getType( self ):                                                    
        return self.__type       
    def getCase( self ):          
        return self.__case 
                                
        
                           
    #def select( self, setting ):        
    #    if self.__type == ' ':                                                                                 
    #        self.__type = setting.selectName( 'types' )       
    #    if self.__case == ' ':                                                                                 
    #        self.__case = setting.selectName( 'cases' )               
    #    if self._configuration == ' ':                                                                                 
    #        self._configuration = setting.selectName( 'configurations', self._subject.getComputer() )
                    

                    
                    
#################################################################
#  class Build
#  Task:
#      Used for building operation
#      everything is stored in parent class Item
        
class Build(Item):        
 
    def __init__( self, subject, configuration ):

        self.__type = 'no'
        self.__case = 'no'

        Item.__init__( self, subject, configuration,
                           subject.adaptPath( subject.getDirectory() + 'Build_' + configuration + '\\' )  # build item directory
                         )   

    def getType( self ):                                                    
        return self.__type       
    def getCase( self ):          
        return self.__case 
                                                   
    #def select( self, setting ):                       
    #    if self._configuration == ' ':                                                                                 
    #        self._configuration = setting.selectName( 'configurations', self._subject.getComputer() )    
            
             