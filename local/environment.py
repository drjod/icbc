
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
#      Select tested subject and test items (user input or preset)
#      Generate instance Operation (configure, select and execute operation)
#

class Environment:  
    
    ##############################################
    #  Environment: constructor
    #
    
    def __init__( self, computer='', user='', code='', branch='', type='', case='', configuration='', mode='', operation='', stage='',
                  mySQL_user='root', mySQL_password='*****', mySQL_host='localhost', mySQL_schema='testing_environment' ):
                  
        mySQL_struct = setting.MySQL ( mySQL_user, mySQL_password, mySQL_host, mySQL_schema )
        self.__subject_inst = subject.Subject( computer, user, code, branch  )                                                              
        self.__setting_inst = setting.Setting ( type, case, configuration, mode, operation, stage, mySQL_struct )
        
        print( '\n-----------------------------------------------------------------' )
        
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
        del self.__subject_inst  
        del self.__setting_inst
                         
    #################################################################
    #  Environment: run  
    #  Task:
    #      main functions
    #def __init__( self, name, operatingSystem, state, rootDirectory, user, code, branch ):
                            
    def run( self ): 
        
        self.__subject_inst.select( self.__setting_inst )  
        selectedMode = self.__setting_inst.selectMode()
                
        selectedTypeVector = []
        selectedCaseVector = []
        selectedConfigurationVector = [] 
            
        if selectedMode == 't':
            selectedTypeVector.append( self.__setting_inst.selectExampleGroup( 'types' ) )
            selectedCaseVector.append( self.__setting_inst.selectExampleGroup( 'cases' ) )
        else:
            selectedTypeVector.append( '-1' )
            selectedCaseVector.append( '-1' )          
        selectedConfigurationVector.append( self.__setting_inst.selectExampleGroup( 'configurations' ) )
        
        if selectedMode == 'b':    
            operation_inst = operation.Building( self.__subject_inst )
        elif selectedMode == 't':  
            operation_inst = operation.Testing( self.__subject_inst )
        else:    
            message.console( type='ERROR', notSupported=selectedMode )   
        
        operation_inst.selectOperation( self.__setting_inst.getPreselectedOperation() )
          
        if operation_inst.getSelectedOperation() == 's': 
            self.__setting_inst.reselect( self.__subject_inst )
        else:              
            for type in selectedTypeVector:
                for case in selectedCaseVector:
                    for configuration in selectedConfigurationVector:
            
                        example_inst = setting.Example( type, case, configuration )
                        
                        if selectedMode == 'b':  
                            item_inst = item.Build( self.__subject_inst, example_inst.configuration )
                        elif selectedMode == 't':             
                            item_inst = item.Test( self.__subject_inst, example_inst )
                                    
                        #if int( self.__gateToMySQL.getStage( str( row0['id'] ), str( row1['id'] ) ) ) <= configurationShared.testingDepth: 
                       
                        operation_inst.operate( item_inst ) 
                        #else:
                        #    message.console( type='INFO', text='inactive - item is of depth ' + self.__gateToMySQL.getStage( str( row0['id'] ), str( row1['id'] ) ) )
                        del item_inst          
                        
        del operation_inst
        
        print( '\n-----------------------------------------------------------------' )    
        
        
        
        if self.__setting_inst.getPreselectedOperation() == '':   
            self.run()   
             

