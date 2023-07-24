# import core packages
import fnmatch
import os
import shutil
import py_compile
from zipfile import PyZipFile, ZIP_STORED

from Utility.helpers_path import remove_file, ensure_path_created, get_rel_path, replace_extension, remove_dir
from Utility.helpers_symlink import symlink_remove_win, symlink_exists_win


def compile_slim(src_dir: str, zf: PyZipFile) -> None:
    """
    compiles a slim mod (Contains only the pyc files)
    modified from andrew's code.
    https://sims4studio.com/thread/15145/started-python-scripting

    it is not reccomended to use this function because it's not reccomended to only have pyc files in your project
    as it makes your project less flexible. going forward this will not be called by default.

    :param src_dir: source folder
    :param zf: Zip File Handle
    :return: Nothing
    """

    for folder, subs, files in os.walk(src_dir):
        for filename in fnmatch.filter(files, '*.py'):
            file_path_py = folder + os.sep + filename
            file_path_pyc = replace_extension(file_path_py, "pyc")
            rel_path_pyc = get_rel_path(file_path_pyc, src_dir)

            py_compile.compile(file_path_py, file_path_pyc)
            zf.write(file_path_pyc, rel_path_pyc)
            remove_file(file_path_pyc)


def compile_full(src_dir: str, zf: PyZipFile) -> None:
    """
    compiles a full mod (Contains all files in source including python files which it then compiles
    modified from andrew's code.
    https://sims4studio.com/thread/15145/started-python-scripting

    :param src_dir: source folder
    :param zf: zip File Handle
    :return: Nothing
    """

    for folder, subs, files in os.walk(src_dir):
        for filename in fnmatch.filter(files, '*.py'):
            file_path_py = folder + os.sep + filename
            file_path_pyc = replace_extension(file_path_py, "pyc")
            rel_path_pyc = get_rel_path(file_path_pyc, src_dir)

            py_compile.compile(file_path_py, file_path_pyc)
            zf.write(file_path_pyc, rel_path_pyc)
            remove_file(file_path_pyc)
        for filename in fnmatch.filter(files, '*[!p][!y][!c]'):
            rel_path = get_rel_path(folder + os.sep + filename, src_dir)
            zf.write(folder + os.sep + filename, rel_path)


def compile_src(creator_name: str, src_dir: str, build_dir: str, mods_dir: str, mod_name: str = "Untitled") -> None:
    """
    packages your mod into a proper mod file. It creates 2 mod files, a full mod file which contains all the files
    in the source folder unchanged along with the compiled python versions next to uncompiled ones and a slim mod-file
    which contains only the compiled versions.

    modified from andrew's code.
    https://sims4studio.com/thread/15145/started-python-scripting

    :param creator_name: the creators name
    :param src_dir: source dir for the mod files
    :param build_dir: place to put the mod files
    :param mods_dir: place to an extra copy of the slim mod file for testing
    :param mod_name: name to call the mod
    :return: Nothing
    """

    # prepend creator name to mod name
    mod_name = creator_name + '_' + mod_name
    mods_sub_dir = os.path.join(mods_dir, mod_name)

    # create ts4script paths
    ts4script_full_build_path = os.path.join(build_dir, mod_name + '.ts4script')
    ts4script_mod_path = os.path.join(mods_sub_dir, mod_name + '.ts4script')

    print("clearing out old builds...")

    # delete and re-create build and sub-folder in Mods
    is_devmode = symlink_exists_win("", mods_dir, mod_name)
    symlink_remove_win("", mods_dir, mod_name)

    if is_devmode:
        print("exiting Dev Mode...")

    remove_dir(build_dir)

    ensure_path_created(build_dir)
    ensure_path_created(mods_sub_dir)

    print("re-building mod...")

    # compile the mod
    zf = PyZipFile(ts4script_full_build_path, mode='w', compression=ZIP_STORED, allowZip64=True, optimize=2)
    compile_full(src_dir, zf)
    zf.close()

    # copy it over to the mods folder
    shutil.copyfile(ts4script_full_build_path, ts4script_mod_path)

    print("----------")
    print("complete")
