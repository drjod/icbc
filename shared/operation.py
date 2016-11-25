from sys import stdout, path as syspath
from os import path, listdir, chdir
from platform import system
from subprocess import Popen, call
from glob import glob
from time import time
syspath.append(path.join(path.dirname(__file__), '..', 'customized'))
syspath.append(path.join(path.dirname(__file__), '..', 'pwds'))
from configurationCustomized import location, rootDirectory, outputFile, preplot, tecplot
from gateToCluster import operate as operate_on_cluster, call_winscp
from simulationData import SimulationData
from utilities import message, generate_folder, dos2unix, unix2dos, remove_file, clear_file, compare_files
from utilities import append_to_file, adapt_path, copy_file, move_file
from utilities import record_regression_of_file, unpack_tar_file, copy_input_files
from utilities import pack_tar_file, write_tecplot_macro_for_jpg, select_from_options
from configurationShared import inputFileEndings, outputFileEndings, additionalInputFileEndings, examplesName


class Operation:
    """
    parent class of Building, Plotting, Simulating
    """
    _operation_dict = dict()  # depends on self._selected_operation_type
    _selected_operation = str()
    _selected_operation_type = str()
    _item = None  # class Build, Sim, or Plot (Item)
    _simulation_data = None  # class SimulationData

    def __init__(self, subject):
        """
        :param subject: (class Subject)
        """
        self._subject = subject

    def __del__(self):
        pass

    @property
    def selected_operation(self):
        return self._selected_operation

    @property
    def selected_operation_type(self):
        return self._selected_operation_type

    def select_operation(self, selected_operation):
        """
        set self._selected_operation
        from user input if not already selected via previous loop or constructor of Environment
        else from setting.operation (which is passed to here as function argument)
        Required:
            self._operation_dict (dict)
        :param selected_operation: (string, None if operation not already selected)
        :return:
        """
        print('\n-----------------------------------------------------------------\n') 
        print('Test subject {} {}\n             on {}'.format(
            self._subject.code, self._subject.branch, self._subject.computer))

        if selected_operation:
            self._selected_operation = selected_operation
        else:
            self._selected_operation = select_from_options(self._operation_dict, 'Select operation')

    def set_upload_file_flags(self):
        self._simulation_data = SimulationData(self._selected_operation_type, self._selected_operation)

    def set_numerics_and_processing_data(self, item_type, item_case, item_configuration,
                                         flow_process_name, element_type_name, setting_inst, location_of_operation):
        """
        write files if on local computer and simulationData.ReadFileFlags are set
        :param item_type: (string)
        :param item_case: (string)
        :param item_configuration: (string)
        :param flow_process_name: (string)
        :param element_type_name: (string)
        :param setting_inst: (class Setting)
        :param location_of_operation: (string)
        :return:
        """
        if location == 'local':
            # do database queries
            if self._simulation_data.read_file_flags.numerics:
                setting_inst.set_numerics_data(self._simulation_data, item_case, item_configuration,
                                               flow_process_name, element_type_name)
                if location_of_operation == 'remote':
                    # file transfer
                    self._simulation_data.write_numerics_data_files()
            if self._simulation_data.read_file_flags.processing:
                setting_inst.set_processing_data(self._simulation_data, item_type, item_configuration)
                if location_of_operation == 'remote':
                    # file transfer
                    self._simulation_data.write_processing_data_file()

    def run(self, item):
        """
        direct to cluster or load data files (if necessary) and do operation
        :param item: (class Item (Build, Sim, Plot))
        :param simulation_data: (class SimulationData)
        :return:
        """
        self._item = item
   
        if self._subject.location == 'remote' and location == 'local' \
                and self._selected_operation_type != 'p':  # plotting operations are executed on local computer
            operate_on_cluster(self._subject, item,
                               self._selected_operation_type, self._selected_operation, self._simulation_data)
        else:   
            if location == 'remote':
                # reload modules with data for numerics and parallelization
                if self._simulation_data.read_file_flags.numerics:
                    self._simulation_data.get_num_data_from_modules(self._subject.id_local_process)
                if self._simulation_data.read_file_flags.processing:
                    self._simulation_data.get_processing_data_from_module(self._subject.id_local_process)

            self.operate()  # call member of child class


