from sys import path as syspath
from os import path, chdir, getpid
from subprocess import Popen
syspath.append(path.join(path.dirname(__file__), '..', 'customized'))
syspath.append(path.join(path.dirname(__file__), '..', 'temp'))
from configurationCustomized import location, rootDirectory, walltime, queue
from configurationCustomized import setCompilerVariables, setMklVariables, setMpiVariables
from configurationShared import examplesName, norm, coupling_iterations_min, coupling_iterations_max
from configurationShared import tollerance_linear, tollerance_nonlinear, numberOfGaussPoints
from configurationShared import maxIterations_linear, maxIterations_nonlinear, configuration_set
from utilities import message, adapt_path, str2bool, bool2str, remove_file
from numerics import Global, Processes
from processing import Processing


class ReadFileFlags:
    """
    control data file up- and reloads dependend on selected operation
    numerics and parallelization data Files are reloaded if the corresponding flag is set True
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
    # numerics data that depend on process - process order in list is flow, mass, heat
    # dirs of form {'flow' : (string), 'mass' : (string), 'heat' : (string)}
    __solver_dir = dir()  # solver specification
    __preconditioner_dir = dir()  # 0 no preconditioner, 1 Jacobi, 100 ILU - each process one list item
    __theta_dir = dir()  # 1 implicit, 0, explicit - each process one list item

    __numerics_global = None  # (class numerics.Global) all numerics data
    __processing = None  # (class processing.Processing) data for parallel runs

    __read_file_flags = None  # (class ReadFileFlags)

    def __init__(self, operation_type=None, operation=None):
        self.__solver_dir = {'flow': None, 'mass': None, 'heat': None}
        self.__preconditioner_dir = {'flow': None, 'mass': None, 'heat': None}
        self.__theta_dir = {'flow': None, 'mass': None, 'heat': None}
        self.__numerics_global = Global()
        self.__processing = Processing()
        if operation is not None and operation_type is not None:
            self.__read_file_flags = ReadFileFlags(operation_type, operation)

    def __del__(self):
        del self.__solver_dir
        del self.__preconditioner_dir
        del self.__theta_dir
        del self.__numerics_global
        del self.__processing

    @property
    def read_file_flags(self):
        return self.__read_file_flags

    @property
    def processing(self):
        return self.__processing

    @property
    def numerics_global(self):
        return self.__numerics_global

    @property
    def solver_dir(self):
        return self.__solver_dir

    @property
    def preconditioner_dir(self):
        return self.__preconditioner_dir

    @property
    def theta_dir(self):
        return self.__theta_dir

    @processing.setter
    def processing(self, value):
        self.__processing = value

    @numerics_global.setter
    def numerics_global(self, value):
        self.__numerics_global = value

    @solver_dir.setter
    def solver_dir(self, value):
        self.__solver_dir = value

    @preconditioner_dir.setter
    def preconditioner_dir(self, value):
        self.__preconditioner_dir = value

    @theta_dir.setter
    def theta_dir(self, value):
        self.__theta_dir = value

    def get_num_data_from_modules(self, id_local_process):
        """
        get numerics data global, flow, mass, heat
        function is run on remote computer
        module names contain process id from local computer for its identification
        delete modules after data obtained
        restriction:
            modules are not reloaded since only one operation on remote computer
        :return:
        """
        try:
            numerics_global = __import__('numerics_global_' + id_local_process)
            numerics_flow = __import__('numerics_flow_' + id_local_process)
            numerics_mass = __import__('numerics_mass_' + id_local_process)
            numerics_heat = __import__('numerics_heat_' + id_local_process)
            # get data
            self.__numerics_global.processes.flow = numerics_global.flowProcess
            self.__numerics_global.processes.mass_flag = str2bool(numerics_global.massFlag)
            self.__numerics_global.processes.heat_flag = str2bool(numerics_global.heatFlag)

            self.__numerics_global.coupled_flag = str2bool(numerics_global.coupled_flag)
            self.__numerics_global.lumping_flag = str2bool(numerics_global.lumping_flag)
            self.__numerics_global.non_linear_flag = str2bool(numerics_global.non_linear_flag)

            self.__solver_dir['flow'] = numerics_flow.solver
            self.__preconditioner_dir['flow'] = numerics_flow.precond
            self.__theta_dir['flow'] = numerics_flow.theta
            if self.__numerics_global.processes.mass_flag:
                self.__solver_dir['mass'] = numerics_mass.solver
                self.__preconditioner_dir['mass'] = numerics_mass.precond
                self.__theta_dir['mass'] = numerics_mass.theta
            if self.__numerics_global.processes.heat_flag:
                self.__solver_dir['heat'] = numerics_heat.solver
                self.__preconditioner_dir['heat'] = numerics_heat.precond
                self.__theta_dir['heat'] = numerics_heat.theta
            # remove files
            directory_temp = adapt_path(rootDirectory + 'testingEnvironment\\scripts\icbc\\temp\\')
            remove_file(directory_temp + 'numerics_global_' + id_local_process + '.py', False)
            remove_file(directory_temp + 'numerics_flow_' + id_local_process + '.py', False)
            if self.__numerics_global.processes.mass_flag:
                remove_file(directory_temp + 'numerics_mass_' + id_local_process + '.py', False)
            if self.__numerics_global.processes.heat_flag:
                remove_file(directory_temp + 'numerics_heat_' + id_local_process + '.py', False)
        except Exception as err:
            message(mode='ERROR', text='OS error: {0}'.format(err))

        # remove byte code if it exists
        try:
            remove_file(directory_temp + 'numerics_global_' + id_local_process + '.pyc', False)
            remove_file(directory_temp + 'numerics_flow_' + id_local_process + '.pyc', False)
            if self.__numerics_global.processes.mass_flag:
                remove_file(directory_temp + 'numerics_mass_' + id_local_process + '.pyc', False)
            if self.__numerics_global.processes.heat_flag:
                remove_file(directory_temp + 'numerics_heat_' + id_local_process + '.pyc', False)
        except:
            pass



    def get_processing_data_from_module(self, id_local_process):
        """
        get processing (parallelization) data from module
        function is run on remote computer
        module name contain process id from local computer for its identification
        restriction:
            modules are not reloaded since only one operation on remote computer
        :return:
        """
        try:
            processing = __import__('processing_' + id_local_process)

            self.__processing.number_cpus = processing.numberOfCPUs
            self.__processing.mode = processing.mode

            directory_temp = adapt_path(rootDirectory + 'testingEnvironment\\scripts\icbc\\temp\\')
            remove_file(directory_temp + 'processing_' + id_local_process + '.py', False)
        except Exception as err:
            message(mode='ERROR', text='OS error: {0}'.format(err))

        # remove byte code if it exists
        try:
            remove_file(directory_temp + 'processing_' + id_local_process + '.pyc', False)
        except:
            pass

    def write_processing_data_file(self):
        """
        calls member function write_data_file to write parallelization data into a file,
        which will be later uploaded to remote computer
        :return:
        """
        self.write_data_file('processing_' + str(getpid()) + '.py', output_flag=False)

    def write_numerics_data_files(self):
        """
        calls member function write_data_file to
        write numeics data global flow, mass, heat in separate files,
        which will be later uploaded to remote computer
        function is run on local computer
        :param configuration:
        :return:
        """
        self.write_data_file('numerics_global_' + str(getpid()) + '.py', output_flag=False)
        self.write_data_file('numerics_flow_' + str(getpid()) + '.py', 'flow', output_flag=False)
        if self.__numerics_global.processes.mass_flag:
            self.write_data_file('numerics_mass_' + str(getpid()) + '.py', 'mass', output_flag=False)
        if self.__numerics_global.processes.heat_flag:
            self.write_data_file('numerics_heat_' + str(getpid()) + '.py', 'heat', output_flag=False)

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
            if self.__numerics_global.coupled_flag:
                file_stream.write('\n$OVERALL_COUPLING\n')
                file_stream.write(' ' + coupling_iterations_min + ' ' + coupling_iterations_max + '\n')

            self.write_process_into_numerics_file(file_stream, 'flow')
            if self.__numerics_global.processes.mass_flag:
                self.write_process_into_numerics_file(file_stream, 'mass')
            if self.__numerics_global.processes.heat_flag:
                self.write_process_into_numerics_file(file_stream, 'heat')
            file_stream.write('\n#STOP\n')
            file_stream.close()

    def write_process_into_numerics_file(self, file_stream, process):
        """
        write num data for a selected process into file
        called by write_num for each process
        uses member variables and global variables from file configurationShared
        restrictions:
            matrix storage is preset
        :param file_stream: (file)
        :param process: (string) ['flow', 'mass', 'heat']
        :return:
        """
        file_stream.write('\n#NUMERICS\n')
        #  PCS
        file_stream.write(' $PCS_TYPE\n')
        if process == 'flow':
            file_stream.write('  ' + self.__numerics_global.processes.flow + '\n')
        elif process == 'mass':
            file_stream.write('  MASS_TRANSPORT\n')
        elif process == 'heat':
            file_stream.write('  HEAT_TRANSPORT\n')
        # LUMPING
        if self.__numerics_global.lumping_flag and process == 'flow':  # only flow gets lumped
            file_stream.write(' $ELE_MASS_LUMPING\n')
            file_stream.write('  1\n')
        # LINEAR SOLVER
            file_stream.write(' $LINEAR_SOLVER\n')
        if self.__processing.mode == 'mpi_nodes':
            file_stream.write('; method precond error_tolerance max_iterations theta\n')
            file_stream.write('  petsc ' + self.__solver_dir[process] + '  ' +
                              self.__preconditioner_dir[process] + '  ' +
                              tollerance_linear + '  ' + maxIterations_linear + ' 1. \n')
        elif self.__processing.mode == 'omp':  # matrix storage is 4
            file_stream.write('; method norm error_tolerance max_iterations theta precond storage\n')
            file_stream.write(self.__solver_dir[process] + '  ' + norm + ' ' + tollerance_linear + '  ' +
                              maxIterations_linear + '  ' + self.__theta_dir[process] + '   ' +
                              self.__preconditioner_dir[process] + ' 4\n')
        elif self.__processing.mode == 'sequential' or self.__processing.mode == 'mpi_elements':
            file_stream.write('; method norm error_tolerance max_iterations theta precond storage\n')
            file_stream.write('  ' + self.__solver_dir[process] + '  ' + norm + '  ' + tollerance_linear + '  ' +
                              maxIterations_linear + '  ' + self.__theta_dir[process] + '  ' +
                              self.__preconditioner_dir[process] + '  ' + '2' + '\n')
        else:
            message(mode='ERROR', text='Mode ' + self.__processing.mode + ' not supported')
        # NONLINEAR SOLVER
        if self.__numerics_global.non_linear_flag:
            file_stream.write(' $NON_LINEAR_ITERATIONS\n')
            file_stream.write(';type -- error_method -- max_iterations -- relaxation -- tolerance(s)\n')
            file_stream.write('  PICARD LMAX ' + maxIterations_nonlinear + ' 0.0 ' + tollerance_nonlinear + '\n')
        # NUMBER OF GAUSS POINTS
        file_stream.write(' $ELE_GAUSS_POINTS\n')
        file_stream.write('  ' + numberOfGaussPoints + '\n')
        # COUPLING
        if self.__numerics_global.coupled_flag:
            file_stream.write('$COUPLING_CONTROL\n')
            file_stream.write(' LMAX ' + tollerance_nonlinear + '\n')
      
    def write_data_file(self, file_name, process='global', output_flag=True):
        """
        called by member function writeData
        to write numerics or parallelization data into a file
        :param file_name: (string)
        :param process: (string) used for solver, preconditioner, theta lists with flow, mass heat process
        :param output_flag: (bool)
        :return:
        """
        try:
            file_stream = open(rootDirectory + '\\testingEnvironment\\scripts\\icbc\\temp\\' + file_name, 'w')
        except OSError as err:
            message(mode='ERROR', text='OS error: {0}'.format(err))
        else:
            if output_flag:
                message(mode='INFO', text='Writing ' + location + ' ' + file_name)
            if file_name == 'numerics_global_' + str(getpid()) + '.py':
                # file_stream.write('coupling_iterations_min = \'' + coupling_iterations_min + '\' \n')
                # file_stream.write('coupling_iterations_max = \'' + coupling_iterations_max + '\' \n')
                file_stream.write('flowProcess = \'' + self.__numerics_global.processes.flow + '\' \n')
                file_stream.write('massFlag = \'' + bool2str(self.__numerics_global.processes.mass_flag) + '\' \n')
                file_stream.write('heatFlag = \'' + bool2str(self.__numerics_global.processes.heat_flag) + '\' \n\n')
                file_stream.write('coupled_flag = \'' + bool2str(self.__numerics_global.coupled_flag) + '\' \n')
                file_stream.write('lumping_flag = \'' + bool2str(self.__numerics_global.lumping_flag) + '\' \n')
                file_stream.write('non_linear_flag = \'' + bool2str(self.__numerics_global.non_linear_flag) + '\' \n')
            elif file_name == 'processing_' + str(getpid()) + '.py':
                file_stream.write('numberOfCPUs = \'' + self.__processing.number_cpus + '\' \n')
                file_stream.write('mode = \'' + self.__processing.mode + '\' \n')
            elif (file_name == 'numerics_flow_' + str(getpid()) + '.py' or
                          file_name == 'numerics_mass_' + str(getpid()) + '.py' or
                          file_name == 'numerics_heat_' + str(getpid()) + '.py'):
                # file_stream.write('maxIterations_linear = \'' + maxIterations_linear + '\' \n')
                # file_stream.write('maxIterations_nonlinear = \'' + maxIterations_nonlinear + '\' \n')
                # file_stream.write('norm = \'' + norm + '\' \n')
                # file_stream.write('tollerance_linear = \'' + tollerance_linear + '\' \n')
                # file_stream.write('tollerance_nonlinear = \'' + tollerance_nonlinear + '\' \n')
                file_stream.write('solver = \'' + self.__solver_dir[process] + '\' \n')
                file_stream.write('precond = \'' + self.__preconditioner_dir[process] + '\'\n')
                # file_stream.write('matrixStorage = \'sparse\'\n')
                # file_stream.write('numberOfGaussPoints = \'' + numberOfGaussPoints + '\'\n')
                file_stream.write('theta = \'' + self.__theta_dir[process] + '\'\n')
            else:
                message(mode='ERROR', text='Wrong file name ' + file_name)
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
            except Exception as err:
                message(mode='ERROR', text="{0}".format(err))
        else:
            message(mode='ERROR', text='Mesh file missing')
