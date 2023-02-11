import linux_tools
from classes import LinuxWindow


def produce_final_list():
    internalSet = linux_tools.produce_final_set()
    pList = []
    for item in internalSet:
        print(item)
        print(type(item))
        pList.append(LinuxWindow(item,0,0,0,0))
    return pList