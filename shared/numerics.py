class processes:
    """
    contains flow process name and flag for mass and heat
    used in numerics class Global
    """
    _flow = 'NO_FLOW'
    _massFlag = '0'  # becomes unity if MASS_TRANSPORT exists 
    _heatFlag = '0'  # becomes unity if HEAT_TRANSPORT exists

    def __init__(self):
        pass

    def set(self, flow, massFlag, heatFlag):
        self._flow = flow
        self._massFlag = massFlag
        self._heatFlag = heatFlag


class Global:
    """
    stores numerics data from mySQL
    except the ones which depend on process
    used to write data files, which can be transfered to remote computer
    """
    _prcs = '0'
    _processes = []  # first element always flow, than mass and heat if exist

    _coupledFlag = '0'
    _lumpingFlag = '0'  # only flow lumped
    _nonlinearFlag = '0'  # only flow nonlinear

    def __init__(self):
        del self._processes[:]

    def __del__(self):
        del self._processes[:]

    def set(self, prcs, coupledFlag, lumpingFlag, nonlinearFlag):
        self._prcs = prcs
 
        self._processes.append('flow')
        if prcs._massFlag == '1':
            self._processes.append('mass')
        if prcs._heatFlag == '1':
            self._processes.append('heat')

        self._coupledFlag = coupledFlag
        self._lumpingFlag = lumpingFlag
        self._nonlinearFlag = nonlinearFlag



