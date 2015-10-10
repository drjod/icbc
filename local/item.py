# import os
# import configurationLocal
import subject
import message 
import setting

class Item:  
    
    ##############################################
    #  item: constructor
    #
    
    def __init__( self, subject, configuration, directory ):     
        self._subject = subject
        self._configuration = configuration
        self._directory = directory
        
        #message.console( type='INFO', text='item ' + configuration )
                              
        #self.__levelsRepository = [ self.__rootDirectory, 'testingEnvironment', name, 'repository', self.__cType, self.__cCase ] 
        #self.__levelsitem = [ self.__rootDirectory), 'testingEnvironment', name, code, branch, 'items', 'files', self.__cType, self.__cCase, self.__cConfiguration ]    

    #################################################################
    #  Subject: destructor
    #
    
    def __del__( self ):
        del self._subject   
                  
    def getSubject( self ):
        return self._subject 
    def getConfiguration( self ):
        return self._configuration                                        
    def getDirectory( self ):
        return self._directory 

#################################################################
                                            
class Test(Item):
        
    def __init__( self, subject, example ):
    
        self.__type = example.type
        self.__case = example.case        
        self.__directoryRepository = subject.adaptPath( subject.getRootDirectory() + 'testingEnvironment\\'+ subject.getComputer() \
                                                        + '\\repository\\' + example.type + '\\' + example.case + '\\' )
             
        # message.console( type='INFO', text='item ' + self.getNameString() ) 
         
        Item.__init__( self, subject, example.configuration,
                       subject.adaptPath( subject.getDirectory() + 'examples\\files\\' \
                                          + example.type + '\\' + example.case + '\\' + example.configuration + '\\' ) # test case directory
                     )
        
    def getDirectoryRepository( self ):
        return self.__directoryRepository  
               
    def getNameString( self ): 
        return self.__type + ' ' + self.__case + ' ' + self._configuration
    
        
                            
    def select( self, setting ):
            
        if self.__type == '':                                                                                 
            self.__type = setting.selectName( 'types' )       
        if self.__case == '':                                                                                 
            self.__case = setting.selectName( 'cases' )               
        if self._configuration == '':                                                                                 
            self._configuration = setting.selectName( 'configurations', self._subject.getComputer() )
                    

                    
                    
#################################################################
        
class Build(Item):        
 
    def __init__( self, subject, configuration ):

  
        Item.__init__( self, subject, configuration,
                           subject.adaptPath( subject.getDirectory() + 'sources\\' + 'Build_' + configuration + '\\' )  # build item directory
                         )   

                   
                                 
    def select( self, setting ):
                         
        if self._configuration == '':                                                                                 
            self._configuration = setting.selectName( 'configurations', self._subject.getComputer() )    
            
             