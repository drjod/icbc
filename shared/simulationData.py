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
from numerics import Global, Processes
from processing import Processing

import numerics_global_ogs_fem, numerics_flow_ogs_fem, numerics_mass_ogs_fem, numerics_heat_ogs_fem
import numerics_global_ogs_fem_sp, numerics_flow_ogs_fem_sp, numerics_mass_ogs_fem_sp, numerics_heat_ogs_fem_sp
import numerics_global_ogs_fem_mkl, numerics_flow_ogs_fem_mkl, numerics_mass_ogs_fem_mkl, numerics_heat_ogs_fem_mkl
import numerics_global_ogs_fem_mpi, numerics_flow_ogs_fem_mpi, numerics_mass_ogs_fem_mpi, numerics_heat_ogs_fem_mpi
import numerics_global_ogs_fem_petsc, numerics_flow_ogs_fem_petsc, numerics_mass_ogs_fem_petsc
import numerics_heat_ogs_fem_petsc
import prc_ogs_fem, prc_ogs_fem_sp, prc_ogs_fem_mkl, prc_ogs_fem_mpi, prc_ogs_fem_petsc

class ReadFileFlags:
    """
    control data file reloads dependend on selected operation
    numerics and parallelization data Files are reloaded if flags are set True
    """
    __numerics = False
    __processing = False

    def __init__(self, operation_type, operation):
        if operation_type == 's':  # simulation
            if operation == 'n':  # write num
                self.__numerics = True
            if operation == 'n' or operation == 't' or operation == 'm':  # write num, write pbs, mesh partition
                self.__processing = True

    @property
    def numerics(self):
        return self.__numerics

    @property
    def processing(self):
        return self.__processing


