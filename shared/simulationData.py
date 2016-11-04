from sys import path as syspath, exc_info
from os import path, chdir
from subprocess import Popen
from importlib import reload
syspath.append(path.join(path.dirname(__file__), '..', 'customized'))
syspath.append(path.join(path.dirname(__file__), '..', 'temp'))
from configurationCustomized import location, rootDirectory, walltime, queue
from configurationCustomized import setCompilerVariables, setMklVariables, setMpiVariables
from configurationShared import examplesName, norm, coupling_iterations_min, coupling_iterations_max
from configurationShared import tollerance_linear, tollerance_nonlinear, numberOfGaussPoints
from configurationShared import maxIterations_linear, maxIterations_nonlinear
from utilities import message, adapt_path
from numerics import Global, processes
from processing import Processing

import numerics_global_OGS_FEM, numerics_flow_OGS_FEM, numerics_mass_OGS_FEM, numerics_heat_OGS_FEM
import numerics_global_OGS_FEM_SP, numerics_flow_OGS_FEM_SP, numerics_mass_OGS_FEM_SP, numerics_heat_OGS_FEM_SP
import numerics_global_OGS_FEM_MKL, numerics_flow_OGS_FEM_MKL, numerics_mass_OGS_FEM_MKL, numerics_heat_OGS_FEM_MKL
import numerics_global_OGS_FEM_MPI, numerics_flow_OGS_FEM_MPI, numerics_mass_OGS_FEM_MPI, numerics_heat_OGS_FEM_MPI
import numerics_global_OGS_FEM_PETSC, numerics_flow_OGS_FEM_PETSC, numerics_mass_OGS_FEM_PETSC
import numerics_heat_OGS_FEM_PETSC
import prc_OGS_FEM, prc_OGS_FEM_SP, prc_OGS_FEM_MKL, prc_OGS_FEM_MPI, prc_OGS_FEM_PETSC

class ReadFileFlags:
    """
    control data file reloads dependend on selected operation
    numerics and parallelization data Files are reloaded if flags are set True
    """
    _numerics = False
    _processing = False

    def __init__(self, operation_type, operation):
        if operation_type == 's': # simulation
            if operation == 'n':  # write num
                self._numerics = True
            if operation == 'n' or operation == 't' or operation == 'm': # write num, write pbs, mesh partition 
                self._processing = True

    @property
    def numerics(self):
        return self._numerics

    @property
    def processing(self):
        return self._processing

