import platform
from enum import Enum
import wgui
import lgui4

def get_current_os():
    return platform.system()

current_os = get_current_os()

match current_os[0].lower():
    case "w":
        wgui.wgui()
    case "l":
        lgui4.lgui()
    case 'm':
        print("Mac not yet supported")

