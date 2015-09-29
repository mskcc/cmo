import os,subprocess, sys

def test_bin_scripts():
    bin_dir = "../bin/"
    for file in os.listdir(bin_dir):
        yield check_for_help, os.path.join(bin_dir, file)

def check_for_help(file):
    proc = subprocess.Popen(["/opt/common/CentOS_6-dev/python/python-2.7.10/bin/python", file,"-h"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    [stdout, stderr] = proc.communicate()
    if stderr.find("usage:") > -1:
        pass
    elif stdout.find("usage:") > -1:
        pass
    else:
        assert False
        