class SimulationData:
    """
    contains the numerics data from mySQL database
    interface to write *.num and *.pbs files
    """
    # numerics data that depend on process
    __preconditioner = list()  # 0 no preconditioner, 1 Jacobi, 100 ILU - each process one list item
    __theta = list()  # 1 implicit, 0, explicit - each process one list item
    __solver = list()

    __numerics = None  # all numerics data - Global
    __processing = None  # parallelization

    def __init__(self, operation_type=None, operation=None):
        if operation is not None and operation_type is not None:
            self.__read_file_flags = ReadFileFlags(operation_type, operation)

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
            if self.__read_file_flags.numerics:
                # global numerics
                if configuration == "OGS_FEM":
                    reload(numerics_global_ogs_fem)
                elif configuration == "OGS_FEM_SP":
                    reload(numerics_global_ogs_fem_sp)
                elif configuration == "OGS_FEM_MKL":
                    reload(numerics_global_ogs_fem_mkl)
                elif configuration == "OGS_FEM_MPI":
                    reload(numerics_global_ogs_fem_mpi)
                elif configuration == "OGS_FEM_PETSC":
                    reload(numerics_global_ogs_fem_petsc)
                else:
                    message(mode='ERROR', text='Failed to import numerics_global')
                # flow numerics
                if configuration == "OGS_FEM":
                    reload(numerics_flow_ogs_fem)
                elif configuration == "OGS_FEM_SP":
                    reload(numerics_flow_ogs_fem_sp)
                elif configuration == "OGS_FEM_MKL":
                    reload(numerics_flow_ogs_fem_mkl)
                elif configuration == "OGS_FEM_MPI":
                    reload(numerics_flow_ogs_fem_mpi)
                elif configuration == "OGS_FEM_PETSC":
                    reload(numerics_flow_ogs_fem_petsc)
                else:
                    message(mode='ERROR', text='Failed to import numeric.flow')
                # mass numerics - imports always
                if configuration == "OGS_FEM":
                    reload(numerics_mass_ogs_fem)
                elif configuration == "OGS_FEM_SP":
                    reload(numerics_mass_ogs_fem_sp)
                elif configuration == "OGS_FEM_MKL":
                    reload(numerics_mass_ogs_fem_mkl)
                elif configuration == "OGS_FEM_MPI":
                    reload(numerics_mass_ogs_fem_mpi)
                elif configuration == "OGS_FEM_PETSC":
                    reload(numerics_mass_ogs_fem_petsc)
                else:
                    message(mode='ERROR', text='Failed to import numerics_mass')
                # heat numerics - imports always
                if configuration == "OGS_FEM":
                    reload(numerics_heat_ogs_fem)
                elif configuration == "OGS_FEM_SP":
                    reload(numerics_heat_ogs_fem_sp)
                elif configuration == "OGS_FEM_MKL":
                    reload(numerics_heat_ogs_fem_mkl)
                elif configuration == "OGS_FEM_MPI":
                    reload(numerics_heat_ogs_fem_mpi)
                elif configuration == "OGS_FEM_PETSC":
                    reload(numerics_heat_ogs_fem_petsc)
                else:
                    message(mode='ERROR', text='Failed to import numerics_heat')
        except Exception as e:
            message(mode='ERROR', text="*****")

    def import_processing_data_files(self, configuration):
        """
        import files with mySQL data on remote computer
        :param configuration:
        :return:
        """
        try:
            if configuration == "OGS_FEM":
                reload(prc_ogs_fem)
            elif configuration == "OGS_FEM_SP":
                reload(prc_ogs_fem_sp)
            elif configuration == "OGS_FEM_MKL":
                reload(prc_ogs_fem_mkl)
            elif configuration == "OGS_FEM_MPI":
                reload(prc_ogs_fem_mpi)
            elif configuration == "OGS_FEM_PETSC":
                reload(prc_ogs_fem_petsc)
            else:
                message(mode='ERROR', text='Failed to import prc')
        except Exception as e:
            message(mode='ERROR', text="*****")

    def get_num_data_from_modules(self, configuration):
        """
        put numerics data from module into SimData
        :param configuration:
        :return:
        """
        if configuration == "OGS_FEM":
            self.get_num_data_from_modules_ogs_fem()
        elif configuration == "OGS_FEM_SP":
            self.get_num_data_from_modules_ogs_fem_sp()
        elif configuration == "OGS_FEM_MKL":
            self.get_num_data_from_modules_ogs_fem_mkl()
        elif configuration == "OGS_FEM_MPI":
            self.get_num_data_from_modules_ogs_fem_mpi()
        elif configuration == "OGS_FEM_PETSC":
            self.get_num_data_from_modules_ogs_fem_petsc()

    def get_num_data_from_modules_ogs_fem(self):
        """

        :return:
        """
        glob_num = Global()
        prcs = Processes()

        preconditioner = list()
        solver = list()
        theta = list()

        prcs.set(numerics_global_ogs_fem.flowProcess,
                 numerics_global_ogs_fem.massFlag, numerics_global_ogs_fem.heatFlag)
        glob_num.set(prcs, numerics_global_ogs_fem.coupled_flag,
                     numerics_global_ogs_fem.lumping_flag, numerics_global_ogs_fem.non_linear_flag)
        
        theta.append(numerics_flow_ogs_fem.theta)
        solver.append(numerics_flow_ogs_fem.solver)
        preconditioner.append(numerics_flow_ogs_fem.precond)
        
        if numerics_global_ogs_fem.massFlag == '1':
            theta.append(numerics_mass_ogs_fem.theta)
            solver.append(numerics_mass_ogs_fem.solver)
            preconditioner.append(numerics_mass_ogs_fem.precond)

        if numerics_global_ogs_fem.heatFlag == '1':
            theta.append(numerics_heat_ogs_fem.theta)
            solver.append(numerics_heat_ogs_fem.solver)
            preconditioner.append(numerics_heat_ogs_fem.precond)

        self.set_numerics(glob_num, solver, preconditioner, theta) 

    def get_num_data_from_modules_ogs_fem_sp(self):
        """

        :return:
        """
        glob_num = Global()
        prcs = Processes()

        preconditioner = list()
        solver = list()
        theta = list()

        prcs.set(numerics_global_ogs_fem_sp.flowProcess,
                 numerics_global_ogs_fem_sp.massFlag, numerics_global_ogs_fem_sp.heatFlag)
        glob_num.set(prcs, numerics_global_ogs_fem_sp.coupled_flag,
                    numerics_global_ogs_fem_sp.lumping_flag, numerics_global_ogs_fem_sp.non_linear_flag)
        
        theta.append(numerics_flow_ogs_fem_sp.theta)
        solver.append(numerics_flow_ogs_fem_sp.solver)
        preconditioner.append(numerics_flow_ogs_fem_sp.precond)
        
        if numerics_global_ogs_fem_sp.massFlag == '1':
            theta.append(numerics_mass_ogs_fem_sp.theta)
            solver.append(numerics_mass_ogs_fem_sp.solver)
            preconditioner.append(numerics_mass_ogs_fem_sp.precond)

        if numerics_global_ogs_fem_sp.heatFlag == '1':
            theta.append(numerics_heat_ogs_fem_sp.theta)
            solver.append(numerics_heat_ogs_fem_sp.solver)
            preconditioner.append(numerics_heat_ogs_fem_sp.precond)

        self.set_numerics(glob_num, solver, preconditioner, theta) 

    def get_num_data_from_modules_ogs_fem_mkl(self):
        """

        :return:
        """
        glob_num = Global()
        prcs = Processes()

        preconditioner = list()
        solver = list()
        theta = list()

        prcs.set(numerics_global_ogs_fem_mkl.flowProcess,
                 numerics_global_ogs_fem_mkl.massFlag, numerics_global_ogs_fem_mkl.heatFlag)
        glob_num.set(prcs, numerics_global_ogs_fem_mkl.coupled_flag,
                     numerics_global_ogs_fem_mkl.lumping_flag, numerics_global_ogs_fem_mkl.non_linear_flag)
        
        theta.append(numerics_flow_ogs_fem_mkl.theta)
        solver.append(numerics_flow_ogs_fem_mkl.solver)
        preconditioner.append(numerics_flow_ogs_fem_mkl.precond)
        
        if numerics_global_ogs_fem_mkl.massFlag == '1':
            theta.append(numerics_mass_ogs_fem_mkl.theta)
            solver.append(numerics_mass_ogs_fem_mkl.solver)
            preconditioner.append(numerics_mass_ogs_fem_mkl.precond)

        if numerics_global_ogs_fem_mkl.heatFlag == '1':
            theta.append(numerics_heat_ogs_fem_mkl.theta)
            solver.append(numerics_heat_ogs_fem_mkl.solver)
            preconditioner.append(numerics_heat_ogs_fem_mkl.precond)

        self.set_numerics(glob_num, solver, preconditioner, theta) 

    def get_num_data_from_modules_ogs_fem_mpi(self):
        """

        :return:
        """
        glob_num = Global()
        prcs = Processes()

        preconditioner = list()
        solver = list()
        theta = list()

        prcs.set(numerics_global_ogs_fem_mpi.flowProcess,
                 numerics_global_ogs_fem_mpi.massFlag, numerics_global_ogs_fem_mpi.heatFlag)
        glob_num.set(prcs, numerics_global_ogs_fem_mpi.coupled_flag,
                     numerics_global_ogs_fem_mpi.lumping_flag, numerics_global_ogs_fem_mpi.non_linear_flag)
        
        theta.append(numerics_flow_ogs_fem_mpi.theta)
        solver.append(numerics_flow_ogs_fem_mpi.solver)
        preconditioner.append(numerics_flow_ogs_fem_mpi.precond)
        
        if numerics_global_ogs_fem_mpi.massFlag == '1':
            theta.append(numerics_mass_ogs_fem_mpi.theta)
            solver.append(numerics_mass_ogs_fem_mpi.solver)
            preconditioner.append(numerics_mass_ogs_fem_mpi.precond)

        if numerics_global_ogs_fem_mpi.heatFlag == '1':
            theta.append(numerics_heat_ogs_fem_mpi.theta)
            solver.append(numerics_heat_ogs_fem_mpi.solver)
            preconditioner.append(numerics_heat_ogs_fem_mpi.precond)

        self.set_numerics(glob_num, solver, preconditioner, theta) 

    def get_num_data_from_modules_ogs_fem_petsc(self):
        """

        :return:
        """
        glob_num = Global()
        prcs = Processes()

        preconditioner = list()
        solver = list()
        theta = list()

        prcs.set(numerics_global_ogs_fem_petsc.flowProcess,
                 numerics_global_ogs_fem_petsc.massFlag, numerics_global_ogs_fem_petsc.heatFlag)
        glob_num.set(prcs, numerics_global_ogs_fem_petsc.coupled_flag,
                     numerics_global_ogs_fem_petsc.lumping_flag, numerics_global_ogs_fem_petsc.non_linear_flag)
        
        theta.append(numerics_flow_ogs_fem_petsc.theta)
        solver.append(numerics_flow_ogs_fem_petsc.solver)
        preconditioner.append(numerics_flow_ogs_fem_petsc.precond)
        
        if numerics_global_ogs_fem_petsc.massFlag == '1':
            theta.append(numerics_mass_ogs_fem_petsc.theta)
            solver.append(numerics_mass_ogs_fem_petsc.solver)
            preconditioner.append(numerics_mass_ogs_fem_petsc.precond)

        if numerics_global_ogs_fem_petsc.heatFlag == '1':
            theta.append(numerics_heat_ogs_fem_petsc.theta)
            solver.append(numerics_heat_ogs_fem_petsc.solver)
            preconditioner.append(numerics_heat_ogs_fem_petsc.precond)

        self.set_numerics(glob_num, solver, preconditioner, theta)

    def get_processing_data_from_module(self, configuration):
        """
        put processing data (parallel, ...) from module into SimData
        :param configuration:
        :return:
        """
        if configuration == "OGS_FEM":
            self.get_processing_data_from_module_ogs_fem()
        elif configuration == "OGS_FEM_SP":
            self.get_processing_data_from_module_ogs_fem_sp()
        elif configuration == "OGS_FEM_MKL":
            self.get_processing_data_from_module_ogs_fem_mkl()
        elif configuration == "OGS_FEM_MPI":
            self.get_processing_data_from_module_ogs_fem_mpi()
        elif configuration == "OGS_FEM_PETSC":
            self.get_processing_data_from_module_ogs_fem_petsc()

    def get_processing_data_from_module_ogs_fem(self):
        """

        :return:
        """
        proc = Processing()
        proc.set(prc_ogs_fem.numberOfCPUs, prc_ogs_fem.mode)
        self.set_processing(proc)

    def get_processing_data_from_module_ogs_fem_sp(self):
        """

        :return:
        """
        proc = Processing()
        proc.set(prc_ogs_fem_sp.numberOfCPUs, prc_ogs_fem_sp.mode)
        self.set_processing(proc)

    def get_processing_data_from_module_ogs_fem_mkl(self):
        """

        :return:
        """
        proc = Processing()
        proc.set(prc_ogs_fem_mkl.numberOfCPUs, prc_ogs_fem_mkl.mode)
        self.set_processing(proc)

    def get_processing_data_from_module_ogs_fem_mpi(self):
        """

        :return:
        """
        proc = Processing()
        proc.set(prc_ogs_fem_mpi.numberOfCPUs, prc_ogs_fem_mpi.mode)
        self.set_processing(proc)

    def get_processing_data_from_module_ogs_fem_petsc(self):
        """

        :return:
        """
        proc = Processing()
        proc.set(prc_ogs_fem_petsc.numberOfCPUs, prc_ogs_fem_petsc.mode)
        self.set_processing(proc)

    def set_processing(self, processing):
        """
        store the parallelization data from mySQL
        :param processing:
        :return:
        """
        self.__processing = processing

    def set_numerics(self, numerics, solver, preconditioner, theta):
        """
        store the numerics data from mySQL
        """
        self.__numerics = numerics
        self.__solver = solver
        self.__preconditioner = preconditioner
        self.__theta = theta

    def write_processing_data(self, configuration):
        """
        calls member function write_data_file to
        write parallelization data into a file
        which can be transfered to remote computer
        :param configuration:
        :return:
        """
        self.write_data_file('prc_' + configuration + '.py', 0, 0, 0)

    def write_numerics_data(self, configuration):
        """
        calls member function write_data_file to
        write files with numerics data (flow, mass, heat separately)
        which can be transfered to remote computer
        item always sim containing type, case configuration
        :param configuration:
        :return:
        """
        self.write_data_file('numerics_global_' + configuration + '.py', 0, 0, 0)

        i = 0
        for process in self.__processes:  # loop over flow, mass, heat
            self.write_data_file('numerics_' + process + '_' + configuration + '.py',
                                 self.__solver[i], self.__preconditioner[i], self.__theta[i])
            i += 1

    def write_num(self, directory):
        """
        Reads global numerics and parallelization data from files and writes *.num file for simulation
        :param directory:
        :return:
        """
        try:
            file_stream = open(directory + examplesName + '.num', 'w')
        except OSError as err:
            message(mode='ERROR', text='OS error: {0}'.format(err))
        else:
            if self.__numerics.coupled_flag == '1':
                file_stream.write('\n$OVERALL_COUPLING\n')
                file_stream.write(' ' + coupling_iterations_min + ' ' + coupling_iterations_max + '\n')

            self.write_process_into_numerics_file(file_stream, 0)  # flow
            if self.__numerics.prcs.mass_flag == '1':
                self.write_process_into_numerics_file(file_stream, 1)
            if self.__numerics.prcs.heat_flag == '1':
                self.write_process_into_numerics_file(file_stream, 2)
            file_stream.write('\n#STOP\n')
            file_stream.close()

    def write_process_into_numerics_file(self, file_stream, process_id):
        """
        called by write_num for each process
        reads numerics data file and writes num data for a selected process into file
        :param file_stream:
        :param process_id:
        :return:
        """
        file_stream.write('\n#NUMERICS\n')
        #  PCS
        file_stream.write(' $PCS_TYPE\n')
        if process_id == 0:
            file_stream.write('  ' + self.__numerics.prcs.flow + '\n')
        elif process_id == 1:
            file_stream.write('  MASS_TRANSPORT\n')
        elif process_id == 2:
            file_stream.write('  HEAT_TRANSPORT\n')
        # LUMPING
        if self.__numerics.lumping_flag == '1' and process_id == 0:   # only flow gets lumped
            file_stream.write(' $ELE_MASS_LUMPING\n')
            file_stream.write('  1\n')
        # LINEAR SOLVER
            file_stream.write(' $LINEAR_SOLVER\n')
        if self.__processing.mode == 'mpi_nodes':
            file_stream.write('; method precond error_tolerance max_iterations theta\n')
            file_stream.write('  petsc ' + self.__solver[process_id] + '  ' + self.__preconditioner[process_id] +
                              '  ' + tollerance_linear + '  ' + maxIterations_linear + ' 1. \n')
        elif self.__processing.mode == 'omp':  # matrix storage is 4
            file_stream.write('; method norm error_tolerance max_iterations theta precond storage\n')
            file_stream.write(self.__solver[process_id] + '  ' + norm + ' ' + tollerance_linear + '  ' +
                              maxIterations_linear + '  ' + self.__theta[process_id] + '   ' +
                              self.__preconditioner[process_id] + ' 4\n')
        elif self.__processing.mode == 'sequential' or self.__processing.mode == 'mpi_elements':
            file_stream.write('; method norm error_tolerance max_iterations theta precond storage\n')
            file_stream.write('  ' + self.__solver[process_id] + '  ' + norm + '  ' + tollerance_linear + '  ' +
                              maxIterations_linear + '  ' + self.__theta[process_id] + '  ' +
                              self.__preconditioner[process_id] + '  ' + '2' + '\n')
        else:
            message(mode='ERROR', text='Mode ' + self.__processing.mode + ' not supported')
        # NONLINEAR SOLVER
        if self.__numerics.non_linear_flag == '1':
            file_stream.write(' $NON_LINEAR_ITERATIONS\n')
            file_stream.write(';type -- error_method -- max_iterations -- relaxation -- tolerance(s)\n')
            file_stream.write('  PICARD LMAX ' + maxIterations_nonlinear + ' 0.0 ' + tollerance_nonlinear + '\n')
        # NUMBER OF GAUSS POINTS
        file_stream.write(' $ELE_GAUSS_POINTS\n')
        file_stream.write('  ' + numberOfGaussPoints + '\n')
        # COUPLING
        if self.__numerics.coupled_flag == '1':
            file_stream.write('$COUPLING_CONTROL\n')
            file_stream.write(' LMAX ' + tollerance_nonlinear + '\n')
      
    def write_data_file(self, file_name, solver, precond, theta):
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
            file_stream = open(rootDirectory + '\\testingEnvironment\\scripts\\icbc\\temp\\' + file_name, 'w')
        except OSError as err:
            message(mode='ERROR', text='OS error: {0}'.format(err))
        else:
            message(mode='INFO', text='Writing ' + location + ' ' + file_name)
            if file_name.find('numerics_global') > -1:
                # file_stream.write('coupling_iterations_min = \'' + coupling_iterations_min + '\' \n')
                # file_stream.write('coupling_iterations_max = \'' + coupling_iterations_max + '\' \n')
                file_stream.write('flowProcess = \'' + self.__numerics.prcs.flow + '\' \n')
                file_stream.write('massFlag = \'' + self.__numerics.prcs.mass_flag + '\' \n')
                file_stream.write('heatFlag = \'' + self.__numerics.prcs.heat_flag + '\' \n\n')
                file_stream.write('coupled_flag = \'' + self.__numerics.coupled_flag + '\' \n')
                file_stream.write('lumping_flag = \'' + self.__numerics.lumping_flag + '\' \n')
                file_stream.write('non_linear_flag = \'' + self.__numerics.non_linear_flag + '\' \n')
            elif file_name.find('prc') > -1:
                file_stream.write('numberOfCPUs = \'' + self.__processing.number_cpus + '\' \n')
                file_stream.write('mode = \'' + self.__processing.mode + '\' \n')
            else:
                # file_stream.write('maxIterations_linear = \'' + maxIterations_linear + '\' \n')
                # file_stream.write('maxIterations_nonlinear = \'' + maxIterations_nonlinear + '\' \n')
                # file_stream.write('norm = \'' + norm + '\' \n')
                # file_stream.write('tollerance_linear = \'' + tollerance_linear + '\' \n')
                # file_stream.write('tollerance_nonlinear = \'' + tollerance_nonlinear + '\' \n')
                file_stream.write('solver = \'' + str(solver) + '\' \n')
                file_stream.write('precond = \'' + str(precond) + '\'\n')
                # file_stream.write('matrixStorage = \'sparse\'\n')
                # file_stream.write('numberOfGaussPoints = \'' + numberOfGaussPoints + '\'\n')
                file_stream.write('theta = \'' + str(theta) + '\'\n')

            file_stream.close()
    
    def write_pbs(self, directory, executable, item_type):
        """
        reloads prc.py to get parallelization data and writes *.pbs file
        :param directory:
        :param executable:
        :param item_type:
        :return:
        """
        # config
        omp_threads = None
        if self.__processing.mode == 'sequential':
            ncpus = '1'
            command = ' '
            place = 'group=host'
        elif self.__processing.mode == 'omp':
            ncpus = self.__processing.number_cpus
            omp_threads = self.__processing.number_cpus
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
            file_stream = open(directory + 'run.pbs', 'w')
        except OSError as err:
            message(mode='ERROR', text='OS error: {0}'.format(err))
        else:
            file_stream.write('#!/bin/bash\n')
            file_stream.write('#PBS -o ' + directory + 'screenout.txt\n')
            file_stream.write('#PBS -j oe\n')
            file_stream.write('#PBS -r n\n')
            file_stream.write('#PBS -l walltime=' + walltime + '\n')
            file_stream.write('#PBS -l select=1:ncpus=' + ncpus)
            if omp_threads:
                file_stream.writelines(':ompthreads=' + ncpus)
            file_stream.write(':mem=3gb\n')
            file_stream.write('#PBS -l place=' + place + '\n')
            file_stream.write('#PBS -q ' + queue + '\n')
            file_stream.write('#PBS -N ' + item_type + '\n')
            file_stream.write('\n')
            file_stream.write('cd $PBS_O_WORKDIR\n')
            file_stream.write('\n')
            file_stream.write('. /usr/share/Modules/init/bash\n')
            file_stream.write('\n')
            file_stream.write(setCompilerVariables)
            file_stream.write(setMklVariables)
            file_stream.write(setMpiVariables)
            file_stream.write('\n')
            file_stream.write('time ' + command + executable + ' ' + directory + examplesName + '\n')
            file_stream.write('\n')
            file_stream.write('qstat -f $PBS_JOBID\n')
            file_stream.write('exit\n')
            file_stream.close()

    def partition_mesh(self, directory):
        """
        reloads prc.py to get parallelization data and writes *.pbs file
        :param directory:
        :return:
        """
        script_partition = rootDirectory + adapt_path('testingEnvironment\\scripts\\') + 'partition.sh'

        chdir(directory)
        mesh_file = directory + examplesName + '.msh'
        if path.isfile(mesh_file):
            try:
                if self.__processing.mode == 'mpi_elements':  # for OGS_FEM_MPI, ...
                    Popen(script_partition + ' ' + self.__processing.number_cpus + ' -e -asci ' + directory, shell=True)
                if self.__processing.mode == 'mpi_nodes':    # for OGS_FEM_PETSC
                    Popen(script_partition + ' ' +
                          self.__processing.number_cpus + ' -n -binary ' + directory, shell=True)
            except Exception as e:
                message(mode='ERROR', text="*****")
        else:
            message(mode='ERROR', text='Mesh file missing')