class Building(Operation):
    """

    """
    def __init__(self, subject):
        """
        :param subject: (class Subject)
        """
        self._selected_operation_type = 'b'

        self._operation_dict = {'b': '(b)uild', 'u': '(u)pdate', 'c': '(c)lear', 'w': '(w)ait', 's': 're(s)elect'}
        Operation.__init__(self, subject)

    def operate(self):
        """
        configure build and call operation for this build
        :return:
        """

        if self._selected_operation == 'b':
            self.build()
        elif self._selected_operation == 'u':
            self.update_release()  
        elif self._selected_operation == 'c':
            self.clear_folder()     
        elif self._selected_operation == 'w':
            self.wait()                                                                                                   
        else:
            message(mode='ERROR', not_supported='Operation {}'.format(self._selected_operation))

    def build(self):
        """
        call subprocess to build new release
        :return:
        """
        message(mode='INFO', text='Building {}'.format(self._item.configuration))
        try:
            Popen(self._subject.get_build_command(self._item), shell=True)
        except Exception as err:
            message(mode='ERROR', text='{}'.format(err))

    def update_release(self):
        """
        copy built files in special folder and rename them for release
        generate new release folder if it does not exist
        :return:
        """
        message(mode='INFO', text='Updating release {} {}'.format(system(), self._item.configuration))

        generate_folder(self._subject.directory + 'releases')
        built_file = self._subject.get_built_file(self._item)
        copy_file(built_file, self._subject.get_built_file_for_release(self._item))

    def clear_folder(self):
        """
        delete built files (from folder where they are after compilation)
        :return:
        """
        message(mode='INFO', text='Removing release {} {}'.format(system(), self._item.configuration))
        remove_file(self._subject.get_built_file(self._item, False))

    def wait(self):
        """
        wait until release exists
        :return:
        """
        message(mode='INFO', text='Waiting for release {} {}'.format(system(), self._item.configuration))
        wait_for_file(self._subject.get_built_file(self._item))


