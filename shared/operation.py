from sys import stdout, exc_info, path as syspath
from os import path, mkdir, makedirs, listdir, chdir, remove, stat, access, R_OK
from platform import system
from subprocess import Popen, call, check_call
from glob import glob
from time import time
from shutil import copyfile, copy, move
from filecmp import cmp
syspath.append(path.join(path.dirname(__file__), '..', 'customized'))
syspath.append(path.join(path.dirname(__file__), '..', 'pwds'))
from configurationCustomized import location, rootDirectory, outputFile, preplot, tecplot
from gateToCluster import operate as operate_on_cluster
from item import Item
from simulationData import SimulationData
from utilities import message, generate_folder, dos2unix, unix2dos, remove_file, adapt_path, select_from_options
from utilities import record_differences_between_files, download_file_with_winscp, unpack_tar_file, import_files
from utilities import pack_tar_file
from configurationShared import inputFileEndings, outputFileEndings, additionalFileEndings, examplesName


class Operation:
    """

    """
    _selected_operation = str()
    _selected_operation_type = str()
    _item = Item()
    _operation_dict = dict()
    _simulation_data = SimulationData()   # put to Simulation below

    def __init__(self, subject):
        """

        :param subject:
        """
        self._subject = subject
        self._gate_flag = False

    def __del__(self):
        pass

    @property
    def selected_operation(self):
        return self._selected_operation

    @property
    def selected_operation_type(self):
        return self._selected_operation_type

    def select_operation(self, preselected_operation):
        """
        user input if operation has not been already selected (operation_preselected !=' ')
        :param preselected_operation: (string), None if operation not already selected
        :return: selected_operation (string)
        Required:
            self._operation_dict (dict)
        """
        print('\n-----------------------------------------------------------------\n') 
        print('Test subject ' + self._subject.code + ' ' + self._subject.branch)
        print('             on ' + self._subject.computer)

        if not preselected_operation:
            self._selected_operation = select_from_options(self._operation_dict, 'Select operation')
        else:
            self._selected_operation = preselected_operation
        return self._selected_operation

    def run(self, item, simulation_data):
        """
        direct to cluster or load data files (if necessary) and do operation
        :param item: of type Item
        :param simulation_data: of type SimulationData
        :return:
        """
        self._simulation_data = simulation_data
   
        if self._subject.location == 'remote' and location == 'local' \
                and not self._selected_operation_type == 'p':
            operate_on_cluster(self._subject, item,
                               self._selected_operation_type, self._selected_operation, self._simulation_data)
        else:   
            if location == 'remote':
                # file transfer
                if simulation_data.read_file_flags.numerics:
                    simulation_data.import_num_data_files(item.configuration)
                    simulation_data.get_num_data_from_modules(item.configuration)
                if simulation_data.read_file_flags.processing:
                    simulation_data.import_processing_data_files(item.configuration)
                    simulation_data.getProcessingDataFromModule(item.configuration)
            self.operate(item)


class Building(Operation):
    """

    """

    def __init__(self, subject):
        """
        :param subject:
        """
        self._selected_operation_type = 'b'

        self._operation_dict = {'b': 'build', 'u': 'update', 'c': 'clear', 'w': 'wait', 's': 'reselect'}
        Operation.__init__(self, subject)

    def operate(self, build):
        """
        configure build and call operation for this build
        :param build:
        :return:
        """
        self._item = build 

        if self._selected_operation == 'b':
            self.build_release()  
        elif self._selected_operation == 'u':
            self.update_release()  
        elif self._selected_operation == 'c':
            self.clear_folder()     
        elif self._selected_operation == 'w':
            self.wait()                                                                                                   
        else:
            message(mode='ERROR', not_supported='Operation ' + self._selected_operation)

    def build_release(self):
        """
        run one of the selected test items with selected code
        :return:
        """
        message(mode='INFO', text='Building ' + self._item.configuration)
        try:
            Popen(self._subject.get_buildcommand(self._item), shell=True)
        except:
            message(mode='ERROR', text='%s' % exc_info()[0])

    def update_release(self):
        """
        copy and rename windows binaries
        :return:
        """
        try:
            stat(self._subject.directory + 'releases')
        except:
            mkdir(self._subject.directory + 'releases')
        
        message(mode='INFO', text='Updating release ' + system() + ' ' + self._item.configuration)
        
        if path.isfile(self._subject.get_executable(self._item)) and \
                access(self._subject.get_executable(self._item), R_OK):
            copy(self._subject.get_executable(self._item), self._subject.get_executable_for_release(self._item))  
        else:
            message(mode='ERROR', text='Binary does not exist - nothing done')

    def clear_folder(self):   
        """
        delete release binaries
        :return:
        """
        message(mode='INFO', text='Removing release ' + system() + ' ' + self._item.configuration)
        try:
            remove(self._subject.get_executable(self._item))
        except OSError:
            message(mode='ERROR', text='%s' % exc_info()[0])

    def wait(self):
        """
        wait until release exists
        :return:
        """
        message(mode='INFO', text='Waiting for release ' + system() + ' ' + self._item.configuration)
        wait_for_file(self._subject.get_executable(self._item))


