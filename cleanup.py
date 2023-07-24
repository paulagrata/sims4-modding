import shutil
from Utility.helpers_debug import debug_teardown
from Utility.helpers_path import remove_dir
from Utility.helpers_symlink import symlink_remove_win
from settings import mods_folder, debug_mod_subfolder, creator_name, project_name, build_path

print("removing Debug Setup...")
debug_teardown(mods_folder, debug_mod_subfolder)

print("removing Mod Folder in Mods...")
symlink_remove_win(creator_name, mods_folder, project_name)

print("removing Build folder...")
remove_dir(build_path)

print("")
print("complete... all build artifacts have been removed!")
