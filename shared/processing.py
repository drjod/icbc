
######################################################################
#
# parallelization class Parallelization
# Task:
#   holds parallelization data from mySQL database to write *.num and *.pbs files 
#


class Processing:
    
    _numberOfCPUs = '0'
    _mode = '0' # sequential, omp, mpi_nodes, mpi_elements

    def __init__( self ):
        pass

    def set ( self, numberOfCPUs, mode):

        self._numberOfCPUs = numberOfCPUs
        self._mode = mode
        




