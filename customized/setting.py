import utilities
import mysql.connector
import copy
import sys, os
import numerics, processing

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import gateToMySQL, configurationCustomized
import simulationData



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
        #self.__gateToMySQL = gateToMySQL.GateToMySQL( mySQL_struct )   
        #utilities.message( type='INFO', text='Connect ' + mySQL_struct.user + ' to ' + mySQL_struct.host + ' ' + mySQL_struct.schema  )
        
    def __del__( self ):    
        del self.__gateToMySQL
        
    def connectToMySQL( self ):
        utilities.message( type='INFO', text='Connect ' + self.__mySQL_struct.user + ' to ' + self.__mySQL_struct.host + ' ' + self.__mySQL_struct.schema  )
        self.__gateToMySQL = gateToMySQL.GateToMySQL(  self.__mySQL_struct )

    def disconnectFromMySQL( self ):
        #utilities.message( type='INFO', text='Disconnecting'  )
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
                                                      
    def getLevel( self, case ):
       return self.__gateToMySQL.getColumnEntry( 'cases', 
                                                  self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                  'level') 
                                                                   
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
    #  Setting: selectGroup
    #  Task:
    #      get user input - table names
    #  Parameter: 
    #      table (string): name of table in SQL schema
    #  Return:    
    #      names (list of strings, nested list if table = 'cases')   
    #    
    
    def selectGroup( self, table, computer = None ):      
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
        if table == 'types': # range only for types
            print( '   r range' )    
        # select
        selectedId = input( '\n   by typing number: ' )    
        if table == 'types':
            if selectedId == 'a': # took all             
                for i in range( 0, len( idList )):
                    self.__selectedTypeIdList.append( copy.deepcopy( idList[i] ) )      
            elif selectedId == 'r': # took range
                lowerRange = input( '\n       From: ' )    
                upperRange = input( '\n         To: ' )
                for i in range( int(lowerRange), int(upperRange) + 1):
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
        elif selectedId == 'r': 
            if table == 'types':
                for j in self.__selectedTypeIdList:
                    i = 0
                    for idInst in idList:
                        if not ( idInst == j ):                
                            i = i+1
                        else:
                            break
                    
                    nameList.append( copy.deepcopy( nameSubList[i] ) )
                return nameList   # returning nested list [['...']]
            else:
                utilities.message( type='ERROR', text='Range supported only for types' )
                return None
        else: # single item
            # get list id (global to local)
            i = 0
            for idInst in idList:
                if not ( idInst == selectedId ):                
                    i = i+1
                else:
                    break
                    
            nameList.append( copy.deepcopy( nameSubList[i] ) )
            if table == 'cases':
                nameList2 = []
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
            utilities.message( type='WARNING', text='That was not a number' )
            return False
                       
        return True 

    ##############################################
    #  Setting: selectItemConstituentGroup
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
            if len ( self.__itemConstituents.typeList ) == 0 or not self.__itemConstituents.typeList[0]:   
                return self.selectGroup( table = 'types' ) 
            else:
                return self.__itemConstituents.typeList 
        elif groupType == 'cases':
            if len( self.__itemConstituents.caseList ) == 0 or self.__itemConstituents.caseList[0] == [None]:   
                return self.selectGroup( table = 'cases' ) 
            else:
                return self.__itemConstituents.caseList 
        elif groupType == 'configurations':
            if len( self.__itemConstituents.configurationList ) == 0 or not self.__itemConstituents.configurationList[0]:    
                return self.selectGroup( table = 'configurations', 
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
        theta = []
        # this prcs is put into globNum
        prcs.set( self.__gateToMySQL.getNameFromId( 'flow_processes',
                                                            self.__gateToMySQL.getColumnEntry( 'cases', 
                                                            self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                            'flow_id' ) ),
                                                        self.__gateToMySQL.getColumnEntry( 'cases', 
                                                            self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                            'mass' ),                                                                                    
                                                        self.__gateToMySQL.getColumnEntry( 'cases', 
                                                            self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                            'heat' ) ) 
        # generall numerics data 
        globNum.set ( prcs, 
                          self.__gateToMySQL.getColumnEntry( 'cases', 
                                                                 self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                                 'coupled' ),                                                                     
                          self.__gateToMySQL.getColumnEntry( 'cases', 
                                                                 self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                                 'lumping' ),
                          self.__gateToMySQL.getColumnEntry( 'cases', 
                                                                 self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                                 'nonlinear' ) )  
                                 
        solver = self.__gateToMySQL.getColumnEntry( 'cases', 
                                                                 self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                                 'solver' )
        # the data that dependent on process
        preconditioner.append( self.convertPreconditionerCode( configuration, 
                                                         self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'flow_precond' ) ) )
        preconditioner.append( self.convertPreconditionerCode( configuration, 
                                                         self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'mass_precond' ) ) ) 
        preconditioner.append( self.convertPreconditionerCode( configuration, 
                                                         self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'heat_precond' ) ) )

        theta.append ( self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'flow_theta' ) ) 
        theta.append ( self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'mass_theta' ) ) 
        theta.append ( self.__gateToMySQL.getColumnEntry( 'cases', 
                                                      self.__gateToMySQL.getIdFromName( 'cases', case ), 
                                                      'heat_theta' ) )

        # store data in simulationData.simData() - local in environment.run()                                                                                                                                                        
        simData.setNum( globNum, solver, preconditioner, theta )  
                                                                                                                                                                                                           
        return simData
    

    #################################################################
    #  Setting: convertPreconditionerCode
    #  Task:
    #      Converts code in mySQL database into preconditioner specification in ogs input file
    #          1st bit is set 1: preconditioner used in configuration OGS_FEM           (specification 1, Jacobi)     100 is iLU
    #          2nd bit is set 1: preconditioner used in configuration OGS_FEM_SP        (specification 1, Jacobi)
    #          ...
    #

    def convertPreconditionerCode( self, configuration, code ):

        b = '-1'             # bit in code
        specification = '-1' # number for preconditioner in input file

        # select bit and specification according to configuration
        if configuration == 'OGS_FEM':
            b = '0'
            specification = '1'
        elif configuration == 'OGS_FEM_SP':
            b = '1'
            specification = '1' 
        elif configuration == 'OGS_FEM_MKL':
            b = '2'
            specification = '1' 
        elif configuration == 'OGS_FEM_MPI' or configuration == 'OGS_FEM_MPI_KRC':
            b = '3'
            specification = '1' 
        #elif configuration == 'OGS_FEM_PETSC':
        #    b = '4'
        #    specification = '1' 
        else:
            utilities.message( type='ERROR', notSupported=configuration )
            return '0'

        # set and return preconditioner specification for num input file 
        if bool(int(code)&(1<<int(b))) == True:
            return specification
        else:
            return '0'
                      