import subprocess
import fileinput
import item
import subject
import platform
import message
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized

def operate( subject, item, operationType, operation ):
  
    f = open( 'F:\\tools\\icbc-0.2\\icbc\\customized\\remote_run.sh', 'w' )
    f.write( '#!/bin/sh\n' )
    f.write( 'module load python3.3\n' )
    f.write( 'python /home/sungw389/tools/icbc-0.2/shared/run_remote.py ' )
    f.write( subject.getComputer() + ' ' + subject.getUser() + ' ' + subject.getCode() + ' ' + subject.getBranch() + ' ' )
    f.write( item.getType() + ' ' + item.getCase() + ' ' + item.getConfiguration() + ' ' )
    f.write( operationType + ' ' + operation + ' 3 \n' ) # testing depth        
    f.close()
        
    subprocess.call( 'plink sungw389@rzcluster.rz.uni-kiel.de -pw fuwyek90 -m F:\\tools\\icbc-0.2\\icbc\\customized\\remote_run.sh', shell=True)# stdout=f )
 
    print( '\n-----------------------------------------------------------------' )
    message.console( type='INFO', text='Back to ' + configurationCustomized.location + ' ' + platform.node() + ' ' + platform.system() )


    #os.remove( directoryPlots + '_genJPG.mcr' )   