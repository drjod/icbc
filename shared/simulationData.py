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
            if operation == 'n' or operation == 'b' or operation == 'm':  # write num, write pbs, mesh partition
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
    # dirs of form {'flow': (string), 'mass': (string), 'heat': (string),
    #               'deformation': (string), 'fluid_momentum': (string), 'overland': (string)}
    __solver_dir = dir()  # solver specification
    __preconditioner_dir = dir()  # 0 no preconditioner, 1 Jacobi, 100 ILU - each process one list item
    __theta_dir = dir()  # 1 implicit, 0, explicit - each process one list item

    __numerics_global = None  # (class numerics.Global) all numerics data
    __processing = None  # (class processing.Processing) data for parallel runs

    __read_file_flags = None  # (class ReadFileFlags)

    def __init__(self, operation_type=None, operation=None):
        self.__solver_dir = {'flow': None, 'mass': None, 'heat': None,
                             'deformation': None, 'fluid_momentum': None, 'overland': None}
        self.__preconditioner_dir = {'flow': None, 'mass': None, 'heat': None,
                             'deformation': None, 'fluid_momentum': None, 'overland': None}
        self.__theta_dir = {'flow': None, 'mass': None, 'heat': None,
                             'deformation': None, 'fluid_momentum': None, 'overland': None}
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

    def get_num_data_for_process(self, process_name, id_local_process, directory_temp):
        module = __import__('numerics_{}_{}'.format(process_name, id_local_process))
        if process_name == 'global':
            self.__numerics_global.coupled_flag = str2bool(module.coupled_flag)
            self.__numerics_global.lumping_flag = str2bool(module.lumping_flag)
            self.__numerics_global.non_linear_flag = str2bool(module.non_linear_flag)

            self.__numerics_global.processes.flow = module.flow_process
            self.__numerics_global.processes.mass_flag = str2bool(module.mass_flag)
            self.__numerics_global.processes.heat_flag = str2bool(module.heat_flag)
            self.__numerics_global.processes.deformation_flag = str2bool(module.deformation_flag)
            self.__numerics_global.processes.fluid_momentum_flag = str2bool(module.fluid_momentum_flag)
            self.__numerics_global.processes.overland_flag = str2bool(module.overland_flag)
            print('def: '+str(self.__numerics_global.processes.deformation_flag))
        else:
            self.__solver_dir[process_name] = module.solver
            self.__preconditioner_dir[process_name] = module.precond
            self.__theta_dir[process_name] = module.theta
        remove_file('{}numerics_{}_{}.py'.format(directory_temp, process_name, id_local_process), False)
        try:  # remove byte code if it exists
            remove_file(directory_temp + 'numerics_{}_{}.pyc'.format(process_name, id_local_process), False)
        except:
            pass

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
            directory_temp = adapt_path('{}testingEnvironment\\scripts\icbc\\temp\\'.format(rootDirectory))
            # first global to get process flags
            self.get_num_data_for_process('global', id_local_process, directory_temp)
            # processes
            self.get_num_data_for_process('flow', id_local_process, directory_temp)
            if self.__numerics_global.processes.mass_flag:
                self.get_num_data_for_process('mass', id_local_process, directory_temp)
            if self.__numerics_global.processes.heat_flag:
                self.get_num_data_for_process('heat', id_local_process, directory_temp)
            if self.__numerics_global.processes.deformation_flag:
                self.get_num_data_for_process('deformation', id_local_process, directory_temp)
            if self.__numerics_global.processes.fluid_momentum_flag:
                self.get_num_data_for_process('fluid_momentum', id_local_process, directory_temp)
            if self.__numerics_global.processes.overland_flag:
                self.get_num_data_for_process('overland', id_local_process, directory_temp)
        except Exception as err:
            message(mode='ERROR', text='OS error: {0}'.format(err))

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

            self.__processing.number_cpus = processing.number_cpus
            self.__processing.mode = processing.mode

            directory_temp = adapt_path('testingEnvironment\\scripts\icbc\\temp\\'.format(rootDirectory))
            remove_file(directory_temp + 'processing_{}.py'.format(id_local_process), False)
        except Exception as err:
            message(mode='ERROR', text='OS error: {}'.format(err))

        # remove byte code if it exists
        try:
            remove_file(directory_temp + 'processing_{}.pyc'.format(id_local_process), False)
        except:
            pass

    def write_processing_data_file(self):
        """
        calls member function write_data_file to write parallelization data into a file,
        which will be later uploaded to remote computer
        :return:
        """
        self.write_data_file('processing_{}.py'.format(getpid()), output_flag=False)

    def write_numerics_data_files(self):
        """
        calls member function write_data_file to
        write numeics data global flow, mass, heat, deformation, fluid_momentum, overland in separate files,
        which will be later uploaded to remote computer
        function is run on local computer
        :param configuration:
        :return:
        """
        self.write_data_file('numerics_global_{}.py'.format(getpid()), output_flag=False)
        self.write_data_file('numerics_flow_{}.py'.format(getpid()), 'flow', output_flag=False)
        if self.__numerics_global.processes.mass_flag:
            self.write_data_file('numerics_mass_{}.py'.format(getpid()), 'mass', output_flag=False)
        if self.__numerics_global.processes.heat_flag:
            self.write_data_file('numerics_heat_{}.py'.format(getpid()), 'heat', output_flag=False)
        if self.__numerics_global.processes.deformation_flag:
            self.write_data_file('numerics_deformation_{}.py'.format(getpid()), 'deformation', output_flag=False)
        if self.__numerics_global.processes.fluid_momentum_flag:
            self.write_data_file(
                'numerics_fluid_momentum_{}.py'.format(getpid()), 'fluid_momentum', output_flag=False)
        if self.__numerics_global.processes.overland_flag:
            self.write_data_file('numerics_overland_{}.py'.format(getpid()), 'overland', output_flag=False)

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
        uses member variables and global variables from file configurationShared
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
        file_stream.write('  {}\n'.format(numberOfGaussPoints ))
        # COUPLING
        if self.__numerics_global.coupled_flag:
            file_stream.write('$COUPLING_CONTROL\n')
            file_stream.write(' LMAX {}\n'.format(tollerance_nonlinear))
      
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
                message(mode='INFO', text='Writing {} {}'.format(location, file_name))
            if file_name == 'numerics_global_{}.py'.format(getpid()):
                # file_stream.write('coupling_iterations_min = \'' + coupling_iterations_min + '\' \n')
                # file_stream.write('coupling_iterations_max = \'' + coupling_iterations_max + '\' \n')
                file_stream.write('flow_process = \'{}\' \n'.format(self.__numerics_global.processes.flow))
                file_stream.write('mass_flag = \'{}\' \n'.format(bool2str(self.__numerics_global.processes.mass_flag)))
                file_stream.write('heat_flag = \'{}\' \n'.format(bool2str(self.__numerics_global.processes.heat_flag)))
                file_stream.write('deformation_flag = \'{}\' \n'.format(
                    bool2str(self.__numerics_global.processes.deformation_flag)))
                file_stream.write('fluid_momentum_flag = \'{}\' \n'.format(
                    bool2str(self.__numerics_global.processes.fluid_momentum_flag)))
                file_stream.write('overland_flag = \'{}\' \n\n'.format(
                    bool2str(self.__numerics_global.processes.overland_flag)))
                file_stream.write('coupled_flag = \'{}\' \n'.format(bool2str(self.__numerics_global.coupled_flag)))
                file_stream.write('lumping_flag = \'{}\' \n'.format(bool2str(self.__numerics_global.lumping_flag)))
                file_stream.write('non_linear_flag = \'{}\' \n'.format(
                    bool2str(self.__numerics_global.non_linear_flag)))
            elif file_name == 'processing_{}.py'.format(getpid()):
                file_stream.write('number_cpus = \'{}\' \n'.format(self.__processing.number_cpus))
                file_stream.write('mode = \'{}\' \n'.format(self.__processing.mode))
            elif (file_name == 'numerics_flow_{}.py'.format(getpid()) or
                          file_name == 'numerics_mass_{}.py'.format(getpid()) or
                          file_name == 'numerics_heat_{}.py'.format(getpid()) or
                          file_name == 'numerics_deformation_{}.py'.format(getpid()) or
                          file_name == 'numerics_fluid_momentum_{}.py'.format(getpid()) or
                          file_name == 'numerics_overland_{}.py'.format(getpid())
                  ):
                # file_stream.write('maxIterations_linear = \'' + maxIterations_linear + '\' \n')
                # file_stream.write('maxIterations_nonlinear = \'' + maxIterations_nonlinear + '\' \n')
                # file_stream.write('norm = \'' + norm + '\' \n')
                # file_stream.write('tollerance_linear = \'' + tollerance_linear + '\' \n')
                # file_stream.write('tollerance_nonlinear = \'' + tollerance_nonlinear + '\' \n')
                file_stream.write('solver = \'{}\' \n'.format(self.__solver_dir[process]))
                file_stream.write('precond = \'{}\'\n'.format(self.__preconditioner_dir[process]))
                # file_stream.write('matrixStorage = \'sparse\'\n')
                # file_stream.write('numberOfGaussPoints = \'' + numberOfGaussPoints + '\'\n')
                file_stream.write('theta = \'{}\'\n'.format(self.__theta_dir[process]))
            else:
                message(mode='ERROR', text='Wrong file name {}'.format(file_name))
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
            message(mode='ERROR', not_supported='Mode {}'.format(self.__processing.mode))
            return
        # write
        try:
            file_stream = open('{}run.pbs'.format(directory), 'w')
        except OSError as err:
            message(mode='ERROR', text='OS error: {}'.format(err))
        else:
            file_stream.write('#!/bin/bash\n')
            file_stream.write('#PBS -o {}screenout.txt\n'.format(directory))
            file_stream.write('#PBS -j oe\n')
            file_stream.write('#PBS -r n\n')
            file_stream.write('#PBS -l walltime={}\n'.format(walltime))
            file_stream.write('#PBS -l select=1:ncpus={}'.format(ncpus))
            if omp_threads:
                file_stream.writelines(':ompthreads={}'.format(ncpus))
            file_stream.write(':mem=3gb\n')
            file_stream.write('#PBS -l place={}\n'.format(place))
            file_stream.write('#PBS -q {}\n'.format(queue))
            file_stream.write('#PBS -N {}\n'.format(item_type))
            file_stream.write('\n')
            file_stream.write('cd $PBS_O_WORKDIR\n')
            file_stream.write('\n')
            file_stream.write('. /usr/share/Modules/init/bash\n')
            file_stream.write('\n')
            file_stream.write(setCompilerVariables)
            file_stream.write(setMklVariables)
            file_stream.write(setMpiVariables)
            file_stream.write('\n')
            file_stream.write('time {}{} {}{}\n'.format(command, executable, directory, examplesName))
            file_stream.write('\n')
            file_stream.write('qstat -f $PBS_JOBID\n')
            file_stream.write('exit\n')
            file_stream.close()

    def partition_mesh(self, directory):
        """
        reloads prc.py to get parallelization data and writes *.pbs file
        :param directory: (string)
        :return:
        """
        script_partition = '{}{}partition.sh'.format(rootDirectory, adapt_path('testingEnvironment\\scripts\\'))

        chdir(directory)
        mesh_file = '{}{}.msh'.format(directory, examplesName)
        if not path.isfile(mesh_file):  # no file *.msh, than look if one remained from previous mesh partitioning
            mesh_file = '{}{}_mesh.txt'.format(directory, examplesName)

        if path.isfile(mesh_file):
            try:
                if self.__processing.mode == 'mpi_elements':  # for OGS_FEM_MPI, ...
                    Popen(script_partition + ' {} -e -asci {}'.format(
                        self.__processing.number_cpus, directory), shell=True)
                if self.__processing.mode == 'mpi_nodes':    # for OGS_FEM_PETSC
                    Popen('{} {} -n -binary {}'.format(
                        script_partition, self.__processing.number_cpus, directory), shell=True)
            except Exception as err:
                message(mode='ERROR', text="{}".format(err))
        else:
            message(mode='ERROR', text='Mesh file missing')
