import os,subprocess, sys

def test_bin_scripts():
    (current_dir,_) = os.path.split(os.path.realpath(__file__))
    bin_dir = os.path.join(current_dir, "../bin/")
    for file in os.listdir(bin_dir):
        yield check_for_help, os.path.join(bin_dir, file)

def check_for_help(file):
    if hasattr(sys, 'real_prefix'): #we're in a virtualenv
        python = "python"
    else:
        python = "/opt/common/CentOS_6-dev/python/python-2.7.10/bin/python"
    proc = subprocess.Popen([python,  file,"-h"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    [stdout, stderr] = proc.communicate()
    if stderr.find("usage:") > -1:
        pass
    elif stdout.find("usage:") > -1:
        pass
    else:
        assert False
        
