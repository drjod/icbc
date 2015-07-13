#!/bin/sh

. ./template_pbs.sh


Template_num(){

echo "#NUMERICS
\$PCS_TYPE
  GROUNDWATER_FLOW
\$ELE_MASS_LUMPING
  1
\$LINEAR_SOLVER
; method error_tolerance max_iterations theta precond storage
  ${para_num_GROUNDWATER[${ndx[2]}]}
;\$NON_LINEAR_ITERATIONS
;type -- error_method -- max_iterations -- relaxation -- tolerance(s)
; PICARD LMAX 100 0.0 5.0e2
\$ELE_GAUSS_POINTS
  2



#NUMERICS
\$PCS_TYPE
  MASS_TRANSPORT
\$ELE_GAUSS_POINTS
  2
\$LINEAR_SOLVER 
; method error_tolerance max_iterations theta precond storage
  ${para_num_MASS[${ndx[2]}]}
;\$NON_LINEAR_ITERATIONS
;type -- error_method -- max_iterations -- relaxation -- tolerance(s)
; PICARD LMAX .01 0.0 1.0e-2
;\$FEM_FCT
;  1 0 

#STOP" > /$path2member/test.$ending

}
