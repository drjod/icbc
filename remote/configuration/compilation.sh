#!/bin/sh


#########################################################################################
#
# compilation configuration by JOD
#
# Task: set paths for compiler and libs
#		specification for OpenGeoSys on RZ cluster Kiel
#				INTEL COMPILER
#				cmake
#				MPI / OPENMP
#				MKL
#				PETSC
#
# Requirements: login variable is set
#				

#########################################################################################


cConfigurations=( 			# SOURCE CODE CONFIGURATIONS
	"OGS_FEM" 
	"OGS_FEM_SP" 
	"OGS_FEM_MKL" 
	"OGS_FEM_PETSC" 
	"OGS_FEM_MPI" 
 )


### LIBS


MKL="cluster/Software/intel14/composer_xe_2013_sp1.0.080/mkl"
MKL_FOLDER="$(pwd)/Libs/MKL"

# if [ "$VERSION_PETSC" == "3.5" ]; then
 
	# PETSC="cluster/Software/Dpetsc/petsc-3.5.3_intel"  

# else

	PETSC="work_j/SoftwareSL/Dpetsc/Dintel14/petsc-3.3-p4"				

# fi
	
	
### COMPILER

INTEL="cluster/Software/intel14/composer_xe_2013_sp1/bin"
INTEL_MPI="cluster/Software/intel14/impi/4.1.1.036/intel64/bin"

									
ICC="$INTEL/icc"
ICPC="$INTEL/icpc"

MPIICC="$INTEL_MPI/mpiicc"
MPIICPC="$INTEL_MPI/mpiicpc"

# if [ "$VERSION_PETSC" == "3.5" ]; then
 
	# INTEL_MPI="opt/mpich/bin"            
	# MPIICC_PETSC="$INTEL_MPI/mpicc"    					
	# MPIICPC_PETSC="$INTEL_MPI/mpicxx"  

# else

	MPIICC_PETSC="$MPIICC"   					
	MPIICPC_PETSC="$MPIICC" 			

# fi
	
	
compilerTable=( #	-DPARALLEL_USE_OPENMP= 	-DCMAKE_C_COMPILER= 	-DCMAKE_CXX_COMPILER=		
					"OFF"					"$ICC"					"$ICPC"					# OGS_FEM 
					"OFF"					"$ICC"					"$ICPC"					# OGS_FEM_SP 
					"ON"					"$ICC"					"$ICPC"					# OGS_FEM_MKL
					"OFF"					"$MPIICC_PETSC"			"$MPIICPC_PETSC"		# OGS_FEM_PETSC 
					"OFF"					"$MPIICC"				"$MPIICPC"				# OGS_FEM_MPI 
 )
 
 
 . /$INTEL/compilervars.sh intel64
 # . /$INTEL_MPI/mpivars.sh
 
 
###### PATHS FOR MKL 


export MKLROOT=/$MKL
export MKLPATH=/$MKL/lib/intel64
export MKLINCLUDE=/$MKL/include
export MKL_INCLUDE_DIR=$MKL_INCLUDE_DIR:/$MKL/include
export MKL_LIB_PATH=$MKL_LIB_PATH:/$MKL/lib/intel64
	
export MKL_PROCESS_INCLUDES=$MKL_PROCESS_INCLUDES:/$MKL_FOLDER/64 
export MKL_PROCESS_LIBS=$MKL_PROCESS_LIBS:/$MKL_FOLDER/64
	
export PATH=$PATH:/cluster/intel/mkl/10.2.2.025/lib/64
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/$MKL/lib/intel64


. /$MKL/bin/intel64/mklvars_intel64.sh


###### PATHS FOR PETSC


export PETSC_DIR=/$PETSC
export PETSC_ARCH=linux-intel-opt
export PATH=$PATH:/$PETSC/include
     
export PATH=$PATH:/cluster/Software/intel14/composer_xe_2013_sp1.0.080/compiler/lib/intel64 


##############################################################################################
