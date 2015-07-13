#!/bin/sh

#########################################################################################
#
# configuration input by JOD
#
# Task: configuration for easyPeasy
#		OpenGeoSys test cases 
#
# Requirements: login variable is set
#
#########################################################################################


. ./templates.sh


COMPARISON_flag=0

filename="test"
##### MEMBER NAMES 

cLevels=( 
			"Case" "Type" "Configuration" 
)


cLevel0=( 
	"BC_ST_TEST" 
	"1D_analyt"
	"ogataBanks"
	"2D_analyt"
	"2D_analyt_LIQUID_FLOW"
	"connectedNodes"
	"2D_plume"
	"elder"
	"elderPTC"
	"ImmobileGas" 
	"2D_radial"
	"boxes"
	"2d_Modell_grid10mRefined"
	"2d_Modell_grid10m"
	"2d_Modell_grid10mRefinedLowContrast"
	"2d_Modell_grid10mLowContrast"
	"2d_Modell_grid10mRefined_PTC"
	"2d_Modell_grid10m_PTC"
	"saltRise"
	"3D_iglu"
 )


cLevel1=( 
	"0_1_1" "0_1_2" "0_2_1" "0_2_2" "1_1_1" "1_1_2" "1_2_1" "2_1_1" "2_1_2" "2_2_1" "2_2_2"		# BC_ST_TEST
	"line" "quad" "tri" "pri" "tet"															 	# 1D_analyt
	"thermal" "solute"                                                                          # ogataBanks
	"quad" "tri" 																				# 2D_analyt
	"quad" "tri" 																				# 2D_analyt_LIQUID_FLOW
	"case0" "case1" "case2"                                                                     # connectedNodes
	"thermal" "solute"                                                                          # 2D_plume
	"haline" "thermal" "thermohaline"															# elder
	"haline" "thermohaline"																		# elderPTC
	"2D_35m_50m_withoutDiss_Refined"															# ImmobileGas
	"BestFit" 																					# 2D_radial
	"2D_xy_advection_quad" "2D_xy_advection_tri" "2D_xy_diffusion_quad" "2D_xy_diffusion_tri"	# boxes
	"2D_xz_advection_quad" "2D_xz_advection_tri" "2D_xz_diffusion_quad" "2D_xz_diffusion_tri"	#   "
	"3D_advection_hex" "3D_diffusion_hex"                                                       #   "
    "T"	"TH" "THC" "Injection"                                                                  # 2d_Modell_grid10mRefined
	"T"	"TH" "THC" "Injection"                                                                  # 2d_Modell_grid10m
	"T"	"TH" "THC" "Injection"                                                                  # 2d_Modell_grid10mRefinedLowContrast
	"T"	"TH" "THC" "Injection"                                                                  # 2d_Modell_grid10mLowContrast
	"T"	"TH" "THC" "Injection"                                                                  # 2d_Modell_grid10mRefinedPTC
	"T"	"TH" "THC" "Injection"                                                                  # 2d_Modell_grid10mPTC
	"T"	"TH" "THC" "Injection"                                                                  # saltRise
	"3D_5d_stagnation"                                                                          # 3D iglu
 )

 
cLevel2=( "OGS_FEM" "OGS_FEM_SP" "OGS_FEM_MKL" "OGS_FEM_MPI" "OGS_FEM_PETSC" )



##### BRANCHING

        
nLevel1=(      # TREE	 
		"11" # BC_ST_TEST
		"5"  # 1D_analyt
		"2"  # ogataBanks
		"2"  # 2D_analyt
		"2"  # 2D_analyt_LIQUID_FLOW
		"3"  # connectedNodes
		"2"  # 2D_plume
		"3"  # elder
		"2"  # elderPTC
		"1"  # ImmobileGas
		"1"  # 2D_radial
		"10"  # boxes
		"4"  # 2d_Modell_grid10mRefined
		"4"  # 2d_Modell_grid10m
		"4"  # 2d_Modell_grid10mRefinedLowContrast
		"4"  # 2d_Modell_grid10mLowContrast
		"4"  # 2d_Modell_grid10mRefinedPTC
		"4"  # 2d_Modell_grid10mPTC
		"4"  # saltRise
		"1"  # 3D_iglu
 )       


#####


##### ICBC UPDATE


