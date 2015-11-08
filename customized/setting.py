import message
import mysql.connector
import copy
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import gateToMySQL
import simulationData

# structs

class mySQL:
    def __init__( self, user, password, host, schema):
        self.user = user                                   
        self.password = password
        self.host = host
        self.schema = schema

class itemConstituents:
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

    __selectedTypeIdList = []  # for tree structure (types, cases)

    def __init__( self, typeList, caseList, configurationList, operationType, preselectedOperation, testingDepth, mySQL_struct ):
    
        self.__itemConstituents = itemConstituents( typeList, caseList, configurationList )
        self.__operationType = operationType                           # building or testing                         
        self.__preselectedOperation = preselectedOperation             # if specified, operation done only once
        self.__testingDepth = testingDepth                                         
                                
        self.__mySQL_struct = mySQL_struct
        self.__gateToMySQL = gateToMySQL.GateToMySQL( mySQL_struct )
            
        message.console( type='INFO', text='Connect ' + mySQL_struct.user + ' to ' + mySQL_struct.host + ' ' + mySQL_struct.schema  )
        
    def __del__( self ):    
        del self.__gateToMySQL
        
    def getItemConstituents( self ):
        return self.__itemConstituents
    def getPreselectedOperation( self ):
        return self.__preselectedOperation     
        
    def getLocation( self, computer ):     
        return self.__gateToMySQL.getColumnEntry( 'computer', 
                                                  self.__gateToMySQL.getIdFromName( 'computer', computer ), 
                                                  'location') 
    def getOperatingSystem( self, computer ):     
        return self.__gateToMySQL.getColumnEntry( 'computer', 
                                                  self.__gateToMySQL.getIdFromName( 'computer', computer ), 
                                                  'operating_system') 
 
    def getRootDirectory( self, computer, user ): 
        return self.__gateToMySQL.getRootDirectory( self.__gateToMySQL.getIdFromName( 'computer', computer ), self.__gateToMySQL.getIdFromName( 'user', user ) )  
          
    def getHostname( self, computer):
        return self.__gateToMySQL.getColumnEntry( 'computer', 
                                                  self.__gateToMySQL.getIdFromName( 'computer', computer ), 
                                                  'hostname')  
    
    def getUser( self, superuser, computer ):
        return self.__gateToMySQL.getNameFromId( 'user' , 
                                                 self.__gateToMySQL.getUserIdFromSuperuser( superuser, computer ) ) 
                                                      
                                                             
    def setTypeList( self, list):
        self.__itemConstituents.typeList = list 
    def setCaseList( self, list):        
        self.__itemConstituents.caseList = list       
    def setConfigurationList( self, list):                
        self.__itemConstituents.configurationList = list
                                                             
    #################################################################
    #  Setting: selectOperationType 
    #  Task:
    #      select between building and testing (simulating, plotting)
    #        
        
    def selectOperationType( self ):
        if self.__operationType == ' ':
            operationTypeList = []
            operationTypeList.append( '    (b)uilding')
            operationTypeList.append( '    (s)imulating')
            operationTypeList.append( '    (p)lotting') 
            print('\n Select operation type:') 
            for operationType in operationTypeList:
                print( operationType )             
            selectedOperationType = input( '\n' )
            
            if selectedOperationType == 'b' or selectedOperationType == 's' or selectedOperationType == 'p':
                self.__operationType = selectedOperationType                  
            else:
                message.console( type='ERROR', text='Operation type ' + selectedOperationType + ' does not exist. Try again.' )   
                self.selectOperationType()
                
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
           
        optionList = []
        optionList.append( '    o(p)eration type')
        optionList.append( '    (c)omputer')        
        optionList.append( '    c(o)de')
        optionList.append( '    (b)ranch')
        optionList.append( '    co(n)figuration')
        if self.__operationType == 's' or self.__operationType == 'p': 
            optionList.append( '    (e)xample')
            optionList.append( '    (t)ype')
            optionList.append( '    c(a)se')
             
        # select
        print( '\nSelect:\n' )        
        for option in optionList:
            print( option )          
        selectedOption = input( '\n' )
        # set variable(s) to  
        if str( selectedOption ) == 'c':  
            subject.setComputer(' ')    
            subject.setUser(' ')   # user must be reselected too                 
        if str( selectedOption ) == 'o':  
            subject.setCode(' ') 
            subject.setBranch(' ')    # branch must be reselected too               
        if str( selectedOption ) == 'b':  
            subject.setBranch(' ') 
            
        if str( selectedOption ) == 't' or str( selectedOption ) == 'e':            
            self.__testCases.typeList = [' ']
            self.__testCases.caseList = [[' ']] # case must be reselected too
            self.__selectedTypeIdList.clear()
        if str( selectedOption ) == 'a' or str( selectedOption ) == 'e':             
            self.__testCases.caseList = [[' ']]
        if str( selectedOption ) == 'n' or str( selectedOption ) == 'e':             
            self.__testCases.configurationList = [' ']   
        if str( selectedOption ) == 'p':             
            self.__operationType = ' '  
                    
    #################################################################        
    #  Setting: selectGroup
    #  Task:
    #      get user input - table names
    #  Parameter: 
    #      table (string): name of table in SQL schema
    #  Return:    
    #      names (list of strings, nested list if table = 'cases')   
    #    
    
    def selectGroup( self, table, computer = '' ):      
        nameList = []
        nameSubList = []
        idList = []     
        # get items list with options 
        if table == 'cases':          
            if len( self.__selectedTypeIdList ) > 1: # all types         
                for typeId in self.__selectedTypeIdList:
                    items = self.__gateToMySQL.getNamesFromIdGroup( 'cases', 'a', selectedType_id = typeId )
                    for row in items:
                        nameSubList.append ( str( row['name'] ) ) 
                    nameList.append ( copy.deepcopy( nameSubList ) )
                    nameSubList.clear()                    
                return nameList      
            else: # cases for specific type
                items = self.__gateToMySQL.getNamesFromIdGroup( 'cases', 'a', 
                                                                selectedType_id = self.__selectedTypeIdList[0] )  
        elif table == 'configurations':
            items = self.__gateToMySQL.getNamesFromIdGroup( 'configurations', 'a', 
                                                             self.__gateToMySQL.getIdFromName( 'computer', computer ) )
        else:    
            items = self.__gateToMySQL.getNamesFromIdGroup( table, 'a' )
        # print options             
        print( '\nSelect from ' + table + ':\n' )  
        for row in items:
            print( '   ' + str( row['id'] ) + ' ' + str( row['name'] ) )
            nameSubList.append ( copy.deepcopy( str( row['name'] ) ) )
            idList.append ( copy.deepcopy( str( row['id'] ) ) )
            
        if table == 'types' or table == 'cases' or table == 'configurations':  
            print( '   a all' )    
        # select
        selectedId = input( '\n   by typing number: ' )    
        if table == 'types':
            if selectedId == 'a':              
                for i in range( 0, len( idList )):
                    self.__selectedTypeIdList.append( copy.deepcopy( idList[i] ) )            
            else:
                self.__selectedTypeIdList.append( copy.deepcopy( selectedId ) )
        print( '\n-----------------------------------------------------------------' )    
        # id to name (list)
        if selectedId == 'a':  
            if table == 'cases':
                nameList.append( copy.deepcopy( nameSubList ) )
                return nameList   # returning nested list [['...']]
            else:    
                return nameSubList
        else:
            # get list id (global to local)
            i = 0
            for idInst in idList:
                if not ( idInst == selectedId ):                
                    i = i+1
                else:
                    break
                    
            nameList.append( copy.deepcopy( nameSubList[i] ) )
            if table == 'cases':
                nameList2= []
                nameList2.append( copy.deepcopy( nameList ) )
                return nameList2   # returning nested list [['...']]
            else:       
                return nameList     
    
               
    ##############################################
    #  Setting: checkSelectedId
    #  Task:
    #      looks if a number has been typed in      
    #      no check whether selected item exists
    #  Parameter:
    #      table (string): name of table in SQL schema
    #      selectedId (string): input to be checked
    #  Return:
    #      True : ok
    #      False : exception
    #
        
    def checkSelectedId( self, table, selectedId):  
        if table == 'types' or table == 'cases' or table == 'branches' or table == 'configurations':  
            if selectedId == 'a':
                return True   # all selected        
        try:
            val = int( selectedId )
        except ValueError:
            message.console( type='WARNING', text='That was not a number' )
            return False
                       
        return True 

    ##############################################
    #  Setting: selectTestCasesGroup
    #  Task:
    #    calls member function selectGroup to specify item constituents  
    #    if they are not previously selected
    #  Parameter:
    #    table (string): [types, cases, configurations] 
    #  Return:
    #    list (string) for one item  constituent (meaning: types, cases, configuration)  
    #    nested list if table = 'cases'
    #
    
    def selectItemConstituentGroup( self, groupType, computerOfSubject = '' ):
    
        if groupType == 'types':           
            if len ( self.__itemConstituents.typeList ) == 0 or self.__itemConstituents.typeList[0] == ' ':   
                return self.selectGroup( table = 'types' ) 
            else:
                return self.__itemConstituents.typeList 
        elif groupType == 'cases':
            if len( self.__itemConstituents.caseList ) == 0 or self.__itemConstituents.caseList[0] == [' ']:   
                return self.selectGroup( table = 'cases' ) 
            else:
                return self.__itemConstituents.caseList 
        elif groupType == 'configurations':
            if len( self.__itemConstituents.configurationList ) == 0 or self.__itemConstituents.configurationList[0] == ' ':    
                return self.selectGroup( table = 'configurations', 
                                         computer = computerOfSubject )
            else:
                return self.__itemConstituents.configurationList             

    ##############################################
    #  Setting: selectTestCasesGroup
    #  Task:
    #     Used to write *.num *.pbs files
    #
    
    def setSimulationData( self, simulationData, type, case, configuration ):
                
        flowProcess = self.__gateToMySQL.getNameFromId( 'flow_processes',
                                                        self.__gateToMySQL.getColumnEntry( 'cases', 
                                                                                           self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                                                           'flow_id' )
                                                       )
        massFlag = self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'mass' )                                                                                    
        heatFlag = self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'heat' )  
        coupledFlag = self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'coupled' )                                               
        numberOfCPUs = self.__gateToMySQL.getColumnEntry( 'types', 
                                                    self.__gateToMySQL.getIdFromName( 'types', type ), 
                                                    'numberOfCPUS' )    
        processing = self.__gateToMySQL.getColumnEntry( 'configurations', 
                                                      self.__gateToMySQL.getIdFromName( 'configurations', configuration ), 
                                                      'processing' )                  
        lumpingFlag = self.__gateToMySQL.getColumnEntry( 'cases', 
                                                    self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                    'lumping' )
        nonlinearFlag = self.__gateToMySQL.getColumnEntry( 'cases', 
                                                    self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                    'nonlinear' )                                                                                                                                             
        simulationData.set( flowProcess, massFlag, heatFlag, coupledFlag, processing, numberOfCPUs, lumpingFlag, nonlinearFlag )                                                                                                                                                                                             
        return simulationData                         