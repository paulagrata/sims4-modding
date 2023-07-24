import fnmatch
import os

from settings import projects_tuning_path

# for pretty progress and results
col_count = 0
suc_count = 0
fail_count = 0
skip_count = 0
count = 0

failed_filename_list = []


def loop_end() -> None:
    """
    completed one iteration of a loop, this handles pretty progress and output

    :return: Nothing
    """

    global count
    global col_count

    count += 1
    col_count += 1
    if col_count >= 80:
        col_count = 0
        print("")


def attempt_rename(from_path: str, to_folder: str, to_file_stem: str) -> None:
    """
    attempts a rename, and if the file exists, tries to append increasing letters to the end to make the rename
    happen. if the rename still cannot happen it throws an error.

    :param from_path: Path to file which needs renaming
    :param to_folder: Path to same folder file is in
    :param to_file_stem: New name of file without extension

    :return: Nothing
    """

    # suffixes to append to the filename, in order, when a rename fails
    attempts = ['', '_a', '_b', '_c', '_d']

    # whether it was successful, a failed rename means we need to throw an error
    success = False

    # loop through each of the suffixes, the first suffix is empty because we always try no suffix first
    # and attempt the rename
    for attempt in attempts:
        try:
            os.rename(from_path, to_folder + os.sep + to_file_stem + attempt + ".xml")
            success = True
            break
        except:
            pass

    # throw error if success is still false meaning we went through all the possible suffix options and it still didn't
    # work
    if not success:
        raise NameError("Failed to rename file")


def begin_fix() -> None:
    """
    function that does everything, loops through a Tunings folder and renames the tuning files to be in plain
    english.

    :return: Nothing
    """

    global suc_count
    global fail_count
    global skip_count
    global failed_filename_list

    print("fixing filenames...")
    print("")

    # go through all the files in all the folders in the Tuning folder
    for folder, subs, files in os.walk(projects_tuning_path):
        for filename in fnmatch.filter(files, '*.xml'):

            # break it up into pieces. the files are separated by dots
            # this goes from
            # "03B33DDF!00000000!0D94E80BE40B3604.sims.loan_tuning.Tuning.xml"
            # to
            # ["03B33DDF!00000000!0D94E80BE40B3604", "sims", "loan_tuning", "Tuning", "xml"]
            new_filename = filename.split(".")

            # do a check to see if this file is already fixed
            # a fixed file will only have one dot, the extension. Skip if it's already fixed
            if len(new_filename) <= 2:
                print("_", end="")
                skip_count += 1
                loop_end()
                continue

            # this magic mangles the split filename to go from
            # "03B33DDF!00000000!0D94E80BE40B3604.sims.loan_tuning.Tuning.xml"
            # to
            # "sims_loan_tuning.xml"
            # Much prettier don't you agree?
            new_filename.pop(0)
            new_filename.pop()
            new_filename.pop()
            new_filename = "_".join(new_filename)

            # this does the renaming, if the renamer function fails after all renaming attempts then chalk it up
            # to a failure and report it
            try:
                attempt_rename(folder + os.sep + filename, folder, new_filename)
                print(".", end="")
                suc_count += 1
            except:
                print("x", end="")
                fail_count += 1
                failed_filename_list.append(folder + os.sep + filename)

            loop_end()

    # the nice pretty results output
    print("")
    print("")
    print("Completed")
    print("S: " + str(suc_count) + " [" + str(round((suc_count/count) * 100, 2)) + "%], ", end="")
    print("F: " + str(fail_count) + " [" + str(round((fail_count/count) * 100, 2)) + "%], ", end="")
    print("X: " + str(skip_count) + " [" + str(round((skip_count / count) * 100, 2)) + "%], ", end="")
    print("T: " + str(count))

    # and the list of files that failed to rename if there are any
    if len(failed_filename_list) > 0:
        print("")
        print("Failed to rename files:")
        print("")
        print("\n".join(failed_filename_list))
        print("")


# a confirmation to make sure the user has done what this scripts expects them to have done
print("This requires using Sims 4 Studio to export all Tuning files using sub-folders at the currently")
print("configured location: " + projects_tuning_path)
answer = input("Have you done this? [y/n]: ")

if answer is "y":
    begin_fix()
