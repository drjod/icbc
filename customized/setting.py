import utilities
import mysql.connector
import copy
import sys, os
import numerics, processing

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import gateToMySQL, configurationCustomized
import simulationData


#################################################################
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

class lists: # stores lists for member setNames
    def __init__( self ):
        self._name = []     # contains selected names
        self._nameSub = []  # to generate nested nameList for table cases, which depends on selected type
        self._id = []       # stores selected ids
        self._items = []    # entries contain id and name from database
     
        
#################################################################
#  class Setting
#  Task:
#      console input 
#      hosts TestCases lists, gateToMySQL
#            preselectedOperation, operationType
#
           
class Setting:

    __selectedTypeIdList = []  # for tree structure (types, cases) - to know selected type when cases are selected

    def __init__( self, typeList, caseList, configurationList, operationType, preselectedOperation, testMode, mySQL_struct ):
    
        self.__itemConstituents = itemConstituents( typeList, caseList, configurationList )
        self.__operationType = operationType                           # building or testing                         
        self.__preselectedOperation = preselectedOperation             # if specified, operation done only once
        self.__testMode = testMode  # to switch off select                                        
        self.__mySQL_struct = mySQL_struct
        #self.__gateToMySQL = gateToMySQL.GateToMySQL( mySQL_struct )   
        #utilities.message( type='INFO', text='Connect ' + mySQL_struct.user + ' to ' + mySQL_struct.host + ' ' + mySQL_struct.schema  )
        
    def __del__( self ):  
        pass  
        # del self.__gateToMySQL
        
    def connectToMySQL( self ):
        utilities.message( type='INFO', text='Connect ' + self.__mySQL_struct.user + ' to database ' + self.__mySQL_struct.host + ' ' + self.__mySQL_struct.schema  )
        self.__gateToMySQL = gateToMySQL.GateToMySQL(  self.__mySQL_struct )

    def disconnectFromMySQL( self ):
        #utilities.message( type='INFO', text='Disconnecting'  )
        del self.__gateToMySQL
    
    def getItemConstituents( self ):
        return self.__itemConstituents
    def getPreselectedOperation( self ):
        return self.__preselectedOperation     
        
    def getLocation( self, computerName ):     
        return self.__gateToMySQL.getColumnEntry( 'computer', 
                                                  self.__gateToMySQL.getIdFromName( 'computer', computerName ), 
                                                  'location') 
    def getOperatingSystem( self, computerName ):     
        return self.__gateToMySQL.getColumnEntry( 'computer', 
                                                  self.__gateToMySQL.getIdFromName( 'computer', computerName ), 
                                                  'operating_system') 
 
    def getRootDirectory( self, computerName, userName ): 
        return self.__gateToMySQL.getRootDirectory( self.__gateToMySQL.getIdFromName( 'computer', computerName ), self.__gateToMySQL.getIdFromName( 'user', userName ) )  
          
    def getHostname( self, computerName ):
        return self.__gateToMySQL.getColumnEntry( 'computer', 
                                                  self.__gateToMySQL.getIdFromName( 'computer', computerName ), 
                                                  'hostname')  
    
    def getUser( self, superuserName, computerName ):
        return self.__gateToMySQL.getNameFromId( 'user' , 
                                                 self.__gateToMySQL.getUserIdFromSuperuser( superuserName, computerName ) ) 
                                                      
    def getState( self, caseName ):
        return self.__gateToMySQL.getColumnEntry( 'cases', self.__gateToMySQL.getIdFromName( 'cases', caseName ), 'state' ) 
                                                                   
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
        if not self.__operationType:
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
                utilities.message( type='ERROR', text='Operation type ' + selectedOperationType + ' does not exist. Try again.' )   
                self.selectOperationType()
                
        return self.__operationType            
                
    #################################################################
    #  Setting: reselect
    #  Task:
    #      asks for user input which variable to reselect     
    #      and sets choosen variable to ' ' (caseList to [' '])
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
            subject.setComputer(None)    
            subject.setUser(None)   # user must be reselected too                 
            self.__itemConstituents.configurationList = [None]  # and also configurations since these depend on computer
        if str( selectedOption ) == 'o':  
            subject.setCode(None) 
            subject.setBranch(None)    # branch must be reselected too               
        if str( selectedOption ) == 'b':  
            subject.setBranch(None) 
            
        if str( selectedOption ) == 't' or str( selectedOption ) == 'e':            
            self.__itemConstituents.typeList = [None]
            self.__itemConstituents.caseList = [[None]]         # case must be reselected too
            self.__selectedTypeIdList.clear()
        if str( selectedOption ) == 'a' or str( selectedOption ) == 'e':             
            self.__itemConstituents.caseList = [[None]]
        if str( selectedOption ) == 'n' or str( selectedOption ) == 'e':             
            self.__itemConstituents.configurationList = [None]   
        if str( selectedOption ) == 'p':             
            self.__operationType = None  
                    
    #################################################################        
    #  Setting: set names
    #  Task:
    #      returns names (list of strings, nested list if table = 'cases')
    #      for a table obtained from database and user selection  
    #  Parameter: 
    #      table (string): name of table in SQL schema

    
    def setNames( self, table, computer = None ):      

        lists_inst= lists() 
        names = []

        self.getItemsFromDatabase( table, computer, lists_inst)  
        if len(lists_inst._name) > 0: # for table cases if in table types all or range  was selected 
            return lists_inst._name  # know already names, so return them directly
        selectedId = self.selectId(table, lists_inst)                 
        names = self.id2name(table, selectedId, lists_inst)

        del lists_inst
        return names
      
    ##############################################
    #  Setting: getItemsFromDatabase
    #  Task:     
    #      fill lists_inst._items with instances (id, name) from database
    #      if table cases and more than on type selected, fill lists_inst._name directly since selectId for case not required
    #      class member to have access to __selectedTypeIdList

    def getItemsFromDatabase( self, table, computer, lists_inst ):

        if table == 'cases':   # has sublist for each type (nested list)      
            if len( self.__selectedTypeIdList ) > 1: # more than one type was selected         
                for typeId in self.__selectedTypeIdList:
                    lists_inst._items = self.__gateToMySQL.getNamesFromIdGroup( 'cases', 'a', selectedType_id = typeId )
                    for row in lists_inst._items:
                        lists_inst._nameSub.append ( str( row['name'] ) ) 
                    lists_inst._name.append ( copy.deepcopy( lists_inst._nameSub ) ) # append to _name to return this directly (without selectId)
                    lists_inst._nameSub.clear()                    
            else: # cases for specific type
                lists_inst._items = self.__gateToMySQL.getNamesFromIdGroup( 'cases', 'a', 
                                                                selectedType_id = self.__selectedTypeIdList[0] )  
        elif table == 'configurations': # since it depends on computer
            lists_inst._items = self.__gateToMySQL.getNamesFromIdGroup( 'configurations', 'a', 
                                                             self.__gateToMySQL.getIdFromName( 'computer', computer ) )
        else:    # computer, user, ... (anything but cases, configurations - see list in environment constructor)
            lists_inst._items = self.__gateToMySQL.getNamesFromIdGroup( table, 'a' ) 


    ##############################################
    #  Setting: selectId
    #  Task:   
    #      print options on console 
    #      fill lists_inst._nameSub with names from lists_inst_items 
    #  Requirements:
    #      items in lists_inst must be set
       
    def selectId( self, table, lists_inst ):

        if self.__testMode == False:  
            # print options             
            print( '\nSelect from ' + table + ':\n' )  

        for row in lists_inst._items:
            if self.__testMode == False:
                print( '   ' + str( row['id'] ) + ' ' + str( row['name'] ) )
            lists_inst._nameSub.append ( copy.deepcopy( str( row['name'] ) ) )
            lists_inst._id.append ( copy.deepcopy( str( row['id'] ) ) )
 
        if self.__testMode == True:
            # TESTMODE: preselect in testMode anything but examples (types, cases, configurations) and specify level in database
            # all examples are selected here and level is checked in operation instance 
            selectedId = 'a'
        else:
            print( '   a all' )  
            if table == 'types': # range only for types supported
                print( '   r range' )    
            # select
            #
            selectedId = input( '\n   by typing number: ' ) 

        if table == 'types': # set self.__selectedTypeIdList
            if selectedId == 'a': # selected all             
                for i in range( 0, len( lists_inst._id )):
                    self.__selectedTypeIdList.append( copy.deepcopy( lists_inst._id[i] ) )      
            elif selectedId == 'r': # selected range - so get the lower and upper range limits now
                lowerRange = input( '\n       From: ' )    
                upperRange = input( '\n         To: ' )
                for i in range( int(lowerRange), int(upperRange) + 1):
                    self.__selectedTypeIdList.append( copy.deepcopy( lists_inst._id[i] ) )                                           
            else:
                self.__selectedTypeIdList.append( copy.deepcopy( selectedId ) )
        print( '\n-----------------------------------------------------------------' )   
         
        return selectedId

    #################################################################
    #  Global: id2name
    #  Task:
    #      Convert id to name (list) and return this as a nested list [['...']]
    #      class member to have access to __selectedTypeIdList
 
    def id2name( self, table, selectedId, lists_inst):

        if selectedId == 'a':
            if table == 'cases':
                lists_inst._name.append( copy.deepcopy( lists_inst._nameSub ) )  
                return lists_inst._name
            else:    
                return lists_inst._nameSub
        elif selectedId == 'r': 
            if table == 'types':
                for id in self.__selectedTypeIdList:    
                    lists_inst._name.append( copy.deepcopy( lists_inst._nameSub[getListId( id, lists_inst._id)] ) )
                return lists_inst._name  
            else:
                utilities.message( type='ERROR', text='Range supported only for types' )
                return None
        else: # single item           
            lists_inst._name.append( copy.deepcopy( lists_inst._nameSub[getListId( selectedId, lists_inst._id)] ) )
            if table == 'cases':
                nameList2 = []
                nameList2.append( copy.deepcopy( lists_inst._name ) ) 
                return nameList2
            else:       
                return lists_inst._name  

                                                                    
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
            utilities.message( type='WARNING', text='That was not a number' )
            return False
                       
        return True 

    ##############################################
    #  Setting: setItemConstituents
    #  Task:
    #    calls member function selectNames to get item constituents  
    #    if they are not previously selected (i.e. in environment constructor or anywhere in last operations)
    #  Parameter:
    #    table (string): [types, cases, configurations] 
    #  Return:
    #    list (string) for one item  constituent (meaning: types, cases, configuration)  
    #    nested list if table = 'cases'
    #
    
    def setItemConstituents( self, groupType, computerOfSubject = '' ):
    
        if groupType == 'types':           
            if len ( self.__itemConstituents.typeList ) == 0 or not self.__itemConstituents.typeList[0]:   
                return self.setNames( table = 'types' ) 
            else:
                return self.__itemConstituents.typeList 
        elif groupType == 'cases':
            if len( self.__itemConstituents.caseList ) == 0 or self.__itemConstituents.caseList[0] == [None]:   
                return self.setNames( table = 'cases' ) 
            else:
                return self.__itemConstituents.caseList 
        elif groupType == 'configurations':
            if len( self.__itemConstituents.configurationList ) == 0 or not self.__itemConstituents.configurationList[0]:    
                return self.setNames( table = 'configurations', 
                                         computer = computerOfSubject )
            else:
                return self.__itemConstituents.configurationList             



    def setProcessingData( self, simData, type, case, configuration ):

        proc = processing.Processing()

        proc.set( self.__gateToMySQL.getColumnEntry( 'types', 
                                                                 self.__gateToMySQL.getIdFromName( 'types', type ), 
                                                                 'numberOfCPUs' ),    
                          self.__gateToMySQL.getColumnEntry( 'configurations', 
                                                                 self.__gateToMySQL.getIdFromName( 'configurations', configuration ), 
                                                                 'processing' ) )

        simData.setProcessing( proc )  
                                                                                                                                                                                                                
        return simData

    ##############################################
    #  Setting: setNumData
    #  Task:
    #     get mumerics and parallelization data frpm mySQL database
    #     data are used later on to write *.num *.pbs files
    #
    
    def setNumData( self, simData, type, case, configuration ):
                
        globNum = numerics.Global()
        prcs = numerics.processes() 

        preconditioner = []
        solver = []
        theta = []
        # this prcs is put into globNum
        prcs.set( self.__gateToMySQL.getNameFromId( 'flow_processes',
                                                            self.__gateToMySQL.getColumnEntry( 'cases', 
                                                            self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                            'flow_id' ) ),
                                                        self.__gateToMySQL.getColumnEntry( 'cases', 
                                                            self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                            'mass_flag' ),                                                                                    
                                                        self.__gateToMySQL.getColumnEntry( 'cases', 
                                                            self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                            'heat_flag' ) ) 
        # generall numerics data 
        globNum.set ( prcs, 
                          self.__gateToMySQL.getColumnEntry( 'cases', 
                                                                 self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                                 'coupled_flag' ),                                                                     
                          self.__gateToMySQL.getColumnEntry( 'cases', 
                                                                 self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                                 'lumping_flow' ),
                          self.__gateToMySQL.getColumnEntry( 'cases', 
                                                                 self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                                 'nonlinear_flag' ) )                         
        # the data that dependent on process      
        solver.append( self.convertNumericsDbEntry2specifcation( configuration, self.__gateToMySQL.getColumnEntry( 
            'cases', self.__gateToMySQL.getIdFromName( 'cases', case ), 'solver_flow_' + configuration ), 'solver' ) ) 
         
        solver.append( self.convertNumericsDbEntry2specifcation( configuration, self.__gateToMySQL.getColumnEntry( 
            'cases', self.__gateToMySQL.getIdFromName( 'cases', case ), 'solver_mass_' + configuration ), 'solver' ) )                            

        solver.append( self.convertNumericsDbEntry2specifcation( configuration, self.__gateToMySQL.getColumnEntry( 
            'cases', self.__gateToMySQL.getIdFromName( 'cases', case ), 'solver_heat_' + configuration ), 'solver' ) ) 
        

        preconditioner.append( self.convertNumericsDbEntry2specifcation( configuration, self.__gateToMySQL.getColumnEntry( 
            'cases', self.__gateToMySQL.getIdFromName( 'cases', case ), 'preconditioner_flow_' + configuration ), 'preconditioner' ) ) 
         
        preconditioner.append( self.convertNumericsDbEntry2specifcation( configuration, self.__gateToMySQL.getColumnEntry( 
            'cases', self.__gateToMySQL.getIdFromName( 'cases', case ), 'preconditioner_mass_' + configuration ), 'preconditioner' ) )                            

        preconditioner.append( self.convertNumericsDbEntry2specifcation( configuration, self.__gateToMySQL.getColumnEntry( 
            'cases', self.__gateToMySQL.getIdFromName( 'cases', case ), 'preconditioner_heat_' + configuration ), 'preconditioner' ) ) 


        theta.append ( self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'theta_flow' ) ) 
        theta.append ( self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'theta_mass' ) ) 
        theta.append ( self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'theta_heat' ) )

        # store data in simulationData.simData() - local in environment.run()                                                                                                                                                        
        simData.setNum( globNum, solver, preconditioner, theta )  
                                                                                                                                                                                                           
        return simData
    
    #################################################################
    #  Setting: convertNumericsDbEntry2specifcation
    #      numericsType: 'solver' or 'preconditioner'
    def convertNumericsDbEntry2specifcation( self, configuration, entry, numericsType ):
        value = ''
        try:
            if not  (entry == 'null' ):
                solverTableName = self.__gateToMySQL.getColumnEntry( 'configurations', self.__gateToMySQL.getIdFromName( 'configurations', configuration ), numericsType + '_table_name') 
                return self.__gateToMySQL.getColumnEntry( solverTableName, entry, 'specification')
            else:
                return '-1'
        except:
            utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] )  
                

#################################################################
#  Global: getListId
#  Task:
#      Convert from global id to local id

def getListId( selectedId, idList):

    i = 0
    for idInst in idList:
        if not ( idInst == selectedId ):                
            i = i+1
        else:
            break

    return i


