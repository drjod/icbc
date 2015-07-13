#!/bin/sh


###################################################################################################
#
# easyPeasy operation by JOD
#		
# Task: setup of test cases
#
# Requirements: configOperation() must know the ordering - take care if modifying
#
###################################################################################################


cOperations=( 

	"display (t)ree" 	# 0
	"(b)uild folder" 	# 1
	"(i)mport from repository [or gate]"	# 2
 	"e(x)port to repository [or gate]"		# 3
	"(a)pply template" 		# 4	
	"check (p)arameter"		# 5
	"rep(l)ace content"		# 6
	"(e)dit file"			# 7
	"(d)elete file"			# 8
	"(s)tore results [also in reference folder]" 	# 9
	"(c)ompare with reference"		# 10
	"perf(o)rm partition"			# 11 
	"(u)pdate ICBC"			        # 12 
	"(r)un $cCode"					# 13
	"rechoose (m)ember" 			# 14
	
) 				# !!! 1ST LETTER CONSISTENT WITH INTERFACE

  		
nOperations=${#cOperations[@]}


###################################################################################################
#
# Task:		      
# Requirements:  
#		
###################################################################################################


operate()
{

	setPaths
	case $operation in
	
		"t"|"T") tree_display;;
		"b"|"B") folder_build;;
		"i"|"I") repository_import;;
		"x"|"X") repository_export;;
		"a"|"A") template_apply;;
		"p"|"P") parameter_check;;
		"l"|"L") content_replace;;
		"e"|"E") file_edit;;
		"d"|"D") file_delete;;
		"s"|"S") results_store;;
		"c"|"C") reference_compare;;
		"o"|"O") partition_perform;;
		"u"|"U") icbc_update;;
		"r"|"R") code_run;;  
		"m"|"M"|"0"|"1") ;;  
		*) ;;
		                            # 1ST LETTER- MIND CONSISTENCE WITH INTERFACE
	esac
	
	echo ""
	echo -e "OPERATION DONE"

}


###################################################################################################
#
# Task:	  	global configuration for selected operation	  
#			in addition 0: abort
#						1: restart easyPeasy
#
# Requirements: matching cOperations NUMBERING
#		
###################################################################################################


