#!/bin/sh


#########################################################################################
#
# icbc interface by JOD
#
# Task: Link local and remote
#		link icbc to easyPeasy and lemonSqueezy
#
# Requirements: mind input parameters (see configuration below) 
#
#########################################################################################


##### CONFIGURATION


workfolder=$1
login=$2
cCode=$3
cVersion=$4

if [ "$6" == "lemonSqueezy" ]; then

	operation=${5:2:1}   # 3rd letter

else

	operation=${5:0:1}   # 1st letter

fi


##### FOR CALL FROM LOCAL 


path2icbc="/home/$login/tools/icbc"   # !!!!! VARIABLE login MUST ALREADY BE INITIALIZED - SUCKS 
. $path2icbc/configuration/remote.sh   
. $path2icbc/configuration/shared.sh 

nVersions=${#cVersions[@]} 	# OF SOURCE CODE


##### INITIALIZATION


mode=$6						# !!!!! PARAMETER TRANSFER NEEDED 
ALLOW_BUILD_flag=$7				# TO ENABLE icbc CALLING 		
SELECT_MEMBER_flag=$8		# easyPeasy and lemonSqueezy	


# echo "DEBUG - workfolder $1 - login $2 - cCode $3 - cVersion $4 - operation $5 - mode $6 - BUILD_flag $7 - SELECT_MEMBER_flag $8"

 
#########################################################################################


if	[ "$mode" == "easyPeasy" ] || [ "$mode" == "lemonSqueezy" ]; then	

	echo -e "\n_______________________________________________________________________________"
	echo "__________________     $mode     ___________ ^ ^ _____________"
	echo -e "__________________________________________________('.')________________________"

fi


#####  SINGLE LOOP - SELECT MEMBER AND DO (ALREADY KNOWN) OPERATION


. $path2icbc/$mode/global.sh 	# GET SELECT AND OPERATION FUNCTIONS
getSetup
				
if [ "$SELECT_MEMBER_flag" -eq 1 ]; then	

	selectMember

fi

configOperation
operateGlobally
