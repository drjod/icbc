#!/bin/bash


#########################################################################################################
#
# easyPeasy global by JOD
#
# Task: 		easyPeasy kernel 
#				handle access to input files
#				currently 3 level connected by tree and fence in this order
#
# Requirements: 
#
#########################################################################################################


. $path2icbc/easyPeasy/operation.sh


###################################################################################################
#
# Task:          get input configuration  
#        
# Requirements: 
#
###################################################################################################


getSetup()
{

	cd /$path2icbc/configuration	# USE CD TO GET ALSO TEMPLATES - !!!!! ALSO IN configOperation() CASE a
	. ./input.sh				
           
	nLevels=3
	nLevel0=${#cLevel0[@]}
	nLevel2=${#cLevel2[@]}
	nProcesses=${#processes[@]}

}


###################################################################################################
#
# Task:          input;sets up table / tree structure   
#        
# Requirements: 
#
###################################################################################################


configSelect()
{

	case $flac in

		"lvl0")

      		nMembers=$nLevel0   					
			;;

		"lvl1")

 			if [ "${sndx[0]}" == "a" ]; then

				sndx[1]=a		# TAKE ALSO ALL
				nMembers=0

			else

      			nMembers=${nLevel1[${sndx[0]}]}		# TREE

			fi			
			;;

		"lvl2")

      		nMembers=$nLevel2
			;;

		*) 	

			echo -e "\n\n   ERROR - Only 3 level supported\n\n"
			exit
			;;

	esac

}



###################################################################################################
#
# Task:          input         
# 
# Requirements: 
#
###################################################################################################


selectMember()
{ 
	
	echo ""
	echo -e "\n_______________________________________________________________________________\n"
	echo ""

	sndx[0]=0
    inverted[0]=0	
	nMembers=$nLevel0
	selected="a"
	for ((i=0; i<$((nLevels)); i++))
	do
		inverted[$i]=0
		flac="lvl$i"
		configSelect
		
		if [ "$nMembers" -gt 1 ]; then

			echo -e "SELECT ${cLevels[$i]}\n"

			for ((j=0; j<nMembers; j++))
			do

				#index=$((gndx[1] * $nLevel2))
				#index=$((ndx[2] + $index))

				#if [ "${status[$index]}" -eq "1" ]; then

					echo -e "\t $j: \c"
					glIndex=$j
					ndx[0]=${sndx[0]}		
					echoMember

				#fi

			done
		
			echo -e "\t a: All\n"

			
			if [ "$nMembers" -gt 10 ]; then   # DOUBLE DIGIT			
				read sndx[$i]
			else
				read -n1 sndx[$i]
			fi	
	
		elif [ "$nMembers" -eq 1 ]; then

			sndx[$i]=0

		fi

		##### SHELL OUTPUT

		if [ "${sndx[$i]}" == "a" ]; then

			echo -e "\n\n\t\tSelected all ${cLevels[$i]}\n"

		elif [ "${sndx[$i]}" -ge 0 ] && [ "${sndx[$i]}" -lt "$nMembers" ]; then 
			if [ "${inverted[$i]}" -eq 0 ]; then
				echo -e "\n\n\t\tSelected ${cLevels[$i]} \c" 
			else
				echo -e "\n\n\t\tSelected not ${cLevels[$i]} \c"			
			fi
			glIndex=${sndx[$i]}
			ndx[0]=${sndx[0]}		
			echoMember
			echo ""
		else

			echo -e "\n\n   ERROR - ${cLevels[$i]} ${sndx[$i]} does not exist\n\n"
			start
	
		fi
	
	done

}


###################################################################################################
#
# Task:         to get global ndx in tree
#
# Requirements: gndx (=level 0 (global) ndx), flac 
#
###################################################################################################