processes=(
"LIQUID_FLOW"
"HEAT_TRANSPORT"
"MASS_TRANSPORT"
)

##### PARTITIONING

partitioning=( "0" "0" "0" "e" "n" )		# e: BY ELEMENTS (GENERATES ASCI) - n: BY NODES (GENERATES BINARY)

#  OGS_FEM OGS_FEM_SP OGS_FEM_MKL OGS_FEM_MPI OGS_FEM_PETSC
numberCPUs=( 
        "1" "1" "1" "2" "2"  # BC_ST_TEST
		"1" "1" "1" "2" "2"  # 1D_analyt
		"1" "1" "1" "2" "2"  # ogataBanks
		"1" "1" "1" "2" "2"  # 2D_analyt
		"1" "1" "1" "2" "2"  # 2D_analyt_LIQUID_FLOW
		"1" "1" "1" "2" "2"  # connectedNodes   
		"1" "1" "1" "2" "2"  # 2D_plume
		"1" "1" "1" "2" "2"  # elder
		"1" "1" "1" "2" "2"  # elderPTC
		"1" "1" "1" "2" "2"  # immobileGas
		"1" "1" "1" "2" "2"  # 2D_radial
		"1" "1" "1" "2" "2"  # boxes	r
		"1" "1" "1" "16" "16"  # 2d_Modell_grid10mRefined		
		"1" "1" "1" "2" "2"  # 2d_Modell_grid10m	
		"1" "1" "1" "16" "16"  # 2d_Modell_grid10mRefinedLowContrast		
		"1" "1" "1" "2" "2"  # 2d_Modell_grid10mLowContrast	
		"1" "1" "1" "16" "16"  # 2d_Modell_grid10mRefinedPTC		
		"1" "1" "1" "2" "2"  # 2d_Modell_grid10mPTC
		"1" "1" "1" "4" "4"  # saltRise
		"1" "1" "1" "16" "16"  # 3d_iglu
)





##### STATUS

  # 1: active   0: inactive
