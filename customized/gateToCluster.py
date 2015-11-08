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
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pwds'))

def operate( subject, item, operationType, operation, simulationData ):
    
    mod = __import__( subject.getComputer() )    
    try:
        f = open( configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\customized\\remote_run.sh', 'w' )
    except OSError as err:
        message.console( type='ERROR', text='OS error: {0}'.format(err) ) 
    else:
        f.write( '#!/bin/sh\n' )
        f.write( 'module load python3.3\n' )
        f.write( 'python ' + subject.getRootDirectory() + 'testingEnvironment/scripts/icbc/customized/run_remote.py ' )
        f.write( subject.getComputer() + ' ' + subject.getUser() + ' ' + subject.getCode() + ' ' + subject.getBranch() + ' ' )
        if operationType == 'b': # building
            f.write( 'No No  ' + item.getConfiguration() + ' ' )
        else:
            f.write( item.getType() + ' ' + item.getCase() + ' ' + item.getConfiguration() + ' ' )
        f.write( operationType + ' ' + operation + ' ' + str( configurationCustomized.testingDepth ) + ' ' ) 
        if operationType == 's': # simulation
            f.write( simulationData.getFlowProcess() + ' ' + simulationData.getMassProcessFlag() + ' ' + simulationData.getHeatProcessFlag() + ' ' + simulationData.getCoupledFlag() + ' ' + simulationData.getProcessing() + ' ' + simulationData.getNumberOfCPUs() + ' ' + simulationData.getLumpingFlag() + ' ' + simulationData.getNonlinearFlag() )      
        else:
            f.write( 'No No No No No No No No ')
        f.close()
      
    try:
        subprocess.call( 'plink ' + subject.getUser() + '@' + subject.getHostname() + ' -pw ' + mod.pwd + ' -m ' + configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\customized\\remote_run.sh', shell=True)# stdout=f )
    except:
        message.console( type='ERROR', text='Plink call failed' )   
    

   