class SimulationData:
    """
    contains the numerics data from mySQL database
    interface to write *.num and *.pbs files
    """
    # numerics data that depend on process
    __preconditioner = list() # 0 no preconditioner, 1 Jacobi, 100 ILU - each process one list item
    __theta = list()  # 1 implicit, 0, explicit - each process one list item
    __solver = list()

    __numerics = None # all numerics data - Global
    __processing = None # parallelization

    def __init__(self, operation_type=None, operation=None):
        if not operation is None and not operation_type is None:
            self.__read_file_flags =  ReadFileFlags(operation_type, operation)

    def __del__(self):  
        del self.__preconditioner[:]
        del self.__theta[:]

    @property
    def read_file_flags(self):
        return self.__read_file_flags

    def import_num_data_files(self, configuration):
        """
        import files with mySQL data on remote computer
        :param configuration:
        :return:
        """
        try:
            if self.__read_file_flags._numerics:
                # global numerics
                if configuration == "OGS_FEM":
                    reload(numerics_global_OGS_FEM)
                elif configuration == "OGS_FEM_SP":
                    reload(numerics_global_OGS_FEM_SP)
                elif configuration == "OGS_FEM_MKL":
                    reload(numerics_global_OGS_FEM_MKL)
                elif configuration == "OGS_FEM_MPI":
                    reload(numerics_global_OGS_FEM_MPI)
                elif configuration == "OGS_FEM_PETSC":
                    reload(numerics_global_OGS_FEM_PETSC)
                else:
                    message(mode='ERROR', text='Failed to import numerics_global')
                # flow numerics
                if configuration == "OGS_FEM":
                    reload(numerics_flow_OGS_FEM)
                elif configuration == "OGS_FEM_SP":
                    reload(numerics_flow_OGS_FEM_SP)
                elif configuration == "OGS_FEM_MKL":
                    reload(numerics_flow_OGS_FEM_MKL)
                elif configuration == "OGS_FEM_MPI":
                    reload(numerics_flow_OGS_FEM_MPI)
                elif configuration == "OGS_FEM_PETSC":
                    reload(numerics_flow_OGS_FEM_PETSC)
                else:
                    message(mode='ERROR', text='Failed to import numerics_flow')
                # mass numerics - imports always
                if configuration == "OGS_FEM":
                    reload(numerics_mass_OGS_FEM)
                elif configuration == "OGS_FEM_SP":
                    reload(numerics_mass_OGS_FEM_SP)
                elif configuration == "OGS_FEM_MKL":
                    reload(numerics_mass_OGS_FEM_MKL)
                elif configuration == "OGS_FEM_MPI":
                    reload(numerics_mass_OGS_FEM_MPI)
                elif configuration == "OGS_FEM_PETSC":
                    reload(numerics_mass_OGS_FEM_PETSC)
                else:
                    message(mode='ERROR', text='Failed to import numerics_mass')
                # heat numerics - imports always
                if configuration == "OGS_FEM":
                    reload(numerics_heat_OGS_FEM)
                elif configuration == "OGS_FEM_SP":
                    reload(numerics_heat_OGS_FEM_SP)
                elif configuration == "OGS_FEM_MKL":
                    reload(numerics_heat_OGS_FEM_MKL)
                elif configuration == "OGS_FEM_MPI":
                    reload(numerics_heat_OGS_FEM_MPI)
                elif configuration == "OGS_FEM_PETSC":
                    reload(numerics_heat_OGS_FEM_PETSC)
                else:
                    message(mode='ERROR', text='Failed to import numerics_heat')
        except:
            message(mode='ERROR', text='Failed to import num data from files')

    def import_processing_data_files(self, configuration):
        """
        import files with mySQL data on remote computer
        :param configuration:
        :return:
        """
        try:
            if configuration == "OGS_FEM":
                reload(prc_OGS_FEM)
            elif configuration == "OGS_FEM_SP":
                reload(prc_OGS_FEM_SP)
            elif configuration == "OGS_FEM_MKL":
                reload(prc_OGS_FEM_MKL)
            elif configuration == "OGS_FEM_MPI":
                reload(prc_OGS_FEM_MPI)
            elif configuration == "OGS_FEM_PETSC":
                reload(prc_OGS_FEM_PETSC)
            else:
                message(mode='ERROR', text='Failed to import prc')
        except:
            message(mode='ERROR', text='Failed to import processing data from files')

    def get_num_data_from_modules(self, configuration):
        """
        put numerics data from module into SimData
        :param configuration:
        :return:
        """
        if configuration == "OGS_FEM":
            self.get_num_data_from_modules_OGS_FEM()
        elif configuration == "OGS_FEM_SP":
            self.get_num_data_from_modules_OGS_FEM_SP()
        elif configuration == "OGS_FEM_MKL":
            self.get_num_data_from_modules_OGS_FEM_MKL()
        elif configuration == "OGS_FEM_MPI":
            self.get_num_data_from_modules_OGS_FEM_MPI()
        elif configuration == "OGS_FEM_PETSC":
            self.get_num_data_from_modules_OGS_FEM_PETSC()

    def get_num_data_from_modules_OGS_FEM(self):
        """

        :return:
        """
        globNum = Global()
        prcs = processes() 

        preconditioner = list()
        solver = list()
        theta = list()

        prcs.set(numerics_global_OGS_FEM.flowProcess,
                 numerics_global_OGS_FEM.massFlag, numerics_global_OGS_FEM.heatFlag)
        globNum.set(prcs, numerics_global_OGS_FEM.coupledFlag,
                    numerics_global_OGS_FEM.lumpingFlag, numerics_global_OGS_FEM.nonlinearFlag)
        
        theta.append(numerics_flow_OGS_FEM.theta)
        solver.append(numerics_flow_OGS_FEM.solver)
        preconditioner.append(numerics_flow_OGS_FEM.precond)
        
        if numerics_global_OGS_FEM.massFlag == '1':
            theta.append(numerics_mass_OGS_FEM.theta)
            solver.append(numerics_mass_OGS_FEM.solver)
            preconditioner.append(numerics_mass_OGS_FEM.precond)

        if numerics_global_OGS_FEM.heatFlag == '1':
            theta.append(numerics_heat_OGS_FEM.theta)
            solver.append(numerics_heat_OGS_FEM.solver)
            preconditioner.append(numerics_heat_OGS_FEM.precond)

        self.setNum(globNum, solver, preconditioner, theta) 

    def get_num_data_from_modules_OGS_FEM_SP(self):
        """

        :return:
        """
        globNum = Global()
        prcs = processes() 

        preconditioner = list()
        solver = list()
        theta = list()

        prcs.set(numerics_global_OGS_FEM_SP.flowProcess,
                 numerics_global_OGS_FEM_SP.massFlag, numerics_global_OGS_FEM_SP.heatFlag)
        globNum.set(prcs, numerics_global_OGS_FEM_SP.coupledFlag,
                    numerics_global_OGS_FEM_SP.lumpingFlag, numerics_global_OGS_FEM_SP.nonlinearFlag)
        
        theta.append(numerics_flow_OGS_FEM_SP.theta)
        solver.append(numerics_flow_OGS_FEM_SP.solver)
        preconditioner.append(numerics_flow_OGS_FEM_SP.precond)
        
        if numerics_global_OGS_FEM_SP.massFlag == '1':
            theta.append(numerics_mass_OGS_FEM_SP.theta)
            solver.append(numerics_mass_OGS_FEM_SP.solver)
            preconditioner.append(numerics_mass_OGS_FEM_SP.precond)

        if numerics_global_OGS_FEM_SP.heatFlag == '1':
            theta.append(numerics_heat_OGS_FEM_SP.theta)
            solver.append(numerics_heat_OGS_FEM_SP.solver)
            preconditioner.append(numerics_heat_OGS_FEM_SP.precond)

        self.setNum(globNum, solver, preconditioner, theta) 

    def get_num_data_from_modules_OGS_FEM_MKL(self):
        """

        :return:
        """
        globNum = Global()
        prcs = processes() 

        preconditioner = list()
        solver = list()
        theta = list()

        prcs.set(numerics_global_OGS_FEM_MKL.flowProcess,
                 numerics_global_OGS_FEM_MKL.massFlag, numerics_global_OGS_FEM_MKL.heatFlag)
        globNum.set(prcs, numerics_global_OGS_FEM_MKL.coupledFlag,
                    numerics_global_OGS_FEM_MKL.lumpingFlag, numerics_global_OGS_FEM_MKL.nonlinearFlag)
        
        theta.append(numerics_flow_OGS_FEM_MKL.theta)
        solver.append(numerics_flow_OGS_FEM_MKL.solver)
        preconditioner.append(numerics_flow_OGS_FEM_MKL.precond)
        
        if numerics_global_OGS_FEM_MKL.massFlag == '1':
            theta.append(numerics_mass_OGS_FEM_MKL.theta)
            solver.append(numerics_mass_OGS_FEM_MKL.solver)
            preconditioner.append(numerics_mass_OGS_FEM_MKL.precond)

        if numerics_global_OGS_FEM_MKL.heatFlag == '1':
            theta.append(numerics_heat_OGS_FEM_MKL.theta)
            solver.append(numerics_heat_OGS_FEM_MKL.solver)
            preconditioner.append(numerics_heat_OGS_FEM_MKL.precond)

        self.setNum(globNum, solver, preconditioner, theta) 

    def get_num_data_from_modules_OGS_FEM_MPI(self):
        """

        :return:
        """
        globNum = Global()
        prcs = processes() 

        preconditioner = list()
        solver = list()
        theta = list()

        prcs.set(numerics_global_OGS_FEM_MPI.flowProcess,
                 numerics_global_OGS_FEM_MPI.massFlag, numerics_global_OGS_FEM_MPI.heatFlag)
        globNum.set(prcs, numerics_global_OGS_FEM_MPI.coupledFlag,
                    numerics_global_OGS_FEM_MPI.lumpingFlag, numerics_global_OGS_FEM_MPI.nonlinearFlag)
        
        theta.append(numerics_flow_OGS_FEM_MPI.theta)
        solver.append(numerics_flow_OGS_FEM_MPI.solver)
        preconditioner.append(numerics_flow_OGS_FEM_MPI.precond)
        
        if numerics_global_OGS_FEM_MPI.massFlag == '1':
            theta.append(numerics_mass_OGS_FEM_MPI.theta)
            solver.append(numerics_mass_OGS_FEM_MPI.solver)
            preconditioner.append(numerics_mass_OGS_FEM_MPI.precond)

        if numerics_global_OGS_FEM_MPI.heatFlag == '1':
            theta.append(numerics_heat_OGS_FEM_MPI.theta)
            solver.append(numerics_heat_OGS_FEM_MPI.solver)
            preconditioner.append(numerics_heat_OGS_FEM_MPI.precond)

        self.setNum(globNum, solver, preconditioner, theta) 

    def get_num_data_from_modules_OGS_FEM_PETSC(self):
        """

        :return:
        """
        globNum = Global()
        prcs = processes() 

        preconditioner = list()
        solver = list()
        theta = list()

        prcs.set(numerics_global_OGS_FEM_PETSC.flowProcess,
                 numerics_global_OGS_FEM_PETSC.massFlag, numerics_global_OGS_FEM_PETSC.heatFlag)
        globNum.set(prcs, numerics_global_OGS_FEM_PETSC.coupledFlag,
                    numerics_global_OGS_FEM_PETSC.lumpingFlag, numerics_global_OGS_FEM_PETSC.nonlinearFlag)
        
        theta.append(numerics_flow_OGS_FEM_PETSC.theta)
        solver.append(numerics_flow_OGS_FEM_PETSC.solver)
        preconditioner.append(numerics_flow_OGS_FEM_PETSC.precond)
        
        if numerics_global_OGS_FEM_PETSC.massFlag == '1':
            theta.append(numerics_mass_OGS_FEM_PETSC.theta)
            solver.append(numerics_mass_OGS_FEM_PETSC.solver)
            preconditioner.append(numerics_mass_OGS_FEM_PETSC.precond)

        if numerics_global_OGS_FEM_PETSC.heatFlag == '1':
            theta.append(numerics_heat_OGS_FEM_PETSC.theta)
            solver.append(numerics_heat_OGS_FEM_PETSC.solver)
            preconditioner.append(numerics_heat_OGS_FEM_PETSC.precond)

        self.setNum(globNum, solver, preconditioner, theta)

    def getProcessingDataFromModule(self, configuration ):
        """
        put processing data (parallel, ...) from module into SimData
        :param configuration:
        :return:
        """
        if configuration == "OGS_FEM":
            self.getProcessingDataFromModule_OGS_FEM()
        elif configuration == "OGS_FEM_SP":
            self.getProcessingDataFromModule_OGS_FEM_SP()
        elif configuration == "OGS_FEM_MKL":
            self.getProcessingDataFromModule_OGS_FEM_MKL()
        elif configuration == "OGS_FEM_MPI":
            self.getProcessingDataFromModule_OGS_FEM_MPI()
        elif configuration == "OGS_FEM_PETSC":
            self.getProcessingDataFromModule_OGS_FEM_PETSC()


    def getProcessingDataFromModule_OGS_FEM(self):
        """

        :return:
        """
        proc = Processing()

        proc.set(prc_OGS_FEM.numberOfCPUs, prc_OGS_FEM.mode)

        self.setProcessing(proc)

    def getProcessingDataFromModule_OGS_FEM_SP(self):
        """

        :return:
        """
        proc = Processing()

        proc.set(prc_OGS_FEM_SP.numberOfCPUs, prc_OGS_FEM_SP.mode)

        self.setProcessing(proc)

    def getProcessingDataFromModule_OGS_FEM_MKL(self):
        """

        :return:
        """
        proc = Processing()

        proc.set(prc_OGS_FEM_MKL.numberOfCPUs, prc_OGS_FEM_MKL.mode)

        self.setProcessing(proc)

    def getProcessingDataFromModule_OGS_FEM_MPI(self):
        """

        :return:
        """
        proc = Processing()

        proc.set(prc_OGS_FEM_MPI.numberOfCPUs, prc_OGS_FEM_MPI.mode)

        self.setProcessing(proc)

    def getProcessingDataFromModule_OGS_FEM_PETSC(self):
        """

        :return:
        """
        proc = Processing()

        proc.set(prc_OGS_FEM_PETSC.numberOfCPUs, prc_OGS_FEM_PETSC.mode)

        self.setProcessing(proc)

    def setProcessing(self, processing):
        """
        store the parallelization data from mySQL
        :param processing:
        :return:
        """
        self.__processing = processing

    def setNum(self, numerics, solver, preconditioner, theta):
        """
        store the numerics data from mySQL
        """
        self.__numerics = numerics
        self.__solver = solver
        self.__preconditioner = preconditioner
        self.__theta = theta

    def write_processing_data(self, configuration):
        """
        calls member function writeDataFile to
        write parallelization data into a file
        which can be transfered to remote computer
        :param configuration:
        :return:
        """
        self.writeDataFile('prc_' + configuration + '.py', 0, 0, 0)

    def write_numerics_data(self, configuration):
        """
        calls member function writeDataFile to
        write files with numerics data (flow, mass, heat separately)
        which can be transfered to remote computer
        item always sim containing type, case configuration
        :param configuration:
        :return:
        """
        self.writeDataFile('numerics_global_' + configuration + '.py', 0, 0, 0)

        i = 0
        for process in self.___processes: # loop over flow, mass, heat
            self.writeDataFile('numerics_' + process + '_' + configuration + '.py',
                               self.__solver[i], self.__preconditioner[i], self.__theta[i])
            i += 1

    def write_num(self, directory):
        """
        Reads global numerics and parallelization data from files and writes *.num file for simulation
        :param directory:
        :return:
        """
        try:
            fileStream = open(directory + examplesName + '.num', 'w')
        except OSError as err:
            message(mode='ERROR', text='OS error: {0}'.format(err))
        else:
            if self.___coupledFlag == '1':
                fileStream.write('\n$OVERALL_COUPLING\n')
                fileStream.write(' ' + coupling_iterations_min + ' ' + coupling_iterations_max + '\n')

            self.writeProcessIntoNumFile(fileStream, 0) # flow
            if self.___prcs._massFlag == '1':
                self.writeProcessIntoNumFile(fileStream, 1)
            if self.___prcs._heatFlag == '1':
                self.writeProcessIntoNumFile(fileStream, 2)
            fileStream.write('\n#STOP\n')
            fileStream.close()

    def writeProcessIntoNumFile(self, filestream, process_id):
        """
        called by write_num for each process
        reads numerics data file and writes num data for a selected process into file
        :param filestream:
        :param process_id:
        :return:
        """
        filestream.write('\n#NUMERICS\n')
        #  PCS
        filestream.write(' $PCS_TYPE\n')
        if process_id == 0:
            filestream.write('  ' + self.___prcs._flow  + '\n')
        elif process_id == 1:
            filestream.write('  MASS_TRANSPORT\n')
        elif process_id == 2:
            filestream.write('  HEAT_TRANSPORT\n')
        # LUMPING
        if self.___lumpingFlag == '1' and process_id == 0:   # only flow gets lumped
            filestream.write(' $ELE_MASS_LUMPING\n')
            filestream.write('  1\n')
        # LINEAR SOLVER
            filestream.write(' $LINEAR_SOLVER\n')
        if self.__processing.mode == 'mpi_nodes':
            filestream.write('; method precond error_tolerance max_iterations theta\n')
            filestream.write('  petsc ' + self.__solver[process_id] + '  ' + self.__preconditioner[process_id]
                             + '  ' + tollerance_linear  + '  ' + maxIterations_linear + ' 1. \n')
        elif self.__processing.mode == 'omp':  # matrix storage is 4
            filestream.write('; method norm error_tolerance max_iterations theta precond storage\n')
            filestream.write(self.__solver[process_id] + '  ' + norm  + ' ' + tollerance_linear + '  '
                             + maxIterations_linear + '  ' + self.__theta[process_id]  + '   '
                             + self.__preconditioner[process_id]  + ' 4\n')
        elif self.__processing.mode == 'sequential' or self.__processing.mode == 'mpi_elements':
            filestream.write('; method norm error_tolerance max_iterations theta precond storage\n')
            filestream.write('  ' + self.__solver[process_id] + '  ' + norm + '  ' + tollerance_linear + '  '
                              + maxIterations_linear + '  '
                              + self.__theta[process_id] + '  ' + self.__preconditioner[process_id] + '  ' + '2' + '\n')
        else:
             message(mode='ERROR', text='Mode ' + self.__processing.mode + ' not supported')
        # NONLINEAR SOLVER
        if self.___nonlinearFlag == '1':
            filestream.write(' $NON_LINEAR_ITERATIONS\n')
            filestream.write(';type -- error_method -- max_iterations -- relaxation -- tolerance(s)\n')
            filestream.write('  PICARD LMAX ' + maxIterations_nonlinear  + ' 0.0 ' + tollerance_nonlinear + '\n')
        # NUMBER OF GAUSS POINTS
        filestream.write(' $ELE_GAUSS_POINTS\n')
        filestream.write('  ' + numberOfGaussPoints + '\n')
        # COUPLING
        if self.___coupledFlag == '1':
            filestream.write('$COUPLING_CONTROL\n')
            filestream.write(' LMAX ' + tollerance_nonlinear + '\n')
      
    def writeDataFile(self, file_name, solver, precond, theta):
        """
        called by member function writeData
        to write numerics or parallelization data into a file
        :param file_name:
        :param solver:
        :param precond:
        :param theta:
        :return:
        """
        try:
            filestream = open(rootDirectory + '\\testingEnvironment\\scripts\\icbc\\temp\\' + file_name, 'w')
        except OSError as err:
            message.console(type='ERROR', text='OS error: {0}'.format(err))
        else:
            message(mode='INFO', text='Writing ' + location + ' ' + file_name)
            if file_name.find('numerics_global') > -1:
                #filestream.write('coupling_iterations_min = \'' + coupling_iterations_min + '\' \n')
                #filestream.write('coupling_iterations_max = \'' + coupling_iterations_max + '\' \n')
                filestream.write('flowProcess = \'' + self.___prcs._flow  + '\' \n')
                filestream.write('massFlag = \'' + self.___prcs._massFlag + '\' \n')
                filestream.write('heatFlag = \'' + self.___prcs._heatFlag + '\' \n\n')
                filestream.write('coupledFlag = \'' + self.___coupledFlag + '\' \n')
                filestream.write('lumpingFlag = \'' + self.___lumpingFlag + '\' \n')
                filestream.write('nonlinearFlag = \'' + self.___nonlinearFlag + '\' \n')
            elif file_name.find('prc') > -1:
                filestream.write('numberOfCPUs = \'' + self.__processing.number_cpus + '\' \n')
                filestream.write('mode = \'' + self.__processing.mode + '\' \n')
            else:
                #filestream.write('maxIterations_linear = \'' + maxIterations_linear + '\' \n')
                #filestream.write('maxIterations_nonlinear = \'' + maxIterations_nonlinear + '\' \n')
                #filestream.write('norm = \'' + norm + '\' \n')
                #filestream.write('tollerance_linear = \'' + tollerance_linear + '\' \n')
                #filestream.write('tollerance_nonlinear = \'' + tollerance_nonlinear + '\' \n')
                filestream.write('solver = \'' + str(solver) + '\' \n')
                filestream.write('precond = \''+  str(precond) + '\'\n')
                #filestream.write('matrixStorage = \'sparse\'\n')
                #filestream.write('numberOfGaussPoints = \'' + numberOfGaussPoints + '\'\n')
                filestream.write('theta = \'' + str(theta) + '\'\n')

            filestream.close()
    
    def write_pbs(self, directory, executable, item_type):
        """
        reloads prc.py to get parallelization data and writes *.pbs file
        :param directory:
        :param executable:
        :param item_type:
        :return:
        """
        # config
        ompthreads = None
        if self.__processing.mode == 'sequential':
            ncpus = '1'
            command = ' '
            place = 'group=host'
        elif self.__processing.mode == 'omp':
            ncpus = self.__processing.number_cpus
            ompthreads = self.__processing.number_cpus
            command = ' '
            place = 'group=host'
        elif self.__processing.mode == 'mpi_elements' or self.__processing.mode == 'mpi_nodes':  # parallel
            ncpus = self.__processing.number_cpus
            command = 'mpirun -r rsh -machinefile $PBS_NODEFILE -n ' + ncpus + ' '
            place = 'scatter'
        else:
           message(mode='ERROR', not_supported='Mode ' + self.__processing.mode)
           return
        # write
        try:
            filestream = open(directory + 'run.pbs', 'w')
        except OSError as err:
            message(mode='ERROR', text='OS error: {0}'.format(err))
        else:
            filestream.write('#!/bin/bash\n')
            filestream.write('#PBS -o ' + directory + 'screenout.txt\n')
            filestream.write('#PBS -j oe\n')
            filestream.write('#PBS -r n\n')
            filestream.write('#PBS -l walltime=' + walltime + '\n')
            filestream.write('#PBS -l select=1:ncpus=' + ncpus)
            if ompthreads:
                filestream.writelines(':ompthreads=' + ncpus)
            filestream.write(':mem=3gb\n')
            filestream.write('#PBS -l place=' + place + '\n')
            filestream.write('#PBS -q ' + queue + '\n')
            filestream.write('#PBS -N ' + item_type +'\n')
            filestream.write('\n')
            filestream.write('cd $PBS_O_WORKDIR\n')
            filestream.write('\n')
            filestream.write('. /usr/share/Modules/init/bash\n')
            filestream.write('\n')
            filestream.write(setCompilerVariables)
            filestream.write(setMklVariables)
            filestream.write(setMpiVariables)
            filestream.write('\n')
            filestream.write('time ' + command + executable + ' ' + directory + examplesName + '\n')
            filestream.write('\n')
            filestream.write('qstat -f $PBS_JOBID\n')
            filestream.write('exit\n')
            filestream.close()

    def partition_mesh(self, directory):
        """
        reloads prc.py to get parallelization data and writes *.pbs file
        :param directory:
        :return:
        """
        script_partition = rootDirectory + adapt_path('testingEnvironment\\scripts\\') + 'partition.sh'

        chdir(directory)
        meshfile = directory + examplesName + '.msh'
        if path.isfile(meshfile):
            try:
                if self.__processing.mode == 'mpi_elements':  # for OGS_FEM_MPI, ...
                    Popen(script_partition + ' ' + self.__processing.number_cpus + ' -e -asci ' + directory, shell=True)
                if self.__processing.mode == 'mpi_nodes':    # for OGS_FEM_PETSC
                    Popen(script_partition + ' ' +
                          self.__processing.number_cpus + ' -n -binary ' + directory, shell=True)
            except:
                message(mode='ERROR', text='%s' % exc_info()[0])
        else:
            message(mode='ERROR', text='Mesh file missing')
