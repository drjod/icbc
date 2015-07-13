#!/bin/sh


#############################################################################################
#
# lemon squeezy global by JOD
#
# Task: Take member for operation
#
# Requirements: 
#
#############################################################################################


. $path2icbc/lemonSqueezy/operation.sh

###################################################################################################
#
# Task:          get compiler configuration  
#        
# Requirements: 
#
###################################################################################################


getSetup()
{
	
	. $path2icbc/configuration/compilation.sh  
  	
	nConfigurations=${#cConfigurations[@]}

}


#############################################################################################
#
# Task: 	build or not? 
#			select via shell
#			
# Requirements: set BUILD_flag to unity
#
#############################################################################################


setBuildFlag()
{

	
	if [ "$ALLOW_BUILD_flag" -eq 1 ]; then

		echo -e "\nCreate Build Files ([y]es or no)?"

		read -n1 input

		if [ "$input" == "y" ]; then

			ALLOW_BUILD_flag=1

		else

			ALLOW_BUILD_flag=0
			
		fi

	fi

}


#############################################################################################
#
# Task: 		configuration selection via shell
#
# Requirements: configuration.sh
#
#############################################################################################


selectMember()
{

	echo -e "_______________________________________________________________________________\n"
	echo -e "\nSELECT CONFIGURATION\n" 

	for (( i=0; i<${#cConfigurations[@]}; i++ ))
	do
		echo -e "\t$i: ${cConfigurations[$i]}"
	done
	echo -e "\ta: all"

	read -n1 selectedConfiguration

}


#############################################################################################
#
# Task:			 start operation for selected configurations 
#	
# Requirements:
#
#############################################################################################


operateGlobally()
{

	
	for (( ndx=0; ndx<${#cConfigurations[@]}; ndx++ ))
	do

		if [ "$ndx" == "$selectedConfiguration" ] || [ "$selectedConfiguration" == "a" ]; then
			
			operate

		fi

	done

}


#############################################################################################