status=(
		"1" "1" "1" "1" "1"  # 0_1_1		BC_ST_TEST
		"1" "1" "1" "1" "1"  # 0_1_2
		"1" "1" "1" "1" "1"  # 0_2_1
		"1" "1" "1" "1" "1"  # 0_2_2
		"1" "1" "1" "1" "1"  # 1_1_1
		"1" "1" "1" "1" "1"  # 1_1_2
		"1" "1" "1" "1" "1"  # 1_2_1
		"1" "1" "1" "1" "1"  # 2_1_2
		"1" "1" "1" "1" "1"  # 2_1_2
		"1" "1" "1" "1" "1"  # 2_2_1
		"1" "1" "1" "1" "1"  # 2_2_2
		"1" "1" "1" "1" "1"  # line			1D_analyt
		"1" "1" "1" "1" "1"  # quad
		"1" "1" "1" "1" "1"  # tri
		"1" "1" "1" "1" "1"  # pri
		"1" "1" "1" "1" "1"  # tet
		"1" "1" "1" "1" "1"  # thermal		ogataBanks
		"1" "1" "1" "1" "1"  # solute
		"1" "1" "1" "1" "1"  # quad			2D_analyt
		"1" "1" "1" "1" "1"  # tri
		"1" "1" "1" "1" "1"  # quad			2D_analyt_LIQUID_FLOW
		"1" "1" "1" "1" "1"  # tri
		"1" "1" "1" "1" "1"  # case0        connectedNodes   
		"1" "1" "1" "1" "1"  # case1
		"1" "1" "1" "1" "1"  # case2
		"1" "1" "1" "1" "1"  # thermal		2D_plume
		"1" "1" "1" "1" "1"  # solute
		"1" "1" "1" "1" "1"  # haline		elder
		"1" "1" "1" "1" "1"  # thermal
		"1" "1" "1" "1" "1"  # thermohaline
		"1" "1" "1" "1" "1"  # haline		elderPTC
		"1" "1" "1" "1" "1"  # thermohaline
		"1" "0" "0" "1" "1"  # 2D_35m_50m_withoutDiss_Refined	immobileGas
		"1" "0" "1" "1" "1"  # BestFit							2D_radial
		"1" "1" "1" "1" "1"  # 2D_xy_advection_quad				boxes
		"1" "1" "1" "1" "1"  # 2D_xy_advection_tri
		"1" "1" "1" "1" "1"  # 2D_xy_diffusion_quad				
		"1" "1" "1" "1" "1"  # 2D_xy_diffusion_tri
		"1" "1" "1" "1" "1"  # 2D_xz_advection_quad				
		"1" "1" "1" "1" "1"  # 2D_xz_advection_tri
		"1" "1" "1" "1" "1"  # 2D_xz_diffusion_quad				
		"1" "1" "1" "1" "1"  # 2D_xz_diffusion_tri
		"1" "1" "1" "1" "1"  # 3D_advection_hex
		"1" "1" "1" "1" "1"  # 3D_diffusion_hex		
		"1" "1" "1" "1" "1"  # T 2d_Modell_grid10mRefined	
		"1" "1" "1" "1" "1"  # TH	
		"1" "1" "1" "1" "1"  # THC 	
		"1" "1" "1" "1" "1"  # Injection	
		"1" "1" "1" "1" "1"  # T 2d_Modell_grid10m
		"1" "1" "1" "1" "1"  # TH	
		"1" "1" "1" "1" "1"  # THC 	
		"1" "1" "1" "1" "1"  # Injection	
		"1" "1" "1" "1" "1"  # T 2d_Modell_grid10mRefinedLowContrast	
		"1" "1" "1" "1" "1"  # TH	
		"1" "1" "1" "1" "1"  # THC 	
		"1" "1" "1" "1" "1"  # Injection	
		"1" "1" "1" "1" "1"  # T 2d_Modell_grid10mLowContrast
		"1" "1" "1" "1" "1"  # TH	
		"1" "1" "1" "1" "1"  # THC 	
		"1" "1" "1" "1" "1"  # Injection
		"1" "1" "1" "1" "1"  # T 2d_Modell_grid10mRefinedPTC
		"1" "1" "1" "1" "1"  # TH	
		"1" "1" "1" "1" "1"  # THC 	
		"1" "1" "1" "1" "1"  # Injection	
		"1" "1" "1" "1" "1"  # T 2d_Modell_grid10mPTC
		"1" "1" "1" "1" "1"  # TH	
		"1" "1" "1" "1" "1"  # THC 	
		"1" "1" "1" "1" "1"  # Injection		
		"1" "1" "1" "1" "1"  # T saltRise
		"1" "1" "1" "1" "1"  # TH	
		"1" "1" "1" "1" "1"  # THC 	
		"1" "1" "1" "1" "1"  # Injection	
		"1" "1" "1" "1" "1"  # 3D_5d_stagnation 3d_iglu		
)
   
	
para_num_GROUNDWATER=(
 "2      6 1.e-014       3000           1.0   100       2"
 "2      6 1.e-014       3000           1.0   100       2"
 "805 2 1.0e-14 3000 1.0 100 4" 
 "2      6 1.e-014       3000           1.0   1 2"
 "petsc bcgs bjacobi 1.e-15 3000 1.0"
)

para_num_LIQUID=(
 "2      6 1.e-014       3000           1.0   100       2"
 "2      6 1.e-014       3000           1.0   100       2"
 "805 2 1.0e-14 3000 1.0 100 4" 
 "2      6 1.e-014       3000           1.0   1       2"
 "petsc bcgs bjacobi 1.e-15 3000 1.0"
)

para_num_HEAT=(
 "2      6 1.e-014       3000           1.   100       2"
 "2      6 1.e-014       3000           1.    100       2"
 "805 2 1.0e-14 3000 1.  100 4" 
 "2      6 1.e-014       3000           1.   1       2"
 "petsc bcgs asm 1.e-14 3000 1. "
)

para_num_MASS=(
 "2      6 1.e-014       3000           0.5   100       2"
 "2      6 1.e-014       3000           0.5   100       2"
 "805 2 1.0e-14 3000 0.5 100 4" 
 "2      6 1.e-014       3000           0.5   1       2"
 "petsc bcgs asm 1.e-14 3000 0.5"
)

para_num_PTC=(
 "2      6 1.e-014       10000           1.0   100       2"
 "2      6 1.e-014       10000           1.0   100       2"
 "805 2 1.0e-14 10000 1.0 100 4" 
 "2      6 1.e-014       10000           1.0   1       2"
 "petsc bcgs asm 1.e-14 10000 1.0"
)



	









