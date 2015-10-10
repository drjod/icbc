import message
import mysql.connector
import gateToMySQL

class MySQL:
    def __init__( self, user, password, host, schema):
        self.user = user                                   
        self.password = password
        self.host = host
        self.schema = schema

class Example:
    def __init__( self, type, case, configuration):
        self.type = type                                   
        self.case = case
        self.configuration = configuration
     
        
#################################################################        
           
class Setting:

    __computerId = ''
    __selectedTypeId = ''

    def __init__( self, type, case, condition, mode, preselectedOperation, stage, mySQL_struct ):
    
        self.__preExample = Example( type, case, condition )
        self.__mode = mode                                             # build or test                         
        self.__preselectedOperation = preselectedOperation             # if specified, operation done only once
        self.__stage = stage                                           # testing depth 
                                
        self.__mySQL_struct = mySQL_struct
        self.__gateToMySQL = gateToMySQL.GateToMySQL( mySQL_struct )
        message.console( type='INFO', text='Connect ' + mySQL_struct.user + ' to ' + mySQL_struct.host + ' ' + mySQL_struct.schema  )
        
    def __del__( self ):    
        del gateToMySQL
        
    def getPreExample( self ):
        return self.__preExample
    def getPreselectedOperation( self ):
        return self.__preselectedOperation     
        
    def getOperatingSystem( self ):    
        return self.__gateToMySQL.getColumnEntry( 'computer', self.__computerId, 'operating_system' )
    def getState( self ):     
        return self.__gateToMySQL.getColumnEntry( 'computer', self.__computerId, 'state')
    def getRootDirectory( self, user ):      
        return self.__gateToMySQL.getRootDirectory( self.__computerId, self.__gateToMySQL.getIdFromName( 'user', user ) ) 
        
    def setComputerId( self, computer ):
        self.__computerId = self.__gateToMySQL.getIdFromName( 'computer', computer )    
                                                
    #################################################################
    #  Environment: selectMode 
    #  Task:
    #      select either build or test
    #        
        
    def selectMode( self ):
        if self.__mode == '':
            print('\n Select mode: (b)uild or (t)est') 
            
            selectedMode = input( '\n' )
            
            if selectedMode == 'b' or selectedMode == 't':
                self.__mode = selectedMode                  
            else:
                message.console( type='ERROR', text='Mode is (build) or (t)est. Try again.' )   
                self.selectMode()
                
        return self.__mode            
                
    #################################################################
    #  Environment: reselect
    #  Task:
    #
    
    def reselect ( self, subject ):
           
        options = []
        options.append( '    (m)ode')
        options.append( '    (c)omputer')        
        options.append( '    c(o)de')
        options.append( '    (b)ranch')
        options.append( '    co(n)figuration')
        if self.__mode == 't': 
            options.append( '    (e)xample')
            options.append( '    (t)ype')
            options.append( '    c(a)se')
       
        
        # select
        print( '\nSelect:\n' )        
        for option in options:
            print( option )          
        selectedOption = input( '\n' )
 
        if str( selectedOption ) == 'p':  
            subject.setComputer ('')                     
        if str( selectedOption ) == 'o':  
            subject.setCode ('') 
        if str( selectedOption ) == 'b':  
            subject.setBranch ('') 
            
        if str( selectedOption ) == 't' or str( selectedOption ) == 'e':     
            self.__preExample.type = ''
        if str( selectedOption ) == 'a' or str( selectedOption ) == 'e':             
            self.__preExample.case = ''
        if str( selectedOption ) == 'n' or str( selectedOption ) == 'e':             
            self.__preExample.configuration = ''   
        if str( selectedOption ) == 'm':             
            self.__mode = ''  
                    
    #################################################################        
    #  SelectName
    #  Task:
    #      get user input - table ids (primary key)
    #      cals itself again if user input is not a number
    #  Parameter: 
    #      table (string): name of table in SQL schema
    #  Return:    
    #      name (string)   
    #    
    
    def selectName( self, table ):      
        # get items list with options 
        if table == 'cases':
            if self.__preExample.type == 'a':
                return 'a' # all types -> all cases
            else: # cases for specific type
                print ( self.__selectedTypeId )
                items = self.__gateToMySQL.getNamesFromIdGroup( table, 'a', selectedType_id = self.__selectedTypeId )  
        elif table == 'configurations':
            items = self.__gateToMySQL.getNamesFromIdGroup( 'configurations', 'a', self.__computerId )
        else:    
            items = self.__gateToMySQL.getNamesFromIdGroup( table, 'a' )
        # print options  
        nameVector = []
        idVector = []                            
        print( '\nSelect from ' + table + ':\n' )  
        for row in items:
            print( '   ' + str( row['id'] ) + ' ' + str( row['name'] ) )
            nameVector.append ( str( row['name'] ) ) 
            idVector.append ( str( row['id'] ) )
            
        if table == 'types' or table == 'cases' or table == 'configurations':  
            print( '   a all' )    
        # select
        selectedId = input( '\n   by typing number: ' )    
        
        self.__selectedTypeId = selectedId
        print( '\n-----------------------------------------------------------------' )
    
        # id to name
        if selectedId == 'a':
        
            if table == 'types':      
                if self.__preExample.type == 'a':    
                    pass
        
            return nameVector
        else:
            i = 0
            for idInst in idVector:
                if not ( idInst == selectedId ):                
                    i = i+1
                else:
                    break
                    
            return nameVector[i]     
    
         
        #if self.checkSelectedId( table, selectedId ) == False:
        #    SelectedId = self.selectId( table )  # repeat input
                   
        #return selectedId 
        
        
    ##############################################
    #  Environment: checkSelectedId
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
    
    def selectExampleGroup( self, table ):
    
        if table == 'types':
            if self.__preExample.type == '':   
                return self.selectName( 'types' )
            else:
                return ' '
        elif table == 'cases':
            if self.__preExample.case == '':   
                return self.selectName( 'cases' )
            else:
                return ' ' 
        elif table == 'configurations':
            if self.__preExample.configuration == '':   
                return self.selectName( 'configurations' )
            else:
                return ' '               
              