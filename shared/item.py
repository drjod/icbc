import subject
import utilities 
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized

##############################################
# class Item 
# Task:
#    Parent of Build, Sim, Plot
#    hosts directory, subject, configuration for specific test case or item if building operation
#

class Item:  

    def __init__( self, subject, configuration, directory ):     
        self._subject = subject
        self._configuration = configuration
        self._directory = directory
 
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
#  class Build
#  Task:
#      Used in building operations
        
class Build(Item):        
 
    def __init__( self, subject, configuration ):

        Item.__init__( self, subject, configuration,
                           utilities.adaptPath( subject.getDirectory() + 'Build_' + configuration + '\\' )  
                         )   
                                               
   


#################################################################
#  class Test
#  Task:
#     Parent of Sim and Plot

class Test(Item):

    def __init__( self, subject, type, case, configuration, directory ):
    
        self.__type = type
        self.__case = case  

        # utilities.message( type='INFO', text='item ' + self.getNameString() ) 
        Item.__init__( self, subject, configuration, directory )

    def getNameString( self ): 
        return self.__type + ' ' + self.__case + ' ' + self._configuration   
    def getType( self ):                                                    
        return self.__type       
    def getCase( self ):          
        return self.__case 

#################################################################
#  class Sim
#  Task:
#     Used in simulation operations
                                            
class Sim(Test):

    def __init__( self, subject, type, case, configuration ):
          
        self.__directoryRepository = utilities.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\'+ subject.getComputer() \
                                                        + '\\repository\\' + type + '\\' + case + '\\' )           
     
        Test.__init__( self, subject, type, case, configuration,
                       utilities.adaptPath( subject.getDirectory() + 'examples\\files\\' \
                                          + type + '\\' + case + '\\' + configuration + '\\' ) # test case directory
                     )
    # getter    
    def getDirectoryRepository( self ):
        return self.__directoryRepository   
                                              
        
#################################################################
#  class Plot
#  Task:
#     Used in plotting operations
                                            
class Plot(Test):    
           
    def __init__( self, subject, type, case, configuration ):   
          
        example = type + '\\' 
        if case:
            example = example + case + '\\' 
        if configuration:
            example = example + configuration  + '\\'

        localDirectory =  utilities.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\' + subject.getComputer() + '\\' + subject.getCode() + '\\' + subject.getBranch()  + '\\examples\\files\\' + example )
        self.__directorySelectedComputer = utilities.adaptPathSelectedComputer( subject.getDirectory() + 'examples\\files\\' + example, subject.getOperatingSystem() )
 
        Test.__init__( self, subject, type, case, configuration, localDirectory ) 

    def getDirectorySelectedComputer( self ):
        return self.__directorySelectedComputer


                   
    

           