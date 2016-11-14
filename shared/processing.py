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

    @number_cpus.setter
    def number_cpus(self, value):
        self.__number_cpus = value

    @mode.setter
    def mode(self, value):
        self.__mode = value
