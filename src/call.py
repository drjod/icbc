from subprocess import call
from shared import message

class Call:
    """
    subprocess call
    """
    @staticmethod
    def execute(command):
        try:
            call(command, shell=True)
        except Exception as err:
            message(mode='ERROR', text="{}".format(err))