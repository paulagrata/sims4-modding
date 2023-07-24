# core imports
import os
import fnmatch
import shutil
import tempfile
from zipfile import PyZipFile
from pathlib import Path

# helpers
from Utility.helpers_path import replace_extension, get_rel_path, get_file_stem, ensure_path_created
from Utility.helpers_package import install_package, exec_package
from Utility.helpers_time import get_time, get_time_str, get_minutes

# globals
script_package_types = ['*.zip', '*.ts4script']
python_compiled_ext = "*.pyc"

# global counts and timings for all the tasks
total_suc_count = 0
total_fail_count = 0
total_count = 0
total_minutes = 0


def decompile_pre() -> None:
    """
    ensure uncompyle6 is installed and install it if not
    do this first because installation can create an error

    :return: Nothing
    """

    print("checking for decompiler and installing if needed...")
    install_package("uncompyle6")


def decompile_dir(src_dir: str, dest_dir: str, filename: str) -> None:
    """
    decompiles a directory of compiled python files to a different directory
    modified from andrew's code.
    https://sims4studio.com/thread/15145/started-python-scripting

    :param src_dir: path of dir to decompile
    :param dest_dir: path of dir to send decompiled files to
    :param filename: original filename of what's being decompiled (progress output purposes)
    :return: Nothing
    """

    # gain R/W to global counts and timing
    global total_suc_count
    global total_fail_count
    global total_count
    global total_minutes

    # begin clock
    time_start = get_time()

    print("decompiling " + filename)

    # local counts for this one task
    col_count = 0
    suc_count = 0
    fail_count = 0
    count = 0

    # go through each compiled python file in the folder
    for root, dirs, files in os.walk(src_dir):
        for filename in fnmatch.filter(files, python_compiled_ext):

            # get details about the source file
            src_file_path = str(os.path.join(root, filename))
            src_file_rel_path = get_rel_path(src_file_path, src_dir)

            # create destination file path
            dest_file_path = replace_extension(dest_dir + os.path.sep + src_file_rel_path, "py")

            # and ensures the folders exist so there's no error
            # make sure to strip off the file name at the end
            ensure_path_created(str(Path(dest_file_path).parent))

            # decompile it to destination
            success = exec_package("uncompyle6",
                                   "-o " + '"' + dest_file_path + '"' + " " +
                                   '"' + src_file_path + '"')

            # print progress
            # prints a single dot on the same line which gives a nice clean progress report
            # tally number of files and successful / failed files
            if success:
                print(".", end="")
                suc_count += 1
                total_suc_count += 1
            else:
                print("x", end="")
                fail_count += 1
                total_fail_count += 1

            count += 1
            total_count += 1

            # insert a new progress line every 80 characters
            col_count += 1
            if col_count >= 80:
                col_count = 0
                print("")

    time_end = get_time()
    elapsed_minutes = get_minutes(time_end, time_start)
    total_minutes += elapsed_minutes

    # print a newline and then a compact completion message giving successful, failed, and total count stats and timing
    print("")
    print("")
    print("completed")
    print("S: " + str(suc_count) + " [" + str(round((suc_count/count) * 100, 2)) + "%], ", end="")
    print("F: " + str(fail_count) + " [" + str(round((fail_count/count) * 100, 2)) + "%], ", end="")
    print("T: " + str(count) + ", ", end="")
    print(get_time_str(elapsed_minutes))
    print("")


def decompile_zip(src_dir: str, filename: str, dst_dir: str) -> None:
    """
    copies a zip file to a temporary folder, extracts it, and then decompiles it to the projects folder
    modified from andrew's code.
    https://sims4studio.com/thread/15145/started-python-scripting

    :param src_dir: source directory for zip file
    :param filename: zip filename
    :param dst_dir: destination for unzipped files
    :return: Nothing
    """

    # create paths and directories
    file_stem = get_file_stem(filename)

    src_zip = os.path.join(src_dir, filename)
    dst_dir = os.path.join(dst_dir, file_stem)

    tmp_dir = tempfile.TemporaryDirectory()
    tmp_zip = os.path.join(tmp_dir.name, filename)

    # copy zip to temp path
    shutil.copyfile(src_zip, tmp_zip)

    # grab handle to zip file and extract all contents to the same folder
    zip = PyZipFile(tmp_zip)
    zip.extractall(tmp_dir.name)

    # decompile the directory
    decompile_dir(tmp_dir.name, dst_dir, filename)

    # there's a temporary directory bug that causes auto-cleanup to sometimes fail
    # we're preventing crash messages from flooding the screen to keep things tidy
    try:
        tmp_dir.cleanup()
    except:
        pass


def decompile_zips(src_dir: str, dst_dir: str) -> None:
    """
    decompiles a folder of zip files to a destination folder
    modified from andrew's code.
    https://sims4studio.com/thread/15145/started-python-scripting

    :param src_dir: directory to search for and decompile zip files
    :param dst_dir: directory to send decompiled files to
    :return: Nothing
    """
    for root, dirs, files in os.walk(src_dir):
        for ext_filter in script_package_types:
            for filename in fnmatch.filter(files, ext_filter):
                decompile_zip(root, filename, dst_dir)


def decompile_print_totals() -> None:
    print("results")

    # fix Bug #1
    # https://github.com/junebug12851/Sims4ScriptingBPProj/issues/1
    try:
        print("S: " + str(total_suc_count) + " [" + str(round((total_suc_count / total_count) * 100, 2)) + "%], ", end="")
        print("F: " + str(total_fail_count) + " [" + str(round((total_fail_count / total_count) * 100, 2)) + "%], ", end="")
        print("T: " + str(total_count) + ", ", end="")
        print(get_time_str(total_minutes))
    except:
        print("no files were processed, an error has occurred. Is the path to the game folder correct?")
        pass

    print("")