globalndx()
{

	case $flac in

		"lvl0")
			:                            				
			;;
		"lvl1")        # TREE STRUCTURE
			for ((ii=0; ii<ndx[0]; ii++))     
			do
				glIndex=$((glIndex + ${nLevel1[ii]}))
			done	
			;;
		"lvl2")     
                        :       # FENCE (SAME NUMBER OF MEMBERS IN BRANCH)
			#for ((ii=0; ii<ndx[0]; ii++))     
			#do														
			#	glIndex=$((glIndex + ${nLevel2})) 		
			#done	
			;; 
		*) 	
			echo -e "\n\n   ERROR - Only 3 level supported\n\n"
			exit
			;;
				
	esac
	
}


###################################################################################################
#
# Task:          shell output of level member names 
#      
# Requirements:  see globalndx()
#
###################################################################################################


echoMember()
{

	globalndx       # SHIFT ndx	


	case $flac in

		"lvl0")
      			echo -e "${cLevel0[glIndex]}"
			;;

		"lvl1")
      			echo -e "${cLevel1[glIndex]}"
			;;

		"lvl2")
      			echo -e "${cLevel2[glIndex]}"
			;;
		*) 	
			echo -e "\n\n   ERROR - Only 3 level supported\n\n"
			exit
			;;
				
				
	esac

}


###################################################################################################
#
# Task:          option to echoInstance()   
#    
# Requirements:  see globalndx()
#
###################################################################################################


echoMember2()
{

	globalndx       # SHIFT ndx	

	case $flac in

		"lvl0")
				echo -e "\t${cLevel0[glIndex]}"
			;;

		"lvl1")
      			echo -e "\t\t${cLevel1[glIndex]}"
			;;

		"lvl2")
      			#echo -e "${cLevel2[glIndex]}"
			;;
		*) 	
			echo -e "\n\n   ERROR - Only 3 level supported\n\n"
			exit
			;;
				
	esac

}


###################################################################################################
#
# Task:		    sets tree / fence structure
#   
# Requirements:  
#		
###################################################################################################


GetBranches()
{

	case $flac in

		"lvl0")
      			nLevel=$nLevel0
			;;

		"lvl1")
    			nLevel=${nLevel1[${gndx[0]}]}    # TREE	
			;;

		"lvl2")
      			nLevel=$nLevel2                   # FENCE			
			;;

		*) 	
			echo -e "\n\n   ERROR - Only 3 level supported"
			exit
			;;	
			
	esac

}


###################################################################################################
#
# Task:		          get selected member and call operation
#
# Requirements:  
#		
###################################################################################################


operateGlobally()
{

	for ((ndx[0]=0; ndx[0]<nLevel0; ndx[0]++))    
	do

		if [ "${sndx[0]}" == "a" ] || [ "${ndx[0]}" == "${sndx[0]}" ]; then
		
			flac="lvl0"
			glIndex=${ndx[0]}	        
			globalndx	
	 		echo -e "\t${cLevel0[$glIndex]}" 
			gndx[0]=$glIndex	# !!! IMPORTANT FOR NEXT LOOP

		

			for ((ndx[1]=0; ndx[1]<nLevel1[gndx[0]]; ndx[1]++)) 
			do		
	
				if [ "${sndx[1]}" == "a" ] || [ "${ndx[1]}" == "${sndx[1]}" ]; then

					flac="lvl1"
					glIndex=${ndx[1]}	        
					globalndx 
					echo -e "\t\t${cLevel1[$glIndex]}" 
					gndx[1]=$glIndex	

					for ((ndx[2]=0; ndx[2]<nLevel2; ndx[2]++))   
					do                                             

						if [ "${sndx[2]}" == "a" ] || [ "${ndx[2]}" == "${sndx[2]}" ]; then

							flac="lvl2"
							glIndex=${ndx[2]}	        
							globalndx 
							gndx[2]=$glIndex	

							index=$((gndx[1] * $nLevel2))
							index=$((ndx[2] + $index))
							
							if [ "${status[$index]}" -eq "1" ]; then

								echo -e "\t\t\t$cOperation ${cLevel2[${ndx[2]}]}"
								    
								operate
				
							fi
						fi							
					
					done			
				fi
			done			 
		fi
	
	done

}


###################################################################################################
