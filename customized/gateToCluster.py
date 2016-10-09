import subprocess
import fileinput
import item
import subject
import platform, utilities
import simulationData
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pwds'))

#################
#
# Restriction:
#     python 3.3 on cluster (TODO: make object to get such data from database and hold them)

def operate( subject, item, operationType, operation, simulationData ):
    
    mod = __import__( subject.getComputer() )    

    try:
        if simulationData.getReadFileFlags()._numerics == True:  
            subprocess.call( configurationCustomized.winscp + ' /script=' + configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\customized\\winscp_uploadNumericsData_' + item.getConfiguration() + '.txt', 
                            shell=True)# stdout=f )
            print('\n')
        if simulationData.getReadFileFlags()._processing  == True:
            subprocess.call( configurationCustomized.winscp + ' /script=' + configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\customized\\winscp_uploadProcessingData_' + item.getConfiguration() + '.txt', 
                            shell=True)# stdout=f )
            print('\n')
    except:
        utilities.message( type='ERROR', text='Winscp call for data upload failed' ) 

    if ( operationType == 's' ): # example
        temporaryShellScript =  utilities.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\temp\\remoteRun' + '_' + operationType + '_' + operation + '_' + item.getType() + '_' + item.getCase() + '_' + item.getConfiguration() + '.sh' ) 
    else: # building depends only on configuration (plotting is always local)
        temporaryShellScript = utilities.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\temp\\remoteRun' + '_' + operationType + '_' +  operation + '_' + item.getConfiguration() + '.sh' )

    try:
        f = open( temporaryShellScript, 'w' )
    except OSError as err:
        utilities.message( type='ERROR', text='OS error: {0}'.format(err) ) 
    else:
        f.write( '#!/bin/sh\n' )
        f.write( 'module load python3.3\n' )
        f.write( 'python ' + subject.getRootDirectory() + 'testingEnvironment/scripts/icbc/customized/run_remote.py ' )
        f.write( subject.getComputer() + ' ' + subject.getUser() + ' ' + subject.getCode() + ' ' + subject.getBranch() + ' ' )
        if operationType == 'b': # building
            f.write( 'No No  ' + item.getConfiguration() + ' ' )
        else:
            f.write( item.getType() + ' ' + item.getCase() + ' ' + item.getConfiguration() + ' ' )
        f.write( operationType + ' ' + operation ) 
        #if operationType == 's': # simulation
        #    f.write( simulationData.getFlowProcess() + ' ' + simulationData.getMassProcessFlag() + ' ' + simulationData.getHeatProcessFlag() + ' ' + simulationData.getCoupledFlag() + ' ' + simulationData.getProcessing() + ' ' + simulationData.getNumberOfCPUs() + ' ' + simulationData.getLumpingFlag() + ' ' + simulationData.getNonlinearFlag())      
        #else:
        #    f.write( 'No No No No No No No No')
        f.close()
      
    try:
        subprocess.call( 'plink ' + subject.getUser() + '@' + subject.getHostname() + ' -pw ' + mod.pwd + ' -m ' + temporaryShellScript, shell=True)# stdout=f )
    except:
        utilities.message( type='ERROR', text='Plink call failed' )   

    if os.path.isfile(temporaryShellScript) and os.access(temporaryShellScript, os.R_OK):   
        os.remove( temporaryShellScript )
    

   