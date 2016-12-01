from sys import path as syspath
from os import path
syspath.append(path.join(path.dirname(__file__), '..', 'shared'))
from utilities import *


def test_is_in_list_is_true():
    assert is_in_list('c', ['a', 'b', 'c'])


def test_is_in_list_is_false():
    assert not is_in_list('d', ['a', 'b', 'c'])


def test_is_in_list_is_false_for_empty_list():
    assert not is_in_list('d', [])
