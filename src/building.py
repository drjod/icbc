from operation import Operation
from collections import OrderedDict
from shared import message
from os import path


class Building(Operation):
    """

    """
    def __init__(self, subject):
        """
        :param subject: (class Subject)
        """
        self._selected_operation_type = 'b'

        self._operation_dict = OrderedDict([('b', '(b)uild'),
                                            ('u', '(u)pdate'),
                                            ('c', '(c)lear'),
                                            ('g', 'show re(g)ression'),
                                            ('w', '(w)ait'),
                                            ('s', 're(s)elect')])
        Operation.__init__(self, subject)

    def configure(self):
        pass

    def configure_for_item(self, item_type, item_case, item_configuration,
                           flow_process_name, element_type_name, setting_inst):
        pass

    def run(self, item):
        """
        configure build and call operation for this build
        :param item: (class Item)
        :return:
        """
        self._item = item

        if self._selected_operation == 'b':
            self.build()
        elif self._selected_operation == 'u':
            self.update_release()
        elif self._selected_operation == 'c':
            self.clear_folder()
        elif self._selected_operation == 'g':
            self.show_regression()
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

        self.execute(self._subject.get_build_command(self._item))

    def update_release(self):
        """
        copy built files in special folder and rename them for release
        generate new release folder if it does not exist
        :return:
        """
        message(mode='INFO', text='Updating release {}'.format(self._item.configuration))

        self.execute_python('generate_folder', path.join(self._subject.directory, 'releases'))
        self.execute_python('copy_file', self._subject.get_built_file(self._item),
                            self._subject.get_built_file_for_release(self._item))

    def clear_folder(self):
        """
        delete built files (from folder where they are after compilation)
        :return:
        """
        message(mode='INFO', text='Removing release {}'.format(self._item.configuration))

        self.execute_python('remove_file', self._subject.get_built_file(self._item), False)

    def show_regression(self):
        """
        reads file where regression is documented
        :return:
        """
        message(mode='INFO', text='Show regression {}'.format(self._item.configuration))

        file = path.join(self._subject.root_directory, 'testingEnvironment',
                         self._subject.computer, self._subject.code, self._subject.branch,
                         'references', 'deviatingFiles_{}.log'.format(self._item.configuration))
        self.execute_python('show_file_content', file)


    def wait(self):
        """
        wait until release exists
        :return:
        """
        message(mode='INFO', text='Waiting for release {}'.format(self._item.configuration))

        self.execute_python('wait_for_file', self._subject.get_built_file(self._item))
