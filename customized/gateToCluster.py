import subprocess
import fileinput
import item
import subject
import platform
import message
import simulationData
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized

def operate( subject, item, operationType, operation, simulationData ):
 
    f = open( configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\customized\\remote_run.sh', 'w' )
    f.write( '#!/bin/sh\n' )
    f.write( 'module load python3.3\n' )
    f.write( 'python /home/sungw389/testingEnvironment/scripts/icbc/customized/run_remote.py ' )
    f.write( subject.getComputer() + ' ' + subject.getUser() + ' ' + subject.getCode() + ' ' + subject.getBranch() + ' ' )
    if operationType == 'b': # building
        f.write( 'No No  ' + item.getConfiguration() + ' ' )
    else:
        f.write( item.getType() + ' ' + item.getCase() + ' ' + item.getConfiguration() + ' ' )
    f.write( operationType + ' ' + operation + ' 3 ' ) # testing depth  
    if operationType == 's': # simulation
        f.write( simulationData.getFlowProcess() + ' ' + simulationData.getMassProcessFlag() + ' ' + simulationData.getHeatProcessFlag() + ' ' + simulationData.getCoupledFlag() + ' ' + simulationData.getProcessing() + ' ' + simulationData.getNumberOfCPUs() + ' ' + simulationData.getLumpingFlag() + ' ' + simulationData.getNonlinearFlag() )      
    else:
        f.write( 'No No No No No No No No ')
    f.close()
      
    subprocess.call( 'plink sungw389@rzcluster.rz.uni-kiel.de -pw fuwyek90 -m ' + configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\customized\\remote_run.sh', shell=True)# stdout=f )
 
    #print( '\n-----------------------------------------------------------------' )
    #message.console( type='INFO', text='Back to ' + configurationCustomized.location + ' ' + platform.node() + ' ' + platform.system() )

   