import fnmatch

from pathlib import Path

import os
import sims4.commands
from sims4.reload import reload_file


def reload_folder(path: str) -> None:
    """
    reloads all the python files in a folder and all sub-folders

    :param path: folder to reload
    :return: Nothing
    """

    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, "*.py"):
            reload_file(root + os.sep + filename)


@sims4.commands.Command('devmode.reload', command_type=sims4.commands.CommandType.Live)
def _devmode_reload(module: str = "", _connection: int = None) -> None:
    """
    provides functionality to reload a module while in devmode

    type in:
    devmode.reload [path.of.module] to reload the module

    :param module: path of the module to reload
    :param _connection: provided by the game
    :return: Nothing
    """

    # get ability to write to the cheat console and build path to project folder
    output = sims4.commands.CheatOutput(_connection)
    project_folder = str(Path(__file__).parent.parent)

    # stop here if a module path wasn't given, in this case reload the whole project
    if not module:
        reload_folder(os.path.join(project_folder, "Scripts"))
        output("Reloaded entire project")
        return

    # convert module path to a path and build a reload path
    sub_path = module.replace(".", os.sep)
    reload_path = os.path.join(project_folder, "Scripts", sub_path)

    # if it's a folder that exists reload the whole folder
    if os.path.exists(reload_path):
        if os.path.isdir(reload_path):
            reload_folder(reload_path)
            print("Reloaded Folder: " + sub_path)
            return
        else:
            print("Unknown file to reload" + sub_path)
            return

    # assume it's a python file

    # if it doesn't exist then warn the user and stop here
    if not os.path.exists(reload_path + ".py"):
        output("Error: The file or folder doesn't exist to reload")
        output(sub_path + "[.py]")
        return

    # issue the reloading and notify user
    reload_file(reload_path + ".py")
    output("Reloaded: " + sub_path + ".py")
