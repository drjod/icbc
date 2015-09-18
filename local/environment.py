import os
import mysql.connector
import operation

class Environment:
    __computer = -1
    __code = -1
    __branch = -1
    
    __type = -1
    __case = -1
    __configuration = -1
      
    def __init__(self, gateToMySQL):
        self.__gateToMySQL = gateToMySQL

    ##############################################
    # looks if a number has been typed in      
    # no check whether selected item exists
    # 1 : ok
    # 0 : exception
    #
        
    def checkSelectedItem ( self, table, selectedItem):  
    
        if table == "types" or table == "cases" or table == "branches" or table == "configurations":  
            if selectedItem == "a":
                return 1   # all selected
            
        try:
            val = int( selectedItem )
        except ValueError:
            print ( "ERROR - That was not a number" )   
            return 0 
                       
        return 1 
                                      
    ##############################################
    # 
    # if table:
    #    computers, codes, branches:  generally used (case (a)ll does not exist)
    #    types, cases, configurations:  for console output 
    #
               
    def getSelectedItem( self, table, item_id, cursor ):   
        if item_id == "a": 
            return "all " + table  # console output
                     
        cursor.execute ( "SELECT * FROM " + table + " WHERE id=" + str( item_id ) )    
           
        for row in cursor:           
            return ( str( row[1] ) )
     
    ##############################################
    # 
    #    types, cases, configurations 
    #
                       
    def getSelectedItems( self, table, item_id, cursor ):
        if item_id == "a":
           
            if table == "types" or ( table == "cases" and self.__type == "a" ): 
                cursor.execute ( "SELECT * FROM " + table )
            elif table == "cases":   # specific type selected 
                cursor.execute ( "SELECT c.* FROM examples e, cases c WHERE e.case_id = c.id and e.type_id = " + str(self.__type) )
            elif table == "configurations":  # depends on selected computer
                cursor.execute ( "SELECT c.* FROM modi m, configurations c WHERE m.configuration_id = c.id and m.computer_id = " + str(self.__computer) )     
        else:    
            cursor.execute ( "SELECT * FROM " + table + " WHERE id=" + str( item_id ) )    
         
        items = []
        for row in cursor:
            item = {
                'id': row[0],
                'type_name': row[1]
            }
            items.append( item )

        return items 
  
    #################################################################        
    #
    # get user input
    # returns number if selected in range of mysql-table
    # else: it calls itself again 
    #    

    def selectItem( self, table, cursor ):      
                   
        if table == "computer" or table == "codes" or table == "branches" or table == "types" or ( table == "cases" and self.__type == "a" ):   
            cursor.execute ( "SELECT * FROM " + table )    
        elif table == "cases":   # specific type selected 
            cursor.execute ( "SELECT c.* FROM examples e, cases c WHERE e.case_id = c.id and e.type_id = " + str(self.__type) )
        elif table == "configurations":  # depends on selected computer
            cursor.execute ( "SELECT c.* FROM modi m, configurations c WHERE m.configuration_id = c.id and m.computer_id = " + str(self.__computer) )
        else:
            print ("ERROR - table" + table + "not supported")

        items = []              
        for row in cursor:
            item = {
                'id': row[0],
                'type_name': row[1]
            }
            items.append( item )
                                      
        print ( "\nSelect from " + table + ":\n" )
        
        for row in items:
            print ( "   " + str(row['id']) + " " + str( row['type_name'] ) )
            
        if table == "types" or table == "cases" or table == "configurations":  
            print ( "   a all" )    
        
        selectedItem = input( '\n   by typing number: ' )    
        print ( "\n-----------------------------------------------------------------" )
    
        if self.checkSelectedItem( table, selectedItem ) == 0:
            selectedItem = self.selectItem( table, cursor )  # repeat input
                   
        return selectedItem 
                                   
    #################################################################
    # user input: computer, codes, branches 
    #
                       
    def select( self ):                                                                                   
        self.__computer = self.selectItem( "computer", self.__gateToMySQL.getCursor() )
        self.__code = self.selectItem( "codes", self.__gateToMySQL.getCursor() )
        self.__branch = self.selectItem( "branches", self.__gateToMySQL.getCursor() )
       
        print( "SELECTED " + self.getSelectedItem("computer", self.__computer, self.__gateToMySQL.getCursor() ) + " " +
               self.getSelectedItem( "codes", self.__code, self.__gateToMySQL.getCursor() ) + " " +
               self.getSelectedItem( "branches", self.__branch, self.__gateToMySQL.getCursor() ) )    
               
              
        self.__type = self.selectItem( "types", self.__gateToMySQL.getCursor() )
        self.__case = self.selectItem( "cases", self.__gateToMySQL.getCursor() )
        self.__configuration = self.selectItem( "configurations", self.__gateToMySQL.getCursor() )
 
        print( "Selected " + self.getSelectedItem( "types", self.__type, self.__gateToMySQL.getCursor() ) + " " +
               self.getSelectedItem( "cases", self.__case, self.__gateToMySQL.getCursor() ) + " " +
               self.getSelectedItem( "configurations", self.__configuration, self.__gateToMySQL.getCursor() ) ) 
              
    #################################################################
    # loop over examples
    #
                            
    def run ( self ):
    
        cComputer = self.getSelectedItem( "computer", self.__computer, self.__gateToMySQL.getCursor() )
        cCode = self.getSelectedItem( "codes", self.__code, self.__gateToMySQL.getCursor() )
        cBranch = self.getSelectedItem( "branches", self.__branch, self.__gateToMySQL.getCursor() )
        
        print ( "WITH " + cComputer + " " + cCode +  " " + cBranch )      
        op = operation.Operation ( cComputer, cCode, cBranch )
        op.configureGlobal()
        op.select()
        
        # loop    
        for row0 in self.getSelectedItems( "types", self.__type, self.__gateToMySQL.getCursor() ):
            for row1 in self.getSelectedItems( "cases", self.__case, self.__gateToMySQL.getCursor() ):
                for row2 in self.getSelectedItems( "configurations", self.__configuration, self.__gateToMySQL.getCursor() ):
                    cType = str( row0['type_name'] )
                    cCase = str( row1['type_name'] )
                    cConfiguration = str( row2['type_name'] )
                   
                    print ( "EXAMPLE " + cType+ " " + cCase + " " + cConfiguration )                    
                    op.operate( cType, cCase, cConfiguration ) 
                   
                                 
                
        
 
        
      



                               
                                
  