class Simulating(Operation):
    """
    configure and execute operations
    """
    def __init__(self, subject):
        """
        holds testing operations that can be local or remote (e.g. writing files, run code)
        adapt simulationDate.setReadFileFlags according to letters r, n, .... for selected operation for file uploads
        :param subject:
        """
        self._selected_operation_type = 's'

        self._operation_dict = {'r': '(r)un', 'n': 'write (n)um', 'c': '(c)lear folder from results', 'w': '(w)ait',
                                't': 's(t)ore results as reference', 'o': 'c(o)mpare results with reference'}
        if subject.location == 'remote':
            option_dict_amendments = {'i': '(i)mport files from repository (gate)',
                                      'x': 'e(x)port files to repository (gate)', 'b': 'write p(b)s',
                                      'm': '(m)esh partition', 'p': '(p)ack results'}
            self._operation_dict.update(option_dict_amendments)
        option_dict_amendments = {'s': 're(s)elect'}
        self._operation_dict.update(option_dict_amendments)

        Operation.__init__(self, subject)

    def operate(self):
        """
        link to selected operation
        :return:
        """
        if self._selected_operation == 'r':
            self.run_item()  
        elif self._selected_operation == 'n':
            self.write_num()               
        elif self._selected_operation == 'c':
            self.clear_folder()
        elif self._selected_operation == 't':
            self.store_results_as_reference()
        elif self._selected_operation == 'o':
            self.compare_results_with_reference()
        elif self._selected_operation == 'i' and self._subject.location == 'remote':
            self.import_from_repository()
        elif self._selected_operation == 'I' and self._subject.location == 'remote':
            self.import_from_repository(gate_flag=True)
        elif self._selected_operation == 'x' and self._subject.location == 'remote':
            self.export_to_repository()
        elif self._selected_operation == 'X' and self._subject.location == 'remote':
            self.export_to_repository(gate_flag=True)
        elif self._selected_operation == 'b' and self._subject.location == 'remote':
            self.write_pbs()  
        elif self._selected_operation == 'm' and self._subject.location == 'remote':
            self.partition_mesh()  
        elif self._selected_operation == 'p' and self._subject.location == 'remote':
            self.pack_results()
        elif self._selected_operation == 'w':
            self.wait()
        elif self._selected_operation == '0':
            message(mode='INFO', text='No Operation')                                                                         
        else:
            message(mode='ERROR', not_supported='Operation ' + self._selected_operation)

    def run_item(self):
        """
        call subprocess to run code for test item
        :return:
        """
        message(mode='INFO', text='Running {}'.format(self._item.name()))
        try:
            call(self._subject.get_execution_command(self._item), shell=True)
        except Exception as err:
            message(mode='ERROR', text='{}'.format(err))

    def import_from_repository(self, gate_flag=False):
        """
        copy input files from source directory into folder for test runs
        folder is generated if it is missing
        I: source is gate (for file transfer between computer)
        i: source is repository (e.g. for file transfer between branches)
        :return:
        """
        message(mode='INFO', text='Importing {}'.format(self._item.name()))
        if gate_flag:
            message(mode='INFO', text='    From gate')     
            directory_source = self._subject.directory_gate
        else:
            message(mode='INFO', text='    From repository')
            directory_source = self._item.directory_repository

        generate_folder(self._item.directory)
        copy_input_files(directory_source, self._item.directory)

    def export_to_repository(self, gate_flag=False):
        """
        copy input files into destination folder
        X: destination is gate (for file transfer between computer)
        x: destination is repository (e.g. for file transfer between branches)
        destination folder generated if it is missing
        :return:
        """
        message(mode='INFO', text='Exporting {}'.format(self._item.name()))
        if gate_flag:
            message(mode='INFO', text='Into gate')
            directory_destination = self._subject.directory_gate
        else:
            message(mode='INFO', text='Into repository')
            directory_destination = self._item.directory_repository

        generate_folder(directory_destination)
        copy_input_files(self._item.directory, directory_destination)

    def write_num(self):
        """
        call member of SimulationData to write file *.num
        :return:
        """
        message(mode='INFO', text='Write *.num {}'.format(self._item.name()))
        self._simulation_data.write_num(self._item.directory)

    def write_pbs(self): 
        """
        call member of SimulationData to write file run.pbs
        :return:
        """
        message(mode='INFO', text='Write run.pbs {}'.format(self._item.name()))
        self._simulation_data.write_pbs(self._item.directory,
                                        self._subject.get_built_file(self._item), self._item.type)

    def partition_mesh(self): 
        """
        call member of SimulationData to partition shell script
        :return:
        """
        message(mode='INFO', text='Mesh partition {}'.format(self._item.name()))
        self._simulation_data.partition_mesh(self._item.directory)

    def clear_folder(self):   
        """
        delete files
            1. configurationShared.outputFileEndings (*.tec, *.txt, *.plt, *.vtk)
            2. results.tar
            3. configurationShared.outputFile
        (remote folder for remote computer)
        :return:
        """
        message(mode='INFO', text='Clear simulation folder \n    {}'.format(self._item.name()))
        #
        if path.exists(self._item.directory):
            
            for file in listdir(self._item.directory):
                for ending in outputFileEndings: 
                    if file.endswith('.{}'.format(ending)):
                        remove_file(self._item.directory + file) 
                                        
            tarfile_remote = '{}results.tar'.format(self._item.directory)
            remove_file(tarfile_remote)

            output_file = self._item.directory + outputFile
            remove_file(output_file)
        else:
            message(mode='ERROR', text='Directory missing')           

    def pack_results(self):   
        """
        pack results on remote computer into tar file to download them later on
        :return:
        """
        if self._subject.location == 'remote':
            message(mode='INFO', text='Pack results {}'.format(self._item.name()))
            pack_tar_file(self._item.directory)
        else:
            message(mode='INFO', text='{} is local - Nothing done'.format(self._subject.computer))

    def wait(self):   
        """
        Wait until configurationShared.outputFile exists
        :return:
        """
        message(mode='INFO', text='Waiting for output file {}'.format(self._item.name()))
        #
        wait_for_file(self._item.directory + outputFile)

    def store_results_as_reference(self):
        """
        copy results (these are files with endings configurationShared.outputFileEndings)
        into reference folder
        (generates folder for references if it does not exist)
        each computer, case, branch has own reference folder
        :return:
        """
        message(mode='INFO', text='Store results as reference \n    {}'.format(self._item.name()))

        directory_reference = adapt_path("{}references\\{}\\{}\\{}\\{}\\{}\\".format(
            self._subject.directory, self._item.type, self._item.case,
            self._item.flow_process, self._item.element_type, self._item.configuration))


        generate_folder(directory_reference)

        if path.exists(self._item.directory):
            for extension in outputFileEndings:
                for file_name in listdir(self._item.directory):
                    if file_name.endswith('.{}'.format(extension)):
                        copy_file(self._item.directory + file_name, directory_reference)
        else:
            message(mode='ERROR', text='Directory missing')

    def compare_results_with_reference(self):
        """
        compare results with results in reference folder for regression tests
        if file disagrees, add file name to self._subject.directory + 'references\\deviatingFiles.log'
        then call record_differences_between_files(), which writes deviations themselves into
        directory_reference + 'deviations.log'
        configurationCustomized.outputFile are not compared
        :return:
        """
        message(mode='INFO', text='Compare result files with references {}'.format(self._item.name()))

        directory_reference = adapt_path(
            "{}references\\{}\\{}\\{}\\{}\\{}\\".format(
                self._subject.directory, self._item.type, self._item.case,
                self._item.flow_process, self._item.element_type, self._item.configuration))

        if path.exists(directory_reference):
            if path.exists(self._item.directory):
                # clear file that will contain regressions (differences between file contents)
                clear_file('{}deviations.log'.format(directory_reference))

                for file_name in listdir(directory_reference):
                    if file_name != outputFile and file_name != 'deviations.log':
                        # file to check
                        result_comparison_flag = compare_files(self._item.directory + file_name,
                                                               directory_reference + file_name)
                        if not result_comparison_flag:
                            # file contents disagree
                            message(mode='INFO', text='Deviating file: {}'.format(file_name))
                            append_to_file(
                                adapt_path('{}references\\deviatingFiles.log'.format(self._subject.directory)),
                                '{} {}\n'.format(self._item.directory, file_name))

                            record_regression_of_file(file_name, self._item.directory, directory_reference,
                                                      'deviations.log', output_flag=False)
            else:
                message(mode='ERROR', text='Directory missing')
        else:
            message(mode='ERROR', text='Directory with reference files missing')


