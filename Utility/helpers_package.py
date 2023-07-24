from subprocess import run, PIPE, call, DEVNULL
from Utility.helpers_path import get_sys_path, get_sys_scripts_folder, get_full_filepath


def install_package(package: str) -> None:
    """
    this installs a package if it doesn't exist

    bradgonesurfing
    https://stackoverflow.com/questions/57593111/how-to-call-pip-from-a-python-script-and-make-it-install-locally-to-that-script

    :param package: package name to ensure is installed
    :return: Nothing
    """
    # noinspection PyBroadException
    try:
        __import__(package)
    except:
        cmd = get_sys_path()
        args = "-m pip install " + package
        call(cmd + " " + args,
             stdout=DEVNULL,
             stderr=DEVNULL)


def exec_package(package: str, args: str) -> bool:
    """
    executes the cli version of an installed python package

    :param package: package name to execute
    :param args: arguments to provide to the package
    :return: return code for failure or success
    """

    cmd = get_full_filepath(get_sys_scripts_folder(), package)
    result = run(cmd + " " + args, capture_output=True, text=True)
    return (not str(result.stderr)) and (result.returncode == 0)
