import platform
import asyncio
import importlib

def get_current_os():
    return platform.system()

def run_appropriate_gui_module():
    current_os = get_current_os()
    cos_first_letter = current_os[0].lower()

    if cos_first_letter == "w":
        gui_module_name = "wgui"
    elif cos_first_letter == "l":
        gui_module_name = "lgui4"
    else:
        print("Mac not yet supported")
        return

    gui_module = importlib.import_module(gui_module_name)
    asyncio.run(gui_module.main())

run_appropriate_gui_module()
