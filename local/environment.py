import os
import mysql.connector
import gateToMySQL
import operation
import message
import shutil

##############################################
#  class: Environment
#  Task:
#      Select tested subject and test examples (user input or preset)
#      Generate instance Operation (configure, select and execute operation)
#

class Environment:  
    
    ##############################################
    #  Environment: constructor
    #
    
    def __init__( self, computer='', user='', code='', branch='', type='', case='', configuration='', operation='', stage='',
                  mySQL_user='root', mySQL_password='*****', mySQL_host='localhost', mySQL_schema='testing_environment' ):
        self.__gateToMySQL = gateToMySQL.GateToMySQL( mySQL_user, mySQL_password, mySQL_host, mySQL_schema )
 
        self.__computer =      self.__gateToMySQL.getIdFromName( 'computer', computer )
        self.__user =          self.__gateToMySQL.getIdFromName( 'user', user )        
        self.__code =          self.__gateToMySQL.getIdFromName( 'codes', code )
        self.__branch =        self.__gateToMySQL.getIdFromName( 'branches', branch )
        self.__type =          self.__gateToMySQL.getIdFromName( 'types', type )
        self.__case =          self.__gateToMySQL.getIdFromName( 'cases', case )   
        self.__configuration = self.__gateToMySQL.getIdFromName( 'configurations', configuration )
        self.__preselectedOperation = operation
        self.__stage = stage
        
        print( '\n-----------------------------------------------------------------' )
        message.console( type='INFO', text='Connect ' + mySQL_user + ' to ' + mySQL_host + ' ' + mySQL_schema  )
        # print message for already set variables
        if computer is not '':
            message.console( type='INFO', text='Set computer ' + computer )
        if code is not '':
            message.console( type='INFO', text='Set code ' + code )
        if branch is not '':
            message.console( type='INFO', text='Set branch ' + branch )
        if type is not '':
            message.console( type='INFO', text='Set type ' + type )
        if configuration is not '':
            message.console( type='INFO', text='Set configuration ' + configuration )
        print( '\n-----------------------------------------------------------------' )
        
    ##############################################
    #  Environment: destructor
    #
                              
    def __del__( self ):   
        del self.__gateToMySQL   
    
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
                                    
    #################################################################        
    #  Environment: selectId
    #  Task:
    #      get user input - table ids (primary key)
    #      cals itself again if user input is not a number
    #  Parameter: 
    #      table (string): name of table in SQL schema
    #  Return:    
    #      id (string)   
    #    

    def selectId( self, table ):      
        # get items list with options 
        if table == 'cases':
            if self.__type == 'a':
                return 'a' # all types -> all cases
            else: # cases for specific type
                items = self.__gateToMySQL.getNamesFromIdGroup( table, 'a', running_type_id=self.__type )  
        elif table == 'configurations':
            items = self.__gateToMySQL.getNamesFromIdGroup( 'configurations', 'a', computer_id=self.__computer )
        else:    
            items = self.__gateToMySQL.getNamesFromIdGroup( table, 'a' )
        # print options                              
        print( '\nSelect from ' + table + ':\n' )  
        for row in items:
            print( '   ' + str(row['id']) + ' ' + str( row['name'] ) )
        if table == 'types' or table == 'cases' or table == 'configurations':  
            print( '   a all' )    
        # select
        selectedId = input( '\n   by typing number: ' )    
        print( '\n-----------------------------------------------------------------' )
    
        if self.checkSelectedId( table, selectedId ) == False:
            SelectedId = self.selectId( table )  # repeat input
                   
        return selectedId 
                                   
    #################################################################
    #  Environment: GlobalSelectId
    #  Task: 
    #      user input tested subject and test examples 
    #      user provides id if it has not been already set with the constructor   
    #      exceptions handled in selectId
    #
                       
    def globalSelectId( self ):  
        # tested subject (only one)    
        if self.__computer == '':                                                                                 
            self.__computer = self.selectId( 'computer' )
        if self.__user == '':                                                                                 
            self.__user = self.selectId( 'user' )        
        if self.__code == '':                                                                                 
            self.__code = self.selectId( 'codes' )
        if self.__branch == '':                                                                                 
            self.__branch = self.selectId( 'branches' )
       
        message.console( type='INFO', text='Selected ' + 
               self.__gateToMySQL.getNameFromId( 'computer', self.__computer ) + ' ' +
               self.__gateToMySQL.getNameFromId( 'codes', self.__code ) + ' '  + 
               self.__gateToMySQL.getNameFromId( 'branches', self.__branch ) )    
        # test examples    
        if self.__type == '':                                                                                 
            self.__type = self.selectId( 'types' )
        if self.__case == '':                                                                                 
            self.__case = self.selectId( 'cases' )
        if self.__configuration == '':                                                                                 
            self.__configuration = self.selectId( 'configurations' )
 
        message.console( type='INFO', text='Selected ' + 
               self.__gateToMySQL.getNameFromId( 'types', self.__type ) + ' ' +
               self.__gateToMySQL.getNameFromId( 'cases', self.__case ) + ' ' +
               self.__gateToMySQL.getNameFromId( 'configurations', self.__configuration ) ) 

    #################################################################
    #  Environment: reselect
    #  Task:
    #
    
    def reselect ( self ):
           
        options = []
        options.append( '    (c)ode')
        options.append( '    (b)ranch')
        options.append( '    (e)xample')
        options.append( '    (t)ype')
        options.append( '    c(a)se')
        options.append( '    c(o)nfiguration')
        
        # select
        print( '\nSelect:\n' )        
        for option in options:
            print( option )          
        selectedOption = input( '\n' )
              
        if str( selectedOption ) == 'c':  
            self.__code = ''
        if str( selectedOption ) == 'b':  
            self.__branch = ''
        if str( selectedOption ) == 't' or str( selectedOption ) == 'e':     
            self.__type = ''
        if str( selectedOption ) == 'a' or str( selectedOption ) == 'e':             
            self.__case = ''
        if str( selectedOption ) == 'o' or str( selectedOption ) == 'e':             
            self.__configuration = ''            
                                                                                  
    #################################################################
    #  Environment: globalOperate
    #  Task:
    #      constuction and configuration of object Operation 
    #      call of Operation operate for selected test eamples
    #
                            
    def globalOperate( self ):
        # get constituents names (computer, code, branch) of tested subject
        cComputer = self.__gateToMySQL.getNameFromId( 'computer', self.__computer ) 
        cUser = self.__gateToMySQL.getNameFromId( 'user', self.__user )
        cCode = self.__gateToMySQL.getNameFromId( 'codes',  self.__code ) 
        cBranch = self.__gateToMySQL.getNameFromId( 'branches',  self.__branch ) 
        message.console( type='INFO', text='On ' + cComputer + ' ' + cCode + ' ' + cBranch )
        
        path = self.__gateToMySQL.getRootDirectory( self.__computer, self.__user )  
        # message.console( type='INFO', text='Path: ' + path )   
        # construct and configure operation
        op = operation.Operation( cComputer, cCode, cBranch, path,
                                  self.__gateToMySQL.getColumnEntry( 'computer', self.__computer, 'operating_system' ) )                                                    
        selectedOperation = op.select( self.__preselectedOperation )      

        if str( selectedOperation ) == 's':  
            self.reselect()  
        elif str( selectedOperation ) == 'u':
            # message.console( type='INFO', text='Move windows executables' )   
            self.updateRelease()             
        else:  # 'r'un, 'i'mport, e'x'port   
            # loop over examples
            items0 = self.__gateToMySQL.getNamesFromIdGroup( 'types', self.__type )
            items2 = self.__gateToMySQL.getNamesFromIdGroup( 'configurations', self.__configuration, computer_id=self.__computer )
               
            for row0 in items0:
                for row1 in self.__gateToMySQL.getNamesFromIdGroup( 'cases', self.__case, running_type_id=str( row0['id'] ) ):
                    for row2 in items2:
                        cType = str( row0['name'] )
                        cCase = str( row1['name'] )
                        cConfiguration = str( row2['name'] )
                       
                        # message.console( type='INFO', text='Example ' + cType + ' ' + cCase + ' ' + cConfiguration ) 
                        if int( self.__gateToMySQL.getStage( str( row0['id'] ), str( row1['id'] ) ) ) <= int( self.__stage ):  
                            op.operate( cType, cCase, cConfiguration ) 
                        else:
                            message.console( type='INFO', text='inactive - example is of stage ' + self.__gateToMySQL.getStage( str( row0['id'] ), str( row1['id'] ) ) )     
                    
        del op
        
        print( '\n-----------------------------------------------------------------' )
                                
    #################################################################
    #  Environment: run  
    #  Task:
    #      main functions
    #
                            
    def loop( self ): 
        self.selectStage()
        self.globalSelectId()    
        self.globalOperate()   
             
        if self.__preselectedOperation == '':   
            self.loop()
        
        
    #################################################################
    #  Environment: updateRelease
    #  Task:
    #      copy and rename windows binaries
    #
                                   
    def updateRelease( self ): 
        operatingSystem = self.__gateToMySQL.getColumnEntry( 'computer', self.__computer, 'operating_system' )    
        code = self.__gateToMySQL.getNameFromId( 'codes',  self.__code )
        branch = self.__gateToMySQL.getNameFromId( 'branches',  self.__branch )
        path = 'F:\\testingEnvironment\\' + code + '\\' + branch  
         
        try:
            os.stat(path + '\\releases\\' )
        except:
            os.mkdir(path + '\\releases\\' ) 
                           
        if operatingSystem == 'windows':          
            items = self.__gateToMySQL.getNamesFromIdGroup( 'configurations', self.__configuration, computer_id=self.__computer )
            for row in items:      
                message.console( type='INFO', text='Updating release ' + str( operatingSystem ) + ' ' + str( row['name'] ) )   
                if code == 'ogs':
                    fileName = path + '\\sources\\Build_' + str( row['name'] ) + '\\bin\\Release\\ogs.exe'
                    if os.path.isfile(fileName) and os.access(fileName, os.R_OK): 
                        shutil.copy( fileName, 
                                     path + '\\releases\\' + code  + '_' + branch + '_' + 'windows' + '_'  + str( row['name'] ) + '.exe' )  
                    else:
                        message.console( type='ERROR', text='Binary does not exist - nothing done' )                         
                else:
                    message.console( type='ERROR', notSupported=code )                       
        else:
            message.console( type='ERROR', notSupported=operating_system )          
     
                    
    #################################################################
    #  Environment: selectStage
    #  Task:                   
    #      sets stage (string)
    #
                              
    def selectStage( self ):    
        if self.__stage == '':
            print( '\nSelect testing depth (0, 1, 2):\n' )        
       
            selectedStage = input( '\n' ) 
            
            try:
             val = int( selectedStage )
            except ValueError:
                message.console( type='ERROR', text='That was not a number. Try again' )
                self.selectStage()
       
            if val < 0 or val > 2:
                message.console( type='ERROR', text='Number out of range. Try again' )                    
                self.selectStage()        
                
            self.__stage = selectedStage
                  
        
 
        
      

