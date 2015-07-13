#!/bin/sh


###################################################################################################
#
# icbc select by JOD 
#
# Task:       	 input via shell
#
# Requirements:
#
###################################################################################################

	:

###################################################################################################
#
# Task:      	version input    
#
# Requirements:  configuration_shared.sh and global.sh
#
###################################################################################################


selectVersion()
{

	# echo ""
	# echo -e "\n_______________________________________________________________________________\n"
	echo ""

	echo -e "\nSELECT VERSION\n"


	for ((i=0; i<$nVersions; i++))
	do

		echo -e "\t$i : ${cVersions[$i]}"

	done

	echo ""
	read -n1 version_id
	echo ""
	cVersion=${cVersions[$version_id]}
	
	if [ "$version_id" -ge $nVersions ] || [ "$version_id" -lt 0 ] ; then

		echo -e "\n\n   ERROR - Version does not exist\n\n"
		abort
	
	fi

}


###################################################################################################
#
# Task:          operation input
# Requirements:  configuration in global.sh
#
###################################################################################################


selectOperation()
{

	echo -e "\n_______________________________________________________________________________\n"
	echo "Operating on $cCode $cVersion"
	echo -e "\n_______________________________________________________________________________\n"
	echo ""

	echo -e "\nSELECT OPERATION\n"


	for ((i=0; i<$((nOperations)); i++))
	do

		echo -e "\t${cOperations[$i]}"

	done

	echo ""
	read -n1 operation
	echo ""

}


