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

def operate(subject, item, operation_type, operation, simulationData):
    """

    :param subject:
    :param item:
    :param operation_type:
    :param operation:
    :param simulationData:
    :return:
    """
    mod = __import__(subject.computer)

    try:
        if simulationData.read_file_flags.numerics:
            subprocess.call(configurationCustomized.winscp + ' /script=' + configurationCustomized.rootDirectory +
                            'testingEnvironment\\scripts\\icbc\\customized\\winscp_uploadNumericsData_' +
                            item.configuration + '.txt', shell=True)
            print('\n')
        if simulationData.read_file_flags.processing:
            subprocess.call(configurationCustomized.winscp + ' /script=' + configurationCustomized.rootDirectory +
                            'testingEnvironment\\scripts\\icbc\\customized\\winscp_uploadProcessingData_' +
                            item.configuration + '.txt', shell=True)
            print('\n')
    except:
        utilities.message(mode='ERROR', text='Winscp call for data upload failed' ) 

    if ( operation_type == 's' ): # example
        temporaryShellScript =  utilities.adapt_path(
            configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\temp\\remoteRun' + '_' +
            operation_type + '_' + operation + '_' + item.type + '_' + item.case + '_' + item.configuration + '.sh')
    else: # building depends only on configuration (plotting is always local)
        temporaryShellScript = utilities.adapt_path(
            configurationCustomized.rootDirectory + 'testingEnvironment\\scripts\\icbc\\temp\\remoteRun' + '_' +
            operation_type + '_' +  operation + '_' + item.configuration + '.sh')

    try:
        f = open(temporaryShellScript, 'w')
    except OSError as err:
        utilities.message(mode='ERROR', text='OS error: {0}'.format(err))
    else:
        f.write('#!/bin/sh\n' )
        f.write('module load python3.3\n')
        f.write('python ' + subject.directory_root + 'testingEnvironment/scripts/icbc/customized/run_remote.py ')
        f.write(subject.computer + ' ' + subject.user + ' ' + subject.code + ' ' + subject.branch + ' ')
        if operation_type == 'b': # building
            f.write('No No  ' + item.configuration + ' ')
        else:
            f.write(item.type + ' ' + item.case + ' ' + item.configuration + ' ')
        f.write(operation_type + ' ' + operation)
        #if operation_type == 's': # simulation
        #    f.write( simulationData.getFlowProcess() + ' ' + simulationData.getMassProcessFlag()
        # + ' ' + simulationData.getHeatProcessFlag() + ' ' + simulationData.getCoupledFlag() + ' '
        # + simulationData.getProcessing() + ' ' + simulationData.getNumberOfCPUs() + ' '
        # + simulationData.getLumpingFlag() + ' ' + simulationData.getNonlinearFlag())
        #else:
        #    f.write( 'No No No No No No No No')
        f.close()
      
    try:
        subprocess.call('plink ' + subject.user + '@' + subject.hostname +
                        ' -pw ' + mod.pwd + ' -m ' + temporaryShellScript, shell=True)
    except:
        utilities.message(mode='ERROR', text='Plink call failed')

    if os.path.isfile(temporaryShellScript) and os.access(temporaryShellScript, os.R_OK):   
        os.remove(temporaryShellScript)