configOperation()
{

	case $operation in			#	TAKE CARE OF cOperations NUMBERING !!!!!

		"t"|"T")
			echo -e "${cOperations[0]}\n"          # tree_display
							;;


		"b"|"B") 
			echo -e "${cOperations[1]}\n"			# folder_build
			
			easyPeasy_MODIFIED_STREAM_flag=0
			
							;;

		"i"|"I") 
			echo -e "${cOperations[2]}\n"			# import - !!!! PATH TO GATE FOR CAPITAL LETTER (IN setPath())
			echo -e "\nSELECT file ending (pbs, tim, lay, etc., or (a)ll, (n)ame)\n"
			read ending	
			if [ "$ending" == "n" ]; then

				echo -e "\nType name:\n"
				read transferfilename

			fi		
			
			easyPeasy_MODIFIED_STREAM_flag=0
			
			if [ "$operation" == "I" ]; then   # IMPORT FROM GATE FOLDER

				path2repository="home/$login$inputRoot/gate"
				
				easyPeasy_MODIFIED_STREAM_flag=1
				
				# DOS2UNIX
				
				if [ "$ending" == "bin" ]; then

					dos2unix /$path2repository/$filename\_partitioned_msh_cfg${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2member
					dos2unix /$path2repository/$filename\_partitioned_msh_ele${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2member
					dos2unix /$path2repository/$filename\_partitioned_msh_ele_g${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2member
					dos2unix /$path2repository/$filename\_partitioned_msh_nod${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2member        

				elif [ "$ending" == "pbs" ]; then

					dos2unix /$path2repository/$batch
	
				elif [ "$ending" == "lay" ]; then

					dos2unix /$path2repository/*lay
	
				elif [ "$ending" == "n" ]; then # NAME GIVEN

					dos2unix /$path2repository/$transferfilename
	
				elif [ "$ending" == "a" ]; then # ALL

					dos2unix /$path2repository/*
	
				else   # ENDING GIVEN

					dos2unix /$path2repository/${filename}.$ending
	
				fi
		
			else             # IMPORT FROM REPOSITORY

				path2repository="home/$login$inputRoot/repository/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}/${cLevel2[${ndx[2]}]}"

			fi
	
							;;

		"x"|"X") 
			echo -e "${cOperations[3]}\n"			# repository_export - !!!! PATH TO GATE FOR CAPITAL LETTER (IN setPath())
			echo -e "\nSELECT file ending (pbs, tim, lay, etc., or (a)ll, (n)ame)\n"
			read ending	
			if [ "$ending" == "n" ]; then

				echo -e "\nType name:\n"
				read transferfilename

			fi
			
			easyPeasy_MODIFIED_STREAM_flag=0
			
			if [ "$operation" == "X" ]; then   # EXPORT TO GATE FOLDER

				path2repository="home/$login$inputRoot/gate"
				easyPeasy_MODIFIED_STREAM_flag=1

			fi
			

							;;

		"a"|"A") 
			echo -e "${cOperations[4]}\n"			# template_apply
			echo -e "\nSELECT file ending (pbs, mmp, num, etc.)\n"
			read ending 

			cd /$path2icbc/configuration		# USE CD TO GET ALSO TEMPLATES - !!!! ALSO IN easyPeasy global.sh
			. ./input.sh						# REPEATED IN CASE TEMPLATE UPDATE
							;;

					"p"|"P") echo -e "${cOperations[5]}\n"			# parameter_check
			echo -e "\nSELECT file ending (mmp, mfp, msp, etc.)\n"
				read ending 
			echo -e "\nWhich parameter?\n"
			read parameter
			echo ""
							;;
			
		"l"|"L") 
			echo -e "${cOperations[6]}\n"			# content_replace
			echo -e "\nSELECT file ending (mmp, pbs, lay, tec, etc., or (a)ll)\n"
				read ending 
			echo -e "\nText to replace:\n"
				read oldText
			echo ""
			echo -e "\nNew text:\n"
				read newText
			echo ""
							;;

		"e"|"E") 
			echo -e "${cOperations[7]}\n"			# file_edit
			echo -e "\nSELECT file ending (mmp, mfp, msp, etc.)\n"
				read ending		
							;;

		"d"|"D") 
			echo -e "${cOperations[8]}\n"			# file_delete
			echo -e "\nSELECT file ending (pbs, txt, tec, lay, bin, bak, asc, tim etc., or (a)ll, (n)ame)\n"
			read ending	
			if [ "$ending" == "n" ]; then

				echo -e "\nType name:\n"
				read transferfilename

			fi
							;;
		
		"s"|"S") 
			echo -e "${cOperations[9]}\n"			# results_store
			
					
			if [ "$operation" == "s" ] ; then 
			
				easyPeasy_UPDATE_REFERENCE_flag=1
			
			else
				
				easyPeasy_UPDATE_REFERENCE_flag=0
			
			fi
			
			
			if [ -f "$path2totalResults/timeOutput.txt" ]; then  # DELETE OLD TIME OUTPUT

				rm /$path2totalResults/timeOutput.txt
	
			fi
							;;

		"c"|"C") 
			echo -e "${cOperations[10]}\n"			# reference_compare				
							
			easyPeasy_MODIFIED_STREAM_flag=0
							
							;;				
							
		"o"|"O")
			echo -e "${cOperations[11]}\n"			# partition_perform
			
							;;
							
		"u"|"U")
			echo -e "${cOperations[12]}\n"			# icbc_update
			if [ "$operation" == "U" ] ; then 
			
				easyPeasy_UPDATE_FROM_SAME_FOLDER_flag=1
			
			else
				
				easyPeasy_UPDATE_FROM_SAME_FOLDER_flag=0
			
			fi
							;;					
	
		"r"|"R") 
			echo -e "${cOperations[13]}\n"			# code_run
							;;	
		
		"m"|"M")  
			echo -e "${cOperations[14]}\n"			# member_rechoose

			SELECT_MEMBER_flag=1 	
			loop
							;; 
		
		"0")  										# ABORT
			echo -e "NOTHING DONE\n"
		 	abort
							;; 
							
		"1")  
			echo -e "NOTHING DONE\n"
		 	. $path2icbc/run.sh easyPeasy  			# RESTART 
							;; 
          
         *)  
			echo -e "ERROR - OPERATION $operation NOT PROVIDED - NOTHING DONE" 
			loop
							;;
 		
	esac

}


###################################################################################################
#
# Task:         set path to (base) member, storage, 
#               repository folder if not easyPeasy_MODIFIED_STREAM_flag is not set
#				select GATE folder
#
# Requirements: 3 level
#
###################################################################################################


setPaths()
{


	path2base="$workfolder/$login$versionRoot/$cCode/$cVersion$inputRoot" #"/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}/${cLevel2[0]}"
	path2member="$workfolder/$login$versionRoot/$cCode/$cVersion$inputRoot/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}/${cLevel2[${ndx[2]}]}"
    	
	indices="${ndx[0]}_${ndx[1]}_${ndx[2]}"   		 # USED IN PBS TEMPLATE
	member="${cLevel0[${gndx[0]}]}_${cLevel1[${gndx[1]}]}_${cLevel2[${ndx[2]}]}"

	path2results="home/$login$inputRoot/results/$cCode/$cVersion/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}/${cLevel2[${ndx[2]}]}"
	path2totalResults="home/$login$inputRoot/results/$cCode/$cVersion"
	
	if [ "$easyPeasy_MODIFIED_STREAM_flag" == "0" ]; then    # TAKE path2repository WITH CARE ( modify this flag in configOperation() accordingly)
	
		path2repositoryBase="home/$login$inputRoot/repository/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}/${cLevel2[0]}"
		path2repository="home/$login$inputRoot/repository/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}/${cLevel2[${ndx[2]}]}"

	fi
	
}  


###################################################################################################
#
# Task:		 	display members, e.g. for debugging
#     
# Requirements:  
#		
###################################################################################################


tree_display() 
{

	echo ""
	echo -n "   Local indices "
	
	for ((i=0; i<$((nLevels)); i++))
	do
		echo -n "${ndx[$i]} "

        done

	echo -n "Global indices "

	for ((i=0; i<$((nLevels)); i++))
	do
		echo -n "${gndx[$i]} "

        done

	echo ""


}


###################################################################################################
#
# Task:		generate home repository / work input and output / home result storage	by using mkdir command
#	      
# Requirements:  3 level
#						
###################################################################################################


folder_build()
{
 
 	
	### FOR REPOSITORY

	if [[ ! -d "/home/$login$inputRoot/repository/${cLevel0[${gndx[0]}]}" ]]; then

		mkdir /home/$login$inputRoot/repository/${cLevel0[${gndx[0]}]}
	fi

	
	if [[ ! -d "/home/$login$inputRoot/repository/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}" ]]; then

		mkdir /home/$login$inputRoot/repository/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}

	fi
	
	if [[ ! -d "/$path2repository" ]]; then

		mkdir /$path2repository
		  
	else

		echo "   Repository folder existed already"
		  
	fi

	
	### FOR INPUT FILES

	if [[ ! -d "/$workfolder/$login$versionRoot/$cCode/$cVersion$inputRoot" ]]; then

		mkdir /$workfolder/$login$versionRoot/$cCode/$cVersion$inputRoot
	fi


	if [[ ! -d "/$workfolder/$login$versionRoot/$cCode/$cVersion$inputRoot/${cLevel0[${gndx[0]}]}" ]]; then

		mkdir /$workfolder/$login$versionRoot/$cCode/$cVersion$inputRoot/${cLevel0[${gndx[0]}]}
	fi

	
	if [[ ! -d "/$workfolder/$login$versionRoot/$cCode/$cVersion$inputRoot/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}" ]]; then

		mkdir /$workfolder/$login$versionRoot/$cCode/$cVersion$inputRoot/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}

	fi
	
	if [[ ! -d "/$path2member" ]]; then

		mkdir /$path2member
		                                                        
	else

		echo "   Input folder existed already"

	fi			
	
		
	##### FOR RESULTS STORAGE 


	if [[ ! -d "/home/$login$inputRoot/results/$cCode" ]]; then

		mkdir /home/$login$inputRoot/results/$cCode
		
	fi


	if [[ ! -d "/home/$login$inputRoot/results/$cCode/$cVersion" ]]; then

		mkdir /home/$login$inputRoot/results/$cCode/$cVersion
		
	fi


	if [[ ! -d "/home/$login$inputRoot/results/$cCode/$cVersion/${cLevel0[${gndx[0]}]}" ]]; then

		mkdir /home/$login$inputRoot/results/$cCode/$cVersion/${cLevel0[${gndx[0]}]}
		
	fi

	if [[ ! -d "/home/$login$inputRoot/results/$cCode/$cVersion/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}" ]]; then

		mkdir /home/$login$inputRoot/results/$cCode/$cVersion/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}
		
	fi

	if [[ ! -d "/home/$login$inputRoot/results/$cCode/$cVersion/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}/${cLevel2[${ndx[2]}]}" ]]; then

		mkdir /home/$login$inputRoot/results/$cCode/$cVersion/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}/${cLevel2[${ndx[2]}]}
		
	else

		echo "   Storage folder existed already"
	
	fi

}


###################################################################################################
#
# Task:		     generate input files
# 
# Requirements:  specification in test case 
#				 configuration.sh for parameter in combination with
#				 template_pbs.sh for batch files 
# 			 	 template.sh for files in general - call Template_$ending()
#		
###################################################################################################


template_apply() 
{

	
	if [ "$ending" == "pbs" ]; then

		if [ "${numberCPUs[$(($((${ndx[0]} * $nLevel2 ))  + ${ndx[2]}))]}" -gt 1 ]; then   # PARALLEL 

			echo "			parallel"
			Spread_batch_parallel

		else

			echo "			sequential"
			Spread_batch_sequential

		fi
			
	else

		Template_$ending

	fi
	
} 


###################################################################################################
#
# Task:		 	copy input files from repository
#				copy them from GATE folder (instead repository) if operation capital i [I] (see setPath())
#     
# Requirements:  $path2repository
#		
###################################################################################################


repository_import() 
{
	
	if [ "$ending" == "bin" ]; then

		cp /$path2repository/$filename\_partitioned_msh_cfg${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2member
		cp /$path2repository/$filename\_partitioned_msh_ele${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2member
		cp /$path2repository/$filename\_partitioned_msh_ele_g${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2member
		cp /$path2repository/$filename\_partitioned_msh_nod${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2member        


	elif [ "$ending" == "pbs" ]; then

		cp /$path2repository/$batch /$path2member

	elif [ "$ending" == "lay" ]; then

		cp /$path2repository/*lay /$path2member

	elif [ "$ending" == "n" ]; then # NAME GIVEN
		
		cp /$path2repository/$transferfilename /$path2member

	elif [ "$ending" == "a" ]; then # ALL

		cp /$path2repository/* /$path2member

	else   # ENDING GIVEN
		
	    cp /$path2repository/${filename}.$ending /$path2member  #/${filename}.$ending	
	
	fi

} 


###################################################################################################
#	
# Task:		 	copies input files into repository
#				copies them into GATE folder (instead repository) if operation capital i [I] (see setPath())
#     
# Requirements:  $path2repository
#		
###################################################################################################


repository_export() 
{	
					
	if [ "$ending" == "bin" ]; then

		cp /$path2member/$filename\_partitioned_msh_cfg${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2repository
		cp /$path2member/$filename\_partitioned_msh_ele${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2repository
		cp /$path2member/$filename\_partitioned_msh_ele_g${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2repository
		cp /$path2member/$filename\_partitioned_msh_nod${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  /$path2repository       


	elif [ "$ending" == "pbs" ]; then

		cp /$path2member/$batch /$path2repository

	elif [ "$ending" == "lay" ]; then

		cp /$path2member/*lay /$path2repository

	elif [ "$ending" == "n" ]; then	# NAME GIVEN

		cp /$path2member/$transferfilename /$path2repository


	elif [ "$ending" == "a" ]; then #  ALL

		if [ -f $path2repository/* ]; then

			rm /$path2repository/*   	# CLEAR REPOSITORY
			echo "	Repository cleared"
			
		fi
	
		cp /$path2member/* /$path2repository
		cp /$path2member/* /$path2repository

	else
	
	    cp /$path2member/${filename}.$ending /$path2repository 

	fi

} 


###################################################################################################
#  
# Task: 			display line following keyword (e.g. $PERMEABILITY) by using sed command
# 
# Requirements:  
#		
###################################################################################################


parameter_check() 
{
		
	sed -n '/'$parameter'/{n;p;}' /$path2member/${filename}.$ending	

} 


###################################################################################################
#
# Task:				 replacement in input file by using sed command
#      				 e.g. nans can be deleted from output files
# 
# Requirements:  
#		
###################################################################################################


content_replace() 
{

	if [ "$ending" == "pbs" ]; then

		sed -i.bak s/"$oldText"/"$newText"/g /$path2member/$batch

	elif [ "$ending" == "lay" ]; then

		sed -i.bak s/"$oldText"/"$newText"/g /$path2member/*lay
		
	elif [ "$ending" == "tec" ]; then

		sed -i.bak s/"$oldText"/"$newText"/g /$path2member/*tec
		
	elif [ "$ending" == "a" ]; then

		sed -i.bak s/"$oldText"/"$newText"/g /$path2member/*

	else	

		sed -i.bak s/"$oldText"/"$newText"/g /$path2member/${filename}.$ending	

	fi		
	
} 


###################################################################################################
# 
# Task: 			call emacs
#     
# Requirements: supports only input files and batch 
#		
###################################################################################################


file_edit() 
{
	
	if [ "$ending" == "pbs" ]; then

		emacs /$path2member/$batch

	else		

		emacs /$path2member/${filename}.$ending 

	fi
	
} 


###################################################################################################
#
# Task:			Delete whatever file
#	      
# Requirements:  3 level for bin
#		
###################################################################################################


file_delete() 
{
	
	if [ "$ending" == "bin" ]; then

	    rm /$path2member/*bin 
		#rm /$path2member/$filename\_partitioned_msh_cfg${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin 
		#rm /$path2member/$filename\_partitioned_msh_ele${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  
		#rm /$path2member/$filename\_partitioned_msh_ele_g${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin  
		#rm /$path2member/$filename\_partitioned_msh_nod${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}.bin      

	elif [ "$ending" == "asc" ]; then

		rm /$path2member/*asc
		
	elif [ "$ending" == "pbs" ]; then

		rm /$path2member/$batch 
		
	elif [ "$ending" == "bak" ]; then

		rm /$path2member/*bak 

	elif [ "$ending" == "lay" ] || [ "$ending" == "tec" ] || [ "$ending" == "txt" ]; then

		rm /$path2member/*$ending 

		if [ -f $path2repository/*$ending ]; then

			echo "	delete $ending in repository, too"
			rm /$path2repository/*$ending

		fi

	elif [ "$ending" == "n" ]; then 	# COMPLETE NAME GIVEN

		if [ -f /$path2member/$transferfilename  ]; then

			rm /$path2member/$transferfilename 

		elif [ -f /$path2member/$transferfilename  ]; then

			rm /$path2member/$transferfilename 

		else

			echo "	NOTHING DELETED - File $transferfilename not found"

		fi

	elif [ "$ending" == "a" ]; then  # DELETE ALL
		
		rm /$path2member/*

	else

	        rm /$path2member/${filename}.$ending 
	
	fi

} 


###################################################################################################
#
# Task:				store results in homefolder (for synchronization - download)
#					store results in home reference folder if easyPeasy_UPDATE_REFERENCE_flag is set
#					write lines with 4GREP, Time step, Process, PCS error:, Convergence, iteration: in file convergence     
#
# Requirements:  	path to results via setPath in member configuration
#		
###################################################################################################


results_store() 
{

	# COMPARE
	
	if [ "$easyPeasy_UPDATE_REFERENCE_flag" -eq "1" ]; then    # specified in test case configuration.sh

		if [[ ! -d "/$path2repository/reference" ]]; then

			mkdir /$path2repository/reference
			
		fi
		
		cp /$path2member/*tec /$path2repository/reference
		
	fi
		

	cd /$path2member

	
	# PACK AND SEND
	
	if [ -f /$path2member/results.gz ]; then	
	
		rm /$path2member/results.gz
	
	fi
	
	#####
	
	#PACK_flag=0

	#shopt -s nullglob   # CAUSES ISSUE IN SELECT MEMBER
	#shopt -s dotglob
	
	#for pack_ending in tec lay txt
	#do
	
	#	files=(/$path2member/*$pack_ending)
	
	#	if [ ${#files[@]} -gt 0 ]; then

	#		if [ $PACK_flag -eq 0 ]; then

	#			PACK_flag=1
	#			tar cfv results *$pack_ending			
			
	#		else   # results.gz EXISTS ALREADY
		
	#			tar Afv results *$pack_ending
			
	#		fi

	#	fi

	#done
   	
	#for file in `find -name '*.tec'`; do            # replace nan in all *.tec files of all subdfolders

  #grep "$search" $file &> /dev/null
  #if [ $? -eq 0 ]; then
  #  sed -i "s/$search/$substitute/" $file

 # fi  
#done

	tar cfv results *tec *lay *txt	
	
	
	#if [ $PACK_flag -eq 1 ]; then
	
		gzip /$path2member/results
		mv results.gz /$path2results
	
	#else
	
	#	echo "NOTHING TO PACK"
		
	#fi
	
	#####
	
	if [ -f screenout.txt ]; then

		grep 'GREP\|Time step\|Process\|PCS error\|Convergence\|iteration:' screenout.txt > /$path2totalResults/convergence_$member\.txt

		echo -n "$member " >> timeOutput.txt  
		grep "$timeOutput" /$path2member/screenout.txt >> timeOutput.txt 

	fi

} 


###################################################################################################
#
# TASK: compare results with results in (home) reference folder by using diff command
#       write comparison result into diff.txt and copy to home results 
#				
# REQUIREMENTS: 
#						
#
###################################################################################################


reference_compare ()
{


	if [[ -d "/$path2repository/reference" ]]; then
	
	
		if [ -f $path2member/diff.txt ]; then
		
			rm /$path2member/diff.txt		
	
		fi	
	
		for i in $path2repository/reference
		do

			diff -u $i $path2member${i#*reference} >> /$path2member/diff.txt

		done
		
		if [ -f $path2results/diff.txt ]; then

			rm /$path2results/diff.txt
		
		fi


		if [[ -s $path2member/diff.txt ]]; then

			cp /$path2member/diff.txt /$path2results/diff.txt
	
		fi
		
		
	else

		echo "	NOTHING DONE - No reference files found"
	
	fi	


}

###################################################################################################
#
# TASK: mesh partitioning
#		generates asci if partitioning by elements and binary if by nodes
#		does nothing if partitioned mesh already exists - so delete old stuff first with operation d		
#
# REQUIREMENTS: NumberCPUs and partitioning [n,e] in test case configuration
#				test.msh in member folder
#				calls partmesh (METIS) via partition.sh
#		
#
###################################################################################################


partition_perform() 
{


	if [ "${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}" -gt 1 ]; then   # PARALLEL 

		if [ ! -f /$path2member/$filename\_partitioned_msh_cfg${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}\.bin ] && [ ! -f $path2member/${filename}.ddc ]; then 
			
			# PARTITIONING NEEDED					
			
			if [ ! -f /$path2member/${filename}.msh ]; then

				echo -e "\n		ERROR - No ${filename}.msh in base folder ${cLevel2[${ndx[2]}]}\n - NOTHING DONE"

			else

				if [ "${partitioning[${ndx[2]}]}" == "n" ]; then  # PARTITION BY NODES 															

					. $path2icbc/easyPeasy/partition.sh ${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]} -n -binary /$path2member	
												 
				elif [ "${partitioning[${ndx[2]}]}" == "e" ]; then  # PARTITION BY ELEMENTS	
				
					. $path2icbc/easyPeasy/partition.sh ${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]} -e -asci /$path2member	
													
				else
				
					echo -e "\n		ERROR - partitioning must be n or e - NOTHING DONE"
					
				fi
				
			fi          
			
		else

			echo -e "\n 	WARNING - *.bin or *.ddc already here - NOTHING DONE"

		fi
		

	fi

	
}

###################################################################################################
#
# TASK: Update of initial (and boundary conditions)
#		U : take IC/BCs from same folder
#		u : take IC/BCs from folder with identification local index - 1 in level2 (i.e. ${ndx[2]} - 1}) 	 
#
# REQUIREMENTS: 
#		match specifications *.ic, *.out	
#				
#		
#
###################################################################################################

icbc_update() 
{

  	if [ "$easyPeasy_UPDATE_FROM_SAME_FOLDER_flag" -eq 1 ]; then
	
		path2ICBCSource="$path2member"
		
	else # easyPeasy_UPDATE_FROM_SAME_FOLDER_flag = 0
	
		#if [ "$distributionLevelForICBCs" -eq 1 ]; then
			path2ICBCSource="$path2base/${cLevel0[${gndx[0]}]}/${cLevel1[$((${gndx[1]} - 2))]}/${cLevel2[${ndx[2]}]}"
		#elif [ "$distributionLevelForICBCs" -eq 2 ]; then
		#	path2ICBCSource="$path2base/${cLevel0[${gndx[0]}]}/${cLevel1[${gndx[1]}]}/${cLevel2[$((${ndx[2]} - 1))]}"
		#else
		#	echo -e "\n 	ERROR - selected distribution level not supported in icbc update"
		#fi	
	
	fi
	
	for ((process=0; process<nProcesses; process++))
	do
		if [ "${partitioning[${ndx[2]}]}" == "n" ]; then #[ "${numberCPUs[$(($((${ndx[0]} * $nLevel2 ))  + ${ndx[2]}))]}" -gt 1 ]; then # PARALLEL PARTITIONING BY NODES
			for ((core=0; core<${numberCPUs[$(($((${ndx[0]} * $nLevel2 )) + ${ndx[2]}))]}; core++))
			do
			    
				cp /$path2ICBCSource/$filename\_${processes[$process]}\_domain_primary_variables_$core\.txt   /$path2member/$filename\_${processes[$process]}\_IC_$core\.txt	
                
				
				#if [ "$BC_flag" -eq 1 ]; then   # COPY BC

				#	cp /$path2lastLevel/${cLevel2[${${ndx[2]} - 1}]}/$filename\_${processes[$process]}\_LEFT_primary_variables_$core\.txt /$path2member/${processes[$process]}\_LEFT_BC_$core\.txt

				
			done	

		else                          # SEQUENTIAL${${ndx[2]} - 1}
	       	cp /$path2ICBCSource/$filename\_${processes[$process]}\_domain_primary_variables.txt  /$path2member/$filename\_${processes[$process]}\_IC.txt

				#if [ "$BC_flag" -eq 1 ]; then    # COPY BC

				#	cp /$path2lastLevel/${cLevel2[${${ndx[2]} - 1}]}/$filename\_${processes[$process]}\_LEFT_primary_variables\.txt /$path2member/${processes[$process]}\_LEFT_BC\.txt

				#fi	
		fi
	done
  
}  
###################################################################################################
#
# Task:         Submit job
#
# Requirements:  
#
###################################################################################################


code_run()
{

    qsub /$path2member/$batch #  >> $path2member/run.txt
           
} 


###################################################################################################
