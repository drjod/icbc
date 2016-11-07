class Processes:
    """
    contains flow process name and flag for mass and heat
    used in numerics class Global
    """
    __flow = 'NO_FLOW'
    __mass_flag = '0'  # becomes unity if MASS_TRANSPORT exists
    __heat_flag = '0'  # becomes unity if HEAT_TRANSPORT exists

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

    def set(self, flow, mass_flag, heat_flag):
        self.__flow = flow
        self.__mass_flag = mass_flag
        self.__heat_flag = heat_flag


class Global:
    """
    stores numerics data from mySQL
    except the ones which depend on process
    used to write data files, which can be transfered to remote computer
    """
    __prcs = None
    __processes = list()  # first element always flow, than mass and heat if exist

    __coupled_flag = str()
    __lumping_flag = str()  # only flow lumped
    __non_linear_flag = str()  # only flow nonlinear

    def __init__(self):
        del self.__processes[:]

    def __del__(self):
        del self.__processes[:]

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
    def prcs(self):
        return self.__prcs

    @property
    def processes(self):
        return self.__processes

    def set(self, prcs, coupled_flag, lumping_flag, nonlinear_flag):
        self.__prcs = prcs
 
        self.__processes.append('flow')
        if prcs.mass_flag == '1':
            self.__processes.append('mass')
        if prcs.heat_flag == '1':
            self.__processes.append('heat')

        self.__coupled_flag = coupled_flag
        self.__lumping_flag = lumping_flag
        self.__non_linear_flag = nonlinear_flag



