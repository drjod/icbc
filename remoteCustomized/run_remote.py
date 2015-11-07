import configurationCustomized
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
import environment
import platform
import message

message.console( type='INFO', text='On ' + configurationCustomized.location + ' '  + platform.node() + ' ' + platform.system() )

environment = environment.Environment(
                                      computer = sys.argv[1],
                                      user = sys.argv[2], 
                                      code = sys.argv[3],
                                      branch = sys.argv[4],
                                      typeList= [sys.argv[5]], 
                                      caseList= [[sys.argv[6]]], 
                                      configurationList= [sys.argv[7]], 
                                      operationType= sys.argv[8],  
                                      operation = sys.argv[9], 
									  testingDepth = sys.argv[10], 
                                      flowProcess = sys.argv[11],
                                      massProcessFlag = sys.argv[12],
                                      heatProcessFlag = sys.argv[13],
                                      coupledFlag = sys.argv[14],
                                      processing = sys.argv[15],
                                      numberOfCPUs = sys.argv[16],									  
                                      lumpingFlag = sys.argv[17],
                                      nonlinearFlag = sys.argv[18],									  
                                      mySQL_user = ' ', 
                                      mySQL_password = ' ',
                                      mySQL_host = ' ',
                                      mySQL_schema = ' '
                                      )
                  
environment.run()


                  

 




