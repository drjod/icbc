from glob import glob
from os import path, getpid
from collections import OrderedDict
from operation import Operation
from simulationData import SimulationData
from configuration import inputFileEndings, outputFileEndings, additionalInputFileEndings, examplesName
from configuration import outputFile
from shared import message, Commands


class Simulating(Operation):
    """
    configure and execute operations
    """
    __simulation_data = None  # class SimulationData

    def __init__(self, subject):
        """
        holds testing operations that can be local or remote (e.g. writing files, run code)
        adapt simulationDate.setReadFileFlags according to letters r, n, .... for selected operation for file uploads
        :param subject:
        """
        self._selected_operation_type = 's'

        self._operation_dict = OrderedDict([('r', '(r)un'),
                                            ('n', 'write (n)um'),
                                            ('m', '(m)esh partition'),
                                            ('c', '(c)lear folder from results'),
                                            ('w', '(w)ait'),
                                            ('i', '(i)mport files from repository'),
                                            ('x', 'e(x)port files to repository'),
                                            ('t', 's(t)ore results as reference'),
                                            ('o', 'c(o)mpare results with reference'),
                                            ('g', 'show re(g)ression')])
        if subject.remote_flag:
            option_dict_amendments = {'b': 'write (b)atch', 'p': '(p)ack results'}
            self._operation_dict.update(option_dict_amendments)
        option_dict_amendments = {'s': 're(s)elect'}
        self._operation_dict.update(option_dict_amendments)

        Operation.__init__(self, subject)

    def configure(self):
        """
        1.  if operation is to compare results with references, clear log file with names of
            deviating files from previous runs
        2. check if list entries for test items exit
        :param operation_inst: (class Building, Simulating, Plotting (Operation))
        :return: 0 if success; 1 if lists for item not complete
        """
        if self._selected_operation == 'o':
            # the selected operation is to compare results with references
            files = glob(path.join(self._subject.directory, 'references', 'deviatingFiles*'))
            for file in files:
                Commands.remove_file(file, False)

            # clear_file('{}references/deviatingFiles_{}.log'.format(
            #    self._subject_inst.directory, self._item.configuration))

        self.__simulation_data = SimulationData(self._selected_operation)

    def configure_for_item(self, item_type, item_case, item_configuration,
                       flow_process_name, element_type_name, setting_inst):
        """
        write files if ReadFileFlags are set
        :param item_type: (string)
        :param item_case: (string)
        :param item_configuration: (string)
        :param flow_process_name: (string)
        :param element_type_name: (string)
        :param setting_inst: (class Setting)
        :return:
        """
        # do database queries
        if self.__simulation_data.read_file_flags.numerics:
            setting_inst.set_numerics_data(self.__simulation_data, item_case, item_configuration,
                                           flow_process_name, element_type_name)

        if self.__simulation_data.read_file_flags.processing:
            setting_inst.set_processing_data(self.__simulation_data, item_type, item_configuration)

    def run(self, item):
        """
        link to selected operation
        :param item: (class Item)
        :return:
        """
        self._item = item

        if self._selected_operation == 'r':
            self.run_item()
        elif self._selected_operation == 'n':
            self.write_num()
        elif self._selected_operation == 'm':
            self.partition_mesh()
        elif self._selected_operation == 'c':
            self.clear_folder()
        elif self._selected_operation == 't':
            self.store_results_as_reference()
        elif self._selected_operation == 'o':
            self.compare_results_with_reference()
        elif self._selected_operation == 'g':
            self.show_regression()
        elif self._selected_operation == 'i':
            self.import_from_repository()
        elif self._selected_operation == 'I':
            self.import_from_repository(gate_flag=True)
        elif self._selected_operation == 'x':
            self.export_to_repository()
        elif self._selected_operation == 'X':
            self.export_to_repository(gate_flag=True)
        elif self._selected_operation == 'w':
            self.wait()
        elif self._selected_operation == 'b' and self._subject.remote_flag:
            self.write_batch()
        elif self._selected_operation == 'p' and self._subject.remote_flag:
            self.pack_results()
        elif self._selected_operation == '0':
            message(mode='INFO', text='No Operation')
        else:
            message(mode='ERROR', not_supported='Operation {}'.format(self._selected_operation))

    def run_item(self):
        """
        call subprocess to run code for test item
        :return:
        """
        message(mode='INFO', text='Running {}'.format(self._item.name()))

        if self._subject.remote_flag:
            self.execute_python('call', None, 'sbatch', path.join(self._item.directory, 'run'))
        else:
            executable, test_case, output_file = self._subject.get_execution_command(self._item)
            self.execute_python('call', output_file, executable, test_case)

    def import_from_repository(self, gate_flag=False):
        """
        copy input files from source directory into folder for test runs
        folder is generated if it is missing
        I: source is gate (for file transfer between computer)
        i: source is repository (e.g. for file transfer between branches)
        :return:
        """
        message(mode='INFO', text='Importing {}'.format(self._item.name()))

        directory_source = self._subject.gate_directory if gate_flag else self._item.directory_repository

        self.execute_python('generate_folder', self._item.directory)
        self.execute_python('copy_input_files', directory_source, self._item.directory)

    def export_to_repository(self, gate_flag=False):
        """
        copy input files into destination folder
        X: destination is gate (for file transfer between computer)
        x: destination is repository (e.g. for file transfer between branches)
        destination folder generated if it is missing
        :return:
        """
        message(mode='INFO', text='Exporting {}'.format(self._item.name()))

        directory_destination = self._subject.gate_directory if gate_flag else self._item.directory_repository

        self.execute_python('generate_folder', directory_destination)
        self.execute_python('copy_input_files', self._item.directory, directory_destination)

    def write_num(self):
        """
        call member of SimulationData to write file *.num
        :return:
        """
        message(mode='INFO', text='Write numerics file {}'.format(self._item.name()))

        directory_write_destination = '/tmp' if self._subject.remote_flag else self._item.directory
        self.__simulation_data.write_num(directory_write_destination)
        if self._subject.remote_flag:
            self._gateToCluster.upload_file(path.join('/tmp', '{}.num{}'.format(examplesName, getpid())),
                                            path.join(self._item.directory, '{}.num'.format(examplesName)))
            Commands.remove_file(path.join('/tmp', '{}.num{}'.format(examplesName, getpid())), False)

    def write_batch(self):
        """
        call member of SimulationData to write file batch file
        than upload file from tmp directory to remote item directory, it is called 'run' there
        and identified for uploading via pid mark
        (batches only used for remote computer, so nothing is done if subject computer is local)
        :return:
        """
        message(mode='INFO', text='Write batch file {}'.format(self._item.name()))
        if self._subject.remote_flag:
            self.__simulation_data.write_batch(self._item.directory,
                                               self._subject.get_built_file(self._item), self._item.type)
            self._gateToCluster.upload_file(path.join('/tmp', 'run{}'.format(getpid())),
                                            path.join(self._item.directory, 'run'))
            Commands.remove_file(path.join('/tmp', 'run{}'.format(getpid())), False)
        else:
            message(mode='INFO', text='    on local computer - nothing done')

    def partition_mesh(self):
        """
        call member of SimulationData to partition shell script
        :return:
        """
        message(mode='INFO', text='Mesh partition {}'.format(self._item.name()))
        self.__simulation_data.partition_mesh(self)

    def clear_folder(self):
        """
        delete files
            1. configuration.outputFileEndings (*.tec, *.txt, *.plt, *.vtk)
            2. results.tar
            3. configuration.outputFile
        :return:
        """
        message(mode='INFO', text='Clear simulation folder \n    {}'.format(self._item.name()))

        self.execute_python('remove_results', self._item.directory)

    def pack_results(self):
        """
        pack results, e.g. to download them later on
        :return:
        """
        message(mode='INFO', text='Pack results {}'.format(self._item.name()))

        self.execute_python('pack_tar_file', self._item.directory)

    def wait(self):
        """
        Wait until configuration.outputFile exists
        :return:
        """
        message(mode='INFO', text='Waiting for output file {}'.format(self._item.name()))
        #
        self.execute_python('wait_for_file', path.join(self._item.directory, outputFile))

    def store_results_as_reference(self):
        """
        copy results (these are files with endings configuration.outputFileEndings)
        into reference folder
        (generates folder for references if it does not exist)
        each computer, case, branch has own reference folder
        :return:
        """
        message(mode='INFO', text='Store results as reference \n    {}'.format(self._item.name()))

        directory_reference = path.join(self._subject.directory, 'references', self._item.type, self._item.case,
                                        self._item.flow_process, self._item.element_type, self._item.configuration)

        self.execute_python('generate_folder', directory_reference)

        for ending in outputFileEndings:
            self.execute_python('copy_file', ending, directory_reference, False, self._item.directory, True)

    def compare_results_with_reference(self):
        """
        remove file deviations,log in item directory, then record regression for item directory.
        results (deviations) are stored in reference folder 'deviations.log'
        names of files with deviations are stored in folder subject reference 'deviatingFiles_{configuration}.log'
        :return:
        """
        message(mode='INFO', text='Compare result with reference files\n    {}'.format(self._item.name()))

        directory_reference = path.join(self._subject.directory, 'references', self._item.type, self._item.case,
                                        self._item.flow_process, self._item.element_type, self._item.configuration)

        self.execute_python('remove_file', path.join(directory_reference, 'deviations.log'), False)
        self.execute_python('record_regression_for_folder', self._item.directory, directory_reference,
                            self._subject.directory, self._item.configuration, outputFile)

    def show_regression(self):
        """
        print contents from file where regression is documented
        :return:
        """
        message(mode='INFO', text='Show regression\n    {}'.format(self._item.name()))

        file = path.join(self._subject.directory, 'references', self._subject.directory, 'references',
                         self._item.type, self._item.case, self._item.flow_process,
                         self._item.element_type, self._item.configuration, 'deviations.log')

        self.execute_python('show_file_content', file)
