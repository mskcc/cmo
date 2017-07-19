import os, sys, tempfile
from . import util
logger = util.get_logger()



class Gatk:
    def __init__(self,version="default", java_version="default", java_args="-Xmx48g -Xms256m -XX:-UseGCOverheadLimit", temp_dir="/scratch", mutect=False):
        try:
            if mutect:
                self.gatk_jar=util.programs["mutect"][version]
            else:
                self.gatk_jar=util.programs["gatk"][version]
        except KeyError, e:
            logger.critical("Cannot find specified version of gatk in configuration file: %s" % version)
            sys.exit(1)
        try: 
            self.java_cmd=util.programs["java"][java_version]
        except KeyError, e:
            logger.critical("Cannot find specified version of java to run gatk with: %s" % java_version)
            sys.exit(1)
        self.temp_dir=None
        if temp_dir:
            self.temp_dir = temp_dir
        self.java_args = java_args 
        logger.info("selected %s" % self.gatk_jar)
    def gatk_cmd(self, command, java_args_override=None, command_specific_args={}):
        cmd = [self.java_cmd, self.java_args]
        if(self.temp_dir != None):
            if os.path.exists(self.temp_dir):
                cmd = cmd +  ["-Djava.io.tmpdir="+self.temp_dir]
            elif os.path.exists("/srv/data/scratch"):
                cmd = cmd + ["-Djava.io.tmpdir=/srv/data/scratch"]
            else:
                cmd = cmd + ["-Djava.io.tmpdir=" + tempfile.mkdtemp()]
        cmd = cmd + [ "-jar", self.gatk_jar, "-T",command]
        for arg, value in command_specific_args.items():
            if value != None:
                if isinstance(value, list):
                    for val in value:
                        cmd = cmd + ["--"+arg,  "'" + val + "'"]
                elif value == True:
                    cmd = cmd + ["--"+arg]
                elif value != False:
                    cmd = cmd + ["--"+arg, "'" + value + "'"]
        return " ".join(cmd)
    def gatk_cmd_help(self, command):
        cmd = [self.java_cmd, self.java_args, "-jar", self.gatk_jar, "-T", command, " --help"]
        return " ".join(cmd)





