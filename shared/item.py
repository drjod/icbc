import subject
import message 
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
# import setting
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
                           subject.adaptPath( subject.getDirectory() + 'Build_' + configuration + '\\' )  
                         )   
                                               
   


#################################################################
#  class Test
#  Task:
#     Parent of Sim and Plot

class Test(Item):

    def __init__( self, subject, type, case, configuration, directory ):
    
        self.__type = type
        self.__case = case  
        # message.console( type='INFO', text='item ' + self.getNameString() ) 
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
          
        self.__directoryRepository = subject.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\'+ subject.getComputer() \
                                                        + '\\repository\\' + type + '\\' + case + '\\' )           
     
        Test.__init__( self, subject, type, case, configuration,
                       subject.adaptPath( subject.getDirectory() + 'examples\\files\\' \
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
          
        localDirectory =  subject.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\' + subject.getComputer() + '\\' + subject.getCode() + '\\' + subject.getBranch()  + '\\examples\\files\\' + type + '\\' + case + '\\' + configuration  + '\\' )
        self.__directorySelectedComputer = subject.adaptPathSelectedComputer( subject.getDirectory() + 'examples\\files\\' + type + '\\' + case + '\\' + configuration  + '\\' )
 
        Test.__init__( self, subject, type, case, configuration, localDirectory ) 

    def getDirectorySelectedComputer( self ):
        return self.__directorySelectedComputer


                   
    

           