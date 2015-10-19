
import operation
import message
import shutil
import configurationShared
import item
import subject
import setting


##############################################
#  class: Environment
#  Task:
#      hosts instance of classes subject, setting
#      member function run is main function  
#      

class Environment:  
    
    ##############################################
    #  Environment: constructor
    #  Task:
    #    initialization subject, setting   
    #    passes preselected variables
    #  
    
    def __init__( self, computer=' ', user=' ', code=' ', branch=' ', 
                  typeList=[' '], caseList=[[' ']], configurationList=[' '], 
                  operationType=' ',     # [b,t]
                  operation=' ', 
                  testingDepth=' ',
                  mySQL_user='root', mySQL_password='*****', mySQL_host='localhost', mySQL_schema='testing_environment' ):
                  
        mySQL_struct = setting.MySQL ( mySQL_user, mySQL_password, mySQL_host, mySQL_schema )
        self.__subject_inst = subject.Subject( computer, user, code, branch  )                                                              
        self.__setting_inst = setting.Setting ( typeList, caseList, configurationList, operationType, operation, testingDepth, mySQL_struct )
        
        print( '\n-----------------------------------------------------------------' )
        
        # print message for already set variables
        if computer is not ' ':
            message.console( type='INFO', text='Set computer ' + computer )
        if user is not ' ':
            message.console( type='INFO', text='Set user ' + user )
        if code is not ' ':
            message.console( type='INFO', text='Set code ' + code )
        if branch is not ' ':
            message.console( type='INFO', text='Set branch ' + branch )
        if typeList[0] is not ' ':
            for i in range(0, len( typeList )):
                message.console( type='INFO', text='Set type ' + typeList[i] )
        if caseList[0] is not [' ']:
            for i in range(0, len( caseList )):
                for j in range(0, len( caseList[i] )):
                    message.console( type='INFO', text='Set case ' + caseList[i][j] )
        if configurationList[0] is not ' ':
            for i in range(0, len( configurationList )):
                message.console( type='INFO', text='Set configuration ' + configurationList[i] )
        if operationType is not ' ':
            message.console( type='INFO', text='Set operation type ' + operationType )
        if operation is not ' ':
            message.console( type='INFO', text='Set operation ' + operation )           
        if testingDepth is not ' ':
            message.console( type='INFO', text='Set testing depth ' + testingDepth )                            
                
        print( '\n-----------------------------------------------------------------' )
        
                              
    def __del__( self ):   
        del self.__subject_inst  
        del self.__setting_inst
                         
    #################################################################
    #  Environment: run  
    #  Task:
    #      select tested subject and test items (user input or preset)
    #      generate instance Operation (configure, select and execute operation)
    #
                            
    def run( self ): 
        # select subject (computer, user, code, branch)
        self.__subject_inst.select( self.__setting_inst )  
        # select operation (type and itself)
        selectedOperationType = self.__setting_inst.selectOperationType()              
        if selectedOperationType == 'b': # building
            operation_inst = operation.Building( self.__subject_inst )              
        elif selectedOperationType == 't':  # testing  
            operation_inst = operation.Testing( self.__subject_inst )               
        else:    
            message.console( type='ERROR', notSupported=selectedOperationType )      
        operation_inst.selectOperation( self.__setting_inst.getPreselectedOperation() )
        
        if operation_inst.getSelectedOperation() == 's': 
            self.__setting_inst.reselect( self.__subject_inst )
        else:                   
            # select test cases (type, case, configuration)
            if selectedOperationType == 'b': # building 
                self.__setting_inst.setTypeList( [' '] ) 
                self.__setting_inst.setCaseList( [[' ']] )                           
                self.__setting_inst.setConfigurationList( self.__setting_inst.selectTestCasesGroup( 'configurations' ) )   
            elif selectedOperationType == 't':  # testing  
                self.__setting_inst.setTypeList( self.__setting_inst.selectTestCasesGroup( 'types' ) ) 
                if operation_inst.getSelectedOperation() == 'j': # generateJPGs 
                    self.__setting_inst.setCaseList( [[' ']] ) 
                    self.__setting_inst.setConfigurationList( [' '] ) 
                else:      
                    self.__setting_inst.setCaseList( self.__setting_inst.selectTestCasesGroup( 'cases' ) )                   
                    self.__setting_inst.setConfigurationList( self.__setting_inst.selectTestCasesGroup( 'configurations' ) )  
            # loop over test cases 
            typeList_counter = 0        
            for type in self.__setting_inst.getTestCases().typeList: 
                for case in self.__setting_inst.getTestCases().caseList[typeList_counter]:
                    for configuration in self.__setting_inst.getTestCases().configurationList:
                        if selectedOperationType == 'b':  
                            item_inst = item.Build( self.__subject_inst, configuration )
                        elif selectedOperationType == 't':             
                            item_inst = item.Test( self.__subject_inst, type, case, configuration )
                                 
                        #if int( self.__gateToMySQL.getTestingDepth( str( row0['id'] ), str( row1['id'] ) ) ) <= configurationShared.testingDepth: 
                       
                        operation_inst.operate( item_inst ) 
                        #else:
                        #    message.console( type='INFO', text='inactive - item is of depth ' + self.__gateToMySQL.getTestingDepth( str( row0['id'] ), str( row1['id'] ) ) )
                        del item_inst          
                typeList_counter = typeList_counter + 1
                        
        del operation_inst
        
        print( '\n-----------------------------------------------------------------' )    
          
        if self.__setting_inst.getPreselectedOperation() == ' ':   
            self.run()   
             

