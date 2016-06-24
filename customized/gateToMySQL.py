import mysql.connector
import os
import utilities


##############################################
# class GateToMySQL
# Task:
#     fetch entries from SQL database tables
#     with getter member functions  
#

class GateToMySQL:

    ##############################################
    #  GateToMySQL: constructor
    #  Tasks:
    #      connect to database
    #  Parameter:
    #      User (string)
    #      Password (string)
    #      Host (string)
    #      Schema (string): SQL database
    #  Result:
    #     cursor
    #     error message if access to database failed
    #
           
    def __init__( self, mySQL_struct ):
        try:
            cnx = mysql.connector.connect( user = mySQL_struct.user, password = mySQL_struct.password,
                                          host = mySQL_struct.host, database = mySQL_struct.schema ) 
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print( 'ERROR - user name or password wrong' )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print( 'ERROR - database does not exist' )            
            else:
                print( err )   
        else:        
            self.__cnx = cnx	# cursor

    ##############################################
    #  GateToMySQL: descructor
    #
                                            
    def __del__( self ):
        self.__cnx.close()   

    ##############################################
    # GateToMySQL: getNameFromId
    # Task:
    #     id -> name    
    #  parameter:
    #      table (string): name of table in SQL schema s
    #      item_id (string): id where name is searched to 
    #  Return:
    #      name (string)
    #      '-1' if no name found (exception)    
    #  Requirements:
    #      name must be in 2nd colum in SQL table
    #
               
    def getNameFromId( self, table, item_id ):        
        if item_id == 'a': 
            return 'all ' + table  # console output
                         
        cursor = self.__cnx.cursor( buffered=True ) 
        try:
            cursor.execute( 'SELECT * FROM ' + table + ' WHERE id=' + str ( item_id ) )
        except:
            utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] ) 
        row = cursor.fetchone()
        if row is not None:
            return ( str ( row[1] ) )
        else:
            utilities.message( type='ERROR', text='Name for id ' + str ( item_id ) + ' not found in table ' +  + str ( table ) )            
            return '-1' # exception

    ##############################################
    #  GateToMySQL: getIdFromName
    #  Task:
    #      name -> id   
    #      table columns must be: id, name, ...  
    #  Parameter:
    #      table (string): name of table in SQL schema 
    #      name (string): entry in column name
    #  Return:
    #      id (string)
    #      '-1' if no id found (exception)    
    #  Requirements:
    #      id must be in first column in SQL table
    #
            
    def getIdFromName(self, table, name ):
    
        if not name :   # empty string
            return ''  # no name given
        else:    
            cursor = self.__cnx.cursor( buffered=True ) 
            try:
                cursor.execute( 'SELECT t.id FROM ' + table + ' t WHERE t.name=%s',(name, ))
            except:
                utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] )                
            row = cursor.fetchone()
            if row is not None:
                return ( str ( row[0] ) )
            else:
                utilities.message( type='ERROR', text='Column id for ' + str ( name ) + ' not found in table ' +  + str ( table ) )            
                return '-1' # exception            
                                                         
    ##############################################
    #  GateToMySQL: getNamesFromIdGroup
    #  Task:
    #      get table entries (id and name) 
    #  Options: 
    #      1. all
    #      2. for specific id
    #      3. configurations for specific computer
    #      4. cases for specific example type
    #  Parameter:
    #      table (string): name of table in SQL schema
    #      item_id (string): entry in id column (primary key) (e.g. option 2.) 
    #      computer_id (string): for option 3.
    #      running_type_id (string): for option 4.
    #  Return:
    #      items list - no exception handling
    #      item (struct): id, name
    #  Requirements:
    #      if all cases requested, running_type_id must be given
    # 
                       
    def getNamesFromIdGroup( self, table, item_id, computer_id='-1', selectedType_id='-1' ):
        # set cursor       
        cursor = self.__cnx.cursor( buffered=True ) 
        if item_id == 'a':
            
            if table == 'computer' or table == 'user' or table == 'codes' or table == 'branches' or table == 'types':
                try:
                    cursor.execute( 'SELECT * FROM ' + table )
                except:
                    utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] ) 
            elif table == 'cases':   # specific type selected 
                try:
                    cursor.execute( 'SELECT c.* FROM examples e, cases c WHERE e.case_id = c.id and e.type_id = ' + selectedType_id ) 
                except:
                    utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] ) 
            elif table == 'configurations':  # depends on selected computer
                try:
                    cursor.execute( 'SELECT c.* FROM modi m, configurations c WHERE m.configuration_id = c.id and m.computer_id = ' + computer_id )  
                except:
                    utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] )   
            else:
                utilities.message( type='ERROR', notSupported=table )
        else:    
            cursor.execute( 'SELECT * FROM ' + table + ' WHERE id=' + str( item_id ) )    
        # cursor -> struct 
        items = []
        row = cursor.fetchone()
        
        while row is not None:    
            item = {
                'id': row[0],
                'name': row[1]
            }    
            items.append( item )    
            row = cursor.fetchone()
        
        return items

    ##############################################
    #  GateToMySQL: getColumnEntry
    #  Task:
    #      id -> entry in specific column 
    #  Paramter:
    #      table (string): name of table in SQL schema
    #      item_id (string): entry in id column (primary key) 
    #      column_name (string): name of column where entry is searched from 
    #  Return:
    #      column entry as string
    #      '-1' if no entry found (exception)   
                                               
    def getColumnEntry( self, table, item_id, column_name ):
        # set cursor
        cursor = self.__cnx.cursor( buffered=True ) 
        try:
            cursor.execute( 'SELECT t.' + column_name + ' FROM ' + table + ' t WHERE t.id=' + str ( item_id ) )
        except:
            utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] ) 
        #  
        row = cursor.fetchone()
        if not row:
            utilities.message( type='ERROR', text='Column entry of ' + str ( column_name ) + ' not found for id ' +  + str ( item_id ) )        
            return '-1' # exception
        else:
            return ( str ( row[0] ) )
    
            
    ##############################################
    #  GateToMySQL: getRootDirectory
    #  
    # 
    
    def getRootDirectory( self, computer_id, user_id ):
        # set cursor
        cursor = self.__cnx.cursor( buffered=True ) 
        try:
            cursor.execute( 'SELECT p.root FROM paths p WHERE p.computer_id=' + str ( computer_id ) + ' AND p.user_id=' + str ( user_id ) )
        except:
            utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] ) 
        #  
        row = cursor.fetchone()
        if not row:
            utilities.message( type='ERROR', text='Path not found for computer id ' + str ( computer_id ) + ' - user id ' +  str ( user_id ) )
            return '-1' # exception
        else:
            return ( str ( row[0] ) )
     
                    
    ##############################################
    #  GateToMySQL: getState
    #  
    # 
    
    def getState( self, type_id, case_id ):
        # set cursor
        cursor = self.__cnx.cursor( buffered=True ) 
        try:
            cursor.execute( 'SELECT e.state FROM examples e WHERE e.type_id=' + str ( type_id ) + ' AND e.case_id=' + str ( case_id ) )
        except:
            utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] )  
        #  
        row = cursor.fetchone()
        if not row:
            utilities.message( type='ERROR', text='state not found for example ' + str ( type_id ) + ' ' + str ( case_id ) )
            return '1000' # exception - no operation for high number  
        else:
            return ( str ( row[0] ) )
   
        
  
    ##############################################
    #  GateToMySQL: getUserIdFromSuperuser
    #  Task: 
    #     giver user id based on preselected superuser and computer name
    #     this is than used to get the user name
                                
    def getUserIdFromSuperuser( self, superuser, computer ):        
        # set cursor
        cursor = self.__cnx.cursor( buffered=True ) 
        try:
            cursor.execute( "SELECT s.user_id FROM superuser s WHERE s.name='" +  str ( superuser ) +"' AND s.computer_id=" + self.getIdFromName( 'computer', computer ) )
        except:
            utilities.message( type='ERROR', text='%s' % sys.exc_info()[0] ) 
        #  
        row = cursor.fetchone()
        if not row:
            utilities.message( type='ERROR', text='User id not found for superuser ' + str ( superuser ) + ' on ' +  str ( computer ) )
            return '-1' # exception
        else:
            return ( str ( row[0] ) )

            
        
