#!/bin/sh


#########################################################################################################
#
# icbc operation by JOD
#
# Task: compile, copy and test source code 
#
#########################################################################################################


cOperations=( 

	"(g)et" 
	"(u)pdate" 
	"(t)est" 
	"(s)tore" 
	              # 1ST LETTER- MIND CONSISTENCE WITH INTERFACE
) 

  			
nOperations=${#cOperations[@]}


#########################################################################################################
#
# Task: 		global configuration for selected operation
#				0: abort
#				1: restart easyPeasy
#
# Requirements:
#
#########################################################################################################


configOperation()
{

	case $operation in
			
		"0")
		    echo -e " NOTHING DONE \n"
			abort
			;;
			
		"1")  
			echo -e "NOTHING DONE\n"
		 	. $path2icbc/run.sh icbc  				# RESTART 
			;;
			
		*) ;;
			
	esac		

}

#########################################################################################################
#
# Task: 		compile selected configuration and copy this into work directory 
#
# Requirements:
#
#########################################################################################################

getExe()
{

									# BUILD_flag - SELECT_MEMBER_flag
	. $path2icbc/interface.sh $workfolder $login $cCode $cVersion compile lemonSqueezy 1 1

	. $path2icbc/interface.sh $workfolder $login $cCode $cVersion copy lemonSqueezy 1 0
	

}


#########################################################################################################
#
# Task: 		compile all source code configurations and copy into work directory
#
# Requirements:
#
#########################################################################################################


updateExe()
{

	selectedConfiguration=a				
	
	. $path2icbc/interface.sh $workfolder $login $cCode $cVersion compile lemonSqueezy 0 0

	. $path2icbc/interface.sh $workfolder $login $cCode $cVersion copy lemonSqueezy 0 0

}


#########################################################################################################
#
# Task:	        update executables and run test cases
#
# Requirements:
#
#########################################################################################################


testExe()
{


	updateExe

	# SELECT_MEMBER_flag=0			# not needed
	sndx[0]=a 				# 3 level
	sndx[1]=a
	sndx[2]=a	

	. $path2icbc/interface.sh $workfolder $login $cCode $cVersion run easyPeasy 1 1

}


#########################################################################################################
#
# Task: 		store results into home directory
#				for synchronization
#				just calls easyPeasy operation store
#
# Requirements:
#
#########################################################################################################


storeResults()
{

	. $path2icbc/interface.sh $workfolder $login $cCode $cVersion store easyPeasy 1 1
										
}


#########################################################################################################
#
# Task: 		start icbc operations
#
# Requirements: 
#
#########################################################################################################


operate()
{
	
	case $operation in
	
		"g"|"G") 
			getExe
			;;
			
		"u"|"U") 
			updateExe
			;;
			
		"t"|"T") 
			testExe
			;;
			
		"s"|"S") 
			storeResults
			;;
			
		*) 
		    echo -e " NOTHING DONE \n"
			selectOperation
			;;
			
	esac
	
	echo ""
	# echo -e "OPERATION DONE"
	
	mode=icbc
	
}


##########################################################################
