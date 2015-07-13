#!/bin/sh

#########################################################################################
#
# icbc run by JOD
#
# Task: start icbc / easyPeasy / lemonSqueezy
#		main function
#
# Requirements: do configurations
#				partmesh
#				winscp if synchronization
#
#########################################################################################


##### CONFIGURATION


login="sungw389"	# REMOTE

path2icbc="/home/$login/tools/icbc"		 # !!!!! VARIABLE login MUST ALREADY BE INITIALIZED - SUCKS 
. $path2icbc/configuration/remote.sh 
. $path2icbc/configuration/shared.sh # OPTAINED FROM LOCAL - WINSCP SYNCHRONIZATION


##### SAY HELLO ON SHELL

echo -e "\n_________________________()_()_________________________________________________"
echo -e "_________________________('.')_________________________________________________"
echo -e "_________________________()  $1 $icbcVersion      ________________________"
echo -e "_______________________________________________________________________________"


##### SELECT VERSION


nVersions=${#cVersions[@]}    # OF SOURCE CODE
. $path2icbc/select.sh
selectVersion


##### INITIALIZATION FOR LOOP

mode=$1
operation=1					# NOT ZERO
SELECT_MEMBER_flag=1



#########################################################################################
#
# Task: main loop for icbc / easyPeasy / lemonSqueezy
#		select member (input folder / configuration), select and do operation
#
# Requirements: SELECT_MEMBER_flag
#
#########################################################################################


loop()
{
	
	. $path2icbc/$mode/global.sh   # GET FUNCTIONS (MEMBER, OPERATIONS)
	getSetup					   # GET CONFIGURATIONS (EASY PEASY INPUT FOLDER, LEMON SQUEEZY COMPILATION)
	
	ALLOW_BUILD_flag=1	# USED IN LEMON SQUEEZY

	if [ "$SELECT_MEMBER_flag" -eq 1 ]; then

		selectMember
		SELECT_MEMBER_flag=0 	# SELECTED
	fi

	selectOperation
	configOperation 	# GLOBALLY

	operateGlobally

	if [ "$operation" != "0" ]; then

		loop 

	fi

}


if [ "$operation" != "0" ]; then

	loop 

fi


##### EXIT
