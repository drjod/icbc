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

def operate( subject, item, operationType, operation, simulationData, level ):
    
    mod = __import__( subject.getComputer() )    

    try:
        if simulationData.getReadFileFlags()._numerics == True:  
            subprocess.call( configurationCustomized.winscp + ' /script=' + configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\customized\\winscp_uploadNumericsData.txt', 
                            shell=True)# stdout=f )
            print('\n')
        if simulationData.getReadFileFlags()._processing  == True:
            subprocess.call( configurationCustomized.winscp + ' /script=' + configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\customized\\winscp_uploadProcessingData.txt', 
                            shell=True)# stdout=f )
            print('\n')
    except:
        utilities.message( type='ERROR', text='Winscp call for data upload failed' ) 

    if ( operationType == 's' ):
        temporaryShellScript =  utilities.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\customized\\remoteRun' + '_' + operationType + '_' + operation + '_' + item.getType() + '_' + item.getCase() + '_' + item.getConfiguration() + '.sh' ) 
    else:
        temporaryShellScript = utilities.adaptPath( configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\customized\\remoteRun' + '_' + operationType + '_' +  operation + '_' + item.getConfiguration() + '.sh' )

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
        f.write( operationType + ' ' + operation + ' ' + str( configurationCustomized.testingDepth ) + ' ' ) 
        #if operationType == 's': # simulation
        #    f.write( simulationData.getFlowProcess() + ' ' + simulationData.getMassProcessFlag() + ' ' + simulationData.getHeatProcessFlag() + ' ' + simulationData.getCoupledFlag() + ' ' + simulationData.getProcessing() + ' ' + simulationData.getNumberOfCPUs() + ' ' + simulationData.getLumpingFlag() + ' ' + simulationData.getNonlinearFlag())      
        #else:
        #    f.write( 'No No No No No No No No')
        if operationType == 's' or operationType == 'p': # simulation or plotting
            f.write( ' ' + level )      
        else:
            f.write( ' No')
        f.close()
      
    try:
        subprocess.call( 'plink ' + subject.getUser() + '@' + subject.getHostname() + ' -pw ' + mod.pwd + ' -m ' + temporaryShellScript, shell=True)# stdout=f )
    except:
        utilities.message( type='ERROR', text='Plink call failed' )   

    if os.path.isfile(temporaryShellScript) and os.access(temporaryShellScript, os.R_OK):   
        os.remove( temporaryShellScript )
    

   