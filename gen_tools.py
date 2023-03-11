import linux_tools
from classes import LinuxWindow


def produceFinalProcessList():
    internalSet = linux_tools.produceCurrentWindowSet()
    pList = []

    for item in internalSet:
        coords = linux_tools.getCoordsViaName(item)
        pList.append(LinuxWindow(item,coords[1],coords[2],coords[3],coords[4]))
    return pList