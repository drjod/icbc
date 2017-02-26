import pytest
from glob import glob
from os import path

@pytest.mark.parametrize("computer, code, branch", [
    ("amak", "ogs", "ogs_kb1"),
])
def test_if_log_is_empty(computer, code, branch):
    files = glob(path.join('testingEnviroment', computer, code, branch, 'references', 'deviatingFiles*'))
    assert not files

