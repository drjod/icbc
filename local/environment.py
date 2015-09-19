import os
import mysql.connector
import gateToMySQL
import operation


class Environment:  
    __currentType = ""  # for loop over examples when all types selected
    
    def __init__( self, Computer="", Code="", Branch="", Type="", Case="", Configuration="", user='root', 
                  password='*****', host='localhost', schema='testing_environment' ):
        self.__gateToMySQL = gateToMySQL.GateToMySQL( user, password, host, schema )
 
        self.__computer =      self.__gateToMySQL.getIdFromName( "computer", Computer )
        self.__code =          self.__gateToMySQL.getIdFromName( "codes", Code )
        self.__branch =        self.__gateToMySQL.getIdFromName( "branches", Branch )
        self.__type =          self.__gateToMySQL.getIdFromName( "types", Type )
        self.__case =          self.__gateToMySQL.getIdFromName( "cases", Case )   
        self.__configuration = self.__gateToMySQL.getIdFromName( "configurations", Configuration )
        
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
            print( "ERROR - That was not a number" )   
            return 0 
                       
        return 1 
                                    
    #################################################################        
    #
    # get user input
    # returns number if selected in range of mysql-table
    # else: it calls itself again 
    #    

    def selectItem( self, table ):      
        # get items list with options 
        if table == "cases":
            if self.__type == "a":
                return "a" # all types -> all cases
            else:
                items = self.__gateToMySQL.getSelectedItemGroup( table, "a", running_type_id=self.__type )  
        elif table == "configurations":
            items = self.__gateToMySQL.getSelectedItemGroup( "configurations", "a", computer_id=self.__computer )
        else:    
            items = self.__gateToMySQL.getSelectedItemGroup( table, "a" )
        # print options                              
        print( "\nSelect from " + table + ":\n" )  
        for row in items:
            print( "   " + str(row['id']) + " " + str( row['type_name'] ) )
        if table == "types" or table == "cases" or table == "configurations":  
            print( "   a all" )    
        # select
        selectedItem = input( '\n   by typing number: ' )    
        print( "\n-----------------------------------------------------------------" )
    
        if self.checkSelectedItem( table, selectedItem ) == 0:
            selectedItem = self.selectItem( table )  # repeat input
                   
        return selectedItem 
                                   
    #################################################################
    # user input: computer, codes, branches 
    #
                       
    def selectGlobal( self ):  
        # tested subject (only one)    
        if self.__computer == "":                                                                                 
            self.__computer = self.selectItem( "computer" )
        if self.__code == "":                                                                                 
            self.__code = self.selectItem( "codes" )
        if self.__branch == "":                                                                                 
            self.__branch = self.selectItem( "branches" )
       
        print( "SELECTED " + self.__gateToMySQL.getSelectedItem( "computer", self.__computer ) + " " +
               self.__gateToMySQL.getSelectedItem( "codes", self.__code ) + " "  + 
               self.__gateToMySQL.getSelectedItem( "branches", self.__branch ) )    
        # test cases               
        
        if self.__type == "":                                                                                 
            self.__type = self.selectItem( "types" )
        if self.__case == "":                                                                                 
            self.__case = self.selectItem( "cases" )
        if self.__configuration == "":                                                                                 
            self.__configuration = self.selectItem( "configurations" )
 
        print( "SELECTED " + self.__gateToMySQL.getSelectedItem( "types", self.__type ) + " " +
               self.__gateToMySQL.getSelectedItem( "cases", self.__case ) + " " +
               self.__gateToMySQL.getSelectedItem( "configurations", self.__configuration ) ) 
              
    #################################################################
    # select examples - declare and call operation
    #
                            
    def operateGlobal( self ):
        # tested subject
        cComputer = self.__gateToMySQL.getSelectedItem( "computer", self.__computer ) 
        cCode = self.__gateToMySQL.getSelectedItem( "codes",  self.__code ) 
        cBranch = self.__gateToMySQL.getSelectedItem( "branches",  self.__branch ) 
        
        print( "ON " + cComputer + " " + cCode + " " + cBranch ) 
       
        op = operation.Operation ( cComputer, cCode, cBranch, self.__gateToMySQL.getColumnEntry( "computer", self.__computer, "operating_system" )) #, self.__gateToMySQL.getOperatingSystem ( 1)) #self.__computer ))
        op.configureGlobal()
        op.select()
        
        # loop over examples
        items0 = self.__gateToMySQL.getSelectedItemGroup( "types", self.__type )
        items2 = self.__gateToMySQL.getSelectedItemGroup( "configurations", self.__configuration, computer_id=self.__computer )
           
        for row0 in items0:
            for row1 in self.__gateToMySQL.getSelectedItemGroup( "cases", self.__case, running_type_id=str( row0['id'] ) ):
                for row2 in items2:
                    cType = str( row0['type_name'] )
                    cCase = str( row1['type_name'] )
                    cConfiguration = str( row2['type_name'] )
                   
                    print( "EXAMPLE " + cType + " " + cCase + " " + cConfiguration )                    
                    op.operate( cType, cCase, cConfiguration ) 
                    
                    
    #################################################################
    # 
    #
                            
    def run( self ): 
        self.selectGlobal()    
        self.operateGlobal()    
        
     
                    
                   
                                 
                
        
 
        
      



                               
                                
  

