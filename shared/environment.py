import utilities, configurationShared
import operation, subject, item, simulationData
import shutil, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import setting, configurationCustomized




##############################################
#  class: Environment
#  Task:
#      hosts instance of classes subject, setting
#      member function run is main function  
#      

class Environment:  
  
    __reselectFlag = False
    __currentOperation = None # used for reselect (operation)
    __level = None
    ##############################################
    #  Environment: constructor
    #  Task:
    #    initialization subject, setting   
    #    passes preselected variables
    #  
    
    def __init__( self, superuser = None, computer = None, user = None, code = None, branch = None, 
                  typeList = [None], caseList = [[None]], configurationList = [None], 
                  operationType = '',     # [b,t]
                  operation = None, 
                  testingDepth = None,	
                  level = None,						  
                  mySQL_user='root', mySQL_password='*****', mySQL_host='localhost', mySQL_schema='testing_environment' ):
                  
        mySQL_struct = setting.mySQL ( mySQL_user, mySQL_password, mySQL_host, mySQL_schema )
        self.__subject_inst = subject.Subject( superuser, computer, user, code, branch  )                                                              
        self.__setting_inst = setting.Setting ( typeList, caseList, configurationList, 
                                                operationType, operation, 
                                                testingDepth, 
                                                mySQL_struct )
        #self.__simulationData = simulationData.SimulationData()
        self.__level = level

        if int( configurationCustomized.verbosity ) > 1:
            # print message for already set variables
            if not computer:
                utilities.message( type='INFO', text='Set computer ' + computer )
            if not user:
                utilities.message( type='INFO', text='Set user ' + user )
            if not code:
                utilities.message( type='INFO', text='Set code ' + code )
            if not branch:
                utilities.message( type='INFO', text='Set branch ' + branch )
            if not typeList[0]:
                for i in range(0, len( typeList )):
                    utilities.message( type='INFO', text='Set type ' + typeList[i] )
            if not caseList[0][0]:
                for i in range(0, len( caseList )):
                    for j in range(0, len( caseList[i] )):
                        utilities.message( type='INFO', text='Set case ' + caseList[i][j] )
            if not configurationList[0]:
                for i in range(0, len( configurationList )):
                    utilities.message( type='INFO', text='Set configuration ' + configurationList[i] )
            if not operationType:
                utilities.message( type='INFO', text='Set operation type ' + operationType )
            if not operation:
                utilities.message( type='INFO', text='Set operation ' + operation )           
            if not testingDepth:
                utilities.message( type='INFO', text='Set testing depth ' + testingDepth )                            
            if not simulationData:
                __simulationData = simulationData
                utilities.message( type='INFO', text='Simulation data set' )  

            print( '\n-----------------------------------------------------------------' )                        
                              
    def __del__( self ):   
        del self.__subject_inst  
        del self.__setting_inst
                         
    #################################################################
    #  Environment: run  
    #  Task:
    #      select tested subject and item constituents (user input or preset)
    #      generate instance Operation (configure, select and execute operation)
    #
                            
    def run( self ): 
        #selects
        if configurationCustomized.location == 'local':
            self.__setting_inst.connectToMySQL()   
        self.__subject_inst.select( self.__setting_inst )  

        selectedOperationType = self.__setting_inst.selectOperationType()              
        if selectedOperationType == 'b': # building
            operation_inst = operation.Building( self.__subject_inst )              
        elif selectedOperationType == 's':  # simulating
            operation_inst = operation.Simulating( self.__subject_inst ) 
        elif selectedOperationType == 'p':  # plotting  
            operation_inst = operation.Plotting( self.__subject_inst )                           
        else:    
            utilities.message( type='ERROR', notSupported=selectedOperationType )  
        if self.__reselectFlag == False:
            selectedOperation = operation_inst.selectOperation( self.__setting_inst.getPreselectedOperation() )
            if selectedOperation is not 's':
                self.__currentOperation = selectedOperation # reselect not choosen
        if operation_inst.getSelectedOperation() == 's': 
            self.__setting_inst.reselect( self.__subject_inst  )
            self.__reselectFlag = True
        else:   
            if configurationCustomized.location == 'local':       
                #self.__setting_inst.connectToMySQL()                 
                # selects (type, case, configuration)
                if selectedOperationType == 'b': # building (only configuration)
                    self.__setting_inst.setTypeList( [None] ) 
                    self.__setting_inst.setCaseList( [[None]] )                          
                    self.__setting_inst.setConfigurationList( self.__setting_inst.selectItemConstituentGroup( groupType = 'configurations',
                                                                                                              computerOfSubject = self.__subject_inst.getComputer() ) )                        
                elif selectedOperationType == 's':  # simulating (all item constituents (type, case, configuration))
                    self.__setting_inst.setTypeList( self.__setting_inst.selectItemConstituentGroup( groupType = 'types' ) ) 
                    self.__setting_inst.setCaseList( self.__setting_inst.selectItemConstituentGroup( groupType = 'cases' ) )                                      
                    self.__setting_inst.setConfigurationList( self.__setting_inst.selectItemConstituentGroup( groupType = 'configurations',
                                                                                                              computerOfSubject = self.__subject_inst.getComputer() ) ) 
                elif selectedOperationType == 'p':  # plotting
                    self.__setting_inst.setTypeList( self.__setting_inst.selectItemConstituentGroup( groupType = 'types' ) )
                    if self.__currentOperation == 'j': # generateJPGs (only type)
                        self.__setting_inst.setCaseList( [[None]] ) 
                        self.__setting_inst.setConfigurationList( [None] ) 
                    else:   # all item constituents  (type, case, configuration)
                        self.__setting_inst.setCaseList( self.__setting_inst.selectItemConstituentGroup( groupType = 'cases' ) )                                      
                        self.__setting_inst.setConfigurationList( self.__setting_inst.selectItemConstituentGroup( groupType = 'configurations',
                                                                                                                  computerOfSubject = self.__subject_inst.getComputer() ) )  
            # loop over items 
            if self.__reselectFlag == True:
                self.__reselectFlag = False
            elif self.__setting_inst.getItemConstituents().typeList == None or self.__setting_inst.getItemConstituents().caseList == None or self.__setting_inst.getItemConstituents().configurationList == None:
                utilities.message( type='ERROR', text='Selection of test items failed - No operation' )
            else:
                typeList_counter = 0  
                configuration = None      
                for type in self.__setting_inst.getItemConstituents().typeList:                   
                    for case in self.__setting_inst.getItemConstituents().caseList[typeList_counter]:
                        for configuration in self.__setting_inst.getItemConstituents().configurationList:
        
                            if not self.__level and case:  # (string empty) should not be the case if on remote computer
                                self.__level = self.__setting_inst.getLevel( case ) # database query
                            else:
                                self.__level = '1'

                            if selectedOperationType == 'b': # building 
                                item_inst = item.Build( self.__subject_inst, configuration )
                            elif selectedOperationType == 's': # simulating
                                item_inst = item.Sim( self.__subject_inst, type, case, configuration )
                            elif selectedOperationType == 'p': # plotting
                                item_inst = item.Plot( self.__subject_inst, type, case, configuration )      
                            else:    
                                utilities.message( type='ERROR', notSupported=selectedOperationType )                                                             

                            simData = simulationData.SimulationData( selectedOperationType, selectedOperation )
                            if configurationCustomized.location == 'local': 
                                # do mysql queries 
                                if simData.getReadFileFlags()._numerics  == True: 
                                    simData = self.__setting_inst.setNumData( simData, type, case, configuration )                         
                                    simData.writeNumData()
                                if simData.getReadFileFlags()._processing  == True: 
                                    simData = self.__setting_inst.setProcessingData( simData, type, case, configuration )
                                    simData.writeProcessingData()

                            operation_inst.run( item_inst, simData, self.__level ) 
                            self.__level = None # since level depends on item

                            del simData

                    del item_inst   
                    if len( self.__setting_inst.getItemConstituents().caseList ) > 1:       
                        typeList_counter = typeList_counter + 1
                    # else do not increment to avoid segmentation fault (case list is not used)

                #print( '\n_________________________________________________________________' )                
            del operation_inst
        
        if configurationCustomized.location == 'local':
            self.__setting_inst.disconnectFromMySQL()  # to reconnect each run in case of table update
          
        if not self.__setting_inst.getPreselectedOperation():   
            self.run()   
             

