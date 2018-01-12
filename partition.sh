#!/bin/bash

##########################################################################
#
# partition by JOD
#
# Task: interface to partmesh (METIS)
#               can be directly called
#               changes name of *.msh to *_mesh.txt if partition by nodes
#
# Requirements: input parameters
#                               $1: number of partitions
#                               $2: partition by -n nodes or -e elements
#                               $3: -asci or else (meaning binary)
#                               $4: path to mesh or empty
#                               !!!! take care that only one *msh file in folder
#
#                set path to partmesh with environmental variable PARTMESH_PATH
#                (export PARTMESH_PATH="/home/...")
#
###########################################################################


#####   SET PATH AND MESH FILE NAME


if [ "$4" != "" ]; then
        path2msh=$4              # FOLDER WITH MESH GIVEN BY $4
else
    	path2msh=$(pwd)          # MESH IS IN CURRENT FOLDER
fi
meshfile=$(find $path2msh -name *.msh)  # including path
# meshfile=$(echo $path2msh | ls | grep *.msh)

echo $meshfile

if [ "$meshfile" == "" ]; then
	echo "ERROR meshfile not found - might be zero or more than one file *msh in folder"
else
	meshfilename=${meshfile%.*}  # remove extension .msh (still with path)

	#####   CALL PARTMESH

	$PARTMESH_PATH/partmesh --ogs2metis $meshfilename
	$PARTMESH_PATH/partmesh --metis2ogs -np $1 $2 $3 $meshfilename

	#### CLEAR-UP

	# rm ${meshfile%.*}\.mes*

	case $2 in
		"-n")  # PARTITION BY NODES
        		# rm $path2msh/$meshfilename\_ren*
                	mv $meshfile ${meshfilename}.meshbackup    # CHANGE NAME of *.msh file

                	#if [ "$3" == "-asci" ]; then
                        	# mv $meshfilename\_partitioned_$1\.msh $meshfilename\_partitioned.msh
                	#fi
                	;;

        		"-e") # PARTITION BY ELEMENTS
                	if [ "$3" == "-asci" ]; then
                        	mv $meshfilename\.$1\ddc $meshfilename\.ddc
                	else
                    		echo "ERROR - Option $3 not supported"
                	fi
                	;;

        	*)
          		echo "ERROR - Option $2 not supported"
                	;;
	esac

fi
