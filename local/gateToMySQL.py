import mysql.connector
import os

class GateToMySQL:
    
    
    def __init__( self, User, Password, Host, Schema ):
        try:
            cnx = mysql.connector.connect( user = User, password = Password,
                                          host = Host, database = Schema ) 
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print( "ERROR - user name or password wrong" )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print( "ERROR - database does not exist" )            
            else:
                print( err )   
        else:        
            self.__cnx = cnx	
                    
    def __del__( self ):
        self.__cnx.close()   
        
             
    ##############################################
    # 
    # if table:
    #    computers, codes, branches:  generally used (case (a)ll does not exist)
    #    types, cases, configurations:  for console output 
    # return:
    #    string item or "-1"
    #
               
    def getSelectedItem( self, table, item_id ):        
        if item_id == "a": 
            return "all " + table  # console output
                         
        cursor = self.__cnx.cursor( buffered=True ) 
        cursor.execute( "SELECT * FROM " + table + " WHERE id=" + str ( item_id ) )
         
        row = cursor.fetchone()
        if row is not None:
            return ( str ( row[1] ) )
        else:
            return "-1" # exception
                   
    ##############################################
    # 
    #   used for types, cases, configurations in loop over examples 
    #   return:
    #     items list - no exception handling
    #
                           
    def getSelectedItemGroup( self, table, item_id, computer_id=-1, running_type_id=-1 ):
        # set cursor
        cursor = self.__cnx.cursor( buffered=True ) 
        if item_id == "a":
           
            if table == "computer" or table == "codes" or table == "branches" or table == "types":
            #if table == "types": # or ( table == "cases" and self.__type == "a" ): 
                cursor.execute( "SELECT * FROM " + table )
            elif table == "cases":   # specific type selected 
                cursor.execute( "SELECT c.* FROM examples e, cases c WHERE e.case_id = c.id and e.type_id = " + str( running_type_id )) # + str(self.__type) )
            elif table == "configurations":  # depends on selected computer
                cursor.execute( "SELECT c.* FROM modi m, configurations c WHERE m.configuration_id = c.id and m.computer_id = " + str( computer_id ) )    
            else:
                print( "ERROR - schema " + table + " not supported in gateToMySQL.getSelectedItemGroup" )     
        else:    
            cursor.execute( "SELECT * FROM " + table + " WHERE id=" + str( item_id ) )    

        # cursor -> struct 
        items = []
        row = cursor.fetchone()
        
        while row is not None:    
            item = {
                'id': row[0],
                'type_name': row[1]
            }    
            items.append( item )    
            row = cursor.fetchone()
        
        return items

    ##############################################

                                               
    def getColumnEntry(self, table, item_id, column_name ):
    
        cursor = self.__cnx.cursor( buffered=True ) 
        cursor.execute( "SELECT t." + column_name + " FROM " + table + " t WHERE t.id=" + str ( item_id ) )
         
        row = cursor.fetchone()
        if row is not None:
            return ( str ( row[0] ) )
        else:
            return "-1" # exception

    ##############################################                        
    # only one id !!
            
    def getIdFromName(self, table, name ):
    
        if name == "":
            return ""  # no name given
        else:    
            cursor = self.__cnx.cursor( buffered=True ) 
            cursor.execute( """SELECT t.id FROM """ + table+ """ t WHERE t.name=%s""",(name, ))
             
            row = cursor.fetchone()
            if row is not None:
                return ( str ( row[0] ) )
            else:
                return "-1" # exception            
            
                            
        
        
        
