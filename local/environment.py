import os
import mysql.connector
import gateToMySQL
import operation


class Environment:  
    __currentType = ""  # for loop over examples when all types selected
    
    def __init__( self, Computer="", Code="", Branch="", Type="", Case="", Configuration="", user='root', 
                  password='*****', host='localhost', schema='testing_environment' ):
        self.__gateToMySQL = gateToMySQL.GateToMySQL( user, password, host, schema )
 
        self.__computer =      self.__gateToMySQL.fromNameToId( "computer", Computer )
        self.__code =          self.__gateToMySQL.fromNameToId( "codes", Code )
        self.__branch =        self.__gateToMySQL.fromNameToId( "branches", Branch )
        self.__type =          self.__gateToMySQL.fromNameToId( "types", Type )
        self.__case =          self.__gateToMySQL.fromNameToId( "cases", Case )   
        self.__configuration = self.__gateToMySQL.fromNameToId( "configurations", Configuration )
        
    def __del__( self ):   
        del self.__gateToMySQL   
    
    ##############################################
    # looks if a number has been typed in      
    # no check whether selected item exists
    # 1 : ok
    # 0 : exception
    #
        
    def checkSelectedItem( self, table, selectedItem):  
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
    #   used for types, cases, configurations in loop over examples 
    #
                       
    def getSelectedItemGroup( self, table, item_id, cursor ):
        # set cursor
        if item_id == "a":
           
            if table == "types": # or ( table == "cases" and self.__type == "a" ): 
                cursor.execute ( "SELECT * FROM " + table )
            elif table == "cases":   # specific type selected 
                cursor.execute ( "SELECT c.* FROM examples e, cases c WHERE e.case_id = c.id and e.type_id = " + self.__currentType ) # + str(self.__type) )
            elif table == "configurations":  # depends on selected computer
                cursor.execute ( "SELECT c.* FROM modi m, configurations c WHERE m.configuration_id = c.id and m.computer_id = " + str(self.__computer) )     
        else:    
            cursor.execute ( "SELECT * FROM " + table + " WHERE id=" + str( item_id ) )    
        # cursor -> struct
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
        # set cursor                   
        if table == "computer" or table == "codes" or table == "branches" or table == "types": #  or ( table == "cases" and self.__type == "a" ):   
            cursor.execute ( "SELECT * FROM " + table )    
        elif table == "cases":  
            if self.__type == "a":
                return "a"       # all types -> all cases
            else:
                cursor.execute ( "SELECT c.* FROM examples e, cases c WHERE e.case_id = c.id and e.type_id = " + str(self.__type) )
        elif table == "configurations":  # depends on selected computer
            cursor.execute ( "SELECT c.* FROM modi m, configurations c WHERE m.configuration_id = c.id and m.computer_id = " + str(self.__computer) )
        else:
            print ("ERROR - table" + table + "not supported")
        # cursor -> struct
        items = []              
        for row in cursor:
            item = {
                'id': row[0],
                'type_name': row[1]
            }
            items.append( item )
        # print options                              
        print ( "\nSelect from " + table + ":\n" )  
        for row in items:
            print ( "   " + str(row['id']) + " " + str( row['type_name'] ) )
        if table == "types" or table == "cases" or table == "configurations":  
            print ( "   a all" )    
        # select
        selectedItem = input( '\n   by typing number: ' )    
        print ( "\n-----------------------------------------------------------------" )
    
        if self.checkSelectedItem( table, selectedItem ) == 0:
            selectedItem = self.selectItem( table, cursor )  # repeat input
                   
        return selectedItem 
                                   
    #################################################################
    # user input: computer, codes, branches 
    #
                       
    def selectGlobal( self ):  
        # tested subject (only one)    
        if self.__computer == "":                                                                                 
            self.__computer = self.selectItem( "computer", self.__gateToMySQL.getCursor() )
        if self.__code == "":                                                                                 
            self.__code = self.selectItem( "codes", self.__gateToMySQL.getCursor() )
        if self.__branch == "":                                                                                 
            self.__branch = self.selectItem( "branches", self.__gateToMySQL.getCursor() )
       
        print( "SELECTED " + self.getSelectedItem("computer", self.__computer, self.__gateToMySQL.getCursor() ) + " " +
               self.getSelectedItem( "codes", self.__code, self.__gateToMySQL.getCursor() ) + " " +
               self.getSelectedItem( "branches", self.__branch, self.__gateToMySQL.getCursor() ) )    
        # test cases               
        if self.__type == "":                                                                                 
            self.__type = self.selectItem( "types", self.__gateToMySQL.getCursor() )
        if self.__case == "":                                                                                 
            self.__case = self.selectItem( "cases", self.__gateToMySQL.getCursor() )
        if self.__configuration == "":                                                                                 
            self.__configuration = self.selectItem( "configurations", self.__gateToMySQL.getCursor() )
 
        print( "SELECTED " + self.getSelectedItem( "types", self.__type, self.__gateToMySQL.getCursor() ) + " " +
               self.getSelectedItem( "cases", self.__case, self.__gateToMySQL.getCursor() ) + " " +
               self.getSelectedItem( "configurations", self.__configuration, self.__gateToMySQL.getCursor() ) ) 
              
    #################################################################
    # select examples - declare and call operation
    #
                            
    def operateGlobal( self ):
        # tested subject
        cComputer = self.getSelectedItem( "computer", self.__computer, self.__gateToMySQL.getCursor() )
        cCode = self.getSelectedItem( "codes", self.__code, self.__gateToMySQL.getCursor() )
        cBranch = self.getSelectedItem( "branches", self.__branch, self.__gateToMySQL.getCursor() )
        
        print ( "WITH " + cComputer + " " + cCode +  " " + cBranch )      
        op = operation.Operation ( cComputer, cCode, cBranch) #, self.__gateToMySQL.getOperatingSystem ( 1)) #self.__computer ))
        op.configureGlobal()
        op.select()
        
        # loop over examples   
        for row0 in self.getSelectedItemGroup( "types", self.__type, self.__gateToMySQL.getCursor() ):
            self.__currentType = str(row0['id'] )
            for row1 in self.getSelectedItemGroup( "cases", self.__case, self.__gateToMySQL.getCursor() ):
                for row2 in self.getSelectedItemGroup( "configurations", self.__configuration, self.__gateToMySQL.getCursor() ):
                    cType = str( row0['type_name'] )
                    cCase = str( row1['type_name'] )
                    cConfiguration = str( row2['type_name'] )
                   
                    print ( "EXAMPLE " + cType+ " " + cCase + " " + cConfiguration )                    
                    op.operate( cType, cCase, cConfiguration ) 
                    
                    
    #################################################################
    # 
    #
                            
    def run ( self ): 
        self.selectGlobal()    
        self.operateGlobal()    
        
     
                    
                   
                                 
                
        
 
        
      



                               
                                
  

