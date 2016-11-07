class Processing:
    """
    holds parallelization data from mySQL database to write *.num and *.pbs files
    """
    __number_cpus = '0'
    __mode = '0'  # sequential, omp, mpi_nodes, mpi_elements

    def __init__(self):
        pass

    @property
    def number_cpus(self):
        return self.__number_cpus

    @property
    def mode(self):
        return self.__mode

    def set(self, number_cpus, mode):
        self.__number_cpus = number_cpus
        self.__mode = mode