class Plotting(Operation):
    """
    testing operations on local computer (concerning simulations that can be local or remote)
    e.g. downloading results, plotting)
    """

    def __init__(self, subject):
        """

        :param subject:
        """
        self._selected_operation_type = 'p'

        self._operation_dict = {'p': '(p)replot', 'j': 'generate (j)pgs', 'n': 'replace (n)ans and inds',
                                'c': '(c)lear folder', 'w': '(w)ait', 's': 're(s)elect'}
        if subject.location == 'remote':
            option_dict_amendments = {'g': '(g)et results'}
            self._operation_dict.update(option_dict_amendments)

        Operation.__init__(self, subject)

    def operate(self):
        """
        link to specific operation
        :return:
        """
        if self._selected_operation == 'g':
            self.get_results()
        elif self._selected_operation == 'p':
            self.preplot()
        elif self._selected_operation == 'j':
            self.generate_jpgs()
        elif self._selected_operation == 'n':
            self.replace_nans_and_inds()
        elif self._selected_operation == 'c':
            self.clear_folder()
        elif self._selected_operation == 'w':
            self.wait()
        else:
            message(mode='ERROR', not_supported='Operation {}'.format(self._selected_operation))

    def get_results(self):
        """
        download and unpack tar file from remote to local computer,
        if local computer is windows, convert files into dos-format
        :return:
        """
        if self._subject.location == 'remote':
            message(mode='INFO', text='Get results {}'.format(self._item.name()))

            mod = __import__(self._subject.computer)
            generate_folder(self._item.directory)

            if path.exists(self._item.directory):
                # clear local directory
                files = glob(self._item.directory + '*')
                for file in files:
                    remove_file(file)

                winscp_command = 'get {}results.tar {}'.format(
                    self._item.directory_computer_selected, self._item.directory)
                call_winscp([winscp_command], self._subject.user, self._subject.hostname, mod.pwd, output_flag=True)

                unpack_tar_file(self._item.directory)  # tar file on local computer

                if system() == 'Windows':
                    message(mode='INFO', text='    Convert to dos')
                    for file in listdir(self._item.directory):
                        unix2dos(file, output_flag=False)
            else:
                message(mode='ERROR', text='Directory missing')
        else:
            message(mode='INFO', text='{} is local - Nothing done'.format(self._subject.computer))

    def replace_nans_and_inds(self):
        """
        replace each nan by 999 and remove each IND in all tec files
        :return:
        """
        message(mode='INFO', text='Replace nans and inds {}'.format(self._item.name()))

        if path.exists(self._item.directory):
            for file_name in listdir(self._item.directory):
                if file_name.endswith('.tec'):
                    message(mode='INFO', text='File: {}'.format(file_name))
                    try:
                        infile = open(self._item.directory + file_name, 'r')
                        outfile = open('{}new_{}'.format(self._item.directory, file_name), 'w')
                    except Exception as err:
                        message(mode='ERROR', text='{}'.format(err))
                    else:
                        for line in infile:
                            line = line.replace('nan', '999')
                            line = line.replace('#IND', '')
                            outfile.write(line)
                        infile.close()
                        outfile.close()
                        move_file('{}new_{}'.format(self._item.directory, file_name), self._item.directory + file_name)
        else:
            message(mode='ERROR', text='Directory missing')

    def preplot(self):
        """
        call preplot via subprocess to generate *.plt's for all *.tec found in folder
        :return:
        """
        message(mode='INFO', text='Preplot {}'.format(self._item.name()))

        if path.exists(self._item.directory):
            chdir(self._item.directory)
            for file in listdir(self._item.directory):
                if file.endswith('.tec'):
                    message(mode='INFO', text='File: {}'.format(file))
                    try:
                        call('{} {}{}'.format(preplot, self._item.directory, file), shell=True)
                    except Exception as err:
                        message(mode='ERROR', text='{}'.format(err))
        else:
            message(mode='ERROR', text='Directory missing')

    def generate_jpgs(self):
        """
        generate JPG with tecplot
            1. generate tecplot macro
            2. call tecplot via subprocess
            3. remove tecplot macro
        :return:
        """
        message(mode='INFO', text='Generate Jpgs ' + self._item.type)

        if path.exists(self._subject.directory_plot):
            chdir(self._subject.directory_plot)
            for file in glob("{}*".format(self._item.type)):
                filename = path.splitext(file)[0]
                message(mode='INFO', text='    {}'.format(filename))
                write_tecplot_macro_for_jpg(self._subject.directory_plot, filename)

                layout = '{}{}.lay'.format(self._subject.directory_plot, filename)
                try:
                    call('{} {} -b -p {}_genJPG.mcr'.format(tecplot, layout, self._subject.directory_plot), shell=True)
                except Exception as err:
                    message(mode='ERROR', text='{}'.format(err))
                remove_file('{}_genJPG.mcr'.format(self._subject.directory_plot), output_flag=False)
        else:
            message(mode='ERROR', text='Directory missing')

    def clear_folder(self):   
        """
        delete *.tec, *.txt, *.asc, *plt and results.tar (local folder for remote computer)
        :return:
        """
        message(mode='INFO', text='Clear plotting folder ' + self._item.name())
        #
        remove_file("{}results_{}.jpg".format(self._subject.directory_plot, self._item.type))

        if path.exists(self._item.directory):
            for file in listdir(self._item.directory):
                for ending in outputFileEndings:
                    if file.endswith('.{}'.format(ending)):
                        if self._subject.location == 'remote' or ending != 'tec':
                            # do not delete tec if local
                            remove_file(self._item.directory + file)

                # myLocalTarFile = self._item.directory + 'results.tar'  # done in get_results()
                # if path.isfile(myLocalTarFile):
                #     remove(myLocalTarFile)

        else:
            message(mode='ERROR', text='Directory missing')
        # if location == 'remote':
        #    for file in listdir(self._item.getLocalDirectory()):
        #        for ending in outputFileEndings:
        #            if file.endswith('.' + ending):
        #                remove(self._item.getLocalDirectory() + file)

    def wait(self):
        """
        wait until jpg file is in folder
        :return:
        """
        message(mode='INFO', text='Waiting for jpg file {}'.format(self._item.type))
        wait_for_file("{}results_{}.jpg".format(self._subject.directory_plot, self._item.type))


def wait_for_file(file_name):
    """
    Used by members to wait until a file exists
    prints a dot each second when waiting
    :param file_name:
    :return:
    """
    stdout.flush()
    start = time()

    i = 1
    while not path.exists(file_name):
        if time()-start > i:
            stdout.write('.')
            stdout.flush()
            i += 1
