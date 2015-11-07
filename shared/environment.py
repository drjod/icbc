import operation
import message
import shutil
import configurationShared
import item
import subject
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import setting
import configurationCustomized
import simulationData




##############################################
#  class: Environment
#  Task:
#      hosts instance of classes subject, setting
#      member function run is main function  
#      

class Environment:  
  
    __reselectFlag = False
    ##############################################
    #  Environment: constructor
    #  Task:
    #    initialization subject, setting   
    #    passes preselected variables
    #  
    
    def __init__( self, computer =' ', user =' ', code =' ', branch =' ', 
                  typeList = [' '], caseList = [[' ']], configurationList = [' '], 
                  operationType = ' ',     # [b,t]
                  operation = ' ', 
                  testingDepth = ' ',
                  flowProcess = ' ', massProcessFlag = ' ', heatProcessFlag = ' ',
                  coupledFlag = ' ', processing = ' ', numberOfCPUs = ' ' , lumpingFlag = ' ', nonlinearFlag = ' ',								  
                  mySQL_user='root', mySQL_password='*****', mySQL_host='localhost', mySQL_schema='testing_environment' ):
                  
        mySQL_struct = setting.MySQL ( mySQL_user, mySQL_password, mySQL_host, mySQL_schema )
        self.__subject_inst = subject.Subject( computer, user, code, branch  )                                                              
        self.__setting_inst = setting.Setting ( typeList, caseList, configurationList, 
                                                operationType, operation, 
                                                testingDepth, 
                                                mySQL_struct )
        self.__simulationData = simulationData.SimulationData( flowProcess, massProcessFlag, heatProcessFlag, coupledFlag, processing, numberOfCPUs, lumpingFlag, nonlinearFlag)
        print( '\n-----------------------------------------------------------------' )
        
        if int( configurationCustomized.verbosity ) > 1:
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
            if caseList[0][0] is not ' ':
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
            if simulationData is not ' ':
                __simulationData = simulationData
                message.console( type='INFO', text='Simulation data set' )                
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
        self.__subject_inst.select( self.__setting_inst )  

        selectedOperationType = self.__setting_inst.selectOperationType()              
        if selectedOperationType == 'b': # building
            operation_inst = operation.Building( self.__subject_inst )              
        elif selectedOperationType == 's':  # simulating
            operation_inst = operation.Simulating( self.__subject_inst ) 
        elif selectedOperationType == 'p':  # plotting  
            operation_inst = operation.Plotting( self.__subject_inst )                           
        else:    
            message.console( type='ERROR', notSupported=selectedOperationType )  
        if self.__reselectFlag == False:
            operation_inst.selectOperation( self.__setting_inst.getPreselectedOperation() )
        
     
        if operation_inst.getSelectedOperation() == 's': 
            self.__setting_inst.reselect( self.__subject_inst )
            self.__reselectFlag = True
        else:   
            if configurationCustomized.location == 'local':                        
                # select test cases (type, case, configuration)
                if selectedOperationType == 'b': # building 
                    self.__setting_inst.setTypeList( [' '] ) 
                    self.__setting_inst.setCaseList( [[' ']] )                          
                    self.__setting_inst.setConfigurationList( self.__setting_inst.selectTestCasesGroup( groupType = 'configurations',
                                                                                                        computerOfSubject = self.__subject_inst.getComputer() ) )                        
                elif selectedOperationType == 's':  # simulating
                    self.__setting_inst.setTypeList( self.__setting_inst.selectTestCasesGroup( groupType = 'types' ) ) 
                    self.__setting_inst.setCaseList( self.__setting_inst.selectTestCasesGroup( groupType = 'cases' ) )                                      
                    self.__setting_inst.setConfigurationList( self.__setting_inst.selectTestCasesGroup( groupType = 'configurations',
                                                                                                        computerOfSubject = self.__subject_inst.getComputer() ) ) 
                elif selectedOperationType == 'p':  # plotting
                    self.__setting_inst.setTypeList( self.__setting_inst.selectTestCasesGroup( groupType = 'types' ) )
                    if operation_inst.getSelectedOperation() == 'j': # generateJPGs 
                        self.__setting_inst.setCaseList( [[' ']] ) 
                        self.__setting_inst.setConfigurationList( [' '] ) 
                    else:      
                        self.__setting_inst.setCaseList( self.__setting_inst.selectTestCasesGroup( groupType = 'cases' ) )                                      
                        self.__setting_inst.setConfigurationList( self.__setting_inst.selectTestCasesGroup( groupType = 'configurations',
                                                                                                        computerOfSubject = self.__subject_inst.getComputer() ) )  
            # loop over test cases 
            if self.__reselectFlag == True:
                self.__reselectFlag =False
            else:
                typeList_counter = 0  
                configuration = ' '      
                for type in self.__setting_inst.getTestCases().typeList: 
                    for case in self.__setting_inst.getTestCases().caseList[typeList_counter]:
                        for configuration in self.__setting_inst.getTestCases().configurationList:

                            if selectedOperationType == 'b': # building 
                                item_inst = item.Build( self.__subject_inst, configuration )
                            elif selectedOperationType == 's': # simulating
                                item_inst = item.Sim( self.__subject_inst, type, case, configuration )
                            elif selectedOperationType == 'p': # plotting
                                item_inst = item.Plot( self.__subject_inst, type, case, configuration )      
                            else:    
                                message.console( type='ERROR', notSupported=selectedOperationType )                                                             

                            if configurationCustomized.location == 'local': 
                                # do mysql queries 
                                if selectedOperationType == 's':  
                                    # get data to write *.num, *.pbs or partition mesh
                                    self.__simulationData = self.__setting_inst.setSimulationData( self.__simulationData, type, case, configuration )                         

                            operation_inst.run( item_inst, self.__simulationData ) 

                    del item_inst          
                    typeList_counter = typeList_counter + 1

                print( '\n-----------------------------------------------------------------' )                
            del operation_inst
        
            
          
        if self.__setting_inst.getPreselectedOperation() == ' ':   
            self.run()   
             

