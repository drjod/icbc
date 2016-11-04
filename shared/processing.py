class Processing:
    """
    holds parallelization data from mySQL database to write *.num and *.pbs files
    """
    _number_cpus = '0'
    _mode = '0'  # sequential, omp, mpi_nodes, mpi_elements

    def __init__(self):
        pass

    @property
    def number_cpus(self):
        return self._number_cpus

    @property
    def mode(self):
        return self._mode

    def set(self, number_cpus, mode):
        self._number_cpus = number_cpus
        self._mode = mode
