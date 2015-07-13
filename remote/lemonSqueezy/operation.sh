#!/bin/sh


#############################################################################################
#
# lemon squeezy operation by JOD	
#
# Task: 		compilation and shift of executable to work directory 
#				consistant with	icbc / easyPeasy to allow use of same loop
#
# Requirements:
#
#############################################################################################


cOperations=( 

	"co(m)pile" 
	"co(p)y" 
	"co(n)figuration rechoose"
	
) 
							# !!! 3RD LETTER - MIND CONSISTENCE WITH INTERFACE
							
nOperations=${#cOperations[@]}


#############################################################################################
#
# Task: 		global configuration for selected operation
#				in addition 0: abort
#							1: restart easyPeasy		
#			
# Requirements: 
#
#############################################################################################


configOperation()
{

	case $operation in
	
		"m"|"M") 
			getSetup   # IN CASE OF CHANGES
			setBuildFlag
			;;
			
		"p"|"P") 
			:
			;;
			
		"n"|"N")
			:
			;;
			
		"0")
			echo -e " NOTHING DONE \n"
			abort
			;;
			
		"1")  
			echo -e "NOTHING DONE\n"
		 	. $path2icbc/run.sh lemonSqueezy  				# RESTART 
			;;
			
		*) 
		    :
			;;
			
	esac

}


#############################################################################################
#
# Task: 		copy executable from home into work	
#
# Requirements:
#
#############################################################################################


copyExe()
{
		
	cd /home/$login$versionRoot/$cCode/$cVersion/sources
	
	if [ -d "Build_${cConfigurations[$ndx]}/bin" ]; then
			
		cd Build_${cConfigurations[$ndx]}/bin

		if [ -f $cCode ]; then
			
			echo "COPY $cCode_${cConfigurations[$ndx]}"  		# COPY FROM HOME DIR

			if [ ! -d "/$workfolder/$login$versionRoot/$cCode/$cVersion" ]; then

				mkdir /$workfolder/$login$versionRoot/$cCode/$cVersion

			fi

			cp $cCode /$workfolder/$login$versionRoot/$cCode/$cVersion/$cCode\_${cConfigurations[$ndx]}
				
		fi

		cd ..
		cd ..
		
	fi

}


#############################################################################################
#
# Task: 		build and make
#
# Requirements: lemonSqueezy configuration
#
#############################################################################################


compileExe()
{
				
	cd /home/$login$versionRoot/$cCode/$cVersion/sources
	
	echo -e	"\n_______________________________________________________________________________\n"
	echo -e	"	START COMPILATION ${cConfigurations[$ndx]}"
	echo -e	"_______________________________________________________________________________\n"				

	if [ "$ALLOW_BUILD_flag" -eq 1 ]; then   # set in run.sh / interface.sh /configOperation()

		rm -r Build_${cConfigurations[$ndx]}
		mkdir Build_${cConfigurations[$ndx]}
		cd Build_${cConfigurations[$ndx]}

		cmake .. -D${cConfigurations[$ndx]}=ON -DPARALLEL_USE_OPENMP=${compilerTable[(($ndx * 3))]} -DCMAKE_C_COMPILER=/${compilerTable[(($ndx * 3 + 1))]} -DCMAKE_CXX_COMPILER=/${compilerTable[(($ndx * 3 + 2))]}
																			#	3 COLUMNS IN COMPILERTABLE
		make -j $nCPUs
				
		cd ..
				
	else

		if [ -d "Build_${cConfigurations[$ndx]}" ]; then	
			cd Build_${cConfigurations[$ndx]}
			make -j $nCPUs

		fi
			
	fi
	
}


#########################################################################################################
#
# Task: 		start selected operation	
#
# Requirements:
#
#########################################################################################################


operate()
{

	case $operation in
	
		"m"|"M") 
			compileExe
			;;
			
		"p"|"P") 
			copyExe
			;;
			
		"n"|"N")
			SELECT_MEMBER_flag=1
			;;
			
		"0")
			;;
			
		*) 
		        echo -e " NOTHING DONE \n"
			selectOperation
			;;
			
	esac
	
	echo ""
	echo -e "OPERATION DONE"

}


#########################################################################################################
