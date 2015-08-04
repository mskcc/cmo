import os, sys
from . import util




class Gatk:
    def __init__(self,version="default", java_version="default", java_args="-Xmx48g Xms256m -XX:-UseGCOverheadLimit", temp_dir="/tmp"):
        try:
            self.gatk_jar=util.programs["gatk"][version]
        except KeyError, e:
            print >>sys.stderr, "Cannot find specified version of piard in configuration file: %s" % version
            sys.exit(1)
        try: 
            self.java_cmd=util.programs["java"][version]
        except KeyError, e:
            print >>sys.stderr, "Cannot find specified version of java to run gatk with: %s" % version
            sys.exit(1)
        self.java_args = java_args + "-Djava.io.tmpdir=" + temp_dir
    def gatk_cmd(self, command, default_args_override={}, command_specific_args={}):
        cmd = [self.java_cmd, self.java_args, "-jar", self.gatk_jar, "-T",command]
        for arg, value in self.default_args.items():
            if arg not in default_args_override:
                cmd = cmd + [arg + "=" + value]
            else:
                cmd = cmd + [arg + "=" + default_args_override[arg]]
        for arg, value in command_specific_args.items():
            if value != None:
                cmd = cmd + [arg + "=" + value]
        return " ".join(cmd)
    def gatk_cmd_help(self, command):
        cmd = [self.java_cmd, self.java_args, "-jar", self.gatk_jar, "-T", command, " --help"]
        return " ".join(cmd)





