class Processes:
    """
    contains flow process name and flag for mass and heat
    used in numerics class Global
    """
    __flow = 'NO_FLOW'
    # flags True if process exists
    __mass_flag, __heat_flag = bool(), bool()  # MASS_TRANSPORT - HEAT_TRANSPORT
    __deformation_flag, __fluid_momentum_flag, __overland_flag = \
        bool(), bool(), bool()  # DEFORMATION - FLUID_MOMENTUM -OVERLAND_FLOW

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

    @property
    def deformation_flag(self):
        return self.__deformation_flag

    @property
    def fluid_momentum_flag(self):
        return self.__fluid_momentum_flag

    @property
    def overland_flag(self):
        return self.__overland_flag

    @flow.setter
    def flow(self, value):
        self.__flow = value

    @mass_flag.setter
    def mass_flag(self, value):
        self.__mass_flag = value

    @heat_flag.setter
    def heat_flag(self, value):
        self.__heat_flag = value

    @deformation_flag.setter
    def deformation_flag(self, value):
        self.__deformation_flag = value

    @fluid_momentum_flag.setter
    def fluid_momentum_flag(self, value):
        self.__fluid_momentum_flag = value

    @overland_flag.setter
    def overland_flag(self, value):
        self.__overland_flag = value


class Global:
    """
    stores numerics data taken from database
    except the ones which depend on process
    """
    __processes = None  # class Processes

    __coupled_flag, __lumping_flag, __non_linear_flag = bool(), bool(), bool()
    # ! only flow processes can be lumped or nonlinear

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
