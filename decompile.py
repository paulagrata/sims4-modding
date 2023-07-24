import os
import sys

from Utility.helpers_decompile import decompile_pre, decompile_zips, decompile_print_totals
from Utility.helpers_path import ensure_path_created, remove_dir
from settings import gameplay_folder_data, gameplay_folder_game, projects_python_path

if os.path.exists(projects_python_path):
    print("this will wipe out the old decompilation at: " + projects_python_path)
    answer = input("are you sure you want to do this? [y/n]: ")
    if answer is not "y":
        sys.exit("program aborted by user")

print("Emptying prior decompilation...")
remove_dir(projects_python_path)

# make sure the python folder exists
ensure_path_created(projects_python_path)

# do a pre-setup
decompile_pre()

# Decompile all zips to the python projects folder
print("")
print("Beginning decompilation")
print("THIS WILL SERIOUSLY TAKE A VERY LONG TIME!!! " +
      "Additionally many files will not decompile properly which is normal.")
print("")

decompile_zips(gameplay_folder_data, projects_python_path)
decompile_zips(gameplay_folder_game, projects_python_path)

# Print final statistics
decompile_print_totals()
