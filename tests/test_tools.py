import linux_tools
import unittest


def test_getExecutablePath() -> None:
    processName = "man"
    processDirectory = linux_tools.getExecDir(processName)
    assert processDirectory == "/usr/bin/man"

def test_apply_blacklist() -> None:
    setToBeFiltered = set(open('blacklist.txt'))
    filteredSet = linux_tools.applyBlacklist(setToBeFiltered)
    assert len(filteredSet) == 0

def test_calcGUIRows() -> None:
    assert linux_tools.calcGUIRows([]) == 0  
    assert linux_tools.calcGUIRows([1, 2]) == 0
    assert linux_tools.calcGUIRows([1, 2, 3]) == 1
    assert linux_tools.calcGUIRows([1, 2, 3, 4]) == 1
    assert linux_tools.calcGUIRows([1, 2, 3, 4, 5]) == 1
    assert linux_tools.calcGUIRows([1, 2, 3, 4, 5, 6]) == 2
    assert linux_tools.calcGUIRows([1, 2, 3, 4, 5, 6, 7]) == 2
    assert linux_tools.calcGUIRows([1, 2, 3, 4, 5, 6, 7, 8]) == 2 
    assert linux_tools.calcGUIRows([1, 2, 3, 4, 5, 6, 7, 8, 9]) == 3
