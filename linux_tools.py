import subprocess
import os
from Xlib import X, display
import subprocess
import re
import json
import globalTools
"""
d = display.Display()
s = d.screen()
xroot = s.root
window_list = list()
windows = xroot.query_tree().children
"""
blacklist = list()
wmctrlRef = "wmctrl -r"


def getExecutablePath(processIn):
    result = subprocess.run("which " + processIn,
                            shell=True, capture_output=True)
    return result.stdout.decode().strip()


def getWindowList():
    d = display.Display()
    s = d.screen()
    xroot = s.root
    window_list = list()
    windows = xroot.query_tree().children
    for window in windows:
        text = window.get_wm_class()
        window_list.append(text)
    return window_list


def formatList(listIn):
    # use ast.literal_eval() to convert the string to a list of tuples
    tuples_list = tuple(listIn)

    # use list comprehension to extract the second element of each tuple
    result = [x[0] for x in tuples_list if x is not None]

    # use ','.join() to join the list of strings into one string
    # result = ','.join(result)

    with open("blacklist.txt", "r") as blacklist_file:
        window_set = set(result)
        window_set.difference_update(blacklist_file)

    return window_set


def applyBlacklist(setIn):
    # Read the blacklist from the file
    with open("blacklist.txt", "r") as file:
        blacklist = file.read().splitlines()

    # Compile the blacklist into a set of regular expressions
    blacklist = {re.compile(item) for item in blacklist}

    # Create a new set containing only items that don't match the blacklist
    differenced_set = {x for x in setIn if not any(
        pattern.match(x) for pattern in blacklist)}

    return differenced_set


def produceCurrentWindowSet():
    window_list_active = getWindowList()
    lowercase_list_active = [
        (x[0], x[1].lower()) if x is not None else None for x in window_list_active]
    window_set_active = set(lowercase_list_active)
    window_set_active = formatList(window_set_active)
    lowercase_set_active = {item.lower() for item in window_set_active}

    lowercase_set_active.discard('')

    # remove more blacklisted items
    """
    for p in patternlist:
        lowercase_set_active = {x for x in lowercase_set_active if not p.match(x)}
    """
    setOut = applyBlacklist(lowercase_set_active)

    return setOut


"""
def produceFinalList():
    internalSet = produceCurrentWindowSet()
    pList = []
    for item in internalSet:
        pList.append(item,0,0,0,0)
"""


def cleanWindow(window_name_in):
    ref = ["wmctrl", "-r"]
    command_list_fullscreen = ref.copy()
    command_list_fullscreen.extend([window_name_in, "-b", "remove,fullscreen"])
    command_list_vert = ref.copy()
    command_list_vert.extend([window_name_in, "-b", "remove,maximized_vert"])
    command_list_horz = ref.copy()
    command_list_horz.extend([window_name_in, "-b", "remove,maximized_horz"])
    command_list_size = ref.copy()
    command_list_size.extend([window_name_in, "-e", "0,900,0,1280,720"])
    command_list = [command_list_fullscreen, command_list_horz,
                    command_list_vert, command_list_size]

    for command in command_list:
        subprocess.run(command)


def getExecDir(nameIn):
    try:
        output = subprocess.check_output(["which", nameIn]).decode().strip()
        #output = os.get_exec_path(nameIn)
    except:
        output = None
    return output


def create_script(linuxWindowsIn):
    sleepLine = "sleep 2 && \n"
    initialScriptName = "initial_script.sh"

    f = open(initialScriptName, "w")
    f.write("#!/bin/sh \n")

    for p in linuxWindowsIn:
        f.write(p.path + " & \n")
    f.write(sleepLine)  # CONTINUE FROM HERE
    f.close()
    scriptWindowLines(linuxWindowsIn, initialScriptName)


def scriptWindowLines(windowListIn, scriptFileIn):
    f = open(scriptFileIn, "a")
    lineList = []

    for window in windowListIn:
        lineList.append("{} {} {} {} &&\n".format(
            "wmctrl -r", window.name, "-e", window.stringCoords))

    f.writelines(lineList)


def addAnd(fileIn):
    f = open(fileIn, "a")


def addNewLine(fileIn):
    f = open(fileIn, "a")
    f.write("\n")


def extractNumericalCoordsFromLine(line):
    if line == None:
        return None
    pattern = r'^0x[0-9a-fA-F]+ +(\d) +(\d+) +(\d+) +(\d+) +(\d+).*'
    match = re.match(pattern, line)
    stringActive = None
    if match:
        groups = match.groups()
        stringActive = ','.join(groups)
    else:
        return None

    lst = [int(x) for x in stringActive.split(',')]
    return lst


def getLinesForWindows():
    rawString = subprocess.run("wmctrl -lG", capture_output=True, shell=True)
    return rawString.stdout.decode().split('\n')


def containsString(string, substring):
    return substring in string


def getLineForProcess(linesIn, processNameIn):
    lineOut = None
    for l in linesIn:
        lineLower = l.lower()
        if containsString(lineLower, processNameIn.lower()) == True:
            lineOut = lineLower
    return lineOut


def getCoordsViaName(nameIn):
    windowLines = getLinesForWindows()
    lineInQuestion = getLineForProcess(windowLines, nameIn)
    coords = extractNumericalCoordsFromLine(lineInQuestion)
    if coords == None:
        coords = [0, 0, 0, 1280, 720]
    return coords


def isProcessRunning(processName):
    processSet = produceCurrentWindowSet()
    if processName in processSet:
        return True
    return False


def getFullPathFromPs(psIn):
    text = subprocess.run("ps {}".format(
        psIn), capture_output=True, shell=True)
    pattern = re.compile(r"/[^ ]*")
    match = pattern.search(str(text))
    if match:
        directory = match.group(0)
        return directory
    return None

"""
def getJsonCount():
    cwd = os.getcwd()
    jsonCount = 0
    for file in os.listdir(cwd):
        if file.endswith('.json'):
            jsonCount += 1
    return int(jsonCount)
"""

"""
def writeStackToJson(stackIn):
    writeName = "{}_{}".format(stackIn.name, globalTools.getJsonCount())
    with open(("{}.json".format(writeName)), 'w') as f:
        json.dump(stackIn.to_json(), f, indent=4)
"""

def calcGUIRows(buttonsIn):
    return len(buttonsIn)//3


""" Fulfill this method later
def getAllWindowCoords():
    result = subprocess.run("which " + processIn,
                            shell=True, capture_output=True)
    return None
"""

# addNewLine("initial_script.sh")

"""f = open("demofile2.txt", "a")
f.write("Now the file has more content!")
f.close()

#open and read the file after the appending:
f = open("demofile2.txt", "r")
print(f.read()) """
