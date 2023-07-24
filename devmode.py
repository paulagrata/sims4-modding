from Utility.helpers_debug import debug_install_mod
from Utility.helpers_symlink import symlink_create_win, symlink_exists_win
from settings import mods_folder, src_path, creator_name, project_name, devmode_cmd_mod_src_path, devmode_cmd_mod_name

is_devmode = symlink_exists_win(creator_name, mods_folder, project_name)

if is_devmode:
    print("you're already in Dev Mode")
    raise SystemExit(1)

try:
    symlink_create_win(creator_name, src_path, mods_folder, project_name)
    debug_install_mod(devmode_cmd_mod_src_path, mods_folder, devmode_cmd_mod_name, creator_name + "_" + project_name)
    exec(open("sync_packages.py").read())
except:
    print("an error occurred!")
    pass
