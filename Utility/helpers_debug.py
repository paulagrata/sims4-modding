import py_compile
import tempfile
import os
import shutil
from pathlib import Path
from zipfile import PyZipFile, ZIP_STORED

from Utility.helpers_path import get_sys_folder, get_rel_path, remove_file, replace_extension, remove_dir, \
    ensure_path_created
from Utility.helpers_package import install_package

# Sigma1202 https://www.youtube.com/watch?v=RBnS8m0174U
# 2 part process:
# part 1) install the debugging capability, this is located in an egg file, we must modify the egg and then properly
# install it as a mod so the game will load it and gain the ability to debug with PyCharm Pro
# part 2) must get the game to reach out to our editor, this command makes the game reach out to PyCharm Pro
#initiate the debugging connection, and then you're ready to start debugging.
# the command developed is 'pycharm.debug' and hopefully made all of this very easy for the end user.

def debug_ensure_pycharm_debug_package_installed() -> None:
    """
    ensures the debugging package is installed as requested by PyCharm Pro

    :return: Nothing
    """

    print("making sure you have the debugging package installed...")
    install_package("pydevd-pycharm~=202.7319.64")


def debug_install_mod(mod_src: str, mods_dir: str, mod_name: str, mod_folder_name: str) -> None:
    """
    compiles and installs the mod which adds a cheat code so the user can setup the debugger in-game

    :param mod_src: path to the script which does this
    :param mods_dir: path to the users mod folder
    :param mod_name: name of the mod
    :param mod_folder_name: name of mod subfolder
    :return: Nothing
    """

    print("compiling and installing the cheatcode mod...")

    # get destination file path
    mods_sub_dir = os.path.join(mods_dir, mod_folder_name)
    mod_path = os.path.join(mods_sub_dir, mod_name + '.ts4script')

    ensure_path_created(mods_sub_dir)

    # get compiled path and compile mod
    mod_src_pyc = replace_extension(mod_src, "pyc")
    py_compile.compile(mod_src, mod_src_pyc)

    # create mod at destination and add compiled file to it
    zf = PyZipFile(mod_path, mode='w', compression=ZIP_STORED, allowZip64=True, optimize=2)
    zf.write(mod_src_pyc, mod_name + ".pyc")
    zf.close()


def debug_install_egg(egg_path: str, mods_dir, dest_name: str, mod_folder_name: str) -> None:
    """
    copies the debug egg provided by Pycharm Pro which adds the capability to make debugging happen inside of
    pyCharm Pro. A bit of work goes into this so it'll be much slower.

    :param egg_path: path to the debug egg
    :param mods_dir: path to the mods folder
    :param dest_name: name of the mod
    :param mod_folder_name: name of mod subfolder
    :return:
    """

    print("re-packaging and installing the debugging capability mod...")
    # get egg filename and path
    filename = Path(egg_path).name
    mods_sub_dir = os.path.join(mods_dir, mod_folder_name)
    mod_path = os.path.join(mods_sub_dir, dest_name + ".ts4script")

    ensure_path_created(mods_sub_dir)

    # get python ctypes folder
    sys_ctypes_folder = os.path.join(get_sys_folder(), "Lib", "ctypes")

    # create temp directory
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_egg = tmp_dir.name + os.sep + filename

    # remove old mod in mods folder there, if it exists
    remove_file(mod_path)

    # copy egg to temp path
    shutil.copyfile(egg_path, tmp_egg)

    # extract egg
    # find ezr way to do this ->
    zip = PyZipFile(tmp_egg)
    zip.extractall(tmp_dir.name)
    zip.close()

    # remove archive
    remove_file(tmp_egg)

    # copy ctype folder to extracted archive
    shutil.copytree(sys_ctypes_folder, tmp_dir.name + os.sep + "ctypes")

    # remove that one folder
    remove_dir(tmp_dir.name + os.sep + "ctypes" + os.sep + "__pycache__")

    # grab a handle on the egg
    zf = PyZipFile(mod_path, mode='w', compression=ZIP_STORED, allowZip64=True, optimize=2)

    # add all the files in the tmp directory to the zip file
    for folder, subs, files in os.walk(tmp_dir.name):
        for file in files:
            archive_path = get_rel_path(folder + os.sep + file, tmp_dir.name)
            zf.write(folder + os.sep + file, archive_path)

    zf.close()

    # temporary directory bug that causes auto-cleanup to sometimes fail
    # preventing crash messages from flooding the screen to keep things clean
    try:
        tmp_dir.cleanup()
    except:
        pass


def debug_teardown(mods_dir: str, mod_folder_name: str) -> None:
    """
   deletes the 2 mods, they technically cause the running game to slow down

    :param mods_dir: path to mods directory
    :param mod_folder_name: name of mod subfolder
    :return: Nothing
    """

    print("removing the debugging mod files...")
    mods_sub_dir = os.path.join(mods_dir, mod_folder_name)
    remove_dir(mods_sub_dir)
