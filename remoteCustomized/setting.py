import configurationCustomized 
import copy
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
import message

# structs

class MySQL:
    def __init__( self, user, password, host, schema):
        self.user = user                                   
        self.password = password
        self.host = host
        self.schema = schema

class TestCases:
    def __init__( self, typeList, caseList, configurationList):
        self.typeList = typeList                                   
        self.caseList = caseList
        self.configurationList = configurationList
     
        
#################################################################
#  class Setting
#  Task:
#      console input 
#      hosts TestCases lists, gateToMySQL
#            preselectedOperation, operationType
#
           
class Setting:

    
    #__selectedTypeIdList = []  # for tree structure (types, cases)

    def __init__( self, typeList, caseList, configurationList, operationType, preselectedOperation, testingDepth, mySQL_struct ):
    
        self.__testCases = TestCases( typeList, caseList, configurationList )
        self.__operationType = operationType                           # building or testing                         
        self.__preselectedOperation = preselectedOperation             # if specified, operation done only once
        self.__testingDepth = testingDepth                                         
         
        self.__location = configurationCustomized.location		 

        
    def __del__( self ): 
        pass	
        
        
    def getTestCases( self ):
        return self.__testCases
    def getPreselectedOperation( self ):
        return self.__preselectedOperation     
    def getLocation( self, computer ):
        return self.__location 	
    def setTypeList( self, list):
        self.__testCases.typeList = list 
    def setCaseList( self, list):        
        self.__testCases.caseList = list       
    def setConfigurationList( self, list):                
        self.__testCases.configurationList = list
                                                             
    #################################################################
    #  Setting: selectOperationType 
    #  Task:
    #      select between building and testing
    #        
        
    def selectOperationType( self ):               
        return self.__operationType          
                
    #################################################################
    #  Setting: reselect
    #  Task:
    #      asks for user input which variable to reselect     
    #      and sets choosen variable to ' ' (caseList to [' '])
    #      such that user input is requested later on for this variable   
    #  Parameter:
    #     subject (class): stores variables computer, user, code, branch
    #
    
    def reselect ( self, subject ):
        pass  
                    
    #################################################################        
    #  Setting: selectGroup
    #  Task:
    #      get user input - table names
  
    
    def selectGroup( self, table, computer = '' ):  
        pass	
      
    ##############################################
    #  Setting: selectTestCasesGroup
    #  Task:
    #    calls member function selectGroup for test cases specification 
    #    if test cases are not previously selected
    #  Parameter:
    #    table (string): [types, cases, configurations] 
    #  Return:
    #    list (string) for one test cases level (meaning: types, cases, configuration)  
    #    nested list if table = 'cases'
    #
    
    def selectTestCasesGroup( self, groupType, computerOfSubject = '' ):  
        pass           
                        
              