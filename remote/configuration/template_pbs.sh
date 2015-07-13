#!/bin/sh


Spread_batch_sequential(){

echo "#!/bin/bash
#PBS -o /$path2member/screenout.txt
#PBS -j oe
#PBS -r n
#PBS -l walltime=3:00:00
#PBS -l select=1:ncpus=1:mem=3gb
#PBS -l place=group=host
#PBS -q angus
#PBS -N test_$indices
####

cd \$PBS_O_WORKDIR

#Initialisierung der Module-Umgebung
. /usr/share/Modules/init/bash
#. /usr/local/Modules/3.2.6/init/bash



# Initialisierung der Intel-Umgebung (Compiler und Intel-MKL)
. /cluster/Software/intel14/composer_xe_2013_sp1/bin/compilervars.sh  intel64
. /cluster/Software/intel14/composer_xe_2013_sp1.0.080/mkl/bin/intel64/mklvars_intel64.sh

time /$workfolder/$login/$cCode/$cVersion/ogs_${cLevel2[${ndx[2]}]} /$path2member/test

qstat -f \$PBS_JOBID
exit" > /$path2member/$batch 


}


###############################################################################


Spread_batch_parallel(){


echo "#!/bin/bash
#PBS -o /$path2member/screenout.txt
#PBS -j oe
#PBS -r n
#PBS -l walltime=3:00:00
#PBS -l select=1:ncpus=${numberCPUs[${ndx[2]}]}:mpiprocs=${numberCPUs[${ndx[2]}]}:mem=2gb
#PBS -l place=scatter
#PBS -q angus
#PBS -N test_$indices
####

cd \$PBS_O_WORKDIR

#Initialisierung der Module-Umgebung
. /usr/share/Modules/init/bash
#. /usr/local/Modules/3.2.6/init/bash
#module load openmpi-gnu


# Initialisierung der Intel-Umgebung (Compiler und Intel-MPI)
. /cluster/Software/intel14/composer_xe_2013_sp1/bin/compilervars.sh  intel64
. /cluster/Software/intel14/impi/4.1.1.036/intel64/bin/mpivars.sh

time mpirun -r rsh -machinefile \$PBS_NODEFILE -n ${numberCPUs[${ndx[2]}]} /$workfolder/$login/$cCode/$cVersion/ogs_${cLevel2[${ndx[2]}]} /$path2member/test

qstat -f \$PBS_JOBID
exit" > /$path2member/$batch 


}
