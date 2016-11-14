class Processes:
    """
    contains flow process name and flag for mass and heat
    used in numerics class Global
    """
    __flow = 'NO_FLOW'
    __mass_flag = bool()  # becomes unity if MASS_TRANSPORT exists
    __heat_flag = bool()  # becomes unity if HEAT_TRANSPORT exists

    def __init__(self):
        pass

    @property
    def flow(self):
        return self.__flow

    @property
    def mass_flag(self):
        return self.__mass_flag

    @property
    def heat_flag(self):
        return self.__heat_flag

    @flow.setter
    def flow(self, value):
        self.__flow = value

    @mass_flag.setter
    def mass_flag(self, value):
        self.__mass_flag = value

    @heat_flag.setter
    def heat_flag(self, value):
        self.__heat_flag = value


class Global:
    """
    stores numerics data from mySQL
    except the ones which depend on process
    used to write data files, which can be transfered to remote computer
    """
    __processes = None  # class Processes

    __coupled_flag = bool()
    __lumping_flag = bool()  # only flow lumped
    __non_linear_flag = bool()  # only flow nonlinear

    def __init__(self):
        self.__processes = Processes()

    def __del__(self):
        del self.__processes

    @property
    def coupled_flag(self):
        return self.__coupled_flag

    @property
    def lumping_flag(self):
        return self.__lumping_flag

    @property
    def non_linear_flag(self):
        return self.__non_linear_flag

    @property
    def processes(self):
        return self.__processes

    @processes.setter
    def processes(self, value):
        self.__processes = value

    @coupled_flag.setter
    def coupled_flag(self, value):
        self.__coupled_flag = value

    @lumping_flag.setter
    def lumping_flag(self, value):
        self.__lumping_flag = value

    @non_linear_flag.setter
    def non_linear_flag(self, value):
        self.__non_linear_flag = value
