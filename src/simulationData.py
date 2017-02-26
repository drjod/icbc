from os import path, getpid
from configuration import walltime, queue
from configuration import setCompilerVariables, setMklVariables, setMpiVariables
from configuration import examplesName, norm, coupling_iterations_min, coupling_iterations_max
from configuration import tollerance_linear, tollerance_nonlinear, numberOfGaussPoints
from configuration import maxIterations_linear, maxIterations_nonlinear, configuration_set
from shared import message
from numerics import Global, Processes
from processing import Processing


class ReadFileFlags:
    """
    control data file up- and reloads dependend on selected operation
    numerics and parallelization data Files are reloaded if the corresponding flag is set True
    """
    def __init__(self, operation):
        self.__numerics = True if operation == 'n' else False  # write num
        self.__processing = True if operation == 'n' or operation == 'b' or operation == 'm' \
            else False  # true if write num, write batch script, mesh partition

    @property
    def numerics(self):
        return self.__numerics

    @property
    def processing(self):
        return self.__processing


class SimulationData:
    """
    contains the numerics data from mySQL database
    interface to write numerics (*.num) and batsch script (run) files
    """
    # numerics data that depend on process - process order in list is flow, mass, heat
    # dirs of form {'flow': (string), 'mass': (string), 'heat': (string),
    #               'deformation': (string), 'fluid_momentum': (string), 'overland': (string)}
    __solver_dir = dir()  # solver specification
    __preconditioner_dir = dir()  # 0 no preconditioner, 1 Jacobi, 100 ILU - each process one list item
    __theta_dir = dir()  # 1 implicit, 0, explicit - each process one list item

    __numerics_global = None  # (class numerics.Global) all numerics data
    __processing = None  # (class processing.Processing) data for parallel runs

    def __init__(self, operation):
        self.__solver_dir = {'flow': None, 'mass': None, 'heat': None,
                             'deformation': None, 'fluid_momentum': None, 'overland': None}
        self.__preconditioner_dir = {'flow': None, 'mass': None, 'heat': None,
                             'deformation': None, 'fluid_momentum': None, 'overland': None}
        self.__theta_dir = {'flow': None, 'mass': None, 'heat': None,
                             'deformation': None, 'fluid_momentum': None, 'overland': None}
        self.__numerics_global = Global()
        self.__processing = Processing()
        self.__read_file_flags = ReadFileFlags(operation)

    def __del__(self):
        del self.__solver_dir
        del self.__preconditioner_dir
        del self.__theta_dir
        del self.__numerics_global
        del self.__processing

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

    @property
    def read_file_flags(self):
        return self.__read_file_flags

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

    def write_num(self, directory):
        """
        Reads global numerics and parallelization data from files and writes *.num file for simulation
        *.num file is marked with process id, if ist is made for remote computer (i.e. stored in /tmp folder)
        :param directory:
        :return:
        """
        mark = getpid() if directory == '/tmp' else ''
        try:
            file_stream = open(path.join(directory, '{}.num{}'.format(examplesName, mark)), 'w')
        except OSError as err:
            message(mode='ERROR', text='OS error: {0}'.format(err))
        else:
            if self.__numerics_global.coupled_flag:
                file_stream.write('\n$OVERALL_COUPLING\n')
                file_stream.write(' {} {}\n'.format(coupling_iterations_min, coupling_iterations_max))

            self.write_process_into_numerics_file(file_stream, 'flow')
            if self.__numerics_global.processes.mass_flag:
                self.write_process_into_numerics_file(file_stream, 'mass')
            if self.__numerics_global.processes.heat_flag:
                self.write_process_into_numerics_file(file_stream, 'heat')
            if self.__numerics_global.processes.deformation_flag:
                self.write_process_into_numerics_file(file_stream, 'deformation')
            if self.__numerics_global.processes.fluid_momentum_flag:
                self.write_process_into_numerics_file(file_stream, 'fluid_momentum')
            if self.__numerics_global.processes.overland_flag:
                self.write_process_into_numerics_file(file_stream, 'overland')
            file_stream.write('\n#STOP\n')
            file_stream.close()

    def write_process_into_numerics_file(self, file_stream, process):
        """
        write num data for a selected process into file
        called by write_num for each process
        uses member variables and global variables from file configuration
        hard coded are:
            matrix storage, relaxation in nonlinear iterations, tolerances for nolinear iterations in process overland
        :param file_stream: (file)
        :param process: (string) ['flow', 'mass', 'heat']
        :return:
        """
        file_stream.write('\n#NUMERICS\n')
        #  PCS
        file_stream.write(' $PCS_TYPE\n')
        if process == 'flow':
            file_stream.write('  {}\n'.format(self.__numerics_global.processes.flow))
        elif process == 'mass':
            file_stream.write('  MASS_TRANSPORT\n')
        elif process == 'heat':
            file_stream.write('  HEAT_TRANSPORT\n')
        elif process == 'deformation':
            file_stream.write('  DEFORMATION\n')
        elif process == 'fluid_momentum':
            file_stream.write('  FLUID_MOMENTUM\n')
        elif process == 'overland':
            file_stream.write('  OVERLAND_FLOW\n')
        else:
            message(mode='ERROR', text='Process {} not supported'.format(process))
        # LUMPING
        if self.__numerics_global.lumping_flag and process == 'flow':  # only flow gets lumped
            file_stream.write(' $ELE_MASS_LUMPING\n')
            file_stream.write('  1\n')
        # LINEAR SOLVER
            file_stream.write(' $LINEAR_SOLVER\n')
        if self.__processing.mode == 'mpi_nodes':
            file_stream.write('; method precond error_tolerance max_iterations theta\n')
            file_stream.write('  petsc {}  {}  {}  {} 1.\n'.format(self.__solver_dir[process],
                                                                   self.__preconditioner_dir[process],
                                                                   tollerance_linear, maxIterations_linear))
        elif self.__processing.mode == 'omp':  # matrix storage is 4
            file_stream.write('; method norm error_tolerance max_iterations theta precond storage\n')
            file_stream.write('{} {} {} {} {} {} 4\n'.format(
                self.__solver_dir[process], norm, tollerance_linear, maxIterations_linear,
                self.__theta_dir[process], self.__preconditioner_dir[process]))
        elif self.__processing.mode == 'sequential' or self.__processing.mode == 'mpi_elements':
            file_stream.write('; method norm error_tolerance max_iterations theta precond storage\n')
            file_stream.write('  {} {} {} {} {} {} 2\n'.format(
                self.__solver_dir[process], norm, tollerance_linear, maxIterations_linear,
                self.__theta_dir[process], self.__preconditioner_dir[process]))
        else:
            message(mode='ERROR', text='Mode ' + self.__processing.mode + ' not supported')
        # NONLINEAR SOLVER
        if self.__numerics_global.non_linear_flag:
            file_stream.write(' $NON_LINEAR_ITERATIONS\n')
            if process == 'overland':
                file_stream.write(';type -- error_method -- max_iterations -- relaxation -- tolerance(s)\n')
                file_stream.write('  PICARD LMAX {} 0.0 {}\n'.format(maxIterations_nonlinear, tollerance_nonlinear))
            else:
                file_stream.write('; NEWTON error_tolerance nls_error_tolerance_local  max_iterations  relaxation\n')
                file_stream.write('  NEWTON 1.e-5 1.e-8 {} 0.0\n'.format(maxIterations_nonlinear))
        # NUMBER OF GAUSS POINTS
        file_stream.write(' $ELE_GAUSS_POINTS\n')
        file_stream.write('  {}\n'.format(numberOfGaussPoints))
        # COUPLING
        if self.__numerics_global.coupled_flag:
            file_stream.write('$COUPLING_CONTROL\n')
            file_stream.write(' LMAX {}\n'.format(tollerance_nonlinear))

    def write_batch(self, directory, executable, item_type):
        """
        writes batch file 'run' and marks it with pid for upload
        :param directory: (string)
        :param executable: (string)
        :param item_type: (string)
        :return:
        """
        # config
        omp_threads = None
        if self.__processing.mode == 'sequential':
            nr_cpus = 1
            nr_omp_threads = 1
        elif self.__processing.mode == 'omp':
            nr_cpus = self.__processing.number_cpus
            nr_omp_threads = self.__processing.number_cpus
        elif self.__processing.mode == 'mpi_elements' or self.__processing.mode == 'mpi_nodes':  # parallel
            nr_cpus = self.__processing.number_cpus
            nr_omp_threads = 1
        else:
            message(mode='ERROR', not_supported='Mode {}'.format(self.__processing.mode))
            return
        # write
        try:
            file_stream = open(path.join('/tmp', 'run{}'.format(getpid())), 'w')
        except OSError as err:
            message(mode='ERROR', text='OS error: {}'.format(err))
        else:
            file_stream.write('#!/bin/bash\n')
            file_stream.write('#SBATCH --job-name={}\n'.format(item_type))
            file_stream.write('#SBATCH --output={}\n'.format(path.join(directory, 'out.txt')))
            file_stream.write('#SBATCH --error={}\n'.format(path.join(directory, 'error.txt')))
            file_stream.write('#SBATCH --nodes=1\n')
            file_stream.write('#SBATCH --tasks-per-node={}\n'.format(nr_cpus))
            file_stream.write('#SBATCH --cpus-per-task={}\n'.format(nr_omp_threads))
            file_stream.write('#SBATCH --mem=3G\n')
            file_stream.write('#SBATCH --time={}\n'.format(walltime))
            file_stream.write('#SBATCH --partition={}\n'.format(queue))
            file_stream.write('\n')

            file_stream.writelines('export OMP_NUM_THREADS={}\n'.format(nr_omp_threads))
            file_stream.write('module load intel1502\n')
            if self.__processing.mode == 'mpi_elements':
                file_stream.write('module load intelmpi1502\n')
                file_stream.write('mpirun -np {} '.format(nr_cpus))
            if self.__processing.mode == 'mpi_nodes':
                file_stream.write('module load intelmpi1502\n')
                file_stream.write('module load petsc-3.5.3-intel1502\n')
                file_stream.write('mpirun -np {} '.format(nr_cpus))
            file_stream.write('{} {}\n'.format(executable, path.join(directory, examplesName)))

    def partition_mesh(self, simulating):
        """
        mesh partition
        :param directory: (string)
        :return:
        """
        item_directory = simulating._item.directory
        root_directory = simulating._subject.root_directory

        script_partition = path.join(root_directory, 'testingEnvironment', 'scripts', 'partition.sh')

        try:
            if self.__processing.mode == 'mpi_elements':  # for OGS_FEM_MPI, ...
                simulating.execute_python(
                    'call', 'None {} {} -e -asci {}'.format(  # None for no output file in commands call
                        script_partition, self.__processing.number_cpus, item_directory))
            if self.__processing.mode == 'mpi_nodes':  # for OGS_FEM_PETSC
                simulating.execute_python(
                    'call', 'None {} {} -n -binary {}'.format(  # None for no output file in commands call
                        script_partition, self.__processing.number_cpus, item_directory))
        except Exception as err:
            message(mode='ERROR', text="{}".format(err))

