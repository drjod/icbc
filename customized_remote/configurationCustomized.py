#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
#import utilites
     
location = 'remote'
rootDirectory = '/home/sungw389/'
computer = 'rzcluster'

verbosity = '1'

walltime = '2:00:00'
queue = 'angus'

setCompilerVariables = '. /cluster/Software/intel1502/composer_xe_2015.2.164/bin/compilervars.sh  intel64\n'
setMklVariables = '. /cluster/Software/intel1502/composer_xe_2015.2.164/mkl/bin/intel64/mklvars_intel64.sh\n'
setMpiVariables = '. /cluster/Software/intel1502/impi/5.0.3.048/intel64/bin/mpivars.sh\n'









