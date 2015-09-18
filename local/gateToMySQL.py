import mysql.connector


class GateToMySQL:
    
    def __init__( self, User, Password, Host, Schema ):
        try:
            cnx = mysql.connector.connect( user = User, password = Password,
                                          host = Host, database = Schema )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print ( "ERROR - user name or password wrong" )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print( "ERROR - database does not exist" )            
            else:
                print( err )   
        else:        
            self.__cnx = cnx	
        
    def __del__( self ):
        self.__cnx.close()   
        
    def getCursor( self ):
        return self.__cnx.cursor()       
        
    def fromNameToId (self, table, name ):   
        if name == "":
            return ""
        else:    
            #self.__cnx.cursor().execute ( "SELECT t.* FROM " + str( table ) + " t WHERE t.name = " + str( name ) ) 
            #return self.__cnx.cursor()[0]
            
       
                     
    def getOperatingSystem (self, computer_id ):
        return str( self.__cnx.cursor().execute ( "SELECT c.operating_system FROM computer c WHERE c.id = " + str( computer_id ) ) )                           
        
        
        
