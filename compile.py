from Utility.helpers_compile import compile_src
from settings import mods_folder, src_path, creator_name, build_path, project_name

try:
    compile_src(creator_name, src_path, build_path, mods_folder, project_name)
    exec(open("sync_packages.py").read())
    exec(open("bundle_build.py").read())
except:
    print("error occurred!")
    pass
