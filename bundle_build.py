from zipfile import PyZipFile, ZIP_STORED

import os
import shutil
import tempfile
from settings import build_path, creator_name, project_name
from Utility.helpers_path import ensure_path_created, remove_file, get_rel_path

# build paths and create temp directory
folder_name = creator_name + "_" + project_name
bundle_path = build_path + os.sep + folder_name + "-bundle.zip"
tmp_dir = tempfile.TemporaryDirectory()
tmp_dst_path = tmp_dir.name + os.sep + folder_name

# ensure build directory is created
ensure_path_created(build_path)

# remove existing bundle
remove_file(bundle_path)

# copy build files to tmp dir
shutil.copytree(build_path, tmp_dst_path)

# zip up bundled folder
zf = PyZipFile(bundle_path, mode='w', compression=ZIP_STORED, allowZip64=True, optimize=2)
for root, dirs, files in os.walk(tmp_dir.name):
    for filename in files:
        rel_path = get_rel_path(root + os.sep + filename, tmp_dir.name)
        zf.write(root + os.sep + filename, rel_path)
zf.close()

# there's a temporary directory bug that causes auto-cleanup to sometimes fail [preventing crash messages from flooding the screen to keep things clean]
try:
    tmp_dir.cleanup()
except:
    pass

print("created bundle at: " + "build" + os.sep + folder_name + "-bundle.zip")
