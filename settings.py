import os
from pathlib import Path

#________________________________________
#changeable settings

creator_name = 'befreshyo'

# mod folder location
mods_folder = os.path.expanduser(
    os.path.join('~', 'Documents', 'Electronic Arts', 'The Sims 4', 'Mods')
)

# folder to contain your projects
projects_folder = os.path.expanduser(
    os.path.join('~', 'Documents', 'Sims 4 Projects')
)

# game folder
game_folder = os.path.join('C:', os.sep, 'Program Files (x86)', 'Origin Games', 'The Sims 4')

#________________________________________
# dont change these ->

# folder within this project that contains your python/script files
src_subpath = "src"

# folder within this project that your mods will be built to
build_subpath = "build"

# to hold asset files like xml tuning files and packages
assets_subpath = "assets"

# subpath inside the projects folder to place decompiled python files
projects_python_subpath = "__util" + os.sep + "Python"
projects_tuning_subpath = "__util" + os.sep + "Tuning"

# name of this project, by default it's setup to use the folder name containing the project
project_name = Path(__file__).parent.stem

# dev mode
devmode_cmd_mod_src = "Utility/devmode_cmd.py"
devmode_cmd_mod_name = "devmode-cmd"

#________________________________________
# dont change these some more

# project folder path itself
root_path = str(Path(__file__).parent)

# paths are calculated from the above information
src_path = os.path.join(root_path, src_subpath)
build_path = os.path.join(root_path, build_subpath)
assets_path = os.path.join(root_path, assets_subpath)
devmode_cmd_mod_src_path = os.path.join(Path(__file__).parent, devmode_cmd_mod_src)
projects_python_path = os.path.join(projects_folder, projects_python_subpath)
projects_tuning_path = os.path.join(projects_folder, projects_tuning_subpath)
debug_cmd_mod_src_path = os.path.join(Path(__file__).parent, debug_cmd_mod_src)

# sims 4 data and game folders
gameplay_folder_data = os.path.join(game_folder, 'Data', 'Simulation', 'Gameplay')
gameplay_folder_game = os.path.join(game_folder, 'Game', 'Bin', 'Python')
debug_eggs_path = os.path.join(pycharm_pro_folder, "debug-eggs", "pydevd-pycharm.egg")
