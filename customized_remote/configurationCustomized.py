#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
#import utilites
     
outputFile = 'screenout.txt'	 
location = 'remote'
rootDirectory = '/home/sungw389/'
computer = 'rzcluster'

verbosity = '1'

walltime = '2:00:00'
queue = 'angus'

compiler = 'intel1502'   # must be consistent with build directory and therefore, with script compileInKiel.sh
composer = 'composer_xe_2015.2.164'
mpi_version = '5.0.3.048'

# compiler = 'intel16'
# composer = 'compilers_and_libraries_2016.0.109/linux'
# mpi_version = '5.1.1.109'

setCompilerVariables = '. /cluster/Software/' + compiler + '/' + composer + '/bin/compilervars.sh  intel64\n'
setMklVariables = '. /cluster/Software/' + compiler + '/' + composer + '/mkl/bin/intel64/mklvars_intel64.sh\n'
setMpiVariables = '. /cluster/Software/' + compiler + '/impi/' + mpi_version + '/intel64/bin/mpivars.sh\n'

# id_called_process = 'unused' # to identify uploaded files

# for local computer actually - used since variables are imported by shared file
preplot = ''
tecplot = ''
winscp = ''
localBuild = ''
localRun = ''













