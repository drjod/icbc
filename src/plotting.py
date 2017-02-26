from os import path, listdir
from collections import OrderedDict
from shared import message, Commands
from configuration import inputFileEndings, outputFile, outputFileEndings, additionalInputFileEndings, examplesName
from operation import Operation
from call import Call

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

        self._operation_dict = OrderedDict([('n', 'replace (n)ans and inds'),
                                            ('c', '(c)lear folder'),
                                            ('w', '(w)ait'),
                                            ('s', 're(s)elect')])
        if subject.remote_flag:
            option_dict_amendments = {'g': '(g)et results'}
            self._operation_dict.update(option_dict_amendments)

        Operation.__init__(self, subject)

    def configure(self):
        pass

    def configure_for_item(self, item_type, item_case, item_configuration,
                       flow_process_name, element_type_name, setting_inst):
        pass

    def run(self, item):
        """
        link to specific operation
        :param item: (class Item)
        :return:
        """
        self._item = item

        if self._selected_operation == 'g':
            self.get_results()
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
        :return:
        """
        if self._subject.remote_flag:
            message(mode='INFO', text='Get results {}'.format(self._item.name()))

            directory_local = self._item.directory_local

            Commands.generate_folder(directory_local)
            self._gateToCluster.download_file(
                path.join(self._item.directory, 'results.tar'), directory_local)

            #command = 'python {}'.format(path.join(self._subject.icbc_directory, 'shared.py')) + ' unpack_tar_file ' + path.join(directory_local, 'results.tar')
            #Call(command)
            Commands.unpack_tar_file(directory_local)
        else:
            message(mode='INFO', text='{} is local - Nothing done'.format(self._subject.computer))

    def replace_nans_and_inds(self):
        """
        replace each nan by 999 and remove each IND in all tec files
        :return:
        """
        message(mode='INFO', text='Replace nans and inds {}'.format(self._item.name()))

        directory_local = self._item.directory_local

        for file_name in listdir(directory_local):
            if file_name.endswith('.tec'):
                message(mode='INFO', text='    File: {}'.format(file_name))
                try:
                    infile = open(path.join(directory_local, file_name), 'r')
                    outfile = open(path.join(directory_local, 'new_{}'.format(file_name)), 'w')
                except Exception as err:
                    message(mode='ERROR', text='{}'.format(err))
                else:
                    for line in infile:
                        line = line.replace('nan', '999')
                        line = line.replace('#IND', '888')
                        outfile.write(line)
                    infile.close()
                    outfile.close()
                    Commands.move_file(path.join(directory_local, 'new_{}'.format(file_name)),
                                       path.join(directory_local, file_name))

    def clear_folder(self):
        """
        delete *.tec, *.txt, *.asc, and results.tar from plotting folder

        (local folder of remote computer)
        :return:
        """
        message(mode='INFO', text='Clear plotting folder {}'.format(self._item.name()))

        directory_local = self._item.directory_local
        #
        for file in listdir(directory_local):
            for ending in outputFileEndings:
                if file.endswith('.{}'.format(ending)):
                    Commands.remove_file(path.join(directory_local, file), False)

        Commands.remove_file(path.join(directory_local, 'results.tar'), False)

    def wait(self):
        """
        wait until jpg file is in folder
        :return:
        """
        message(mode='INFO', text='Waiting for output file {}'.format(self._item.name()))
        Commands.wait_for_file(path.join(self._item.directory_local, outputFile))

