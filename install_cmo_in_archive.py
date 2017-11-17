

import cmo, os, subprocess

print cmo.__version__

archive_dir = "/home/johnsoni/cmo_tools"
target_directory = os.path.join(archive_dir, str(cmo.__version__))
print target_directory
pythonpath = os.path.join(target_directory, "lib/python2.7/site-packages/")
print pythonpath
if not os.path.exists(pythonpath):
    os.makedirs(pythonpath)
os.environ['PYTHONPATH']=pythonpath
installation_command = ["python", "setup.py", "install", "--prefix", target_directory]
subprocess.check_call(installation_command)

