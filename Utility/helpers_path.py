import os
import shutil
import sys
import glob
from pathlib import Path


def get_rel_path(path: str, common_base: str) -> str:
    """
    returns path with common parent stripped out

    :param path: path to strip out common parent
    :param common_base: common parent
    :return: path with common parent stripped out
    """
    return str(Path(path).relative_to(common_base))


def get_file_stem(file: str) -> str:
    """
    returns file stem

    :param file: filename with or without path
    :return: just the filename without extension
    """
    return Path(file).stem


def replace_extension(file: str, new_ext: str) -> str:
    """
    replaces an extension from a path to another extension

    :param file: file path
    :param new_ext: new extension to replace with
    :return: new file extension
    """

    p = Path(file)
    return str(p.parent) + os.path.sep + p.stem + "." + new_ext


def get_sys_path() -> str:
    """
    returns absolute path to python executable

    :return: absolute path to Python executable
    """
    return sys.executable


def get_sys_folder() -> str:
    """
    returns folder the python executable is in

    :return: absolute path to Python folder
    """
    return Path(get_sys_path()).parent


def get_sys_scripts_folder() -> str:
    """
    returns the system scripts folder

    :return: absolute path to Python scripts folder
    """
    return os.path.join(get_sys_folder(), 'Scripts')


def get_full_filepath(folder: str, base_name: str) -> str:
    """
    this gets an absolute path to a file of an unknown extension

    [Blender]
    https://stackoverflow.com/questions/19824598/open-existing-file-of-unknown-extension?rq=1

    :param folder: absolute path of file
    :param base_name: name of file with unknown extension
    :return: absolute path to file with extension
    """
    return glob.glob(os.path.join(folder, base_name + '.*'))[0]


def ensure_path_created(path: str) -> None:
    """
    ensures folders are created and exist usually before doing work inside them
    [Blair Conrad & Boris]
    https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory

    :param path: The path to ensure exists
    :return: Nothing
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def remove_dir(path: str) -> None:
    """
    removes all folders and files in a directory
    [Varun]
    https://thispointer.com/python-how-to-delete-a-directory-recursively-using-shutil-rmtree/#:~:text=Delete%20all%20files%20in%20a,contents%20of%20a%20directory%20i.e.&text=It%20accepts%203%20arguments%20ignore_errors%2C%20onerror%20and%20path.

    :param path: Path to recursively remove
    :return: Nothing
    """

    # if you want to turn on verification
    # a = input("Are you sure you want to remove the dir: " + path + " [yes/no]: ")
    # if a.lower() != "yes":
    #     sys.exit(1)

    # remove folder and don't error out if it doesn't exist
    try:
        shutil.rmtree(path, ignore_errors=True)
    except:
        pass


def remove_file(path: str) -> None:
    """
    removes a single file

    :param path: file to remove
    :return: Nothing
    """

    # Uncomment if you want to turn on verification
    # a = input("are you sure you want to remove the file: " + path + " [yes/no]: ")
    # if a.lower() != "yes":
    #     sys.exit(1)

    # remove file and don't error out if it doesn't exist
    try:
        os.remove(path)
    except:
        pass
