import pytest
from glob import glob

@pytest.mark.parametrize("computer, code, branch", [
    ("amak", "ogs", "ogs_kb1"),
])
def test_if_log_is_empty(computer, code, branch):
    files = glob("F:\\testingEnvironment\\{}\\{}\\{}\\references\\deviatingFiles*".format(computer, code, branch))
    assert not files

