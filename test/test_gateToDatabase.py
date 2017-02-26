if not path.join(path.dirname(__file__), 'src') in syspath:
    syspath.append(path.join(path.dirname(__file__), 'src'))
from gateToDatabase import GateToDatabase
from setting import Database

import os

db_inst = Database('jens', 'so3bt4jc', 'localhost', 'testing_environment')
gateToDatabase = GateToDatabase(db_inst)


def test_flow_process_name_list_query():
    #assert gateToDatabase.query_flow_process_name_list('') is None
    assert gateToDatabase.query_flow_process_name_list('1_1_1') == ['LIQUID_FLOW']


def test_element_type_name_list_query():
    #assert gateToDatabase.query_element_type_name_list('','') is None
    #assert gateToDatabase.query_element_type_name_list('diffusion_xy', '') is None
    #assert gateToDatabase.query_element_type_name_list('diffusion_xy', []) is None
    #assert gateToDatabase.query_element_type_name_list('diffusion_xy', ['a']) is None
    assert gateToDatabase.query_element_type_name_list('diffusion_xy',['LIQUID_FLOW']) == \
           ([['quad', 'tri']] or [['tri', 'quad']])
    assert gateToDatabase.query_element_type_name_list('diffusion_xy',['LIQUID_FLOW', 'RICHARDS_FLOW']) == \
           [['quad', 'tri'],['quad', 'tri']] or [['tri', 'quad'],['quad', 'tri']] or \
           [['quad', 'tri'], ['tri', 'quad']] or [['tri', 'quad'], ['tri', 'quad']]


def test_column_entry_query():
    #assert gateToDatabase.query_computer_data('amak', '') is None
    assert gateToDatabase.query_column_entry('computer', 'amak', 'remote_flag') is False
    assert gateToDatabase.query_column_entry('computer', 'amak', 'hostname') == 'localhost'
    assert gateToDatabase.query_column_entry('computer', 'amak', 'root_directory') == '/home/jens'


def test_user_name_query():
    #assert gateToDatabase.query_username('', '') is None
    assert gateToDatabase.query_username('jens', 'amak') == 'jens'
    assert gateToDatabase.query_username('jens', 'rzcluster') == 'sungw389'


#####################################################


def test_foo(mocker):
    # all valid calls
    mocker.patch('os.remove')
    mocker.patch.object(os, 'listdir', autospec=True)
    mocked_isfile = mocker.patch('os.path.isfile')


def test_spy(mocker):
    class Foo(object):
        def bar(self):
            return 42

    foo = Foo()
    mocker.spy(foo, 'bar')

    assert foo.bar() == 42
    assert foo.bar.call_count == 1


def test_stub(mocker):
    def foo(on_something):
        on_something('foo', 'bar')

    stub = mocker.stub(name='on_something_stub')

    foo(stub)
    stub.assert_called_once_with('foo', 'bar')