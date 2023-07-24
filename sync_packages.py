import fnmatch

import os
import shutil
from settings import assets_path, mods_folder, creator_name, project_name, build_path
from Utility.helpers_path import ensure_path_created, remove_file

mod_name_folder_path = mods_folder + os.sep + creator_name + "_" + project_name

ensure_path_created(mod_name_folder_path)
file_list_failed = []


def remove_tl_packages(path: str) -> int:
    count = 0

    # remove existing package files
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, "*.package"):
            remove_file(root + os.sep + filename)
            count+=1

        # Only cover the top-level folder
        break
    return count


def copy_tl_packages(src: str, dest: str) -> int:
    count = 0

    # copy new package files
    for root, dirs, files in os.walk(src):
        for filename in fnmatch.filter(files, "*.package"):
            try:
                shutil.copy(root + os.sep + filename,
                            dest + os.sep + filename)
                count += 1
            except:
                file_list_failed.append(root + os.sep + filename)

        # only cover the top-level folder
        break

    return count


files_removed = remove_tl_packages(mod_name_folder_path)
remove_tl_packages(build_path)

files_added = copy_tl_packages(assets_path, mod_name_folder_path)
copy_tl_packages(assets_path, build_path)

file_difference = files_added - files_removed

print("Synced packages:" +
      " +" + str(files_added) +
      " -" + str(files_removed) +
      " ~" + str(file_difference))

if len(file_list_failed) > 0:
    print("")
    print("Failed to copy these files, make sure the packages are named uniquely")
    print("")
    print("\n".join(file_list_failed))