class Simulating(Operation):
    """
    configure and execute operations
    """
    def __init__(self, subject):
        """
        testing operations that can be local or remote (e.g. writing files, run code)
        adapt simulationDate.setReadFileFlags according to letters r, n, .... for selected operation
        :param subject:
        """
        self._selected_operation_type = 's'

        self._operation_dict = {'r': '(r)un', 'n': 'write (n)um', 'c': '(c)lear folder from results', 'w': 'wait',
                                't': 's(t)ore results as reference', 'o': 'c(o)mpare results with reference'}
        if subject.location == 'remote':
            option_dict_amendments = {'i': '(i)mport files from repository (gate)',
                                      'x': 'e(x)port files to repository (gate)', 't': 'wri(t)e pbs',
                                      'm': '(m)esh partition', 'p': '(p)ack results'}
        self._operation_dict.update(option_dict_amendments)
        option_dict_amendments = {'s': 're(s)elect'}
        self._operation_dict.update(option_dict_amendments)

        Operation.__init__(self, subject)

    def operate(self, sim):
        """
        link to operation
        :param sim:
        :return:
        """
        self._item = sim

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
            self._gate_flag = True
            self.import_from_repository()
        elif self._selected_operation == 'x' and self._subject.location == 'remote':
            self.export_to_repository()
        elif self._selected_operation == 'X' and self._subject.location == 'remote':
            self._gate_flag = True
            self.export_to_repository()
        elif self._selected_operation == 't' and self._subject.location == 'remote':
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
        run code
        :return:
        """
        
        message(mode='INFO', text='Running ' + self._item.name())
        
        if path.exists (self._item.directory):
            try:
                call(self._subject.get_execution_command(self._item), shell=True)
            except:
                message(mode='ERROR', text='%s' % exc_info()[0])
        else:
            message(mode='ERROR', text='Directory missing')

    def import_from_repository(self):
        """
        copy input files from source directory into folder for test runs
        folder is generated if it is missing
        I: source is gate (for file transfer between computer)
        i: source is repository (for file transfer between branches)
        :return:
        """

        message(mode='INFO', text='Importing ' + self._item.name())              
        if self._gate_flag:
            message(mode='INFO', text='    From gate')     
            source_directory = self._subject.directory_gate
        else:
            message(mode='INFO', text='    From repository')
            source_directory = self._item.directory_repository

        # make folder for test item if it does not already exist
        test_list = [  # 'testingEnvironment', self._subject.getName(), self._subject.code, self._subject.branch,
                    'examples', 'files', self._item.type, self._item.case, self._item.configuration]
        generate_folder(self._subject.directory, test_list)

        # set list of file endings
        ending_list = list()
        if self._subject.location == 'remote':  # no input on remote cluster
            ending_list = list(inputFileEndings)
        else:  # ... but on local computer
            option_to_select_endings_selected = input('(e)nding, (n)ame or (a)ll\n')

            # set variable(s) to  
            if str(option_to_select_endings_selected) == 'e':
                ending_selected = input('\n')
                ending_list.append(ending_selected)
            elif str(option_to_select_endings_selected) == 'a':
                ending_list = list(inputFileEndings)
            elif str(option_to_select_endings_selected) == 'n':
                name = input('\n')

            import_files(source_directory, self._item.directory, ending_list, self._gate_flag)


    def export_to_repository(self):
        """
        copy input files into destination folder
        X: destination is gate (for file transfer between computer)
        x: destination is repository (for file transfer between branches)
        destination folder generated if it is missing
        :return:
        """
        message(mode='INFO', text='Exporting ' + self._item.name())   
        if self._gate_flag:
            message(mode='INFO', text='Into gate')
            directory_destination = self._subject.directory_gate
        else:
            message(mode='INFO', text='Into repository')
            directory_destination = self._item.directory_repository
        # make repository folder if it does not exist                
        repository_list = ['testingEnvironment', self._subject.computer, 'repository', self._item.type, self._item.case]
        generate_folder(rootDirectory, repository_list)
        # export  
        if path.exists(self._item.directory):
            for ending in inputFileEndings:      
                file_name = self._item.directory + examplesName + '.' + ending                   
                if path.isfile(file_name) and access(file_name, R_OK):
                    copy(file_name, directory_destination)

            for file in listdir(self._item.directory):  # to copy additional files, e.g. for external chemical solver
                file_name = self._item.directory + file
                for ending in additionalFileEndings: 
                    if file.endswith('.' + ending):
                        message(mode='INFO', text='    Exporting additional file ' + file)
                        copy(file_name, directory_destination)
        else:
            message(mode='ERROR', text='Directory missing')

    def write_num(self):
        """
        write file *.num
        :return:
        """
        message(mode='INFO', text='Write *.num ' + self._item.name())
        
        if path.exists (self._item.directory):
            self._simulation_data.write_num(self._item.directory)
        else:
            message(mode='ERROR', text='Directory missing')

    def write_pbs(self): 
        """
        write file run.pbs
        :return:
        """
        message(mode='INFO', text='Write run.pbs ' + self._item.name())

        if path.exists (self._item.directory):
            self._simulation_data.write_pbs(self._item.directory,
                                            self._subject.get_executable(self._item), self._item.type)
        else:
            message(mode='ERROR', text='Directory missing') 

    def partition_mesh(self): 
        """
        call partition shell script
        :return:
        """
        message(mode='INFO', text='Mesh partition ' + self._item.name())

        if path.exists(self._item.directory):
            self._simulation_data.partition_mesh(self._item.directory)
        else:
            message(mode='ERROR', text='Directory missing')

    def clear_folder(self):   
        """
        delete *.tec, *.txt, *.plt, *.vtk and results.tar (remote folder for remote computer)
        :return:
        """
        message(mode='INFO', text='Clear simulation folder ' + self._item.name())
        #
        if path.exists(self._item.directory):
            
            for file in listdir(self._item.directory):
                for ending in outputFileEndings: 
                    if file.endswith('.' + ending):
                        remove_file(self._item.directory + file) 
                                        
                tarfile_remote = self._item.directory + 'results.tar'
                if path.isfile(tarfile_remote):
                    remove_file(tarfile_remote)

            remove_file(self._item.directory + outputFile)
        else:
            message(mode='ERROR', text='Directory missing')           

    def pack_results(self):   
        """
        pack results on remote computer into tar file to download them later on
        :return:
        """
        if self._subject.location == 'remote':
            message(mode='INFO', text='Pack results ' + self._item.name())

            if path.exists(self._item.directory):
                pack_tar_file(self._item.directory)
            else:     
                message(mode='ERROR', text='Directory missing')
        else:
            message(mode='INFO', text=self._subject.computer + ' is local - Nothing done')

    def wait(self):   
        """
        Wait until outputFile exists
        :return:
        """
        message(mode='INFO', text='Waiting for output file ' + self._item.name())
        #
        wait_for_file(self._item.directory + outputFile)

    def store_results_as_reference(self):
        """
        copy results into reference folder
        (generates folder for references if it does not exist)
        each computer, case, branch has own reference folder
        :return:
        """
        message(mode='INFO', text='Store results as reference ' + self._item.name())

        directory_reference = adapt_path(self._subject.directory + "references\\" + self._item.type +
                                         "\\" + self._item.case + "\\" + self._item.configuration + "\\")
        if not path.exists(directory_reference):
            makedirs(directory_reference)

        if path.exists(self._item.directory):
            for extension in outputFileEndings:
                for file in listdir(self._item.directory):
                    if file.endswith('.' + extension):
                        copyfile(self._item.directory + file , directory_reference + file)
        else:
            message(type='ERROR', text='Directory missing')

    def compare_results_with_reference(self):
        """
        compare results with results in reference folder for regression tests
        if file disagrees, add file name to self._subject.directory + 'references\\deviatingFiles.log'
        then call record_differences_between_files(), which writes deviations themselves into
        directory_reference + 'deviations.log'
        :return: 0: success, 1: no directory for item, 2: no directory for reference file, 100: could not open file
        """
        message(mode='INFO', text='Compare result files with references ' + self._item.name())

        directory_reference = adapt_path(self._subject.directory + "references\\" + self._item.type + "\\" +
                                         self._item.case + "\\" + self._item.configuration + "\\")

        if not path.exists(directory_reference):
            message(mode='ERROR', text='Directory with reference files missing')
            return 2

        if path.exists(self._item.directory):
            open(directory_reference + 'deviations.log', 'w').close()  # clear file content
            for file_name in listdir(directory_reference):
                if file_name != outputFile and file_name != 'deviations.log':
                    result_comparison_flag = cmp(self._item.directory + file_name, directory_reference + file_name)
                    if not result_comparison_flag:  # file contents disagree
                        message(mode='INFO', text='Deviating file: ' + file_name)
                        try:
                            f = open(adapt_path(self._subject.directory + 'references\\deviatingFiles.log'), 'a')
                        except IOError:
                            message(mode='ERROR', text='Cannot open file')
                            return 100
                        else:
                            f.write(self._item.directory + file_name + '\n')
                            if record_differences_between_files(
                                file_name, self._item.directory, directory_reference, 'deviations.log') == 100:
                                return 100
            return 0
        else:
            message(mode='ERROR', text='Directory missing')
            return 1


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

        self._operation_dict = {'g': '(g)et results', 'p': '(p)replot', 'j': 'generate (j)pg',
                                'n': 'replace (n)ans and inds', 'c': '(c)lear folder', 'w': '(w)ait', 's': 're(s)elect'}
        if subject.location == 'remote':
            option_dict_amendments = {'g': '(g)et results'}
        self._operation_dict.update(option_dict_amendments)

        Operation.__init__(self, subject)

    def operate(self, plot):
        """
        link to operation
        :param plot:
        :return:
        """
        self._item = plot

        if self._selected_operation == 'g':
            self.get_results()
        elif self._selected_operation == 'p':
            self.preplot()
        elif self._selected_operation == 'j':
            self.generate_jpg()
        elif self._selected_operation == 'n':
            self.replace_nans_and_inds()
        elif self._selected_operation == 'c':
            self.clear_folder()
        elif self._selected_operation == 'w':
            self.wait()
        else:
            message(mode='ERROR', not_supported='Operation ' + self._selected_operation)

    def get_results(self):
        """
        download and unpack tar file from remote to local computer,
        if local computer is windows, convert files into dos-format
        :return:
        """
        if self._subject.location == 'remote':
            message(mode='INFO', text='Get results ' + self._item.name())

            mod = __import__(self._subject.computer)
            # make repository folder if it does not exist
            repository_list = ['testingEnvironment', self._subject.computer, self._subject.code,
                               self._subject.branch, 'examples', 'files', self._item.type,
                               self._item.case, self._item.configuration]
            generate_folder(rootDirectory, repository_list)

            if path.exists(self._item.directory):
                # clear local directory
                files = glob(self._item.directory + '*')
                for file in files:
                    remove(file)

                download_file_with_winscp(
                    rootDirectory + '\\testingEnvironment\\scripts\\icbc\\customized\\winscp_downloadResults.txt',
                    self._item.directory_computer_selected + 'results.tar' + ' ' + self._item.directory,
                    self._subject.user, self._subject.hostname, mod.pwd)

                unpack_tar_file('results.tar', self._item.directory)  # tar file on lokal computer

                if system() == 'Windows':
                    message(mode='INFO', text='    Convert to dos')
                    for file in listdir(self._item.directory):
                        unix2dos(file)
            else:
                message(mode='ERROR', text='Directory missing')
        else:
            message(mode='INFO', text=self._subject.computer + ' is local - Nothing done')

    def replace_nans_and_inds(self):
        """
        replace each nan by 999 and remove each IND in all tec files
        :return:
        """
        message(mode='INFO', text='Replace nans and inds' + self._item.name())

        if path.exists(self._item.directory):
            chdir(self._item.directory)
            for file in listdir(self._item.directory):
                if file.endswith('.tec'):
                    message(mode='INFO', text='File: ' + file)
                    try:
                        infile = open(file,'r')
                        outfile = open('new_' + file, 'w')
                    except OSError as err:
                        message(mode='ERROR', text='OS error: {0}'.format(err))
                    else:
                        for line in infile:
                            line = line.replace('nan', '999')
                            line = line.replace('#IND', '')
                            outfile.write(line)
                        infile.close()
                        outfile.close()
                        move('new_' + file, file)
        else:
            message(mode='ERROR', text='Directory missing')

    def preplot(self):
        """
        call preplot to generate *.plt's
        :return:
        """
        message(mode='INFO', text='Preplot ' + self._item.name())

        if path.exists(self._item.directory):
            chdir(self._item.directory)
            for file in listdir(self._item.directory):
                if file.endswith('.tec'):
                    message(mode='INFO', text='File: ' + file)
                    try:
                        call(preplot + ' ' + self._item.directory + file, shell=True)
                    except:
                        message(mode='ERROR', text='%s' % exc_info()[0])
        else:
            message(mode='ERROR', text='Directory missing')

    def generate_jpg(self):
        """
        generate JPG with tecplot
        :return:
        """
        message(mode='INFO', text='Generate Jpg ' + self._item.type)

        if path.exists(self._subject.directory_plot):
            layout = self._subject.directory_plot + self._item.type + '.lay'

            chdir(self._subject.directory_plot)
            try:
                f = open(self._subject.directory_plot + '_genJPG.mcr', 'w')
            except OSError as err:
                    message(mode='ERROR', text='OS error: {0}'.format(err))
            else:
                f.write('#!MC 1300\n')
                f.write('#-----------------------------------------------------------------------\n')
                f.write('$!EXPORTSETUP EXPORTFORMAT = JPEG\n')
                f.write('$!EXPORTSETUP IMAGEWIDTH = 1500\n')
                f.write('#-----------------------------------------------------------------------\n')
                f.write("$!EXPORTSETUP EXPORTFNAME = \'" + self._subject.directory_plot + "results_"
                        + self._item.type + ".jpg\'\n")
                f.write('$!EXPORT\n')
                f.write('EXPORTREGION = ALLFRAMES\n')
                f.close()
                print(tecplot + ' ' + layout + ' -b -p ' + self._subject.directory_plot + '_genJPG.mcr')
                try:
                    call(tecplot + ' ' + layout + ' -b -p ' + self._subject.directory_plot + '_genJPG.mcr', shell=True)
                except:
                    message(mode='ERROR', text='%s' % exc_info()[0])
                remove_file(self._subject.directory_plot + '_genJPG.mcr')
        else:
            message(mode='ERROR', text='Directory missing')

    def clear_folder(self):   
        """
        delete *.tec, *.txt, *.asc, *plt and results.tar (local folder for remote computer)
        :return:
        """
        message(mode='INFO', text='Clear plotting folder ' + self._item.name())
        #
        remove_file(self._subject.directory_plot + "results_" + self._item.type + ".jpg")

        if path.exists(self._item.directory):
            for file in listdir(self._item.directory):
                for ending in outputFileEndings:
                    if file.endswith('.' + ending):
                        if self._subject.location == 'remote' or ending != 'tec':
                            # do not delete tec if local
                            remove_file(self._item.directory + file)

                #myLocalTarFile = self._item.directory + 'results.tar'  # done in get_results()
                #if path.isfile(myLocalTarFile):
                #    remove(myLocalTarFile)

        else:
            message(mode='ERROR', text='Directory missing')
        #if location == 'remote':
        #    for file in listdir(self._item.getLocalDirectory()):
        #        for ending in outputFileEndings:
        #            if file.endswith('.' + ending):
        #                remove(self._item.getLocalDirectory() + file)

    def wait(self):
        """
        wait untiel jpg file in folder
        :return:
        """
        message(mode='INFO', text='Waiting for jpg file ' + self._item.type)
        wait_for_file(self._subject.directory_plot + "results_" + self._item.type + ".jpg")


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
