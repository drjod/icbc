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

    ##############################################
    #  Environment: constructor
    #  Task:
    #    initialization subject, setting   
    #    passes preselected variables
    #  
    
    def __init__( self, superuser = None, computer = None, user = None, code = None, branch = None, 
                  typeList = [None], caseList = [[None]], configurationList = [None], 
                  operationType = None,     # [b,s,p]
                  operation = None,   # one-character string
                  testMode = '0', testLevel = '0',			  
                  mySQL_user='root', mySQL_password='*****', mySQL_host='localhost', mySQL_schema='testing_environment' ):

        self.__testing = setting.testing( testMode, testLevel )
    
        mySQL_struct = setting.mySQL ( mySQL_user, mySQL_password, mySQL_host, mySQL_schema )
        self.__subject_inst = subject.Subject( superuser, computer, user, code, branch  )                                                              
        self.__setting_inst = setting.Setting ( typeList, caseList, configurationList, 
                                                operationType, operation, 
                                                self.__testing, 
                                                mySQL_struct )

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
            #if not state:
            #    utilities.message( type='INFO', text='Set state ' + state )
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
    #      generate operation instance (configure, select and execute operation)
    #      database calls are done (to get items lists) if on local computer
    #      loop over items lists to call operation potentially (if operation is called for item, depends on test mode)
    #
                            
    def run( self ): 
        #selects
    
        if configurationCustomized.location == 'local':
            self.__setting_inst.connectToMySQL()   
        self.__subject_inst.select( self.__setting_inst )  
        
        selectedOperationType = self.__setting_inst.selectOperationType()              
        operation_inst = self.setCurrentOperation( selectedOperationType ) # currentOperation is environment member (selectedOperation could be reselect)
        
        if operation_inst.getSelectedOperation() == 's': # reselect
            self.__setting_inst.reselect( self.__subject_inst  ) # decide what to reselect
            self.__reselectFlag = True # than no operation executed
        else:   
            if configurationCustomized.location == 'local':         
                self.__setting_inst.SetItemsLists( selectedOperationType, self.__currentOperation,self.__subject_inst.getComputer() )
            if self.__reselectFlag == True:
                self.__reselectFlag = False # do no operation, rather repeat run with empty string for entity to reselect
            elif self.__setting_inst.getItemConstituents().typeList == None or self.__setting_inst.getItemConstituents().caseList == None or self.__setting_inst.getItemConstituents().configurationList == None:
                utilities.message( type='ERROR', text='Selection of test items failed - No operation' )
            else:
                typeList_counter = 0  
                configuration = None   
     
                for type in self.__setting_inst.getItemConstituents().typeList:                   
                    for case in self.__setting_inst.getItemConstituents().caseList[typeList_counter]:
                        for configuration in self.__setting_inst.getItemConstituents().configurationList:
                            
                            if self.checkIfItemInvolved( case ) == '1':
                                self.goForItemRun( operation_inst, type, case, configuration )

                    if len( self.__setting_inst.getItemConstituents().caseList ) > 1:       
                        typeList_counter = typeList_counter + 1
                    # else do not increment to avoid segmentation fault (case list is not used)

                #print( '\n_________________________________________________________________' )                
            del operation_inst
        
        if configurationCustomized.location == 'local':
            self.__setting_inst.disconnectFromMySQL()  # to reconnect each run in case of table update
        
        if not self.__setting_inst.getPreselectedOperation():   
            self.run()   # repeat if operation was not preselected (test mode or remote)
             
    #################################################################
    #  Environment: setCurrentOperation
    #  Task:
    #     generates intance operartion for environment and returns it
    #     sets currentOperation (member variable of environement) if nor reselect chosen 
    #

    def setCurrentOperation( self, operationType ):

        if operationType == 'b': # building
            operation_inst = operation.Building( self.__subject_inst )              
        elif operationType == 's':  # simulating
            operation_inst = operation.Simulating( self.__subject_inst ) 
        elif operationType == 'p':  # plotting  
            operation_inst = operation.Plotting( self.__subject_inst )                           
        else:    
            utilities.message( type='ERROR', notSupported=operationType )
        if self.__reselectFlag == False:
            selectedOperation = operation_inst.selectOperation( self.__setting_inst.getPreselectedOperation() )
            if selectedOperation is not 's': # s stands for reselect
                self.__currentOperation = selectedOperation # reselect not choosen

        return operation_inst

    #################################################################
    #  Environment: checkIfItemInvolved
    #  Task:
    #     check testMode, state, testLevel 
    #     used for simulation, plotting  operation type (case item exists)
    #     (all items (i.e. configurations) involved in building operation type)
    #
                            
    def checkIfItemInvolved( self,  case ): 

        executeFlag = '1'
         
        if configurationCustomized.location == 'local' and case: 
            if self.__testing.mode == '0': 
                # no test mode - select everything by typing on console 
                #                and than the items in the loop (in environment run) is involved
                pass
            elif self.__testing.mode == '1': 
                # via browser
                executeFlag = self.__setting_inst.getColumnForCase( case, 'state' )    # database query  
            elif self.__testing.mode == '2':
                # jenkins
                if int(self.__testing.level) < int(self.__setting_inst.getColumnForCase( case, 'test_level' )): 
                    executeFlag = '0'    
            else:    
                utilities.message( type='ERROR', notSupported=self.__testing.mode )                                               
               
        return executeFlag
                                  

    #################################################################
    #  Environment: goForItem Run
    #  Task:
    #     generate item instance
    #     generate simulationData - write files (for numerics, processing) 
    #     and then call operation run function  
    #
                            
    def goForItemRun( self,  operation_inst, type, case, configuration ): 

        selectedOperationType = operation_inst.getSelectedOperationType()
                                      
        if selectedOperationType == 'b': # building 
            item_inst = item.Build( self.__subject_inst, configuration )
        elif selectedOperationType == 's': # simulating
            item_inst = item.Sim( self.__subject_inst, type, case, configuration )
        elif selectedOperationType == 'p': # plotting
            item_inst = item.Plot( self.__subject_inst, type, case, configuration )      
        else:    
            utilities.message( type='ERROR', notSupported=operation_inst.getSelectedOperationType() )
            return 0
                                                                                             
        simData = simulationData.SimulationData( selectedOperationType, operation_inst.getSelectedOperation() )
        if configurationCustomized.location == 'local': 
            #      do mysql queries 
            if simData.getReadFileFlags()._numerics  == True: 
                simData = self.__setting_inst.setNumData( simData, type, case, configuration )  
                if self.__subject_inst.getLocation() == 'remote':  
                    # file transfer              
                    simData.writeNumData( configuration )
            if simData.getReadFileFlags()._processing  == True: 
                simData = self.__setting_inst.setProcessingData( simData, type, case, configuration )
                if self.__subject_inst.getLocation() == 'remote':  
                    # file transfer 
                    simData.writeProcessingData( configuration )
                                
        operation_inst.run( item_inst, simData ) 
                                 
        del simData                         
        del item_inst   