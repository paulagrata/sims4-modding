# using PyCharm Pro -> create a configuration using the "Python Debug Server" template
# using these settings:
# host: localhost
# port: 5678
# before running game make sure you select the debug profile and run debug in the editor beforehand
# run debug_teardown.py when done to uninstall the debug capability as it can slow down the game

from Utility.helpers_debug import debug_ensure_pycharm_debug_package_installed, debug_install_mod, debug_install_egg, \
    debug_teardown
from settings import mods_folder, debug_eggs_path, debug_cmd_mod_src_path, debug_cmd_mod_name, debug_capability_name, \
    debug_mod_subfolder

# ensure PyCharm Pro debug package is installed
debug_ensure_pycharm_debug_package_installed()

# install the debug mod and egg
# mod creates a cheat "pycharm.debug" which activates the debug process
# egg injects the code into the game so that the debug process can happen
debug_teardown(mods_folder, debug_mod_subfolder)
debug_install_mod(debug_cmd_mod_src_path, mods_folder, debug_cmd_mod_name, debug_mod_subfolder)
debug_install_egg(debug_eggs_path, mods_folder, debug_capability_name, debug_mod_subfolder)

print("")
print("complete!")
print("")
print("step 1: create a 'Python Debug Server' configuration In PyCharm Pro from the template using")
print("        IDE host name: localhost")
print("        port: 5678")
print("step 2: select debug profile and begin debugging")
print("step 3: load up a playable lot in the game")
print("step 4: enter the cheatcode 'pycharm.debug'")
print("step 5: switch windows to the debugger and hit resume")
print("step 6: the game and debugger are now connected, you're ready to start debugging!")
print("")
print("when you're done debugging, run 'debug_teardown.py' to uninstall the debugging capability. otherwise leaving")
print("it in just makes your game slower")
