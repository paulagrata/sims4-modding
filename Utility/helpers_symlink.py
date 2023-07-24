from Utility.helpers_path import remove_dir, ensure_path_created
from pathlib import Path

import os
from subprocess import run


def get_scripts_path(creator_name: str, mods_dir: str, mod_name: str = "Untitled") -> str:
    """
    this builds a path to the Scripts folder inside the Mod Folder

    :param creator_name: cCreator Name
    :param mods_dir: path to the mods folder
    :param mod_name: name of mod
    :return: path to scripts folder inside mod name folder
    """

    # creator_name can be omitted, if it's not then prefix it
    if creator_name:
        mod_name = creator_name + '_' + mod_name

    # build absolute path to mod name folder
    mods_sub_dir = os.path.join(mods_dir, mod_name)

    # return path to scripts folder inside mod name folder
    return os.path.join(mods_sub_dir, "Scripts")


def exec_cmd(cmd: str, args: str) -> bool:
    """
    this executes a system command and returns whether it was successful or not

    :param cmd: vommand to execute
    :param args: any arguments to command
    :return: successful or not
    """

    # result object of the command
    # if an error occurs, this will be the value used
    result = None

    try:
        # run the command and capture output
        result = run(cmd + " " + args,
                     capture_output=True,
                     text=True,
                     shell=True)
    except:
        pass

    # if the command completely crashed then return false
    if result is None:
        return False

    # otherwise return false if stderr contains error messages and/or the return code is not 0
    return (not str(result.stderr)) and (result.returncode == 0)


def symlink_exists_win(creator_name: str, mods_dir: str, mod_name: str = "Untitled") -> bool:
    """
    checks to see if a scripts folder or file exists inside the mod Folder

    :param creator_name: creator name
    :param mods_dir: path to the mods folder
    :param mod_name: name of mod
    :return: whether a "scripts" file or folder does exist in the mod folder
    """

    scripts_path = get_scripts_path(creator_name, mods_dir, mod_name)
    return os.path.exists(scripts_path)


def symlink_remove_win(creator_name: str, mods_dir: str, mod_name: str = "Untitled") -> None:
    """
    safely removes the Mod Name Folder
    /Mods/ModName/

    ***always use this function to remove the Mod Name Folder***

    :param creator_name: creator Name
    :param mods_dir: path to the mods folder
    :param mod_name: name of Mod
    :return: Nothing
    """

    # build paths
    scripts_path = get_scripts_path(creator_name, mods_dir, mod_name)
    mod_folder_path = str(Path(scripts_path).parent)

    # check whether the scripts folder exists
    exists = symlink_exists_win(creator_name, mods_dir, mod_name)

    # delete the scripts folder and check whether it was successful
    success = exec_cmd("rmdir", '"' + scripts_path + '"')

    # if the scripts folder exists but could not be deleted then print an error message and raise an exception
    if exists and not success:
        print("")
        print("error: scripts folder exists but can't be removed... did you create a scripts folder inside the mod "
              "Folder at: ")
        print(scripts_path)
        print("if so, please manually delete it and try again.")
        print("")
        raise

    # otherwise remove the directory
    remove_dir(mod_folder_path)


def symlink_create_win(creator_name: str, src_dir: str, mods_dir: str, mod_name: str = "Untitled") -> None:
    """
    creates a symlink, it first wipes out the mod that may be there. when entering devmode, you don't compile anymore,
    so any compiled code needs to be removed.

    :param creator_name: creator Name
    :param src_dir: path to the source folder in this project
    :param mods_dir: path to the mods Folder
    :param mod_name: name of Mod
    :return: Nothing
    """

    # build paths
    scripts_path = get_scripts_path(creator_name, mods_dir, mod_name)
    mod_folder_path = str(Path(scripts_path).parent)

    # safely remove folder with symlink
    symlink_remove_win(creator_name, mods_dir, mod_name)

    # re-create folder
    ensure_path_created(mod_folder_path)

    # create scripts folder as a directory junction
    exec_cmd("mklink",
             '/J ' +
             '"' + scripts_path + '" '
             '"' + src_dir + '"')

    print("")
    print("dev Mode is activated, you no longer have to compile after each change, run devmode.reload [path.of.module]")
    print("to reload individual files while the game is running. To exit dev mode, simply run 'compile.py' which will")
    print("return things to normal.")
    print("recomended to test a compiled version before final release after working in Dev Mode")
    print("")
