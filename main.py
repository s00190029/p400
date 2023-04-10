import platform
import asyncio
from enum import Enum

def get_current_os():
    return platform.system()

current_os = get_current_os()
cos_first_letter =  current_os[0].lower()

match cos_first_letter:
    case "w":
        import wgui
        asyncio.run(wgui.wgui())
    case "l":
        import lgui4
        asyncio.run(lgui4.lgui())
    case 'm':
        print("Mac not yet supported")

