from paramiko import SSHClient, AutoAddPolicy
from pysftp import Connection
from shared import message
from os import path, getcwd, chdir
from sys import stdout, path as syspath
if not path.join(path.dirname(__file__), 'access') in syspath:
    syspath.append(path.join(path.dirname(__file__), 'access'))


class GateToCluster:

    __ssh = None
    __sftp = None

    @property
    def ssh(self):
        return self.__ssh

    @property
    def sftp(self):
        return self.__sftp

    def __init__(self, subject):
        """
        connect via ssh and sftp to cluster (subject)
        connection closes when instance is destruced (by __del__)
        :param subject: (class Subject)
        """
        self.__cluster_name = subject.computer

        mod = __import__(self.__cluster_name)  # module with password

        self.__ssh = SSHClient()
        self.__ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            message('INFO', 'Connect to {}'.format(self.__cluster_name))
            self.__ssh.connect(hostname=subject.hostname, port=22, password=mod.pwd, username=subject.user)
            self.__sftp = Connection(host=subject.hostname, password=mod.pwd, username=subject.user)
        except Exception as err:
            message(mode='ERROR', text=str(err))

    def operate(self, command):
        """
        run command on cluster
        (called in operation.execute() if operation is for remote conputer)
        :param command: (string)
        :return:
        """
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self.__ssh.exec_command(command)

            for line in ssh_stdout.readlines():
                stdout.write(line)
                stdout.flush()

            for line in ssh_stderr.readlines():
                stdout.write(line)
                stdout.flush()

        except Exception as err:
            message(mode='ERROR', text=str(err))

    def upload_file(self, file, destination_file):
        """
        run scp put command
        :param file: (string)
        :param destination_file: (string)
        :return:
        """
        try:
            self.__sftp.put(file, destination_file)  # , preserve_mtime=True)
        except Exception as err:
            message('ERROR', str(err))

    def download_file(self, file, destination_folder):
        """
        run scp get command
        :param file: (string)
        :param destination_folder: (string)
        :return:
        """
        try:
            pth = getcwd()
            chdir(destination_folder)
            self.__sftp.get(file, preserve_mtime=True)
            chdir(pth)
        except Exception as err:
            message('ERROR', str(err))

    def __del__(self):
        self.__ssh.close()
        self.__sftp.close()
        message('INFO', 'Disconnect from {}'.format(self.__cluster_name))
